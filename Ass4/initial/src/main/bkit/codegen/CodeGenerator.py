'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
'''
from Visitor import BaseVisitor
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod
from functools import *
from typing import List, Tuple
from AST import *
from copy import deepcopy

from main.bkit.utils.AST import ArrayLiteral, CallExpr, VarDecl


class MethodEnv():
    def __init__(self, frame, sym):
        self.frame = frame
        self.sym = sym


class Symbol:
    def __init__(self, name, mtype, value=None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + self.name + ", " + self.mtype.__class__.__name__ + ", " + self.value.__class__.__name__ + ")"


class CName:
    def __init__(self, n):
        self.value = n

class Index:
    def __init__(self, n):
        self.value = n

class Type(ABC):
    def __eq__(self, other):
        return self.__class__ == other.__class__
class IntType(Type):
    pass
class FloatType(Type):
    pass
class VoidType(Type):
    pass
class Unknown(Type):
    pass
class StringType(Type):
    pass
class BoolType(Type):
    pass

class ClassType(Type):
    def __init__(self, n):
        self.cname = n

class MType(Type):
    def __init__(self, i, o):
        self.partype = i  # List[Type]
        self.rettype = o  # Type

class ArrayType(Type):
    def __init__(self, et, *s):
        self.eleType = et  # Type
        self.dimen = s  # List[int]

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.dimen == other.dimen and self.eleType == other.eleType

class ArrayGen(Type):
    def __init__(self, ctype):
        # cname: String
        self.eleType = ctype

class SubBody():
    def __init__(self, frame, sym, isGlobal=False):
        # frame: Frame
        # sym: List[Symbol]
        self.frame = frame
        self.sym = sym
        self.isGlobal = isGlobal

class Access():
    def __init__(self, frame, sym, isLeft, isFirst, checkArrayType=False):
        # frame: Frame
        # sym: List[Symbol]
        # isLeft: Boolean
        # isFirst: Boolean

        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst
        self.checkArrayType = checkArrayType


class CodeGenerator():
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [Symbol("read", MType([], StringType()), CName(self.libName)),
                Symbol("printLn", MType([], VoidType()), CName(self.libName)),
                Symbol("printStrLn", MType([StringType()], VoidType()), CName(self.libName)),
                Symbol("print", MType([StringType()],VoidType()), CName(self.libName)),
                Symbol("string_of_int", MType([IntType()], StringType()), CName(self.libName)),
                Symbol("float_to_int", MType([IntType()], FloatType()), CName(self.libName)),
                Symbol("int_of_float", MType([FloatType()], IntType()), CName(self.libName)),
                Symbol("int_of_string", MType([StringType()], IntType()), CName(self.libName)),
                Symbol("float_of_string", MType([StringType()], FloatType()), CName(self.libName)),
                Symbol("string_of_float", MType([FloatType()], StringType()), CName(self.libName)),
                Symbol("bool_of_string", MType([StringType()], BoolType()), CName(self.libName)),
                Symbol("string_of_bool", MType([BoolType()], StringType()), CName(self.libName))
                ]

    def gen(self, ast, dir_):
        #ast: AST
        #dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)


class CodeGenVisitor(BaseVisitor):
    def __init__(self, astTree, env, dir_):
        #astTree: AST
        #env: List[Symbol]
        #dir_: File
        self.astTree = astTree
        self.env = env
        self.className = "MCClass"
        self.path = dir_
        self.emit = Emitter(self.path + "/" + self.className + ".j")
        self.listGlobalArray = []
        self.listNormalVarGlobal = []

    #===============================Utils=================================#

    def getInnerMostSymbolic(self, name):
        for item in self.env:
            for sym in item:
                if sym.name == name:
                    return sym

    def getTypeLiteral(self, literal):
        if type(literal).__name__ == "IntLiteral":
            return IntType()
        if type(literal).__name__ == "FloatLiteral":
            return FloatType()
        if type(literal).__name__ == "StringLiteral":
            return StringType()
        if type(literal).__name__ == "BooleanLiteral":
            return BoolType()
        if type(literal).__name__ == "ArrayLiteral":
            # value:List[Literal]
            eleType = self.getTypeLiteral(literal.value[0])
            arrayDimen = ([len(literal.value)] + eleType.dimen) if isinstance(eleType,ArrayType) else [len(literal.value)]
            while isinstance(eleType, ArrayType):
                eleType = eleType.eleType

            return ArrayType(eleType, arrayDimen)
    
    def getProcessType(self, array):
        if type(array).__name__ == "ArrayType":
            return ArrayGen(array.eleType)
        return array

    #===============================Visit Var+Func declare=================================#

    def visitProgram(self, ast, c):
        # decl : List[Decl]
        #c: Any
        self.env = [self.env + visitGlobalType(ast).getGlobalType()]
        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))

        # generate declare
        [self.visit(item, SubBody(None, None, True)) for item in ast.decl]
        # generate class init
        self.genClassInit()
        # generate default constructor
        self.genInit()

        self.emit.emitEPILOG()
        return c

    def genInit(self):
        methodname, methodtype = "<init>", MType([], VoidType())
        frame = Frame(methodname, methodtype.rettype)
        self.emit.printout(self.emit.emitMETHOD(methodname, methodtype, False, frame))
        frame.enterScope(True)
        varname, vartype, varindex = "this", ClassType(self.className), frame.getNewIndex()
        startLabel, endLabel = frame.getStartLabel(), frame.getEndLabel()
        self.emit.printout(self.emit.emitVAR(varindex, varname, vartype, startLabel, endLabel, frame))
        self.emit.printout(self.emit.emitLABEL(startLabel, frame))
        self.emit.printout(self.emit.emitREADVAR(varname, vartype, varindex, frame))
        self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        self.emit.printout(self.emit.emitLABEL(endLabel, frame))
        self.emit.printout(self.emit.emitRETURN(methodtype.rettype, frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))

    def genClassInit(self):
        methodname, methodtype = "<clinit>", MType([], VoidType())
        frame = Frame(methodname, methodtype.rettype)
        self.emit.printout(self.emit.emitMETHOD(methodname, methodtype, False, frame))
        frame.enterScope(True)

        for item in self.listNormalVarGlobal:
            if type(item).__name__ == "VarDecl":
                varName = item.variable.name
                initCode, initType = self.visit(item.varInit, Access(frame, None, False, True))
                self.emit.printout(initCode)
                self.emit.printout(self.emit.emitPUTSTATIC(self.className + "/" + varName, initType, frame))
        for item in self.listGlobalArray:
            size = item.varDimen[0]
            frame.push()
            initCode, initType = self.visit(item.varInit, Access(frame, None, False, True))
            self.emit.printout(self.emit.emitInitNewStaticArray(self.className + "/" + item.variable.name, size, self.getTypeLiteral(item.varInit).eleType, frame, initCode))

        self.emit.printout(self.emit.emitRETURN(methodtype.rettype, frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    def visitVarDecl(self, ast, o: SubBody, paramType = None):
        # variable : Id
        # varDimen : List[int] # empty list for scalar variable
        # varInit  : Literal   # null if no initial
        frame = o.frame
        varName = ast.variable.name
        varType = self.getTypeLiteral(ast.varInit) if not paramType else paramType

        if o.isGlobal:
            self.emit.printout(self.emit.emitATTRIBUTE(varName, self.getProcessType(varType), False, ""))
            if type(varType).__name__ == "ArrayType": 
                self.listGlobalArray.append(ast)
            else:
                self.listNormalVarGlobal.append(ast)
            return

        idx = frame.getNewIndex()
        self.emit.printout(self.emit.emitVAR(idx, varName, self.getProcessType(varType), frame.getStartLabel(), frame.getEndLabel(), frame))

        if ast.varInit != None and type(varType).__name__ != "ArrayType":
            initCode, initType = self.visit(ast.varInit, Access(frame, o.sym, False, True))
            self.emit.printout(initCode)
            self.emit.printout(self.emit.emitWRITEVAR(varName, varType, idx, frame))
        if ast.varInit != None and type(varType).__name__ == "ArrayType":
            size = ast.varDimen[0]
            frame.push()
            initCode, initType = self.visit(ast.varInit, Access(frame, o.sym, False, True))
            self.emit.printout(self.emit.emitInitNewLocalArray(idx, size, varType.eleType, frame, initCode))

        o.sym[0].append(Symbol(varName, varType, Index(idx)))

    def visitFuncDecl(self, ast, param):
        # name: Id
        # param: List[VarDecl]
        # body: Tuple[List[VarDecl],List[Stmt]]
        self.env.insert(0,[])

        methodName = ast.name.name
        sym = self.getInnerMostSymbolic(methodName)
        methodReturnType = sym.mtype.rettype
        frame = Frame(methodName, methodReturnType)
        isProc = isinstance(methodReturnType, VoidType)
        if methodName == 'main':
            sym.mtype.partype = [ArrayType(StringType())]
        intype = sym.mtype.partype

        self.emit.printout(self.emit.emitMETHOD(methodName, sym.mtype, True, frame))
        frame.enterScope(isProc)
        if methodName == 'main':
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))

        subEnv = SubBody(frame, self.env)
        for index in range(len(ast.param)):
            self.visitVarDecl(ast.param[index], subEnv, intype[index])

        [self.visitVarDecl(item, subEnv) for item in ast.body[0]]

        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        [self.visit(item, subEnv) for item in ast.body[1]]
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if isProc:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

        self.env.pop(0)

    #===============================Visit exp=================================#

    def visitBinaryOp(self, ast, o):
        # op:str
        # left:Expr
        # right:Expr
        leftCode, leftType = self.visit(ast.left, o)
        rightCode, rightType = self.visit(ast.right, o)

        if ast.op in ['+', '-', '*', '\\']:
            binCode = self.emit.emitADDOP(ast.op, IntType(), o.frame) if ast.op in ['+', '-'] else self.emit.emitMULOP(ast.op, IntType(), o.frame)
            return leftCode + rightCode + binCode, IntType()
        if ast.op in ['%']:
            binCode = self.emit.emitMOD(o.frame)
            return leftCode + rightCode + binCode, IntType()
        if ast.op in ['==', '!=', '>', '<', '>', '<=', '>=']:
            binCode = self.emit.emitREOP(ast.op, IntType(), o.frame)
            return leftCode + rightCode + binCode, BoolType()

        if ast.op in ['+.', '-.', '*.', '\\.', '=/=', '<.', '>.', '<=.', '>=.']:
            if type(leftType).__name__ == "IntType":
                leftCode = leftCode + self.emit.emitI2F(o.frame)
            if type(rightType).__name__ == "IntType":
                rightCode = rightCode + self.emit.emitI2F(o.frame)
        if ast.op in ['+.', '-.', '*.', '\\.']:
            binCode = self.emit.emitADDOP(ast.op[0], FloatType(), o.frame) if ast.op in ['+.', '-.'] else self.emit.emitMULOP(ast.op[0], FloatType(), o.frame)
            return leftCode + rightCode + binCode, FloatType()
        if ast.op in ['=/=', '<.', '>.', '<=.', '>=.']:
            if ast.op in ['=/=']:
                op = '!='
            elif ast.op in ['<.', '>.']:
                op = ast.op[0]
            else:
                op = ast.op[:-1]
            binCode = self.emit.emitREOP(op, FloatType(), o.frame)
            return leftCode + rightCode + binCode, BoolType()

        if ast.op in ['&&', '||']:
            result = []
            result.append(leftCode)

            labelF = o.frame.getNewLabel() # eval is false
            labelT = o.frame.getNewLabel() # eval is true

            if ast.op == '&&': result.append(self.emit.emitIFFALSE(labelF, o.frame)) # false
            else: result.append(self.emit.emitIFTRUE(labelT, o.frame)) # true

            result.append(rightCode)

            if ast.op == '&&':
                result.append(self.emit.emitIFFALSE(labelF, o.frame)) # false
                result.append(self.emit.emitPUSHICONST("true", o.frame)) # push true
                result.append(self.emit.emitGOTO(labelT, o.frame)) # go to true
                result.append(self.emit.emitLABEL(labelF, o.frame)) # push false
                result.append(self.emit.emitPUSHICONST("false", o.frame))
                result.append(self.emit.emitLABEL(labelT, o.frame))
            else:
                result.append(self.emit.emitIFTRUE(labelT, o.frame)) # true
                result.append(self.emit.emitPUSHICONST("false", o.frame)) # push false
                result.append(self.emit.emitGOTO(labelF, o.frame)) # go to false
                result.append(self.emit.emitLABEL(labelT, o.frame)) # push true
                result.append(self.emit.emitPUSHICONST("true", o.frame))
                result.append(self.emit.emitLABEL(labelF, o.frame))

            return ''.join(result), BoolType()

    def visitUnaryOp(self, ast, o):
        # op:str
        # body:Expr
        expCode, expType = self.visit(ast.body, o)
        if ast.op in ['-']:
            unCode = self.emit.emitNEGOP(IntType(), o.frame)
            return expCode + unCode, IntType()
        if ast.op in ['-.']:
            unCode = self.emit.emitNEGOP(FloatType(), o.frame)
            return expCode + unCode, FloatType()
        if ast.op in ['!']:
            unCode = self.emit.emitNOT(BoolType(), o.frame)
            return expCode + unCode, BoolType()

    def visitCallExpr(self, ast, o):
        # method:Id
        # param:List[Expr]
        return self.callFunctionGen(ast, o, False)

    def visitId(self, ast, o):
        # name : str
        # not index mean that is global variable
        sym = self.getInnerMostSymbolic(ast.name)

        typeEmit = self.getProcessType(sym.mtype)
        if not o.isLeft:
            if type(sym.value) == Index:
                retCode = self.emit.emitREADVAR(sym.name, typeEmit, sym.value.value, o.frame)
            else:
                retCode = self.emit.emitGETSTATIC(sym.value.value + "/" + sym.name, typeEmit, o.frame)
        else:
            if type(sym.value) == Index:
                retCode = self.emit.emitWRITEVAR(sym.name, typeEmit, sym.value.value, o.frame)
            else:
                retCode = self.emit.emitPUTSTATIC(sym.value.value + "/" + sym.name, typeEmit, o.frame)
        return retCode, sym.mtype

    def visitArrayCell(self, ast, o):
        # arr:Expr
        # idx:List[Expr]
        arrCode, arrType = self.visit(ast.arr, Access(o.frame, o.sym, False, True))
        idxCode, idxType = self.visit(ast.idx[0], Access(o.frame, o.sym, False, True))
        if o.isLeft:
            return [arrCode + idxCode, self.emit.emitASTORE(arrType.eleType, o.frame)], arrType.eleType
        return arrCode + idxCode + self.emit.emitALOAD(arrType.eleType, o.frame), arrType.eleType

    #===============================Visit stmts=================================#

    def callFunctionGen(self, ast, o: SubBody, isStatement = False):
        # method:Id
        # param:List[Expr]
        sym = self.getInnerMostSymbolic(ast.method.name)
        cname = sym.value.value
        ctype = sym.mtype
        intype = ctype.partype

        idx = 0
        code, pCode, pType = "", "", ""
        for x in ast.param:
            if type(x).__name__ == "CallExpr":
                pCode, pType = self.visit(x, o)
            else:
                pCode, pType = self.visit(x, Access(o.frame, o.sym, False, True))

            if isinstance(intype[idx],FloatType) and isinstance(pType, IntType):
                pCode = pCode + self.emit.emitI2F(o.frame)
            if type(intype[idx]) is ArrayType:
                pass
            code = code + pCode
            idx = idx + 1
        
        code = code + self.emit.emitINVOKESTATIC(cname + "/" + sym.name, ctype, o.frame) 
        if isStatement: 
            self.emit.printout(code)
        else: 
            return code, ctype.rettype

    def visitAssign(self, ast, o):
        # lhs: LHS
        # rhs: Expr
        isArray = False if type(ast.lhs).__name__ == "Id" else True
        if isArray: [o.frame.push() for i in range(0,2)]
        
        rhsCode, rhsType = self.visit(ast.rhs, Access(o.frame, o.sym, False, True))
        
        if type(rhsType).__name__ != "ArrayType":
            lhsCode, lhsType = self.visit(ast.lhs, Access(o.frame, o.sym, True, True))
            if type(lhsType).__name__ == "FloatType" and type(rhsType).__name__ == "IntType":
                rhsCode = rhsCode + self.emit.emitI2F(o.frame)
            
            if not isArray:
                self.emit.printout(rhsCode + lhsCode)
            else:
                self.emit.printout(lhsCode[0] + rhsCode + lhsCode[1])
                # recover stack status
                [o.frame.pop() for i in range(0,2)]
        else:
            if type(ast.rhs).__name__ == "ArrayLiteral":
                for index in range(rhsType.dimen[0][0]):
                    itemIndex = ArrayCell(ast.lhs, [IntLiteral(index)])
                    self.visitAssign((Assign(itemIndex, ast.rhs.value[index])), o)
            else:
                for index in range(rhsType.dimen[0][0]):
                    itemIndexLeft = ArrayCell(ast.lhs, [IntLiteral(index)])
                    itemIndexRight = ArrayCell(ast.rhs, [IntLiteral(index)])
                    self.visitAssign((Assign(itemIndexLeft, itemIndexRight)), o)

    def visitIf(self, ast, o):
        # ifthenStmt:List[Tuple[Expr,List[VarDecl],List[Stmt]]]
        # elseStmt:Tuple[List[VarDecl],List[Stmt]] # for Else branch, empty list if no Else
        labelList = [o.frame.getNewLabel() for item in range(len(ast.ifthenStmt) + 1)]
        
        currentIdx = 0
        for item in ast.ifthenStmt:
            codeExpr, typeExpr = self.visit(item[0], Access(o.frame, o.sym, False, True))
            self.emit.printout(codeExpr)
            self.emit.printout(self.emit.emitIFFALSE(labelList[currentIdx],o.frame))

            self.env.insert(0,[])
            [self.visitVarDecl(miniItem, o) for miniItem in item[1]]
            [self.visit(miniItem, o) for miniItem in item[2]]
            self.env.pop(0)

            self.emit.printout(self.emit.emitGOTO(labelList[-1], o.frame))
            self.emit.printout(self.emit.emitLABEL(labelList[currentIdx], o.frame))
            currentIdx += 1

        if ast.elseStmt != ([],[]):
            self.env.insert(0,[])
            [self.visitVarDecl(miniItem, o) for miniItem in ast.elseStmt[0]]
            [self.visit(miniItem, o) for miniItem in ast.elseStmt[1]]
            self.env.pop(0)
        self.emit.printout(self.emit.emitLABEL(labelList[-1], o.frame))


    def visitFor(self, ast, o):
        # idx1: Id
        # expr1:Expr
        # expr2:Expr
        # expr3:Expr
        # loop: Tuple[List[VarDecl],List[Stmt]]

        frame = o.frame
        asignItem = Assign(ast.idx1, ast.expr1)
        self.visitAssign(asignItem, o)
        
        frame.enterLoop()
        
        labelBegin = frame.getNewLabel()
        labelExit = frame.getBreakLabel()
        labelContinue = frame.getContinueLabel()
        self.emit.printout(self.emit.emitLABEL(labelBegin, frame))
        
        codeExpr, typeExpr = self.visit(ast.expr2, Access(o.frame, o.sym, False, True))
        self.emit.printout(codeExpr)
        self.emit.printout(self.emit.emitIFFALSE(labelExit,frame))
        
        self.env.insert(0,[])
        [self.visitVarDecl(item, o) for item in ast.loop[0]]
        [self.visit(item, o) for item in ast.loop[1]]
        self.env.pop(0)

        self.emit.printout(self.emit.emitLABEL(labelContinue, frame))
        # update indx1 = idx1 + updateExpr
        codeUpdate, typeUpdate = self.visit(ast.expr3, Access(o.frame, o.sym, False, True))
        idLoad, idLoadType = self.visit(ast.idx1, Access(o.frame, o.sym, False, True))
        idWrite, idWriteType = self.visit(ast.idx1, Access(o.frame, o.sym, True, True))
        addCode = self.emit.emitADDOP("+", typeUpdate, o.frame)
        self.emit.printout((idLoad + codeUpdate + addCode) + idWrite)

        self.emit.printout(self.emit.emitGOTO(labelBegin, frame))
        self.emit.printout(self.emit.emitLABEL(labelExit, frame))
        frame.exitLoop()

    def visitContinue(self, ast, o):
        self.emit.printout(self.emit.emitGOTO(o.frame.getContinueLabel(),o.frame))

    def visitBreak(self, ast, o):
        self.emit.printout(self.emit.emitGOTO(o.frame.getBreakLabel(), o.frame))

    def visitReturn(self, ast, o):
        # expr:Expr
        retType = o.frame.returnType
        if not type(retType) is VoidType:
            expCode, expType = self.visit(ast.expr, Access(o.frame, o.sym, False, True))
            if isinstance(retType,FloatType) and isinstance(expType, IntType):
                expCode = expCode + self.emit.emitI2F(o.frame)
            self.emit.printout(expCode)
        # self.emit.printout(self.emit.emitGOTO(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitRETURN(retType, o.frame))

    def visitDowhile(self, ast, o):
        # sl:Tuple[List[VarDecl],List[Stmt]]
        # exp: Expr
        frame = o.frame
        frame.enterLoop()
        
        labelBegin = frame.getContinueLabel()
        labelExit = frame.getBreakLabel()
        
        self.emit.printout(self.emit.emitLABEL(labelBegin, frame))
        
        self.env.insert(0,[])
        [self.visitVarDecl(item, o) for item in ast.sl[0]]
        [self.visit(item, o) for item in ast.sl[1]]
        self.env.pop(0)

        codeExpr, typeExpr = self.visit(ast.exp, Access(o.frame, o.sym, False, True))
        self.emit.printout(codeExpr)
        self.emit.printout(self.emit.emitIFFALSE(labelExit,frame))

        self.emit.printout(self.emit.emitGOTO(labelBegin, frame))
        self.emit.printout(self.emit.emitLABEL(labelExit, frame))
        frame.exitLoop()

    def visitWhile(self, ast, o):
        # exp: Expr
        # sl:Tuple[List[VarDecl],List[Stmt]]
        frame = o.frame
        frame.enterLoop()
        
        labelBegin = frame.getContinueLabel()
        labelExit = frame.getBreakLabel()
        
        self.emit.printout(self.emit.emitLABEL(labelBegin, frame))
        
        codeExpr, typeExpr = self.visit(ast.exp, Access(o.frame, o.sym, False, True))
        self.emit.printout(codeExpr)
        self.emit.printout(self.emit.emitIFFALSE(labelExit,frame))
        
        self.env.insert(0,[])
        [self.visitVarDecl(item, o) for item in ast.sl[0]]
        [self.visit(item, o) for item in ast.sl[1]]
        self.env.pop(0)

        self.emit.printout(self.emit.emitGOTO(labelBegin, frame))
        self.emit.printout(self.emit.emitLABEL(labelExit, frame))
        frame.exitLoop()

    def visitCallStmt(self, ast, param):
        self.callFunctionGen(ast, param, True)

    #===============================Visit literal=================================#

    def visitIntLiteral(self, ast, o: Access):
        return self.emit.emitPUSHICONST(ast.value, o.frame), IntType()

    def visitFloatLiteral(self, ast, o):
        return self.emit.emitPUSHFCONST(str(ast.value), o.frame), FloatType()

    def visitBooleanLiteral(self, ast, o):
        return self.emit.emitPUSHICONST(str(ast.value).lower(), o.frame), BoolType()

    def visitStringLiteral(self, ast, o):
        return self.emit.emitPUSHCONST('"' + ast.value + '"', StringType(), o.frame), StringType()

    def visitArrayLiteral(self, ast, o):
        # value:List[Literal]
        initCode = ""
        for index in range(len(ast.value)):
            litCode, litType = self.visit(ast.value[index], o)
            initCode += self.emit.emitDUP(o.frame)
            initCode += self.emit.emitPUSHICONST(index, o.frame)
            initCode += litCode
            initCode += self.emit.emitASTORE(litType, o.frame)
        return initCode, self.getTypeLiteral(ast)
        


class visitGlobalType(BaseVisitor):
    def __init__(self, ast):
        self.ast = ast
        self.className = "MCClass"
        self.global_envi = [
            Symbol("int_of_float", MType([FloatType()], IntType())),
            Symbol("float_to_int", MType([IntType()], FloatType())),
            Symbol("int_of_string", MType([StringType()], IntType())),
            Symbol("string_of_int", MType([IntType()], StringType())),
            Symbol("float_of_string", MType([StringType()], FloatType())),
            Symbol("string_of_float", MType([FloatType()], StringType())),
            Symbol("bool_of_string", MType([StringType()], BoolType())),
            Symbol("string_of_bool", MType([BoolType()], StringType())),
            Symbol("read", MType([], StringType())),
            Symbol("printLn", MType([], VoidType())),
            Symbol("printStr", MType([StringType()], VoidType())),
            Symbol("print", MType([StringType()], VoidType())),
            Symbol("printStrLn", MType([StringType()], VoidType()))]

    def getGlobalType(self):
        env = self.visit(self.ast, self.global_envi)
        return deepcopy(env[13:])

    def visitProgram(self, ast, c):
        # decl : List[Decl]
        globalScope = [self.global_envi]
        for item in ast.decl:
            globalScope[0].append(self.visitFuncDeclAtGlance(item, globalScope)) if isinstance(item, FuncDecl) else globalScope[0].append(self.visitVarDecl(item, globalScope, True))

        for item in ast.decl:
            self.visit(item, globalScope) if isinstance(item, FuncDecl) else None

        return globalScope[0]

    # --------------------------------------------------------------- #
    # -------------------------Visit Declare------------------------- #
    # --------------------------------------------------------------- #

    def visitVarDecl(self, ast, param, isGlobal=False):
        # variable : Id
        # varDimen : List[int] # empty list for scalar variable
        # varInit  : Literal   # null if no initial
        indexType = CName(self.className) if isGlobal else Index(None)
        if len(ast.varDimen) == 0:
            return Symbol(ast.variable.name, self.visit(ast.varInit, param), indexType) if ast.varInit else Symbol(ast.variable.name, Unknown(), indexType)
        else:
            typ = self.visit(ast.varInit, param) if ast.varInit else ArrayType(Unknown(), ast.varDimen)
            return Symbol(ast.variable.name, typ, indexType)

    def visitFuncDeclAtGlance(self, ast, param):
        # name: Id
        # param: List[VarDecl]
        # body: Tuple[List[VarDecl],List[Stmt]]
        paramGlance = [Unknown() for item in ast.param]
        return Symbol(ast.name.name, MType(paramGlance, Unknown()), CName(self.className))

    def visitFuncDecl(self, ast, param):
        param.insert(0, [])
        innerScope = param
        # Check param type
        funcType = None
        for item in ast.param:
            innerScope[0].append(self.visitVarDecl(item, innerScope))
        for item in innerScope[-1]:
            if ast.name.name == item.name:
                funcType = item.mtype
                for index in range(len(funcType.partype)):
                    innerScope[0][index].mtype = funcType.partype[index] if innerScope[0][index].mtype == Unknown() else innerScope[0][index].mtype
                    if isinstance(innerScope[0][index].mtype, ArrayType) and isinstance(funcType.partype[index], ArrayType):
                        if innerScope[0][index].mtype.eleType == Unknown():
                            innerScope[0][index].mtype.eleType = funcType.partype[index].eleType
                            funcType.partype[index].eleType
                    if(self.compareArrayType(innerScope[0][index].mtype, funcType.partype[index], None, None, None, param) == "Stop"):
                        continue
                break
        for item in ast.body[0]:
            innerScope[0].append(self.visitVarDecl(item, innerScope))

        #self.updateParameterFuncDecl(ast.name.name, innerScope, len(ast.param))
        innerScope[0].append(Symbol("Function " + ast.name.name, MType([], Unknown())))
        self.updateFromLocalToParam(param)
        for item in ast.body[1]:
            self.visit(item, innerScope)
            self.updateFromLocalToParam(param)
        if not any(isinstance(item, Return) for item in ast.body[1]) and funcType.rettype == Unknown():
            funcType.rettype = VoidType()
        param.pop(0)

    # --------------------------------------------------------------- #
    # -----------------------------Utils----------------------------- #
    # --------------------------------------------------------------- #

    def updateFromLocalToParam(self, param):
        name = self.getFunctionOuterName(param)
        funcDecl = None
        for item in param[-1]:
            if item.name == name and isinstance(item.mtype, MType):
                funcDecl = item
                break
        paramCount = len(funcDecl.mtype.partype)
        newParam = [param[-2][item].mtype for item in range(paramCount)]
        funcDecl.mtype.partype = newParam

    def updateFromParamToLocal(self, funcName, param):
        funcDecl = None
        for item in param[-1]:
            if item.name == funcName and isinstance(item.mtype, MType):
                funcDecl = item
                break
        paramCount = len(funcDecl.mtype.partype)
        for index in range(paramCount):
            param[-2][index].mtype = funcDecl.mtype.partype[index]

    def updateType(self, expr, type, param):
        # update Id or Function return type
        if isinstance(expr, Id) or isinstance(expr, CallExpr) or isinstance(expr, CallStmt):
            name = expr.name if isinstance(expr, Id) else expr.method.name
            isFuncReturnUpdate = False if isinstance(expr, Id) else True
            for item in param:
                for miniItem in item:
                    if miniItem.name == name and not isFuncReturnUpdate:
                        miniItem.mtype = type
                        break
                    if miniItem.name == name and isFuncReturnUpdate:
                        miniItem.mtype.rettype = type
                        break
                else:
                    continue
                break
        # update ArrayCell with index operation
        if isinstance(expr, ArrayCell):
            name = expr.arr.name if isinstance(
                expr.arr, Id) else expr.arr.method.name
            isFuncReturnUpdate = False if isinstance(expr.arr, Id) else True
            for item in param:
                for miniItem in item:
                    if miniItem.name == name and not isFuncReturnUpdate:
                        miniItem.mtype.eleType = type
                        break
                    if miniItem.name == name and isFuncReturnUpdate:
                        miniItem.mtype.rettype.eleType = type
                        break
                else:
                    continue
                break

    def checkFuncCall(self, ast, param):
        # method:Id
        # param:List[Expr]
        self.updateFromLocalToParam(param)

        funcType = None
        for item in param:
            for miniItem in item:
                if miniItem.name == ast.method.name and isinstance(miniItem.mtype, MType):
                    funcType = miniItem.mtype
                    break

        # check param type
        for index in range(len(ast.param)):
            paramType = self.visit(ast.param[index], param)
            inType = funcType.partype[index]

            if isinstance(inType, ArrayType) or isinstance(paramType, ArrayType):
                result = self.compareArrayType(inType, paramType, None, ast.param[index], ast, param)
                if result == "Stop":
                    continue

            if paramType == Unknown():
                self.updateType(ast.param[index], inType, param)
            if inType == Unknown():
                funcType.partype[index] = paramType

            if self.getFunctionOuterName(param) == ast.method.name:
                self.updateFromParamToLocal(ast.method.name, param)

        return funcType.rettype

    def checkStatementInput(self, setToCheck, type, ast, param):
        for item in setToCheck:
            exprType = self.visit(item, param)
            if exprType == Unknown():
                self.updateType(item, type, param)
                self.updateFromLocalToParam(param)

    def visitStatementInnerIf(self, loopStatement, param):
        # loopStatement: Tuple[List[VarDecl],List[Stmt]]
        param.insert(0, [])
        innerScope = param
        for miniItem in loopStatement[0]:
            innerScope[0].append(self.visit(miniItem, innerScope))
        for item in loopStatement[1]:
            self.visit(item, innerScope)
            self.updateFromLocalToParam(param)
        param.pop(0)

    def visitStatementInnerLoop(self, loopStatement, param):
        # loopStatement: Tuple[List[VarDecl],List[Stmt]]
        param.insert(0, [])
        innerScope = param
        for miniItem in loopStatement[0]:
            innerScope[0].append(self.visit(miniItem, innerScope))
        for item in loopStatement[1]:
            self.visit(item, innerScope)
            self.updateFromLocalToParam(param)
        param.pop(0)

    def breakContinueCheck(self, ast, param):
        pass

    def getFunctionOuterName(self, param):
        for item in param[-2]:
            if isinstance(item.mtype, MType):
                return item.name.split(' ')[1]

    def compareArrayType(self, leftType, rightType, leftUpdate, rightUpdate, ast, param):
        if isinstance(leftType, ArrayType) and isinstance(rightType, ArrayType):
            if leftType.dimen == rightType.dimen:
                if leftType.eleType == Unknown():
                    if leftUpdate == None:
                        leftType = rightType
                    else:
                        self.updateType(leftUpdate, rightType, param)
                    return "Stop"
                if rightType.eleType == Unknown():
                    if rightUpdate == None:
                        rightType = leftType
                    else:
                        self.updateType(rightUpdate, leftType, param)
                    return "Stop"
        return "None"

    # --------------------------------------------------------------- #
    # ------------------------Visit Expression----------------------- #
    # --------------------------------------------------------------- #

    def visitBinaryOp(self, ast, param, expectType=Unknown()):
        # op:str
        # left:Expr
        # right:Expr
        leftType = self.visit(ast.left, param)
        rightType = ""

        if ast.op in ['+', '-', '*', '\\', '%', '==', '!=', '<', '>', '<=', '>=']:
            if (leftType == Unknown() or leftType == IntType()):
                if leftType == Unknown():
                    self.updateType(ast.left, IntType(), param)
                rightType = self.visit(ast.right, param)

                if (rightType == Unknown() or rightType == IntType()):
                    if rightType == Unknown():
                        self.updateType(ast.right, IntType(), param)
                    if ast.op in ['==', '!=', '<', '>', '<=', '>=']:
                        return BoolType()
                    return IntType()

        if ast.op in ['+.', '-.', '*.', '\\.', '=/=', '<.', '>.', '<=.', '>=.']:
            if (leftType == Unknown() or leftType == FloatType()):
                if leftType == Unknown():
                    self.updateType(ast.left, FloatType(), param)
                rightType = self.visit(ast.right, param)

                if (rightType == Unknown() or rightType == FloatType()):
                    if rightType == Unknown():
                        self.updateType(ast.right, FloatType(), param)
                    if ast.op in ['=/=', '<.', '>.', '<=.', '>=.']:
                        return BoolType()
                    return FloatType()

        if ast.op in ['&&', '||']:
            if (leftType == Unknown() or leftType == BoolType()):
                if leftType == Unknown():
                    self.updateType(ast.left, BoolType(), param)
                rightType = self.visit(ast.right, param)

                if (rightType == Unknown() or rightType == BoolType()):
                    if rightType == Unknown():
                        self.updateType(ast.right, BoolType(), param)
                    return BoolType()

    def visitUnaryOp(self, ast, param):
        # op:str
        # body:Expr
        bodyType = self.visit(ast.body, param)

        if ast.op in ['-'] and (bodyType == Unknown() or bodyType == IntType()):
            if bodyType == Unknown():
                self.updateType(ast.body, IntType(), param)
            return IntType()
        if ast.op in ['-.'] and (bodyType == Unknown() or bodyType == FloatType()):
            if bodyType == Unknown():
                self.updateType(ast.body, FloatType(), param)
            return FloatType()
        if ast.op in ['!'] and (bodyType == Unknown() or bodyType == BoolType()):
            if bodyType == Unknown():
                self.updateType(ast.body, BoolType(), param)
            return BoolType()

    def visitCallExpr(self, ast, param):
        # method:Id
        # param:List[Expr]
        return self.checkFuncCall(ast, param)

    def visitId(self, ast, param):
        # name : str
        for item in param:
            for miniItem in item:
                if ast.name == miniItem.name and not isinstance(miniItem.mtype, MType):
                    return miniItem.mtype

    def visitArrayCell(self, ast, param):
        # arr:Expr
        # idx:List[Expr]
        arrType = self.visit(ast.arr, param)
        idxType = [self.visit(item, param) for item in ast.idx]

        for index in range(len(idxType)):
            if idxType[index] == Unknown():
                self.updateType(ast.idx[index], IntType(), param)
                idxType[index] = IntType()

        atomicType = arrType
        while isinstance(atomicType, ArrayType):
            atomicType = atomicType.eleType
        return atomicType

    # --------------------------------------------------------------- #
    # -------------------------Visit Statement----------------------- #
    # --------------------------------------------------------------- #

    def visitAssign(self, ast, param):
        # lhs: LHS
        # rhs: Expr
        lhsType = self.visit(ast.lhs, param)
        rhsType = self.visit(ast.rhs, param)

        if isinstance(lhsType, ArrayType) or isinstance(rhsType, ArrayType):
            result = self.compareArrayType(lhsType, rhsType, ast.lhs, ast.rhs, ast, param)
            if result == "Stop":
                return

        if lhsType == Unknown():
            self.updateType(ast.lhs, rhsType, param)
        if rhsType == Unknown():
            self.updateType(ast.rhs, lhsType, param)

    def visitIf(self, ast, param):
        # ifthenStmt:List[Tuple[Expr,List[VarDecl],List[Stmt]]]
        # elseStmt:Tuple[List[VarDecl],List[Stmt]] # for Else branch, empty list if no Else
        elseConvert = (BooleanLiteral(True), ast.elseStmt[0], ast.elseStmt[1])
        self.checkStatementInput(
            [item[0] for item in ast.ifthenStmt], BoolType(), ast, param)
        for item in ast.ifthenStmt + [elseConvert]:
            self.visitStatementInnerIf((item[1], item[2]), param)

    def visitFor(self, ast, param):
        # idx1: Id
        # expr1:Expr
        # expr2:Expr
        # expr3:Expr
        # loop: Tuple[List[VarDecl],List[Stmt]]
        self.checkStatementInput(
            [ast.idx1, ast.expr1, ast.expr3], IntType(), ast, param)
        self.checkStatementInput([ast.expr2], BoolType(), ast, param)
        self.visitStatementInnerLoop(ast.loop, param)

    def visitContinue(self, ast, param):
        self.breakContinueCheck(ast, param)

    def visitBreak(self, ast, param):
        self.breakContinueCheck(ast, param)

    def visitReturn(self, ast, param):
        # expr:Expr # None if no expression
        funcName = self.getFunctionOuterName(param)
        exprType = VoidType() if not ast.expr else self.visit(ast.expr, param)

        for item in param[-1]:
            if item.name == funcName:
                if isinstance(item.mtype.rettype, ArrayType) or isinstance(exprType, ArrayType):
                    result = self.compareArrayType(item.mtype.rettype, exprType, None, ast.expr, ast, param)
                    if result == "Stop":
                        break

                if item.mtype.rettype == Unknown():
                    item.mtype.rettype = exprType
                    break
                if exprType == Unknown():
                    self.updateType(ast.expr, item.mtype.rettype, param)
                    break

    def visitDowhile(self, ast, param):
        # sl:Tuple[List[VarDecl],List[Stmt]]
        # exp: Expr
        self.visitStatementInnerLoop(ast.sl, param)
        self.checkStatementInput([ast.exp], BoolType(), ast, param)

    def visitWhile(self, ast, param):
        # exp: Expr
        # sl:Tuple[List[VarDecl],List[Stmt]]
        self.checkStatementInput([ast.exp], BoolType(), ast, param)
        self.visitStatementInnerLoop(ast.sl, param)

    def visitCallStmt(self, ast, param):
        # method:Id
        # param:List[Expr]
        returnType = self.checkFuncCall(ast, param)
        if returnType == Unknown():
            self.updateType(ast, VoidType(), param)

    # --------------------------------------------------------------- #
    # -------------------------Visit Literal------------------------- #
    # --------------------------------------------------------------- #
    def visitIntLiteral(self, ast, param):
        return IntType()

    def visitFloatLiteral(self, ast, param):
        return FloatType()

    def visitBooleanLiteral(self, ast, param):
        return BoolType()

    def visitStringLiteral(self, ast, param):
        return StringType()

    def visitArrayLiteral(self, ast, param):
        # value:List[Literal]
        eleType = self.visit(ast.value[0], param)

        arrayDimen = ([len(ast.value)] + eleType.dimen) if isinstance(eleType,ArrayType) else [len(ast.value)]
        while isinstance(eleType, ArrayType):
            eleType = eleType.eleType

        return ArrayType(eleType, arrayDimen)
