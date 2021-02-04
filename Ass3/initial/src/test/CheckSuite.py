from main.bkit.utils.AST import BooleanLiteral, CallExpr
from main.bkit.checker.StaticError import Function, Identifier, IndexOutOfRange, InvalidArrayLiteral, NoEntryPoint, NotInLoop, TypeCannotBeInferred, TypeMismatchInExpression, TypeMismatchInStatement, Undeclared, UnreachableFunction
import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

class CheckSuite(unittest.TestCase):
    
    def test_undeclared_function(self):
        """Simple program: main"""
        input = """Function: main
                   Body: 
                        foo();
                   EndBody."""
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_diff_numofparam_stmt(self):
        """Complex program"""
        input = """Function: main  
                   Body:
                        printStrLn();
                    EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,401))
    
    def test_diff_numofparam_expr(self):
        """More complex program"""
        input = """Function: main 
                    Body:
                        printStrLn(read(4));
                    EndBody."""
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_undeclared_function_use_ast(self):
        """Simple program: main """
        input = Program([FuncDecl(Id("main"),[],([],[
            CallExpr(Id("foo"),[])]))])
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_diff_numofparam_expr_use_ast(self):
        """More complex program"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[
                        CallExpr(Id("read"),[IntLiteral(4)])
                        ])]))])
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_diff_numofparam_stmt_use_ast(self):
        """Complex program"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[])]))])
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_1(self):
        input = """
                Var: x;
                Var: y = 123;
                Var: x; 
                Function: main
                    Body:
                    EndBody."""
        expect = str(Redeclared(Variable(), 'x'))
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_2(self):
        input = """
                Var: x;
                Function: x  
                    Body:
                    EndBody.
                Function: main
                    Body:
                    EndBody."""
        expect = str(Redeclared(Function(), 'x'))
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_3(self):
        input = """
                Var: x;
                Function: main
                    Parameter: n, m, x, m
                    Body:
                    EndBody."""
        expect = str(Redeclared(Parameter(), 'm'))
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_4(self):
        input = """
                Var: x;
                Function: main
                    Parameter: n, m, x
                    Body:
                        Var: m;
                    EndBody."""
        expect = str(Redeclared(Variable(), 'm'))
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_5(self):
        input = """
                Var: x;
                Function: main
                    Parameter: n, m
                    Body:
                        Var: x;
                        Var: m;
                    EndBody."""
        expect = str(Redeclared(Variable(), 'm'))
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_6(self):
        input = """
                Var: x;
                Function: y
                    Body:
                    EndBody."""
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_7(self):
        input = """
                Var: x[2] = {1,2};
                Function: main
                    Body:
                        x[1] = 2;
                    EndBody."""
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_8(self):
        input = """
                Var: x[2] = {1,2};
                Function: main
                    Body:
                        foo();
                    EndBody."""
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_9(self):
        input = """
                Var: x, y, z, t;
                Function: main
                    Body:
                        x = 3;
                        m = 4;
                    EndBody."""
        expect = str(Undeclared(Identifier(), 'm'))
        self.assertTrue(TestChecker.test(input,expect,414))

    def test_10(self):
        input = """
                Var: x;
                Function: main
                    Body:
                        x = 5;
                        x = 5.0;
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('x'),FloatLiteral(5.0))))
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_11(self):
        input = """
                Var: x = 5;
                Function: main
                    Body:
                        x = 5.0;
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('x'),FloatLiteral(5.0))))
        self.assertTrue(TestChecker.test(input,expect,416))
    
    def test_12(self):
        input = """
                Var: x = 5;
                Function: main
                    Body:
                        x = {"hello"};
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('x'),ArrayLiteral([StringLiteral('hello')]))))
        self.assertTrue(TestChecker.test(input,expect,417))

    def test_13(self):
        input = """
                Var: x = "Hana";
                Function: main
                    Parameter: x
                    Body:
                        x = 5;
                        x = 5.0;
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('x'),FloatLiteral(5.0))))
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_14(self):
        input = """
                Var: x = "Hana";
                Function: main
                    Parameter: x
                    Body:
                        y = 4;
                    EndBody."""
        expect = str(Undeclared(Identifier(), 'y'))
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_15(self):
        input = """
                Var: x;
                Function: main
                    Parameter: y
                    Body:
                        y = x;
                    EndBody."""
        expect = str(TypeCannotBeInferred(Assign(Id('y'),Id('x'))))
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_16(self):
        input = """
                Var: x = "Hana";
                Function: main
                    Parameter: y
                    Body:
                        x = y;
                        y = 5.0;
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('y'),FloatLiteral(5.0))))
        self.assertTrue(TestChecker.test(input,expect,421))

    def test_17(self):
        input = """
                Var: x;
                Function: main
                    Body:
                        Var: y = 10;
                        x = y;
                        x = 5.0;
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('x'),FloatLiteral(5.0))))
        self.assertTrue(TestChecker.test(input,expect,422))

    def test_18(self):
        input = """
                Function: main
                    Body:
                        foo();
                        x = 2;
                    EndBody.
                Function: foo
                    Body:
                    EndBody."""
        expect = str(Undeclared(Identifier(), 'x'))
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_19(self):
        input = """
                Function: main
                    Body:
                        foo(2);
                    EndBody.
                Function: foo
                    Parameter: y
                    Body:
                        y = 2.3;
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('y'),FloatLiteral(2.3))))
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_20(self):
        input = """
                Var: x = 2;
                Function: main
                    Body:
                        foo(x);
                    EndBody.
                Function: foo
                    Parameter: y
                    Body:
                        y = 2.3;
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('y'),FloatLiteral(2.3))))
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_21(self):
        input = """
                Function: main
                    Body:
                        foo(2, 3, 4);
                    EndBody.
                Function: foo
                    Parameter: y
                    Body:
                        y = 2.3;
                    EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id('foo'),[IntLiteral(2),IntLiteral(3),IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,426))

    def test_22(self):
        input = """
                Var: x[2] = {1,2}; 
                Function: main
                    Body:
                        x[0] = 3;
                        x[1] = "Hello";
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id('x'),[IntLiteral(1)]),StringLiteral('Hello'))))
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_23(self):
        input = """
                Var: x[2][1] = {{1},{2}}; 
                Function: main
                    Body:
                        x[0] = {3};
                    EndBody."""
        expect = str(TypeMismatchInExpression(ArrayCell(Id('x'),[IntLiteral(0)])))
        self.assertTrue(TestChecker.test(input,expect,428))

    def test_24(self):
        input = """
                Var: x[2][1] = {{1.0},{2.0}}; 
                Function: main
                    Body:
                        x[0][0] = 0x12;
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id('x'),[IntLiteral(0),IntLiteral(0)]),IntLiteral(18))))
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_25(self):
        input = """
                Function: main
                    Body:
                        foo()[0] = 0x12;
                    EndBody."""
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,430))

    def test_26(self):
        input = """
                Var: x;
                Function: main
                    Body:
                        x = foo();
                    EndBody.
                Function: foo
                    Body:
                    EndBody."""
        expect = str(TypeCannotBeInferred(Assign(Id('x'),CallExpr(Id('foo'),[]))))
        self.assertTrue(TestChecker.test(input,expect,431))

    def test_27(self):
        input = """
                Var: x = 2;
                Function: main
                    Body:
                        x = foo();
                    EndBody.
                Function: foo
                    Body:
                        Var: y = 1.0;
                        Return y;
                    EndBody."""
        expect = str(TypeMismatchInStatement(Return(Id('y'))))
        self.assertTrue(TestChecker.test(input,expect,432))

    def test_28(self):
        input = """
                Var: x = 2;
                Function: main
                    Body:
                        foo();
                        x = foo();
                    EndBody.
                Function: foo
                    Body:
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('x'),CallExpr(Id('foo'),[]))))
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_29(self):
        input = """
                Var: x = 2;
                Function: foo
                    Body:
                        Var: y = 1;
                        Return y;
                    EndBody.
                Function: main
                    Body:
                        foo();
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(CallStmt(Id('foo'),[])))
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_30(self):
        input = """
                Var: x = 2;
                Function: foo
                    Body:
                        Var: y;
                        Return y;
                    EndBody.
                Function: main
                    Body:
                        foo();
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Return(Id('y'))))
        self.assertTrue(TestChecker.test(input,expect,435))

    def test_31(self):
        input = """
                Var: x = 2, y;
                Function: main
                    Body:
                        x = foo(y);
                    EndBody.
                Function: foo
                    Parameter: t
                    Body:
                        Return t;
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id('x'),CallExpr(Id('foo'),[Id('y')]))))
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_32(self):
        input = """
                Var: x = 2, y;
                Function: main
                    Body:
                        foo(y);
                    EndBody.
                Function: foo
                    Parameter: t
                    Body:
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(CallStmt(Id('foo'),[Id('y')])))
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_33(self):
        input = """
                Var: x[1][1], y;
                Function: main
                    Body:
                        x[y][0] = 2;
                        y = 2.0;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('y'),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_34(self):
        input = """
                Var: x[1][1], y;
                Function: main
                    Body:
                        x[foo(y)][0] = 2;
                    EndBody.
                Function: foo
                    Parameter: t
                    Body:
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(Id('x'),[CallExpr(Id('foo'),[Id('y')]),IntLiteral(0)]),IntLiteral(2))))
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_35(self):
        input = """
                Var: x, y = 1;
                Function: main
                    Body:
                        x = 2 + y + 3.0;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp('+',BinaryOp('+',IntLiteral(2),Id('y')),FloatLiteral('3.0'))))
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_36(self):
        input = """
                Var: x, y = 1, z, t[4] = {1,2,3,4};
                Function: main
                    Body:
                        x = 2 - y \ 3 % y * t[1];
                        z = x;
                        z = "Hana";
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('z'),StringLiteral('Hana'))))
        self.assertTrue(TestChecker.test(input,expect,441))
    
    def test_37(self):
        input = """
                Var: x, y = 1.0, z;
                Function: main
                    Body:
                        x = 2.0 -. y *. 3.0;
                        z = x;
                        z = 2.0 <. 3.0;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('z'),BinaryOp('<.',FloatLiteral(2.0),FloatLiteral(3.0)))))
        self.assertTrue(TestChecker.test(input,expect,442))

    def test_38(self):
        input = """
                Var: x, y = 1.0, z = True, t = 0o123, m;
                Function: main
                    Body:
                        x = -.2.0 -. y *. 3.0;
                        m = -.x;
                        z = m;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('z'),Id('m'))))
        self.assertTrue(TestChecker.test(input,expect,443))

    def test_39(self):
        input = """
                Function: main
                    Parameter: a[3]
                    Body:
                        a = main({1,2,3});
                        Return 2;
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id('a'),CallExpr(Id('main'),[ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])]))))
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_40(self):
        input = """
                Function: main
                    Body:
                        Var: a, b;
                        a = 1 + 2;
                        b = 2. +. foo(1);
                    EndBody.
                Function: foo
                    Parameter: a
                    Body:
                        Return a;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(Id('a'))))
        self.assertTrue(TestChecker.test(input,expect,445))

    def test_41(self):
        input = """
                Var: x[1][2], y[1][2] = {{1,2}};
                Function: main
                    Body:
                        x = y;
                        x = {1,2};
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('x'),ArrayLiteral([IntLiteral(1),IntLiteral(2)]))))
        self.assertTrue(TestChecker.test(input,expect,446))

    def test_42(self):
        input = """
                Var: x[1][2], y[1][2];
                Function: main
                    Body:
                        x = y;
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id('x'),Id('y'))))
        self.assertTrue(TestChecker.test(input,expect,447))
    
    def test_43(self):
        input = """
                Var: x[1][2] = {{1,2}}, y[1][2] = {{1.0,2.0}};
                Function: main
                    Body:
                        x = y;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('x'),Id('y'))))
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_44(self):
        input = """
                Var: x[1][2];
                Function: main
                    Body:
                        x[0][1] = 2;
                        x[0][1] = "Hello";
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id('x'),[IntLiteral(0),IntLiteral(1)]),StringLiteral('Hello'))))
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_45(self):
        input = """
                Var: x[1][1];
                Function: foo
                    Body:
                        Return 1;
                    EndBody.
                Function: main
                    Body:
                        x[0][0] = foo();
                        x = {{1}};
                    EndBody.
                """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,450))

    def test_46(self):
        input = """
                Function: main
                    Body:
                        foo()[1][1] = 1;
                    EndBody.
                Function: foo
                    Body:
                        Var: x[2][2];
                        Return {{1}};
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(CallExpr(Id('foo'),[]),[IntLiteral(1),IntLiteral(1)]),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,451))

    def test_47(self):
        input = """
                Var: x[1], y;
                Function: main
                    Body:
                        x[foo()] = 2;
                        x[goo()] = 1;
                        y = x[foo()] + x[goo()];
                    EndBody.
                Function: foo
                    Body:
                        Return 15%2;
                    EndBody.
                Function: goo
                    Body:
                        Return 1.0 =/= 1.00;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(BinaryOp('=/=',FloatLiteral(1.0),FloatLiteral(1.0)))))
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_48(self):
        input = """
                Var: x = 3.0, y;
                Function: main
                    Body:
                        If True Then 
                            Var: x;
                            x = 2;
                            y = 2;
                        EndIf.
                        y = 1.0;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('y'),FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_49(self):
        input = """
                Var: x = 3.0, y;
                Function: main
                    Body:
                        If bool_of_string("True") Then 
                            Var: x;
                            x = 2;
                            Return x;
                        EndIf.
                        y = 1.0;
                        Return y;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(Id('y'))))
        self.assertTrue(TestChecker.test(input,expect,454))

    def test_50(self):
        input = """
                Var: x = 3.0, y;
                Function: main
                    Body:
                        If y Then 
                            Var: x;
                            x = 2;
                            Return x;
                        EndIf.
                        y = 2.0;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('y'),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_51(self):
        input = """
                Var: x = 3.0, y = 2;
                Function: main
                    Body:
                        If True Then 
                            x = 12.0e3;
                        ElseIf False Then
                            Var: x;
                            x = -0o3;
                        ElseIf True Then
                            Var: x;
                            x = True && False || True;
                            If True Then 
                                Return x;
                            EndIf.
                        Else
                        EndIf.
                        Return y;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(Id('y'))))
        self.assertTrue(TestChecker.test(input,expect,456))

    def test_52(self):
        input = """
                Function: main
                    Body:
                        If foo() Then 
                            foo();
                        EndIf.
                    EndBody.
                Function: foo
                    Body:
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[])))
        self.assertTrue(TestChecker.test(input,expect,457))

    def test_53(self):
        input = """
                Function: main
                    Body:
                        Var: x;
                        If foo(x) Then
                        EndIf.
                    EndBody.
                Function: foo
                    Parameter: x
                    Body:
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(If([(CallExpr(Id('foo'),[Id('x')]),[],[])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,458))

    def test_54(self):
        input = """
                Function: main
                    Body:
                        Var: i;
                        For (i = 0, i <= 10, i + 1) Do 
                            Var: i;
                            i = 2.0;
                        EndFor.
                        i = 5.0;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('i'),FloatLiteral(5.0))))
        self.assertTrue(TestChecker.test(input,expect,459))

    def test_55(self):
        input = """
                Function: main
                    Body:
                        Var: i;
                        For (i = 1, i, i + 1) Do 
                        EndFor.
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(For(Id('i'),IntLiteral(1),Id('i'),BinaryOp('+',Id('i'),IntLiteral(1)),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,460))

    def test_56(self):
        input = """
                Function: main
                    Body:
                        Var: i = 2.0;
                        For (i = 1, True, i + 1) Do 
                        EndFor.
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(For(Id('i'),IntLiteral(1),BooleanLiteral(True),BinaryOp('+',Id('i'),IntLiteral(1)),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,461))

    def test_57(self):
        input = """
                Function: main
                    Body:
                        Var: i = 2;
                        For (i = 1, i != 2, 4.0) Do 
                        EndFor.
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(For(Id('i'),IntLiteral(1),BinaryOp('!=',Id('i'),IntLiteral(2)),FloatLiteral(4.0),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,462))

    def test_58(self):
        input = """
                Function: main
                    Body:
                        Var: i = 0x345;
                        For (i = 1.0, True, i + 1) Do 
                        EndFor.
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(For(Id('i'),FloatLiteral(1.0),BooleanLiteral(True),BinaryOp('+',Id('i'),IntLiteral(1)),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,463))

    def test_59(self):
        input = """
                Function: main
                    Body:
                        Var: i;
                        i = int_of_float(5.0);
                        For (i = 1, True, int_of_float(2.0)) Do 
                            Break;
                            Return i;
                        EndFor.
                        Return;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,464))

    def test_60(self):
        input = """
                Function: main
                    Body:
                        Var: i, x;
                        For (i = 1, True, foo(x)) Do 
                        EndFor.
                    EndBody.
                Function: foo
                    Parameter: x
                    Body:
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(For(Id('i'),IntLiteral(1),BooleanLiteral(True),CallExpr(Id('foo'),[Id('x')]),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,465))

    def test_61(self):
        input = """
                Function: main 
                Body:
                    Var: i, x;
                    Do
                        i = i *. 2.0;
                        If True Then 
                            Var: i;
                            If True Then 
                                i = 5;
                                x = 5;
                                Return i;
                            EndIf.
                        EndIf.
                    While (i <. 50.0) 
                    EndDo. 
                    Return x;
                EndBody.
                """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,466))

    def test_62(self):
        input = """
                Function: main 
                Body:
                    Var: i, x;
                    Do
                        i = 2;
                    While (i <. 50.0) 
                    EndDo. 
                EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp('<.',Id('i'),FloatLiteral(50.0))))
        self.assertTrue(TestChecker.test(input,expect,467))

    def test_63(self):
        input = """
                Function: main 
                Body:
                    Var: i, x;
                    While (i <. 50.0) Do
                        i = 2;
                    EndWhile. 
                EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('i'),IntLiteral(2))))
        self.assertTrue(TestChecker.test(input,expect,468))

    def test_64(self):
        input = """
                Var: main;
                Function: mAIN
                Body:
                    Var: i, x;
                    While (i <. 50.0) Do
                    EndWhile. 
                EndBody.
                """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,469))
    
    def test_65(self):
        input = """
                Function: foo
                    Body:
                        Var: x[2][2];
                        Return {{1}};
                    EndBody.
                Function: main
                    Body:
                        foo()[0][0] = 1;
                    EndBody.
                """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,470))

    def test_66(self):
        input = """
                Function: main
                    Body:
                        Var: x = 1;
                        x = foo()[1][1];
                    EndBody.
                Function: foo
                    Body:
                        Var: x[2][2];
                        Return {{1}};
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id('x'), ArrayCell(CallExpr(Id('foo'),[]),[IntLiteral(1),IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,471))

    def test_67(self):
        input = """
                Function: main
                    Body:
                        Var: x;
                        x[1] = 1;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(ArrayCell(Id('x'),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,472))

    def test_68(self):
        input = """
                Function: main
                    Parameter: a[3]
                    Body:
                        a = {1,2,3};
                        a = main({1,2,3});
                        Return 2;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(2))))
        self.assertTrue(TestChecker.test(input,expect,473))

    def test_69(self):
        input = """
                Function: main
                    Parameter: a[2][1]
                    Body:
                        a = {{1},{2}};
                        a = foo();
                    EndBody.
                Function: foo
                    Body:
                        Return {{1.0},{1.0}};
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(ArrayLiteral([ArrayLiteral([FloatLiteral(1.0)]),ArrayLiteral([FloatLiteral(1.0)])]))))
        self.assertTrue(TestChecker.test(input,expect,474))

    def test_70(self):
        input = """
                Function: main
                    Body:
                        foo()[1] = foo()[3];
                    EndBody.
                Function: foo
                    Body:
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(CallExpr(Id('foo'),[]),[IntLiteral(1)]),ArrayCell(CallExpr(Id('foo'),[]),[IntLiteral(3)]))))
        self.assertTrue(TestChecker.test(input,expect,475))

    def test_71(self):
        input = """ Function: main
                    Parameter: a[1], b[1]
                    Body: 
                        a = b;
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id("a"),Id("b"))))
        self.assertTrue(TestChecker.test(input,expect,476))

    def test_72(self):
        input = """ Function: main
                    Parameter: a[1], b[1]
                    Body: 
                        a[0] = b[0];
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(Id('a'),[IntLiteral(0)]),ArrayCell(Id('b'),[IntLiteral(0)]))))
        self.assertTrue(TestChecker.test(input,expect,477))

    def test_73(self):
        input = """ Var: a;
                    Function: main
                    Body: 
                        Var: a = 2;
                        a = foo;
                    EndBody.
                    Function: foo
                    Body:
                        Return;
                    EndBody.
                """
        expect = str(Undeclared(Identifier(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,478))

    def test_74(self):
        input = """ Function: main
                    Parameter: x,y,z
                    Body: 
                        y = x || (x > z);
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp('>',Id('x'),Id('z'))))
        self.assertTrue(TestChecker.test(input,expect,479))

    def test_75(self):
        input = """ Function: main
                    Body: 
                        Var: a;
                        a = {1,2};
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),ArrayLiteral([IntLiteral(1),IntLiteral(2)]))))
        self.assertTrue(TestChecker.test(input,expect,480))

    def test_76(self):
        input = """ Function: f1
                    Parameter: x
                    Body: 
                        Return {0};
                    EndBody.
        
                    Function: main
                    Parameter: x
                    Body:
                        Var: a[1], n;
                        f1(f2(f3(n)))[0] = a[f3(f2(n))];
                    EndBody.

                    Function: f2
                    Parameter: x
                    Body:
                        Return 0;
                    EndBody.

                    Function: f3
                    Parameter: x
                    Body:
                        Return 0;
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(CallExpr(Id("f1"),[CallExpr(Id("f2"),[CallExpr(Id("f3"),[Id("n")])])]),[IntLiteral(0)]),ArrayCell(Id("a"),[CallExpr(Id("f3"),[CallExpr(Id("f2"),[Id("n")])])]))))
        self.assertTrue(TestChecker.test(input,expect,481))

    def test_77(self):
        input = """ 
                Function: main
                Body:
                    foo(1.1);
                EndBody.
                Function: foo
                Parameter: x
                Body:
                    x=1;
                    Return;
                EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('x'),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,482))

    def test_78(self):
        input = """ Function: foo
                    Parameter: x, y
                    Body:
                        Return x +. y;
                    EndBody.
                    Function: main
                    Parameter: x, y
                    Body: 
                        x = foo(5, 6);
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[IntLiteral(5),IntLiteral(6)])))
        self.assertTrue(TestChecker.test(input,expect,483))

    def test_79(self):
        input = """
                Var: x[2][3], y[2][3];
                Function: main
                    Body:
                        x[1][2] = 3;
                        x = y;
                        y[1][2] = "Hana";
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id('y'),[IntLiteral(1),IntLiteral(2)]),StringLiteral('Hana'))))
        self.assertTrue(TestChecker.test(input,expect,484))

    def test_80(self):
        input = """
                Var: x[2][3], y[1][7];
                Function: main
                    Body:
                        x[1][2] = 3;
                        x = y;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('x'),Id('y'))))
        self.assertTrue(TestChecker.test(input,expect,485))

    def test_81(self):
        input = """
                Function: foo
                    Body:
                        Return "hana";
                    EndBody.
                ** Comment cho vui ** ** Hihi**
                Function: main
                    Body:
                        foo()[2] = 3;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(ArrayCell(CallExpr(Id('foo'),[]),[IntLiteral(2)])))
        self.assertTrue(TestChecker.test(input,expect,486))

    def test_82(self):
        input = """
                Function: main
                    Parameter: x,y,z
                    Body: 
                        y = x || (x + (x && z));
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp('+',Id('x'),BinaryOp('&&',Id('x'),Id('z')))))
        self.assertTrue(TestChecker.test(input,expect,487))

    def test_83(self):
        input = """
                Function: main
                    Body:
                        Var: x;
                        x = (1<=3) || 2 && (3 == 3);
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp('||',BinaryOp('<=',IntLiteral(1),IntLiteral(3)),IntLiteral(2))))
        self.assertTrue(TestChecker.test(input,expect,488))

    def test_84(self):
        input = """
                Function: f
                Parameter: a, b
                Body:
                    If int_of_float(b -. 100e1) < 1 Then
                        a = f(1000, b -. 1.0);
                    EndIf.
                    Return a;
                EndBody.

                Function: main
                    Body:
                        f(1,1.0);
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id('a'),CallExpr(Id('f'),[IntLiteral(1000),BinaryOp('-.',Id('b'),FloatLiteral(1.0))]))))
        self.assertTrue(TestChecker.test(input,expect,489))

    def test_85(self):
        input = """
                Function: main
                    Parameter: x,y,z
                    Body: 
                        y = x + (x +. 2.0);
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp('+.',Id('x'),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,490))

    def test_86(self):
        input = """
                Function: main
                    Parameter: x,y,z
                    Body: 
                        y = x + foo(x) + foo(30.07);
                    EndBody.
                Function: foo
                    Parameter: x
                    Body:
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(CallExpr(Id('foo'),[FloatLiteral(30.07)])))
        self.assertTrue(TestChecker.test(input,expect,491))

    def test_87(self):
        input = """
                Function: main
                    Parameter: x, y, z;
                    Body: 
                        z = 3;
                        y = z + (x +. 2.0);
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp('+',Id('z'),BinaryOp('+.',Id('x'),FloatLiteral(2.0)))))
        self.assertTrue(TestChecker.test(input,expect,492))

    def test_88(self):
        input = """
                Function: main
                Parameter: i
                Body:
                    Var: a;
                    For (i = 10, a >. 2.0,0) Do
                        If a =/= 2. Then
                            Return 1;
                        EndIf.
                        Break;
                    EndFor.
                    Return a;
                EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(Id('a'))))
        self.assertTrue(TestChecker.test(input,expect,493))

    def test_89(self):
        input = """
                Function: main
                Parameter: x[1], y[1]
                Body:
                    x[y[0]] = y[0];
                EndBody.
                """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,494))

    def test_90(self):
        input = """
                Function: foo
                    Parameter: x,y
                    Body:
                        Var: z,k[1][2];
                        If z ==  1 Then 
                            Return 1;
                        Else 
                            x = 1 + main(foo(0,0));
                        EndIf.
                    EndBody.

                Function: main
                Parameter: a
                Body:
                    a = foo(1,1);
                    Return 1;
                EndBody.
                """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,495))

    def test_91(self):
        input = """
                Function: main
                Parameter: main
                Body:
                    main(2);
                EndBody.
                """
        expect = str(Undeclared(Function(),'main'))
        self.assertTrue(TestChecker.test(input,expect,496))

    def test_92(self):
        input = """
        Function: f
            Parameter: a, b
            Body:
                If int_of_float(b -. 100e1) < 1 Then
                    f(1000, b -. 1.0);
                EndIf.
                Return a;
            EndBody.

        Function: main
            Body:
            f(1,1.0);
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(Id('a'))))
        self.assertTrue(TestChecker.test(input, expect, 497))

    def test_93(self):
        input = """
                Function: main
                Parameter: a[2]
                Body:
                    Return a;
                EndBody.
                """
        expect = str(TypeCannotBeInferred(Return(Id('a'))))
        self.assertTrue(TestChecker.test(input,expect,498))

    def test_94(self):
        input = """
                Var: x[2];

                Function: main
                Body:
                    Var: a[2] = {1,2};
                    a = foo();
                EndBody.

                Function: foo
                Body:
                    Return x;
                EndBody.

                Function: goo
                Body:
                    x[0] = "Hana";
                EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id('x'),[IntLiteral(0)]),StringLiteral('Hana'))))
        self.assertTrue(TestChecker.test(input,expect,499))

    def test_95(self):
        input = """Function: main
                   Body: 
                        Return foo();
                   EndBody.
                   Function: foo
                   Body: 
                   EndBody."""
        expect = str(TypeCannotBeInferred(Return(CallExpr(Id('foo'),[]))))
        self.assertTrue(TestChecker.test(input,expect,500))

    def test_96(self):
        input = """ 
                    Function: foo
                        Body: 
                            Return {1,2,3};
                        EndBody.
                    Function: main
                        Body: 
                            Return foo();
                        EndBody.
                   """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,700))

    def test_97(self):
        input = """ 
                    Function: foo
                        Parameter: x[1], y[1]
                        Body: 
                        EndBody.
                    Function: main
                        Body: 
                            Var: x[1];
                            foo(x, {1});
                        EndBody.
                   """
        expect = str(TypeCannotBeInferred(CallStmt(Id('foo'),[Id('x'),ArrayLiteral([IntLiteral(1)])])))
        self.assertTrue(TestChecker.test(input,expect,701))

    def test_98(self):
        input = """ 
                    Function: foo
                        Parameter: x[1], y
                        Body: 
                        EndBody.
                    Function: main
                        Body: 
                            Var: x[1] = {1}, y;
                            foo(x, y);
                        EndBody.
                   """
        expect = "Type Cannot Be Inferred: CallStmt(Id(foo),[Id(x),Id(y)])"
        self.assertTrue(TestChecker.test(input,expect,702))

    def test_99(self):
        input = """ 
                    Function: foo
                        Body: 
                        EndBody.
                    Function: main
                        Body: 
                            Var: x = 2;
                            x = foo();
                        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Assign(Id('x'),CallExpr(Id('foo'),[]))))
        self.assertTrue(TestChecker.test(input,expect,703))

    def test_100(self):
        input = """ 
                    Function: main
                        Body: 
                            Var: x[2];
                            x[1] = {1};
                        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id('x'),[IntLiteral(1)]),ArrayLiteral([IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,704))

    def test_101(self):
        input = """ 
                    Function: main
                        Body: 
                            Var: x = 2;
                            x = foo(1,2);
                        EndBody.
                    Function: foo
                        Parameter: x[2],y
                        Body: 
                            Return 1;
                        EndBody.
                   """
        expect = str(TypeMismatchInStatement(VarDecl(Id('x'),[2],None)))
        self.assertTrue(TestChecker.test(input,expect,705))

    def test_102(self):
        input = """ 
                    Function: main
                        Body: 
                            Var: x = 2;
                            x = foo();
                            x = goo();
                        EndBody.
                    Function: goo
                        Body: 
                            Var: x[2];
                            Return x[0];
                        EndBody.
                    Function: foo
                        Body: 
                            Var: x[2];
                            Return x;
                        EndBody.
                   """
        expect = str(TypeMismatchInStatement(Return(Id('x'))))
        self.assertTrue(TestChecker.test(input,expect,706))

    def test_103(self):
        input = """
            Function: main
            Body:
                Var: a[2], b[2] = {"a", "b"};
                f(a)[0] = b[1];
                Return 1;
            EndBody.

            Function: f
            Parameter: a[2]
            Body:
                Return a;
            EndBody.

        """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(CallExpr(Id('f'),[Id('a')]),[IntLiteral(0)]),ArrayCell(Id('b'),[IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input, expect, 707))

    def test_104(self):
        input = """
            Function: main
            Body:
                Var: a[2], b[2] = {"a", "b"}, c;
                If True Then 
                    Return 1;
                EndIf.         
                c = f(b, f(a, b))[0];
                Return c;
            EndBody.

            Function: f
            Parameter: a[2], b[2]
            Body:
                Return a;
            EndBody.

        """
        expect = str(TypeMismatchInStatement(Return(Id('c'))))
        self.assertTrue(TestChecker.test(input, expect, 708))

    def test_105(self):
        input = """
            Function: main
            Body:
                Var: a[2] = {"a", "b"}, b[2] = {"a", "b"}, c = 1;     
                c = f(a,b);
            EndBody.

            Function: f
            Parameter: a[4], b[2]
            Body:
            EndBody.
        """
        expect = str(TypeMismatchInStatement(VarDecl(Id('a'),[4],None)))
        self.assertTrue(TestChecker.test(input, expect, 709))

    def test_106(self):
        input = """
            Function: main
            Body:
                Var: a, b, c;     
                c = int_of_float(10.0);
                a = float_of_int(10.0);
            EndBody.
        """
        expect = str(Undeclared(Function(),'float_of_int'))
        self.assertTrue(TestChecker.test(input, expect, 710))

    def test_107(self):
        input = """
            Var: x[10];
            Function: main
            Body:
                test()[0] = 1;
                test()[1] = "s";
            EndBody.
            Function: test
            Body:
                Return x;
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(CallExpr(Id('test'),[]),[IntLiteral(0)]),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,711))

    def test_bubble_sort(self):
        input = """
            Function: main
            Body:
                Var: x[10];
                Var: iter;
                For(iter = 0, iter < 10, iter + 1) Do
                    x[iter] = float_of_string(read());
                EndFor.
                bubbleSort(x);
            EndBody.
            Function: bubbleSort
                Parameter: x[10]
                Body:
                    Var: iter, innerIter;
                    For(iter = 0, iter < 10, iter + 1) Do
                        For(innerIter = iter, innerIter < 10, innerIter + 1) Do
                            If x[iter] >. x[innerIter] Then
                                Var: temp;
                                temp = x[iter];
                                x[iter] = x[innerIter];
                                x[innerIter] = temp;
                            EndIf.
                        EndFor.
                    EndFor.
                    For(iter = 0, iter < 10, iter + 1) Do
                        printStr(string_of_float(x[iter]));
                    EndFor.
                EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,712))

    def test_108(self):
        input = """
            Function: foo
                Body:
                EndBody.
            Function: main
                Body:
                    Return foo();
                EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(CallExpr(Id('foo'),[]))))
        self.assertTrue(TestChecker.test(input,expect,713))

    def test_109(self):
        input = """
            Var: x[10], y;
            Function: main
            Body:
                Var: k;
                k = -x[foo(x[0])];
                x = f();
            EndBody.
            Function: foo
            Parameter: y
            Body:
                Return y;
            EndBody.
            Function: f
            Body:
                Var: k[10];
                If k[2] Then
                    Return k;
                EndIf.
                Return x;
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(Id('k'),UnaryOp('-',ArrayCell(Id('x'),[CallExpr(Id('foo'),[ArrayCell(Id('x'),[IntLiteral(0)])])])))))
        self.assertTrue(TestChecker.test(input,expect,714))

    def test_110(self):
        input = """
            Var: x[10], y;
            Function: main
                Body:        
                    foo(x);
                EndBody.
            Function: foo
                Parameter: y
                Body:
                EndBody.
        """
        expect = str(TypeCannotBeInferred(CallStmt(Id('foo'),[Id('x')])))
        self.assertTrue(TestChecker.test(input,expect,715))

    def test_111(self):
        input = """
            Var: x, y, z;
            Function: main
                Body:        
                    y =  int_of_float(x) + 1;
                    x = z;
                    z = 1.0;
                EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,716))

    def test_112(self):
        input = """
        Var: x, a[10], b[5];
        Function: foo
        Parameter: k
        Body:
            a[0] = 1;
            Return a;
        EndBody.
        Function: main
        Parameter: x
        Body:
            If x == 2 Then
            ElseIf b[x] != b[0] Then
            EndIf.
            foo(0e-2)[9] = b[x + 2]*b[x + foo(1e-2)[2 + foo(2.0202)[0 * foo(1.2)[x \ 2]]]] - a[a[a[a[x]]]];
        EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input, expect, 717))

    def test_113(self):
        input = """
        Var: x, a[10], b[5];
        Function: main
        Parameter: x
        Body:
            If b[2] == 2 Then
            ElseIf b[2] && (b[0] || b[4]) Then
            EndIf.
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp('&&',ArrayCell(Id('b'),[IntLiteral(2)]),BinaryOp('||',ArrayCell(Id('b'),[IntLiteral(0)]),ArrayCell(Id('b'),[IntLiteral(4)])))))
        self.assertTrue(TestChecker.test(input, expect, 718))

    def test_114(self):
        input = """
                Function: main
                Parameter: x
                Body:
                    If main(main(5)) Then EndIf. 
                EndBody.
                """
        expect = "Type Mismatch In Statement: If(CallExpr(Id(main),[CallExpr(Id(main),[IntLiteral(5)])]),[],[])Else([],[])"
        self.assertTrue(TestChecker.test(input, expect, 719))

    def test_115(self):
        input = """
            Var: x, a[10], b[5];
            Function: main
            Parameter: x
            Body:
                If foo()[2] == x Then
                ElseIf b[2] && (b[0] || b[4]) Then
                EndIf.
            EndBody.
            Function: foo
            Body:
                a[0] = 1;
                Return a;
            EndBody.
        """
        expect = str(TypeCannotBeInferred(If([(BinaryOp('==',ArrayCell(CallExpr(Id('foo'),[]),[IntLiteral(2)]),Id('x')),[],[]),(BinaryOp('&&',ArrayCell(Id('b'),[IntLiteral(2)]),BinaryOp('||',ArrayCell(Id('b'),[IntLiteral(0)]),ArrayCell(Id('b'),[IntLiteral(4)]))),[],[])], ([],[]))))
        self.assertTrue(TestChecker.test(input, expect, 720))

    def test_116(self):
        input = """
            Var: a, b[2][2], c;
            Function: test
                Parameter: k
                Body:
                    Do
                        test(1);
                    While k EndDo.
                EndBody.
            Function: main
                Body:
                    b[f()][f()] = 123;
                EndBody.
            Function: f
                Body:
                    Var: c[2][3];
                    Return 1;
                EndBody.
        """
        expect =  str(TypeMismatchInStatement(Dowhile(([],[CallStmt(Id('test'),[IntLiteral(1)])]),Id('k'))))
        self.assertTrue(TestChecker.test(input, expect, 721))

    def test_117(self):
        input = """
            Function: main
                Parameter: k
                Body:
                    Do
                        k = 1;
                    While k EndDo.
                EndBody.
        """
        expect =  "Type Mismatch In Statement: Dowhile([],[Assign(Id(k),IntLiteral(1))],Id(k))"
        self.assertTrue(TestChecker.test(input, expect, 722))

    def test_118(self):
        input = """
            Function: main
                Parameter: k
                Body:
                    Var: x;
                    If main(1) Then
                        x = main(True);
                    EndIf.
                EndBody.
        """
        expect =  "Type Mismatch In Expression: CallExpr(Id(main),[BooleanLiteral(true)])"
        self.assertTrue(TestChecker.test(input, expect, 723))

    def test_119(self):
        input = """
            Function: main
            Parameter: x, y
            Body:
                Return x + main(y, x);
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input, expect, 724))

    def test_120(self):
        input = """
            Var: a, b, arr[10][10];
            Function: main
            Parameter: x, y, main
            Body:
                If main && x Then
                    Return y + 1;
                EndIf.
                Return arr[0][0];
            EndBody.
            Function: foo
            Parameter: x, y
            Body:
                arr[0][1] = "s";
            EndBody.
        """
        expect = "Type Mismatch In Statement: Assign(ArrayCell(Id(arr),[IntLiteral(0),IntLiteral(1)]),StringLiteral(s))"
        self.assertTrue(TestChecker.test(input, expect, 725))

    def test_121(self):
        input = """                    
                    Function: main
                    Parameter: x, y
                    Body:                        
                        x = main(1, 2);
                        Return;
                    EndBody.   
                """
        expect = str("Type Cannot Be Inferred: Assign(Id(x),CallExpr(Id(main),[IntLiteral(1),IntLiteral(2)]))")
        self.assertTrue(TestChecker.test(input, expect, 726))

    def test_122(self):
        input = """                    
                    Function: main
                        Parameter: x, y, z, t[3]
                        Body:                        
                            z = x +. t[x];
                            Return;
                        EndBody.   
                """
        expect = str(TypeMismatchInExpression(ArrayCell(Id('t'),[Id('x')])))
        self.assertTrue(TestChecker.test(input, expect, 727))

    def test_123(self):
        input = """ 
                    Function: foo
                        Body:
                        EndBody.                 
                    Function: main
                        Parameter: foo
                        Body:                        
                            If True Then
                                foo();
                            EndIf.
                        EndBody.   
                """
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input, expect, 728))

    #----------------------------------------------------------------#
    #------------------------KSTN Test case--------------------------#
    #----------------------------------------------------------------#
    # def test_kstn_1(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Break;
    #                 EndBody.
    #             """
    #     expect = str(NotInLoop(Break()))
    #     self.assertTrue(TestChecker.test(input,expect,501))

    # def test_kstn_2(self):
    #     input = """
    #             Function: main 
    #             Body:
    #                 Var: i;
    #                 While (i <. 50.0) Do
    #                     Break;
    #                 EndWhile. 
    #                 Continue;
    #             EndBody.
    #             """
    #     expect = str(NotInLoop(Continue()))
    #     self.assertTrue(TestChecker.test(input,expect,502))

    # def test_kstn_3(self):
    #     input = """
    #             Function: main 
    #             Body:
    #                 Var: i;
    #                 While (i < 50) Do
    #                     For (i = 0, i <= 10, i + 1) Do 
    #                         Break;
    #                     EndFor.
    #                 EndWhile. 
    #                 Continue;
    #             EndBody.
    #             """
    #     expect = str(NotInLoop(Continue()))
    #     self.assertTrue(TestChecker.test(input,expect,503))

    # def test_kstn_4(self):
    #     input = """
    #             Function: main 
    #             Body:
    #                 Var: i;
    #                 While (i < 50) Do
    #                     For (i = 0, i <= 10, i + 1) Do 
    #                         If True Then 
    #                             Break;
    #                         EndIf.
    #                     EndFor.
    #                 EndWhile. 
    #                 Continue;
    #             EndBody.
    #             """
    #     expect = str(NotInLoop(Continue()))
    #     self.assertTrue(TestChecker.test(input,expect,504))

    # def test_kstn_5(self):
    #     input = """
    #             Function: main 
    #             Body:
    #                 Var: i;
    #                 While (i < 50) Do
    #                     If True Then 
    #                         If True Then 
    #                         Else
    #                             Break;
    #                         EndIf.
    #                     EndIf.
    #                 EndWhile. 
    #                 Continue;
    #             EndBody.
    #             """
    #     expect = str(NotInLoop(Continue()))
    #     self.assertTrue(TestChecker.test(input,expect,505))

    # def test_kstn_6(self):
    #     input = """
    #             Function: main 
    #             Body:
    #                 If True Then 
    #                 ElseIf False Then
    #                 ElseIf True Then
    #                     Continue;
    #                 Else
    #                 EndIf.
    #             EndBody.
    #             """
    #     expect = str(NotInLoop(Continue()))
    #     self.assertTrue(TestChecker.test(input,expect,506))

    # def test_kstn_7(self):
    #     input = """
    #             Function: main 
    #             Body:
    #                 Var: x[2] = {1, 2, 3.0};
    #             EndBody.
    #             """
    #     expect = str(InvalidArrayLiteral(ArrayLiteral([IntLiteral(1),IntLiteral(2),FloatLiteral(3.0)])))
    #     self.assertTrue(TestChecker.test(input,expect,507))

    # def test_kstn_8(self):
    #     input = """
    #             Var: x[2] = {1,"Hello"};
    #             Function: main
    #                 Body:
    #                 EndBody."""
    #     expect = str(InvalidArrayLiteral(ArrayLiteral([IntLiteral(1),StringLiteral('Hello')])))
    #     self.assertTrue(TestChecker.test(input,expect,508))

    # def test_kstn_9(self):
    #     input = """
    #             Var: x[2] = {{1},{1}, 1};
    #             Function: main
    #                 Body:
    #                 EndBody."""
    #     expect = str(InvalidArrayLiteral(ArrayLiteral([ArrayLiteral([IntLiteral(1)]),ArrayLiteral([IntLiteral(1)]),IntLiteral(1)])))
    #     self.assertTrue(TestChecker.test(input,expect,509))

    # def test_kstn_10(self):
    #     input = """
    #             Var: x[2] = {{{1}},{1}};
    #             Function: main
    #                 Body:
    #                 EndBody."""
    #     expect = str(InvalidArrayLiteral(ArrayLiteral([ArrayLiteral([ArrayLiteral([IntLiteral(1)])]),ArrayLiteral([IntLiteral(1)])])))
    #     self.assertTrue(TestChecker.test(input,expect,510))

    # def test_kstn_11(self):
    #     input = """
    #             Var: x[2] = {{{1, 3.0}},{1}};
    #             Function: main
    #                 Body:
    #                 EndBody."""
    #     expect = str(InvalidArrayLiteral(ArrayLiteral([IntLiteral(1),FloatLiteral(3.0)])))
    #     self.assertTrue(TestChecker.test(input,expect,511))

    # def test_kstn_12(self):
    #     input = """
    #             Function: goo
    #                 Body:
    #                     foo();
    #                 EndBody.
    #             Function: main
    #                 Body:
    #                 EndBody.
    #             Function: foo
    #                 Body:
    #                 EndBody."""
    #     expect = str(UnreachableFunction('goo'))
    #     self.assertTrue(TestChecker.test(input,expect,512))

    # def test_kstn_13(self):
    #     input = """
    #             Function: goo
    #                 Body:
    #                 EndBody.
    #             Function: main
    #                 Body:
    #                     main();
    #                 EndBody.
    #             Function: foo
    #                 Body:
    #                     foo();
    #                 EndBody."""
    #     expect = str(UnreachableFunction('goo'))
    #     self.assertTrue(TestChecker.test(input,expect,513))

    # def test_kstn_14(self):
    #     input = """
    #             Function: goo
    #                 Body:
    #                 EndBody.
    #             Function: main
    #                 Body:
    #                     goo();
    #                 EndBody.
    #             Function: foo
    #                 Body:
    #                     foo();
    #                 EndBody."""
    #     expect = str(UnreachableFunction('foo'))
    #     self.assertTrue(TestChecker.test(input,expect,514))

    # def test_kstn_15(self):
    #     input = """
    #             Var: x[2][2];
    #             Function: main
    #                 Body:
    #                     x[1][1] = 2;
    #                     x[0][2] = -3;
    #                 EndBody."""
    #     expect = str(IndexOutOfRange(ArrayCell(Id('x'),[IntLiteral(0),IntLiteral(2)])))
    #     self.assertTrue(TestChecker.test(input,expect,515))

    # def test_kstn_16(self):
    #     input = """
    #             Var: x[2][2][2], y = 5, z;
    #             Function: main
    #                 Body:
    #                     x[y][z][2] = 2;
    #                 EndBody."""
    #     expect = str(IndexOutOfRange(ArrayCell(Id('x'),[Id('y'),Id('z'),IntLiteral(2)])))
    #     self.assertTrue(TestChecker.test(input,expect,516))

    # def test_kstn_17(self):
    #     input = """
    #             Var: x[2][2][2];
    #             Function: main
    #                 Body:
    #                     x[0][-1][0] = 2;
    #                 EndBody."""
    #     expect = str(IndexOutOfRange(ArrayCell(Id('x'),[IntLiteral(0),UnaryOp('-',IntLiteral(1)),IntLiteral(0)])))
    #     self.assertTrue(TestChecker.test(input,expect,517))

    # def test_kstn_18(self):
    #     input = """
    #             Var: x[2][2], y;
    #             Function: main
    #                 Body:
    #                     y = x[-0][--1] + 2;
    #                 EndBody."""
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,518))

    # def test_kstn_19(self):
    #     input = """
    #             Var: x[2][2], y;
    #             Function: main
    #                 Body:
    #                     y = x[1][---1] + 2;
    #                 EndBody."""
    #     expect = str(IndexOutOfRange(ArrayCell(Id('x'),[IntLiteral(1),UnaryOp('-',UnaryOp('-',UnaryOp('-',IntLiteral(1))))])))
    #     self.assertTrue(TestChecker.test(input,expect,519))

    # def test_kstn_20(self):
    #     input = """
    #             Var: x[2][2], y, z;
    #             Function: main
    #                 Body:
    #                     y = x[1][-z] + 2;
    #                 EndBody."""
    #     expect = str()
    #     self.assertTrue(TestChecker.test(input,expect,520))

    # def test_kstn_21(self):
    #     input = """
    #             Var: x[2][3], y, z;
    #             Function: main
    #                 Body:
    #                     y = x[1][1+1] + 2;
    #                     x[2-3][1] = 3;
    #                 EndBody."""
    #     expect = str(IndexOutOfRange(ArrayCell(Id('x'),[BinaryOp('-',IntLiteral(2),IntLiteral(3)),IntLiteral(1)])))
    #     self.assertTrue(TestChecker.test(input,expect,521))

    # def test_kstn_22(self):
    #     input = """
    #             Var: x[2][3], y, z;
    #             Function: main
    #                 Body:
    #                     y = x[1][-1+1] + 2;
    #                     x[3%2][1*2] = 3;
    #                     x[1][3\\-0] = 1;
    #                 EndBody."""
    #     expect = str(IndexOutOfRange(ArrayCell(Id('x'),[BinaryOp('%',IntLiteral(3),IntLiteral(2)),BinaryOp('*',IntLiteral(1),IntLiteral(2))])))
    #     self.assertTrue(TestChecker.test(input,expect,522))

    # def test_kstn_23(self):
    #     input = """
    #             Var: x[2][3], y, z;
    #             Function: main
    #                 Body:
    #                     y = x[-z][4 + 5 - z] + 2;
    #                     x[z * 7][z % 2] = 2;
    #                     x[z \\ 0][z-7] = 1;
    #                     x[z][1\\0] = 1;
    #                 EndBody."""
    #     expect = str(IndexOutOfRange(ArrayCell(Id('x'),[Id('z'),BinaryOp('\\',IntLiteral(1),IntLiteral(0))])))
    #     self.assertTrue(TestChecker.test(input,expect,523))
    
    


        