
"""
 * @author nhphung
"""
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass
from main.bkit.checker.StaticError import TypeMismatchInStatement
from main.bkit.utils.AST import BooleanLiteral, CallExpr, CallStmt, FuncDecl, IntLiteral
from typing import List, Tuple
from AST import *
from Visitor import *
from StaticError import *
from functools import *
import math

class Type(ABC):
    __metaclass__ = ABCMeta

    def __eq__(self, other):
        return self.__class__ == other.__class__

class Prim(Type):
    __metaclass__ = ABCMeta
    pass

class IntType(Prim):
    pass

class FloatType(Prim):
    pass

class StringType(Prim):
    pass

class BoolType(Prim):
    pass

class VoidType(Type):
    pass

class Unknown(Type):
    pass

@dataclass
class ArrayType(Type):
    dimen: List[int]
    eletype: Type

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.dimen == other.dimen and self.eletype == other.eletype

@dataclass
class MType:
    intype: List[Type]
    restype: Type

@dataclass
class Symbol:
    name: str
    mtype: Type

class StaticChecker(BaseVisitor):
    def __init__(self, ast):
        self.ast = ast
        self.calledFunctions = {}
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
        self.builtinFunction = ["int_of_float","float_to_int", "int_of_string", "string_of_int", "float_of_string", "print",
                                "string_of_float", "bool_of_string", "string_of_bool", "read", "printLn", "printStr", "printStrLn"]

    def check(self):
        return self.visit(self.ast, self.global_envi)

    def visitProgram(self, ast, c):
        # decl : List[Decl]
        globalScope = [self.global_envi]
        for item in ast.decl:
            globalScope[0].append(self.visitFuncDeclAtGlance(item, globalScope)) if isinstance(
                item, FuncDecl) else globalScope[0].append(self.visit(item, globalScope))

        checkEntryPoint = True if any((item.name == "main" and isinstance(item.mtype, MType)) for item in globalScope[0]) else False
        if not checkEntryPoint:
            raise NoEntryPoint()

        for item in ast.decl:
            self.visit(item, globalScope) if isinstance(item, FuncDecl) else None

        for item in globalScope[0]:
            if item.name != "main" and isinstance(item.mtype, MType) and item.name not in self.calledFunctions.keys() and item.name not in self.builtinFunction:
                raise UnreachableFunction(item.name)
        

    # --------------------------------------------------------------- #
    # -------------------------Visit Declare------------------------- #
    # --------------------------------------------------------------- #

    def visitVarDecl(self, ast, param, isParameter=False):
        # variable : Id
        # varDimen : List[int] # empty list for scalar variable
        # varInit  : Literal   # null if no initial
        for item in param[0]:
            if ast.variable.name == item.name and not isParameter:
                raise Redeclared(Variable(), ast.variable.name)
            if ast.variable.name == item.name and isParameter:
                raise Redeclared(Parameter(), ast.variable.name)

        if len(ast.varDimen) == 0:
            return Symbol(ast.variable.name, self.visit(ast.varInit, param)) if ast.varInit else Symbol(ast.variable.name, Unknown())
        else:
            typ = self.visit(ast.varInit, param) if ast.varInit else ArrayType(ast.varDimen, Unknown())
            return Symbol(ast.variable.name, typ)

    def visitFuncDeclAtGlance(self, ast, param):
        # name: Id
        # param: List[VarDecl]
        # body: Tuple[List[VarDecl],List[Stmt]]
        self.checkStatementUnReach(ast.body[1])
        for item in param[0]:
            if ast.name.name == item.name:
                raise Redeclared(Function(), ast.name.name)
        paramGlance = [Unknown() for item in ast.param]
        return Symbol(ast.name.name, MType(paramGlance, Unknown()))

    def visitFuncDecl(self, ast, param):
        param.insert(0, [])
        innerScope = param
        # Check param type
        funcType = None
        for item in ast.param:
            innerScope[0].append(self.visitVarDecl(item, innerScope, True))
        for item in innerScope[-1]:
            if ast.name.name == item.name:
                funcType = item.mtype
                for index in range(len(funcType.intype)):
                    innerScope[0][index].mtype = funcType.intype[index] if innerScope[0][index].mtype == Unknown() else innerScope[0][index].mtype

                    for item in ast.param:
                        if item.variable.name == innerScope[0][index].name:
                            errorParam = item
                            break
                    if(self.compareArrayType(innerScope[0][index].mtype, funcType.intype[index], None, None, errorParam, param) == "Stop"):
                        continue
                    if innerScope[0][index].mtype != Unknown() and funcType.intype[index] != Unknown() and innerScope[0][index].mtype != funcType.intype[index]:
                        raise TypeMismatchInStatement(errorParam)
                break
        for item in ast.body[0]:
            innerScope[0].append(self.visit(item, innerScope))

        #self.updateParameterFuncDecl(ast.name.name, innerScope, len(ast.param))
        innerScope[0].append(Symbol("Function " + ast.name.name, MType([], Unknown())))
        self.updateFromLocalToParam(param)
        for item in ast.body[1]:
            self.visit(item, innerScope)
            self.updateFromLocalToParam(param)

        for item in innerScope[-1]:
            if ast.name.name == item.name:
                if not any(isinstance(miniItem, Return) for miniItem in ast.body[1]) and item.mtype.restype == Unknown():
                    item.mtype.restype = VoidType()
                if item.mtype.restype != VoidType():
                    self.hasReturn(ast.name.name, ast.body[1])
                    if len(ast.body[1]) == 0:
                        raise FunctionNotReturn(ast.name.name)

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
        paramCount = len(funcDecl.mtype.intype)
        newParam = [param[-2][item].mtype for item in range(paramCount)]
        funcDecl.mtype.intype = newParam

    def updateFromParamToLocal(self, funcName, param):
        funcDecl = None
        for item in param[-1]:
            if item.name == funcName and isinstance(item.mtype, MType):
                funcDecl = item
                break
        paramCount = len(funcDecl.mtype.intype)
        for index in range(paramCount):
            param[-2][index].mtype = funcDecl.mtype.intype[index]

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
                        miniItem.mtype.restype = type
                        break
                else:
                    continue
                break
        # update ArrayCell with index operation
        if isinstance(expr, ArrayCell):
            name = expr.arr.name if isinstance(expr.arr, Id) else expr.arr.method.name
            isFuncReturnUpdate = False if isinstance(expr.arr, Id) else True
            for item in param:
                for miniItem in item:
                    if miniItem.name == name and not isFuncReturnUpdate:
                        miniItem.mtype.eletype = type
                        break
                    if miniItem.name == name and isFuncReturnUpdate:
                        miniItem.mtype.restype.eletype = type
                        break
                else:
                    continue
                break
    
    def raiseMisMatchForCheckFuncCall(self, ast):
        if isinstance(ast, CallExpr):
            raise TypeMismatchInExpression(ast)
        if isinstance(ast, CallStmt):
            raise TypeMismatchInStatement(ast)

    def checkFuncCall(self, ast, param):
        # method:Id
        # param:List[Expr]
        if ast.method.name != self.getFunctionOuterName(param):
            self.calledFunctions[ast.method.name] = 1
        self.updateFromLocalToParam(param)

        funcType = None
        for item in param:
            for miniItem in item:
                if miniItem.name == ast.method.name and not isinstance(miniItem.mtype, MType):
                    raise Undeclared(Function(), ast.method.name)
                if miniItem.name == ast.method.name and isinstance(miniItem.mtype, MType):
                    funcType = miniItem.mtype
                    break
        if funcType == None:
            raise Undeclared(Function(), ast.method.name)

        # check param type
        if len(ast.param) != len(funcType.intype):
            self.raiseMisMatchForCheckFuncCall(ast)
        for index in range(len(ast.param)):
            paramType = self.visit(ast.param[index], param)
            inType = funcType.intype[index]

            if paramType == VoidType():
                self.raiseMisMatchForCheckFuncCall(ast)
            if isinstance(inType,ArrayType) or isinstance(paramType, ArrayType):
                result = self.compareArrayType(inType, paramType, None, ast.param[index], ast, param)
                if result == "Stop":
                    continue
                if result == "Type Cannot Be Inferred":
                    return "Type Cannot Be Inferred"

            if paramType == "Type Cannot Be Inferred" or (paramType == Unknown() and inType == Unknown()):
                return "Type Cannot Be Inferred"
            if paramType != Unknown() and inType != Unknown() and paramType != inType:
                self.raiseMisMatchForCheckFuncCall(ast)
            if paramType == Unknown():
                self.updateType(ast.param[index], inType, param)
            if inType == Unknown():
                funcType.intype[index] = paramType
            
            if self.getFunctionOuterName(param) == ast.method.name:
                self.updateFromParamToLocal(ast.method.name, param)

        return funcType.restype

    def checkStatementInput(self, setToCheck, type, ast, param):
        for item in setToCheck:
            exprType = self.visit(item, param)
            if exprType == "Type Cannot Be Inferred":
                raise TypeCannotBeInferred(ast)
            if exprType == Unknown():
                self.updateType(item, type, param)
                self.updateFromLocalToParam(param)
            elif exprType != type:
                raise TypeMismatchInStatement(ast)
    
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
        innerScope[0].append(Symbol("Loop here",StringType()))
        for item in loopStatement[1]:
            self.visit(item, innerScope)
            self.updateFromLocalToParam(param)
        param.pop(0)

    def breakContinueCheck(self, ast, param):
        for item in param:
            for miniItem in item:
                if miniItem.name == "Loop here":
                    return
        raise NotInLoop(ast)

    def getFunctionOuterName(self, param):
        for item in param[-2]:
            if isinstance(item.mtype, MType):
                return item.name.split(' ')[1]

    def getIndexArrayValue(self, indexType):
        if isinstance(indexType, IntLiteral):
            return indexType.value

        if isinstance(indexType, BinaryOp):
            leftVal = self.getIndexArrayValue(indexType.left)
            rightVal = self.getIndexArrayValue(indexType.right)
            if leftVal == -math.inf or rightVal == -math.inf:
                return -math.inf
            op = ['+', '-', '*', '\\', '%']
            value = [leftVal + rightVal, leftVal - rightVal, leftVal * rightVal, math.inf if rightVal == 0 else int(leftVal / rightVal), math.inf if rightVal == 0 else leftVal%rightVal]
            return value[op.index(indexType.op)]
            
        if isinstance(indexType, UnaryOp):
            if(not isinstance(indexType, IntLiteral)):
                value = self.getIndexArrayValue(indexType.body)
                if value == -math.inf:
                    return -math.inf
                return -value

        return -math.inf

    def compareArrayType(self, leftType, rightType, leftUpdate, rightUpdate, ast, param):
        if isinstance(leftType, ArrayType) and isinstance(rightType, ArrayType):
            if leftType.eletype  == Unknown() and rightType.eletype == Unknown():
                return "Type Cannot Be Inferred"
            if leftType.dimen == rightType.dimen:
                if leftType.eletype == Unknown():
                    if leftUpdate == None:
                        leftType = rightType
                    else:
                        self.updateType(leftUpdate, rightType, param)
                    return "Stop"
                if rightType.eletype == Unknown():
                    if rightUpdate == None:
                        rightType = leftType
                    else:
                        self.updateType(rightUpdate, leftType, param)
                    return "Stop"

        if (leftType == Unknown() and isinstance(rightType,ArrayType)):
            if isinstance(leftUpdate, Id):
                raise TypeMismatchInStatement(ast)
            if rightType.eletype == Unknown():
                return "Type Cannot Be Inferred"
        if (rightType == Unknown() and isinstance(leftType,ArrayType)):
            if isinstance(rightUpdate, Id):
                raise TypeMismatchInStatement(ast)
            if leftType.eletype == Unknown():
                return "Type Cannot Be Inferred"

        return "None"

    def checkStatementUnReach(self, stmtList):
        stmtLen = len(stmtList)
        countStopPoint = [0, 0] # sum and return flag
        for index in range(stmtLen):
            if isinstance(stmtList[index], Return) or isinstance(stmtList[index], Break) or isinstance(stmtList[index], Continue):
                countStopPoint[0] = 1
                countStopPoint[1] = 1 if isinstance(stmtList[index], Return) else 0
                if index < stmtLen -1:
                    raise UnreachableStatement(stmtList[index + 1])
            if isinstance(stmtList[index], If):
                ifStmtList = [item[2] for item in stmtList[index].ifthenStmt] + [stmtList[index].elseStmt[1]]
                localCount = 0
                for item in ifStmtList:
                    localCount += self.checkStatementUnReach(item)[0]
                if localCount == len(ifStmtList) and index < stmtLen -1 and stmtList[index].elseStmt[1] != []:
                    raise UnreachableStatement(stmtList[index + 1])
            if isinstance(stmtList[index], For) or isinstance(stmtList[index], While) or isinstance(stmtList[index], Dowhile):
                loopStmtList = stmtList[index].loop[1] if isinstance(stmtList[index], For) else stmtList[index].sl[1]
                self.checkStatementUnReach(loopStmtList)
        return countStopPoint

    def hasReturn(self, funcName, stmtList):
        stmtLen = len(stmtList)
        if stmtLen > 0 and isinstance(stmtList[-1], Return):
            return True
        for index in range(stmtLen):
            if isinstance(stmtList[index], Return):
                return True
            if isinstance(stmtList[index], If):
                ifStmtList = [item[2] for item in stmtList[index].ifthenStmt] + [stmtList[index].elseStmt[1]]
                for item in ifStmtList:
                    if not self.hasReturn(funcName, item) or stmtList[index].elseStmt[1] == []:
                        raise FunctionNotReturn(funcName)
                return True
            if isinstance(stmtList[index], For) or isinstance(stmtList[index], While) or isinstance(stmtList[index], Dowhile):
                loopStmtList = stmtList[index].loop[1] if isinstance(stmtList[index], For) else stmtList[index].sl[1]
                if stmtLen == 1 and not isinstance(stmtList[index], Dowhile):
                    raise FunctionNotReturn(funcName) 
                if not self.hasReturn(funcName, loopStmtList):
                    raise FunctionNotReturn(funcName)
                return True
        raise FunctionNotReturn(funcName)

    # --------------------------------------------------------------- #
    # ------------------------Visit Expression----------------------- #
    # --------------------------------------------------------------- #

    def visitBinaryOp(self, ast, param, expectType = Unknown()):
        # op:str
        # left:Expr
        # right:Expr
        leftType = self.visit(ast.left, param)
        rightType = ""
        if leftType == "Type Cannot Be Inferred":
            return "Type Cannot Be Inferred"

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

        if rightType == "Type Cannot Be Inferred":
            return "Type Cannot Be Inferred"
        raise TypeMismatchInExpression(ast)

    def visitUnaryOp(self, ast, param):
        # op:str
        # body:Expr
        bodyType = self.visit(ast.body, param)
        if bodyType == "Type Cannot Be Inferred":
            return "Type Cannot Be Inferred"

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

        raise TypeMismatchInExpression(ast)

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
        raise Undeclared(Identifier(), ast.name)

    def visitArrayCell(self, ast, param):
        # arr:Expr
        # idx:List[Expr]
        arrType = self.visit(ast.arr, param)
        idxType = [self.visit(item, param) for item in ast.idx]
        if any(item == "Type Cannot Be Inferred" for item in idxType) or arrType == "Type Cannot Be Inferred":
            return "Type Cannot Be Inferred"

        for index in range(len(idxType)):
            if idxType[index] == Unknown():
                self.updateType(ast.idx[index], IntType(), param)
                idxType[index] = IntType()
            if idxType[index] != IntType():
                raise TypeMismatchInExpression(ast)

        if arrType == Unknown():
            if isinstance(ast.arr, Id):
                raise TypeMismatchInExpression(ast)
            return "Type Cannot Be Inferred"

        if not isinstance(arrType, ArrayType) or len(arrType.dimen) != len(idxType):
            raise TypeMismatchInExpression(ast)

        # Index out of range check
        for index in range(len(ast.idx)):
            indexNumber = self.getIndexArrayValue(ast.idx[index])
            if isinstance(indexNumber,IntType) or not isinstance(arrType.dimen[index],int) or indexNumber == -math.inf:
                continue
            if indexNumber == math.inf or indexNumber < 0 or indexNumber >= arrType.dimen[index]:
                raise IndexOutOfRange(ast)

        atomicType = arrType
        while isinstance(atomicType, ArrayType):
            atomicType = atomicType.eletype
        return atomicType

    # --------------------------------------------------------------- #
    # -------------------------Visit Statement----------------------- #
    # --------------------------------------------------------------- #

    def visitAssign(self, ast, param):
        # lhs: LHS
        # rhs: Expr
        lhsType = self.visit(ast.lhs, param)
        rhsType = self.visit(ast.rhs, param)

        if (lhsType == Unknown() and rhsType == Unknown()) or lhsType == "Type Cannot Be Inferred" or rhsType == "Type Cannot Be Inferred":
            raise TypeCannotBeInferred(ast)
        
        if isinstance(ast.lhs, ArrayCell) and isinstance(rhsType, ArrayType):
            raise TypeMismatchInStatement(ast)
        
        if isinstance(lhsType, ArrayType) or isinstance(rhsType, ArrayType):
            result = self.compareArrayType(lhsType, rhsType, ast.lhs, ast.rhs, ast, param)
            if result == "Stop":
                return 
            if result == "Type Cannot Be Inferred":
                raise TypeCannotBeInferred(ast)

        if (lhsType != Unknown() and rhsType != Unknown() and lhsType != rhsType) or lhsType == VoidType() or rhsType == VoidType():
            raise TypeMismatchInStatement(ast)

        if lhsType == Unknown():
            self.updateType(ast.lhs, rhsType, param)
        if rhsType == Unknown():
            self.updateType(ast.rhs, lhsType, param)

    def visitIf(self, ast, param):
        # ifthenStmt:List[Tuple[Expr,List[VarDecl],List[Stmt]]]
        # elseStmt:Tuple[List[VarDecl],List[Stmt]] # for Else branch, empty list if no Else
        elseConvert = (BooleanLiteral(True), ast.elseStmt[0], ast.elseStmt[1])
        self.checkStatementInput([item[0] for item in ast.ifthenStmt],BoolType(), ast, param)
        for item in ast.ifthenStmt + [elseConvert]:
            self.visitStatementInnerIf((item[1],item[2]), param)

    def visitFor(self, ast, param):
        # idx1: Id
        # expr1:Expr
        # expr2:Expr
        # expr3:Expr
        # loop: Tuple[List[VarDecl],List[Stmt]]
        self.checkStatementInput([ast.idx1, ast.expr1, ast.expr3], IntType(), ast, param)
        self.checkStatementInput([ast.expr2],BoolType(), ast, param)
        self.visitStatementInnerLoop(ast.loop, param)

    def visitContinue(self, ast, param):
        self.breakContinueCheck(ast, param)

    def visitBreak(self, ast, param):
        self.breakContinueCheck(ast, param)

    def visitReturn(self, ast, param):
        # expr:Expr # None if no expression
        funcName = self.getFunctionOuterName(param)
        exprType = VoidType() if not ast.expr else self.visit(ast.expr, param)
        if exprType == "Type Cannot Be Inferred":
            raise TypeCannotBeInferred(ast)

        for item in param[-1]:
            if item.name == funcName:
                if (item.mtype.restype == VoidType() or exprType == VoidType()) and ast.expr != None:
                    raise TypeMismatchInStatement(ast)
                
                if isinstance(item.mtype.restype,ArrayType) or isinstance(exprType,ArrayType):
                    result = self.compareArrayType(item.mtype.restype, exprType, None ,ast.expr, ast, param)
                    if result == "Stop": break
                    if result == "Type Cannot Be Inferred":
                        raise TypeCannotBeInferred(ast)

                if item.mtype.restype == Unknown() and exprType == Unknown():
                    raise TypeCannotBeInferred(ast)
                if item.mtype.restype == Unknown():
                    item.mtype.restype = exprType
                    break
                if exprType == Unknown():
                    self.updateType(ast.expr, item.mtype.restype, param)
                    break
                if item.mtype.restype != exprType:
                    raise TypeMismatchInStatement(ast)

    def visitDowhile(self, ast, param):
        # sl:Tuple[List[VarDecl],List[Stmt]]
        # exp: Expr
        self.visitStatementInnerLoop(ast.sl, param)
        self.checkStatementInput([ast.exp],BoolType(), ast, param)

    def visitWhile(self, ast, param):
        # exp: Expr
        # sl:Tuple[List[VarDecl],List[Stmt]]
        self.checkStatementInput([ast.exp],BoolType(), ast, param)
        self.visitStatementInnerLoop(ast.sl, param)

    def visitCallStmt(self, ast, param):
        # method:Id
        # param:List[Expr]
        returnType = self.checkFuncCall(ast, param)
        if returnType == "Type Cannot Be Inferred":
            raise TypeCannotBeInferred(ast)
        if returnType != VoidType() and returnType != Unknown():
            raise TypeMismatchInStatement(ast)
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
        for item in ast.value:
            if self.visit(item, param) != eleType:
                raise InvalidArrayLiteral(ast)

        arrayDimen = ([len(ast.value)] + eleType.dimen) if isinstance(eleType, ArrayType) else [len(ast.value)]
        while isinstance(eleType, ArrayType):
            eleType = eleType.eletype

        return ArrayType(arrayDimen, eleType)
