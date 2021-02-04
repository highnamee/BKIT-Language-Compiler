import unittest
from TestUtils import TestAST
from AST import *

from main.bkit.utils.AST import CallExpr, IntLiteral

class ASTGenSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """Var:x;"""
        expect = Program([VarDecl(Id("x"),[],None)])
        self.assertTrue(TestAST.checkASTGen(input,expect,300))

    def test_simple_program_2(self):
        """Simple program: int main() {} """
        input = """Var:x[1][2];"""
        expect = Program([VarDecl(Id("x"),[1,2],None)])
        self.assertTrue(TestAST.checkASTGen(input,expect,301))

    def test_simple_program_3(self):
        """Simple program: int main() {} """
        input = """Var:x,y;"""
        expect = Program([VarDecl(Id("x"),[],None), VarDecl(Id("y"),[],None)])
        self.assertTrue(TestAST.checkASTGen(input,expect,302))

    def test_simple_program_4(self):
        """Simple program: int main() {} """
        input = """Var:x[2] = 6;"""
        expect = Program([VarDecl(Id("x"),[2],IntLiteral(6))])
        self.assertTrue(TestAST.checkASTGen(input,expect,303))

    def test_simple_program_5(self):
        """Simple program: int main() {} """
        input = """Var:x[2] = True;"""
        expect = Program([VarDecl(Id("x"),[2],BooleanLiteral(True))])
        self.assertTrue(TestAST.checkASTGen(input,expect,304))

    def test_simple_program_6(self):
        """Simple program: int main() {} """
        input = """Var:x[2] = "Hello my fen";"""
        expect = Program([VarDecl(Id("x"),[2],StringLiteral("Hello my fen"))])
        self.assertTrue(TestAST.checkASTGen(input,expect,305))

    def test_simple_program_7(self):
        """Simple program: int main() {} """
        input = """Var:x[2] = {1,2,  3};"""
        expect = Program([VarDecl(Id("x"),[2],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,306))

    def test_simple_program_8(self):
        """Simple program: int main() {} """
        input = """Var:x,y = 4;"""
        expect = Program([VarDecl(Id("x"),[],None), VarDecl(Id("y"),[],IntLiteral(4))])
        self.assertTrue(TestAST.checkASTGen(input,expect,307))

    def test_simple_program_9(self):
        """Simple program: int main() {} """
        input = """Var: m, n[10], b[2][3] = {2,{4}};"""
        expect = Program([VarDecl(Id("m"),[],None), VarDecl(Id("n"),[10],None), VarDecl(Id("b"),[2,3],ArrayLiteral([IntLiteral(2), ArrayLiteral([IntLiteral(4)])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,308))

    def test_simple_program_10(self):
        """Simple program: int main() {} """
        input = """Var: m, n[10], b[2][3] = {{},{4}};"""
        expect = Program([VarDecl(Id("m"),[],None), VarDecl(Id("n"),[10],None), VarDecl(Id("b"),[2,3],ArrayLiteral([ArrayLiteral([]), ArrayLiteral([IntLiteral(4)])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,309))

    def test_simple_program_11(self):
        """Simple program: int main() {} """
        input = """Var: x;
                Function: main 
                    Body:
                    EndBody."""
        expect = Program([VarDecl(Id("x"),[],None),FuncDecl(Id("main"), [], ([], []))])
        self.assertTrue(TestAST.checkASTGen(input,expect,310))

    def test_simple_program_12(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo 
                Parameter: a[5], b 
                Body:
                    Var: r = 10., v;
                EndBody."""
        expect = Program([FuncDecl(Id("foo"), [VarDecl(Id("a"),[5],None),VarDecl(Id("b"),[],None)], ([VarDecl(Id("r"),[],FloatLiteral(10.0)),VarDecl(Id("v"),[],None)], []))])
        self.assertTrue(TestAST.checkASTGen(input,expect,311))

    def test_simple_program_13(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo 
                Parameter: a[5], b 
                Body:
                    **b = 5;**
                EndBody."""
        expect = Program([FuncDecl(Id("foo"), [VarDecl(Id("a"),[5],None),VarDecl(Id("b"),[],None)], ([], []))])
        self.assertTrue(TestAST.checkASTGen(input,expect,312))

    def test_simple_program_14(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    b = 5;
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(Id("b"),IntLiteral(5))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,313))

    def test_simple_program_15(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    b = a + 5;
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([], [Assign(Id("b"),BinaryOp("+",Id("a"),IntLiteral(5)))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,314))

    def test_simple_program_16(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    b = a + 5 + b;
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([], [Assign(Id("b"),BinaryOp("+",BinaryOp("+",Id("a"),IntLiteral(5)),Id("b")))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,315))

    def test_simple_program_17(self):
        """Simple program: int main() {} """
        input = """
            Function: foo
                Body:
                    v = (4. \. 3.) *. 3.14 *. r;
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(Id("v"),BinaryOp("*.",BinaryOp("*.",BinaryOp("\.",FloatLiteral(4.0),FloatLiteral(3.0)),FloatLiteral(3.14)),Id("r")))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,316))

    def test_simple_program_18(self):
        """Simple program: int main() {} """
        input = r"""Var: x = True, y = 1.2e5, z = "hihi";"""
        expect = Program([VarDecl(Id("x"),[],BooleanLiteral(True)),VarDecl(Id("y"),[],FloatLiteral(120000.0)),VarDecl(Id("z"),[],StringLiteral("hihi"))])
        self.assertTrue(TestAST.checkASTGen(input,expect,317))

    def test_simple_program_19(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    Var: x;
                    foo (2 + x, 4. \. y);
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([VarDecl(Id("x"),[],None)],[CallStmt(Id("foo"),[BinaryOp("+",IntLiteral(2),Id("x")),BinaryOp("\.",FloatLiteral(4.0),Id("y"))])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 318))

    def test_simple_program_19(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    Var: x;
                    foo (2 + x, 4. \. y);
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([VarDecl(Id("x"),[],None)],[CallStmt(Id("foo"),[BinaryOp("+",IntLiteral(2),Id("x")),BinaryOp("\.",FloatLiteral(4.0),Id("y"))])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 318))

    def test_simple_program_20(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    Var: x;
                    foo ();
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([VarDecl(Id("x"),[],None)],[CallStmt(Id("foo"),[])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 319))

    def test_simple_program_21(self):
        """Simple program: int main() {} """
        input = r"""
            Function:f
                Body:
                    For (i = 0, i < 10, 2) Do 
                        writeln(i); 
                    EndFor.
                EndBody."""
        expect = Program([FuncDecl(Id("f"),[],([],[For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(10)),IntLiteral(2),([],[CallStmt(Id("writeln"),[Id("i")])]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 320))

    def test_simple_program_22(self):
        """Simple program: int main() {} """
        input = r"""
            Function:f
                Body:
                    Var: x;
                    For (i = 0, i < 10, 2) Do 
                        Var: x;
                        writeln(i); 
                    EndFor.
                EndBody."""
        expect = Program([FuncDecl(Id("f"),[],([VarDecl(Id("x"),[],None)],[For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(10)),IntLiteral(2),([VarDecl(Id("x"),[],None)],[CallStmt(Id("writeln"),[Id("i")])]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 321))

    def test_simple_program_23(self):
        """Simple program: int main() {} """
        input = r"""
            Function:f
                Body:
                    a = foo();
                EndBody."""
        expect = Program([FuncDecl(Id("f"),[],([],[Assign(Id("a"),CallExpr(Id("foo"),[]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 322))

    def test_simple_program_24(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo 
                Body:
                    Do
                        a[i] = b +. 1.0;
                    While (i < 5) 
                    EndDo. 
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Dowhile(([],[Assign(ArrayCell(Id("a"),[Id("i")]),BinaryOp("+.",Id("b"),FloatLiteral(1.0)))]),BinaryOp("<",Id("i"),IntLiteral(5)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 323))

    def test_simple_program_25(self):
        """Simple program: int main() {} """
        input = r"""
        Function: foo
            Body:
                Do
                    i = i + 1;
                    Break;
                    Continue;
                While (i < 5) 
                EndDo. 
            EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Dowhile(([],[Assign(Id("i"),BinaryOp("+",Id("i"),IntLiteral(1))),Break(),Continue()]),BinaryOp("<",Id("i"),IntLiteral(5)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 324))

    def test_simple_program_26(self):
        """Simple program: int main() {} """
        input = r"""
        Function: foo
            Body:
                Do
                    i = i + 1;
                    Return;
                While (i < 5) 
                EndDo. 
            EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Dowhile(([],[Assign(Id("i"),BinaryOp("+",Id("i"),IntLiteral(1))),Return(None)]),BinaryOp("<",Id("i"),IntLiteral(5)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 325))

    def test_simple_program_27(self):
        """Simple program: int main() {} """
        input = r"""
        Function: foo
            Body:
                a[i][1] = a[3][4] + 5 \ (2 * 3) -  a[6][b[1]]; 
                Return a[4][2];
            EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(ArrayCell(Id("a"),[Id("i"),IntLiteral("1")]),BinaryOp("-",BinaryOp("+",ArrayCell(Id("a"),[IntLiteral(3),IntLiteral(4)]),BinaryOp("\\",IntLiteral(5),BinaryOp("*",IntLiteral(2),IntLiteral(3)))),ArrayCell(Id("a"),[IntLiteral(6),ArrayCell(Id("b"),[IntLiteral(1)])]))),Return(ArrayCell(Id("a"),[IntLiteral(4),IntLiteral(2)]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 326))

    def test_simple_program_28(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo 
                Parameter: a[5], y[3][3]
                Body:
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[VarDecl(Id("a"),[5],None),VarDecl(Id("y"),[3,3],None)],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 327))

    def test_simple_program_29(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    While (i < 5) Do
                        i = i + 1;
                    EndWhile. 
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[While(BinaryOp("<",Id("i"),IntLiteral(5)),([],[Assign(Id("i"),BinaryOp("+",Id("i"),IntLiteral(1)))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 328))

    def test_simple_program_30(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
            Body:
            If True Then 
                foo();
            EndIf.
            EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[If([(BooleanLiteral(True),[],[CallStmt(Id("foo"),[])])],([],[]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 329))

    def test_simple_program_31(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
            Body:
            If True Then 
                foo();
            ElseIf False Then
                foo();
            EndIf.
            EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[If([(BooleanLiteral(True),[],[CallStmt(Id("foo"),[])]),(BooleanLiteral(False),[],[CallStmt(Id("foo"),[])])],([],[]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 330))

    def test_simple_program_32(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
            Body:
            If True Then 
                foo();
            ElseIf False Then
                foo();
            Else
                foo();
            EndIf.
            EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[If([(BooleanLiteral(True),[],[CallStmt(Id("foo"),[])]),(BooleanLiteral(False),[],[CallStmt(Id("foo"),[])])],([],[CallStmt(Id("foo"),[])]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 331))

    def test_simple_program_33(self):
        """Simple program: int main() {} """
        input = """Var: x;
                Var: y = True;
                Function: foo
                    Body:
                    EndBody.
                Function: main 
                    Body:
                    EndBody."""
        expect = Program([VarDecl(Id("x"),[],None),VarDecl(Id("y"),[],BooleanLiteral(True)),FuncDecl(Id("foo"),[],([],[])),FuncDecl(Id("main"),[],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,332))

    def test_simple_program_34(self):
        """Simple program: int main() {} """
        input = """Function: foo
                    Body: 
                        x = a[!-2 * 3 + b[1]] ;
                    EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(Id("x"),ArrayCell(Id("a"),[BinaryOp("+",BinaryOp("*",UnaryOp("!",UnaryOp("-",IntLiteral(2))),IntLiteral(3)),ArrayCell(Id("b"),[IntLiteral(1)]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,333))

    def test_simple_program_35(self):
        """Simple program: int main() {} """
        input = """Function: foo
                    Body: 
                        x = !!a + 1 != b ;
                    EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(Id("x"),BinaryOp("!=",BinaryOp("+",UnaryOp("!",UnaryOp("!",Id("a"))),IntLiteral(1)),Id("b")))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,334))

    def test_simple_program_36(self):
        """Simple program: int main() {} """
        input = """Function: foo
                    Body: 
                        x = (--a == b) != b ;
                    EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(Id("x"),BinaryOp("!=",BinaryOp("==",UnaryOp("-",UnaryOp("-",Id("a"))),Id("b")),Id("b")))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,335))

    def test_simple_program_37(self):
        """Simple program: int main() {} """
        input = """Function: foo
                    Body: 
                        Var: x;
                        Var: y[2];
                    EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([VarDecl(Id("x"),[],None),VarDecl(Id("y"),[2],None)],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,336))

    def test_simple_program_38(self):
        """Simple program: int main() {} """
        input = """Function: foo
                    Body: 
                        foo();
                        foo();
                    EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[CallStmt(Id("foo"),[]),CallStmt(Id("foo"),[])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,337))

    def test_simple_program_39(self):
        """Simple program: int main() {} """
        input = """Function: foo
                    Body: 
                        Var: x;
                        Var: y[2];
                        foo();
                        foo();
                    EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([VarDecl(Id("x"),[],None),VarDecl(Id("y"),[2],None)],[CallStmt(Id("foo"),[]),CallStmt(Id("foo"),[])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,338))

    def test_simple_program_40(self):
        """Simple program: int main() {} """
        input = """Var:x = 0x3, y = 0X3;"""
        expect = Program([VarDecl(Id("x"),[],IntLiteral(3)), VarDecl(Id("y"),[],IntLiteral(3))])
        self.assertTrue(TestAST.checkASTGen(input,expect,339))

    def test_simple_program_41(self):
        """Simple program: int main() {} """
        input = """Var:x[0x1][0o3];"""
        expect = Program([VarDecl(Id("x"),[1,3],None)])
        self.assertTrue(TestAST.checkASTGen(input,expect,340))

    def test_simple_program_42(self):
        """Simple program: int main() {} """
        input = """Var:x = 0o123, y = 0O123;"""
        expect = Program([VarDecl(Id("x"),[],IntLiteral(83)), VarDecl(Id("y"),[],IntLiteral(83))])
        self.assertTrue(TestAST.checkASTGen(input,expect,341))

    def test_if_stmt_1(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                If a!=b Then a = b; EndIf.  
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], (
        [], [If([(BinaryOp("!=", Id("a"), Id("b")), [], [Assign(Id("a"), Id("b"))])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 342))

    def test_if_stmt_2(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                If a+b>c Then 
                    print("Greater than");
                ElseIf a+b < c Then
                    print("Less than");
                Else
                    print("Equal");
                EndIf.
            EndBody."""
        expect = Program([ \
            FuncDecl( \
                Id("foo"), \
                [], \
                ( \
                    [], \
                    [ \
                        If( \
                            [ \
                                (BinaryOp(">", BinaryOp("+", Id("a"), Id("b")), Id("c")), [],
                                 [CallStmt(Id("print"), [StringLiteral("Greater than")])]), \
                                (BinaryOp("<", BinaryOp("+", Id("a"), Id("b")), Id("c")), [],
                                 [CallStmt(Id("print"), [StringLiteral("Less than")])]) \
                                ], \
                            ( \
                                [], \
                                [CallStmt(Id("print"), [StringLiteral("Equal")])] \
                                ) \
                            ) \
                        ] \
                    ) \
                ) \
            ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 343))

    def test_if_stmt_3(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                If isEqual(a,b) Then
                    Var: c; 
                    c = a - b;
                Else
                    Var: d[4][5] = {1,2,3};
                    d[2][3] = a + b;
                EndIf.
            EndBody."""
        expect = Program([ \
            FuncDecl( \
                Id("foo"), \
                [], \
                ( \
                    [], \
                    [ \
                        If( \
                            [ \
                                (CallExpr(Id("isEqual"), [Id("a"), Id("b")]), [VarDecl(Id("c"), [], None)],
                                 [Assign(Id("c"), BinaryOp("-", Id("a"), Id("b")))]), \
                                ], \
                            ( \
                                [VarDecl(Id("d"), [4, 5], ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)]))], \
                                [Assign(ArrayCell(Id("d"), [IntLiteral(2), IntLiteral(3)]),
                                        BinaryOp("+", Id("a"), Id("b")))] \
                                ) \
                            ) \
                        ] \
                    ) \
                ) \
            ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 344))

    def test_if_stmt_4(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                If True Then 
                ElseIf False Then
                Else
                EndIf.
            EndBody."""
        expect = Program([ \
            FuncDecl( \
                Id("foo"), \
                [], \
                ( \
                    [], \
                    [ \
                        If( \
                            [ \
                                (BooleanLiteral(True), [], []), \
                                (BooleanLiteral(False), [], []) \
                                ], \
                            ( \
                                [], \
                                [] \
                                ) \
                            ) \
                        ] \
                    ) \
                ) \
            ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 345))

    def test_if_stmt_5(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                If True Then 
                    If False Then x = y; EndIf.
                Else
                    If True Then y = x; Else x = y; EndIf.
                EndIf.
            EndBody."""
        expect = Program([ \
            FuncDecl( \
                Id("foo"), \
                [], \
                ( \
                    [], \
                    [ \
                        If( \
                            [ \
                                (BooleanLiteral(True), [],
                                 [If([(BooleanLiteral(False), [], [Assign(Id("x"), Id("y"))])], ([], []))]), \
                                ], \
                            ( \
                                [], \
                                [If([(BooleanLiteral(True), [], [Assign(Id("y"), Id("x"))])],
                                    ([], [Assign(Id("x"), Id("y"))]))] \
                                ) \
                            ) \
                        ] \
                    ) \
                ) \
            ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 346))

    def test_while_stmt_1(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Var: x = 0;
                While x < 100 Do x = x + 1; EndWhile.  
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([VarDecl(Id("x"), [], IntLiteral(0))], [
            While(BinaryOp("<", Id("x"), IntLiteral(100)),
                  ([], [Assign(Id("x"), BinaryOp("+", Id("x"), IntLiteral(1)))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 347))

    def test_while_stmt_2(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                While True && False Do 
                EndWhile.  
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], (
        [], [While(BinaryOp("&&", BooleanLiteral(True), BooleanLiteral(False)), ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 348))

    def test_while_stmt_3(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                While foo() =/= goo() Do
                    While foo() || goo() Do
                        x = y;
                    EndWhile. 
                EndWhile.  
            EndBody."""
        expect = Program([ \
            FuncDecl( \
                Id("foo"), \
                [], \
                ( \
                    [], \
                    [ \
                        While( \
                            BinaryOp("=/=", CallExpr(Id("foo"), []), CallExpr(Id("goo"), [])), \
                            ( \
                                [], \
                                [While(BinaryOp("||", CallExpr(Id("foo"), []), CallExpr(Id("goo"), [])),
                                       ([], [Assign(Id("x"), Id("y"))]))] \
                                ) \
                            ) \
                        ] \
                    ) \
                ) \
            ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 349))

    def test_while_stmt_4(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                While foo() =/= goo() Do
                    While !!foo() Do
                        Var: x, y[2][2][2] = {{{1,2},{3,4}},{{5,6},{7,8}}};
                    EndWhile. 
                EndWhile.  
            EndBody."""
        expect = Program([ \
            FuncDecl( \
                Id("foo"), \
                [], \
                ( \
                    [], \
                    [ \
                        While( \
                            BinaryOp("=/=", CallExpr(Id("foo"), []), CallExpr(Id("goo"), [])), \
                            ( \
                                [], \
                                [While(UnaryOp("!", UnaryOp("!", CallExpr(Id("foo"), []))), (
                                [VarDecl(Id("x"), [], None), VarDecl(Id("y"), [2, 2, 2], ArrayLiteral([ArrayLiteral(
                                    [ArrayLiteral([IntLiteral(1), IntLiteral(2)]),
                                     ArrayLiteral([IntLiteral(3), IntLiteral(4)])]), ArrayLiteral(
                                    [ArrayLiteral([IntLiteral(5), IntLiteral(6)]),
                                     ArrayLiteral([IntLiteral(7), IntLiteral(8)])])]))], []))] \
                                ) \
                            ) \
                        ] \
                    ) \
                ) \
            ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 350))

    def test_while_stmt_5(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                If True Then 
                    While True Do
                    EndWhile.
                EndIf.
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], (
        [], [If([((BooleanLiteral(True), [], [While(BooleanLiteral(True), ([], []))]))], (([], [])))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 351))

    # Dowhile statement test cases
    def test_do_while_stmt_1(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Var: x = 0;
                Do x = x + 1; While x < 100 EndDo.  
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([VarDecl(Id("x"), [], IntLiteral(0))], [
            Dowhile(([], [Assign(Id("x"), BinaryOp("+", Id("x"), IntLiteral(1)))]),
                    BinaryOp("<", Id("x"), IntLiteral(100)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 352))

    def test_do_while_stmt_2(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Do While True && False
                EndDo.  
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], (
        [], [Dowhile(([], []), BinaryOp("&&", BooleanLiteral(True), BooleanLiteral(False)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 353))

    def test_do_while_stmt_3(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Do
                    Do
                        x = y;
                    While foo() || goo()
                    EndDo.
                While foo() =/= goo() 
                EndDo.  
            EndBody."""
        expect = Program([ \
            FuncDecl( \
                Id("foo"), \
                [], \
                ( \
                    [], \
                    [ \
                        Dowhile( \
                            ( \
                                [], \
                                [Dowhile(([], [Assign(Id("x"), Id("y"))]),
                                         BinaryOp("||", CallExpr(Id("foo"), []), CallExpr(Id("goo"), [])))] \
                                ), \
                            BinaryOp("=/=", CallExpr(Id("foo"), []), CallExpr(Id("goo"), [])) \
                            ) \
                        ] \
                    ) \
                ) \
            ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 354))

    def test_do_while_stmt_4(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Do
                    Do
                        Var: x, y[2][2][2] = {{{1,2},{3,4}},{{5,6},{7,8}}};
                    While !!foo()
                    EndDo. 
                While foo() =/= goo()
                EndDo.  
            EndBody."""
        expect = Program([ \
            FuncDecl( \
                Id("foo"), \
                [], \
                ( \
                    [], \
                    [ \
                        Dowhile( \
                            ( \
                                [], \
                                [Dowhile(([VarDecl(Id("x"), [], None), VarDecl(Id("y"), [2, 2, 2], ArrayLiteral([
                                                                                                                    ArrayLiteral(
                                                                                                                        [
                                                                                                                            ArrayLiteral(
                                                                                                                                [
                                                                                                                                    IntLiteral(
                                                                                                                                        1),
                                                                                                                                    IntLiteral(
                                                                                                                                        2)]),
                                                                                                                            ArrayLiteral(
                                                                                                                                [
                                                                                                                                    IntLiteral(
                                                                                                                                        3),
                                                                                                                                    IntLiteral(
                                                                                                                                        4)])]),
                                                                                                                    ArrayLiteral(
                                                                                                                        [
                                                                                                                            ArrayLiteral(
                                                                                                                                [
                                                                                                                                    IntLiteral(
                                                                                                                                        5),
                                                                                                                                    IntLiteral(
                                                                                                                                        6)]),
                                                                                                                            ArrayLiteral(
                                                                                                                                [
                                                                                                                                    IntLiteral(
                                                                                                                                        7),
                                                                                                                                    IntLiteral(
                                                                                                                                        8)])])]))],
                                          []), UnaryOp("!", UnaryOp("!", CallExpr(Id("foo"), []))))] \
                                ), \
                            BinaryOp("=/=", CallExpr(Id("foo"), []), CallExpr(Id("goo"), [])) \
                            ) \
                        ] \
                    ) \
                ) \
            ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 355))

    def test_do_while_stmt_5(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                If True Then 
                    Do
                    While True
                    EndDo.
                EndIf.
            EndBody."""
        expect = Program([ \
            FuncDecl( \
                Id("foo"), \
                [], \
                ( \
                    [], \
                    [ \
                        If( \
                            [ \
                                (BooleanLiteral(True), [], [Dowhile(([], []), BooleanLiteral(True))]) \
                                ], \
                            ( \
                                [], \
                                [] \
                                ) \
                            ) \
                        ] \
                    ) \
                ) \
            ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 356))

    # Break statement test cases
    def test_break_stmt_1(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Break;
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [Break()]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 357))

    # Continue statement test cases
    def test_continue_stmt_1(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Continue;
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [Continue()]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 358))

    # Return statement test cases
    def test_return_stmt_1(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Return;
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [Return(None)]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 359))

    def test_return_stmt_2(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Return foo(x+.y);
            EndBody."""
        expect = Program(
            [FuncDecl(Id("foo"), [], ([], [Return(CallExpr(Id("foo"), [BinaryOp("+.", Id("x"), Id("y"))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 359))

    def test_return_stmt_3(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                Return a * (b-c) + 1;
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], (
        [], [Return(BinaryOp("+", BinaryOp("*", Id("a"), BinaryOp("-", Id("b"), Id("c"))), IntLiteral(1)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 360))

    # Call statement and Function call expression test cases
    def test_call_stmt_1(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                thisIsAFunction();
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [CallStmt(Id("thisIsAFunction"), [])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 361))

    def test_call_stmt_2(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                a_b_c_d(foo() + goo());
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], (
        [], [CallStmt(Id("a_b_c_d"), [BinaryOp("+", CallExpr(Id("foo"), []), CallExpr(Id("goo"), []))])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 362))

    def test_func_call_1(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                a[5][7] = foo(foo(x,y) \. foo(x+y, x-y));
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [Assign(ArrayCell(Id("a"), [IntLiteral(5), IntLiteral(7)]),
                                                               CallExpr(Id("foo"), [BinaryOp("\.", CallExpr(Id("foo"),
                                                                                                            [Id("x"),
                                                                                                             Id("y")]),
                                                                                             CallExpr(Id("foo"), [
                                                                                                 BinaryOp("+", Id("x"),
                                                                                                          Id("y")),
                                                                                                 BinaryOp("-", Id("x"),
                                                                                                          Id(
                                                                                                              "y"))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 363))

    def test_func_call_2(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                foo(a[2][1])[1][2] = goo(a[1] + b[2])[2];
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [Assign(
            ArrayCell(CallExpr(Id("foo"), [ArrayCell(Id("a"), [IntLiteral(2), IntLiteral(1)])]),
                      [IntLiteral(1), IntLiteral(2)]), ArrayCell(CallExpr(Id("goo"), [
                BinaryOp("+", ArrayCell(Id("a"), [IntLiteral(1)]), ArrayCell(Id("b"), [IntLiteral(2)]))]),
                                                                 [IntLiteral(2)]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 364))

    def test_func_call_3(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                foo(foo(foo(foo(1))))[1] = foo(foo(1))[2];
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [Assign(ArrayCell(
            CallExpr(Id("foo"), [CallExpr(Id("foo"), [CallExpr(Id("foo"), [CallExpr(Id("foo"), [IntLiteral(1)])])])]),
            [IntLiteral(1)]), ArrayCell(CallExpr(Id("foo"), [CallExpr(Id("foo"), [IntLiteral(1)])]),
                                        [IntLiteral(2)]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 365))

    # For statement test cases
    def test_for_stmt_1(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                For (i=0, i<10, 2) Do
                    writeln(i);
                EndFor.
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [
            For(Id("i"), IntLiteral(0), BinaryOp("<", Id("i"), IntLiteral(10)), IntLiteral(2),
                ([], [CallStmt(Id("writeln"), [Id("i")])]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 366))

    def test_for_stmt_2(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                For (i=0, 1, 1) Do
                EndFor.
            EndBody."""
        expect = Program(
            [FuncDecl(Id("foo"), [], ([], [For(Id("i"), IntLiteral(0), IntLiteral(1), IntLiteral(1), ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 367))

    def test_for_stmt_3(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                For (i=0, 1, 1) Do
                    For (j=1, True, foo()) Do
                    EndFor.
                EndFor.
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [For(Id("i"), IntLiteral(0), IntLiteral(1), IntLiteral(1), (
        [], [For(Id("j"), IntLiteral(1), BooleanLiteral(True), CallExpr(Id("foo"), []), ([], []))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 368))

    def test_for_stmt_4(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                For (i=0, 1, 1) Do
                    x = y + 1;
                EndFor.
                For (j=1, True, foo()) Do
                    y = x + 1;
                EndFor.
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [For(Id("i"), IntLiteral(0), IntLiteral(1), IntLiteral(1), (
        [], [Assign(Id("x"), BinaryOp("+", Id("y"), IntLiteral(1)))])),
                                                        For(Id("j"), IntLiteral(1), BooleanLiteral(True),
                                                            CallExpr(Id("foo"), []), ([], [Assign(Id("y"),
                                                                                                  BinaryOp("+", Id("x"),
                                                                                                           IntLiteral(
                                                                                                               1)))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 369))

    def test_for_stmt_5(self):
        """Simple program: int main() {} """
        input = """
        Function: foo
            Body:
                For (i=0, 1, 1) Do
                    For (j=1, True, foo()) Do
                        y = x + 1;
                        Continue;
                    EndFor.   
                EndFor.
                For (j=1, True, foo()) Do
                    y = x + 1;
                    Break;
                EndFor.
                Return;                
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [For(Id("i"), IntLiteral(0), IntLiteral(1), IntLiteral(1), ([], [
            For(Id("j"), IntLiteral(1), BooleanLiteral(True), CallExpr(Id("foo"), []),
                ([], [Assign(Id("y"), BinaryOp("+", Id("x"), IntLiteral(1))), Continue()]))])),
                                                        For(Id("j"), IntLiteral(1), BooleanLiteral(True),
                                                            CallExpr(Id("foo"), []), ([], [
                                                                Assign(Id("y"), BinaryOp("+", Id("x"), IntLiteral(1))),
                                                                Break()])), Return(None)]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 370))

    def test_case_72(self):
        input = """
        Function: print
        Parameter: i
        Body:
            print(i);
        EndBody.
        Function: main
        Body:
            print(i);
        EndBody.
        """
        expect = Program([FuncDecl(Id('print'), [VarDecl(Id('i'), [], None)], ([], [CallStmt(Id('print'), [Id('i')])])),
                          FuncDecl(Id('main'), [], ([], [CallStmt(Id('print'), [Id('i')])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 371))

    def test_case_73(self):
        input = """
        Function: test
        Body:
            For(i = 0, i < max, i) Do
                If (i % 7 == 0) && (i % 5 != 0) Then
                    arr = arr + {1};
                EndIf.
            EndFor.
            print(join("", arr));
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [], ([], [
            For(Id('i'), IntLiteral(0), BinaryOp('<', Id('i'), Id('max')), Id('i'), ([], [If([(BinaryOp('&&',
                                                                                                        BinaryOp('==',
                                                                                                                 BinaryOp(
                                                                                                                     '%',
                                                                                                                     Id(
                                                                                                                         'i'),
                                                                                                                     IntLiteral(
                                                                                                                         7)),
                                                                                                                 IntLiteral(
                                                                                                                     0)),
                                                                                                        BinaryOp('!=',
                                                                                                                 BinaryOp(
                                                                                                                     '%',
                                                                                                                     Id(
                                                                                                                         'i'),
                                                                                                                     IntLiteral(
                                                                                                                         5)),
                                                                                                                 IntLiteral(
                                                                                                                     0))),
                                                                                               [], [Assign(Id('arr'),
                                                                                                           BinaryOp('+',
                                                                                                                    Id(
                                                                                                                        'arr'),
                                                                                                                    ArrayLiteral(
                                                                                                                        [
                                                                                                                            IntLiteral(
                                                                                                                                1)])))])],
                                                                                             ([], []))])),
            CallStmt(Id('print'), [CallExpr(Id('join'), [StringLiteral(""""""), Id('arr')])])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 372))

    def test_case_74(self):
        input = """
        Function: test
        Body:
            For(i = 0, i < max, 1) Do
                If is_upper(s[i]) Then
                    d["upper"] = d["upper"] + 1;
                ElseIf is_lower(get(s, i)) Then
                    d["lower"] = d["lower"] + 1;
                Else
                    Continue;
                EndIf.
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [], ([], [
            For(Id('i'), IntLiteral(0), BinaryOp('<', Id('i'), Id('max')), IntLiteral(1), ([], [If([(CallExpr(
                Id('is_upper'), [ArrayCell(Id('s'), [Id('i')])]), [], [Assign(
                ArrayCell(Id('d'), [StringLiteral("""upper""")]),
                BinaryOp('+', ArrayCell(Id('d'), [StringLiteral("""upper""")]), IntLiteral(1)))]), (CallExpr(
                Id('is_lower'), [CallExpr(Id('get'), [Id('s'), Id('i')])]), [], [Assign(
                ArrayCell(Id('d'), [StringLiteral("""lower""")]),
                BinaryOp('+', ArrayCell(Id('d'), [StringLiteral("""lower""")]), IntLiteral(1)))])], ([], [
                Continue()]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 373))

    def test_case_75(self):
        input = """
        Function: test
        Body:
            While True Do
                Var: arr;
                s = input("Enter a string");
                If !s Then Break; EndIf.
                arr = split(s, " ");
                operation = arr[0];
                amount = int_of_string(operation);
                If operation == "A" Then
                    amount = amount + 10;
                EndIf.
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [], ([], [While(BooleanLiteral(True), ([VarDecl(Id('arr'), [], None)], [
            Assign(Id('s'), CallExpr(Id('input'), [StringLiteral("""Enter a string""")])),
            If([(UnaryOp('!', Id('s')), [], [Break()])], ([], [])),
            Assign(Id('arr'), CallExpr(Id('split'), [Id('s'), StringLiteral(""" """)])),
            Assign(Id('operation'), ArrayCell(Id('arr'), [IntLiteral(0)])),
            Assign(Id('amount'), CallExpr(Id('int_of_string'), [Id('operation')])), If([(BinaryOp('==', Id('operation'),
                                                                                                  StringLiteral(
                                                                                                      """A""")), [], [
                                                                                             Assign(Id('amount'),
                                                                                                    BinaryOp('+', Id(
                                                                                                        'amount'),
                                                                                                             IntLiteral(
                                                                                                                 10)))])],
                                                                                       ([], []))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 374))

    def test_case_76(self):
        input = """
        Function: test
        Body:
            While True Do
                s = str(input());
                If len(s) == 0 Then
                    Continue;
                EndIf.
                arr[arr + i] = append(split(arr, " "));
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [], ([], [While(BooleanLiteral(True), ([], [
            Assign(Id('s'), CallExpr(Id('str'), [CallExpr(Id('input'), [])])),
            If([(BinaryOp('==', CallExpr(Id('len'), [Id('s')]), IntLiteral(0)), [], [Continue()])], ([], [])),
            Assign(ArrayCell(Id('arr'), [BinaryOp('+', Id('arr'), Id('i'))]),
                   CallExpr(Id('append'), [CallExpr(Id('split'), [Id('arr'), StringLiteral(""" """)])]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 375))

    def test_case_77(self):
        input = """
        Function: test
        Parameter: str
        Body:
            l = split(str, " ");
            If !l Then print("empty string"); EndIf.
            Return array(l);
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [VarDecl(Id('str'), [], None)], ([], [
            Assign(Id('l'), CallExpr(Id('split'), [Id('str'), StringLiteral(""" """)])),
            If([(UnaryOp('!', Id('l')), [], [CallStmt(Id('print'), [StringLiteral("""empty string""")])])], ([], [])),
            Return(CallExpr(Id('array'), [Id('l')]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 376))

    def test_case_78(self):
        input = """
        Function: square
        Parameter: num
        Body:
            rand();
            sleep(random(randint(max) % int(1e10)));
            Return num * num;
        EndBody.
        Function: main
        Body:
            print(square(10));
        EndBody."""
        expect = Program([FuncDecl(Id('square'), [VarDecl(Id('num'), [], None)], ([], [CallStmt(Id('rand'), []),
                                                                                       CallStmt(Id('sleep'), [
                                                                                           CallExpr(Id('random'), [
                                                                                               BinaryOp('%', CallExpr(
                                                                                                   Id('randint'),
                                                                                                   [Id('max')]),
                                                                                                        CallExpr(
                                                                                                            Id('int'), [
                                                                                                                FloatLiteral(
                                                                                                                    10000000000.0)]))])]),
                                                                                       Return(BinaryOp('*', Id('num'),
                                                                                                       Id('num')))])),
                          FuncDecl(Id('main'), [],
                                   ([], [CallStmt(Id('print'), [CallExpr(Id('square'), [IntLiteral(10)])])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 377))

    def test_case_79(self):
        input = """
        Function: huber
        Parameter: y, x, fn, theta
        Body:
            Var: sum = 0.;
            sum = mean(abs(y - fn(x)), "mean");
            If sum <= theta Then
                Return mean(square(y - fn(x)), "mean") \. 2;
            Else
                Return theta * abs(y - fn(x)) - theta * theta \. 2;
            EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('huber'),
                                   [VarDecl(Id('y'), [], None), VarDecl(Id('x'), [], None), VarDecl(Id('fn'), [], None),
                                    VarDecl(Id('theta'), [], None)], ([VarDecl(Id('sum'), [], FloatLiteral(0.0))], [
                Assign(Id('sum'), CallExpr(Id('mean'), [
                    CallExpr(Id('abs'), [BinaryOp('-', Id('y'), CallExpr(Id('fn'), [Id('x')]))]),
                    StringLiteral("""mean""")])), If([(BinaryOp('<=', Id('sum'), Id('theta')), [], [Return(
                    BinaryOp('\.', CallExpr(Id('mean'), [
                        CallExpr(Id('square'), [BinaryOp('-', Id('y'), CallExpr(Id('fn'), [Id('x')]))]),
                        StringLiteral("""mean""")]), IntLiteral(2)))])], ([], [Return(BinaryOp('-', BinaryOp('*', Id(
                    'theta'), CallExpr(Id('abs'), [BinaryOp('-', Id('y'), CallExpr(Id('fn'), [Id('x')]))])),
                                                                                               BinaryOp('\.',
                                                                                                        BinaryOp('*',
                                                                                                                 Id(
                                                                                                                     'theta'),
                                                                                                                 Id(
                                                                                                                     'theta')),
                                                                                                        IntLiteral(
                                                                                                            2))))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 378))

    def test_case_80(self):
        input = """
        Function: mse
        Parameter: a, b
        Body:
            Var: sum = 0.;
            If len(a) =/= len(b) Then raise(error()); EndIf.
            For(i = 0, i < len(a), 1) Do
                sum = sum + (a[i] - b[i]) * (a[i] - b[i]);
            EndFor.
            print(sum * sum \. 2);
        EndBody.
        """
        expect = Program([FuncDecl(Id('mse'), [VarDecl(Id('a'), [], None), VarDecl(Id('b'), [], None)], (
        [VarDecl(Id('sum'), [], FloatLiteral(0.0))], [If([(BinaryOp('=/=', CallExpr(Id('len'), [Id('a')]),
                                                                    CallExpr(Id('len'), [Id('b')])), [],
                                                           [CallStmt(Id('raise'), [CallExpr(Id('error'), [])])])],
                                                         ([], [])), For(Id('i'), IntLiteral(0), BinaryOp('<', Id('i'),
                                                                                                         CallExpr(
                                                                                                             Id('len'),
                                                                                                             [Id(
                                                                                                                 'a')])),
                                                                        IntLiteral(1), ([], [Assign(Id('sum'),
                                                                                                    BinaryOp('+',
                                                                                                             Id('sum'),
                                                                                                             BinaryOp(
                                                                                                                 '*',
                                                                                                                 BinaryOp(
                                                                                                                     '-',
                                                                                                                     ArrayCell(
                                                                                                                         Id(
                                                                                                                             'a'),
                                                                                                                         [
                                                                                                                             Id(
                                                                                                                                 'i')]),
                                                                                                                     ArrayCell(
                                                                                                                         Id(
                                                                                                                             'b'),
                                                                                                                         [
                                                                                                                             Id(
                                                                                                                                 'i')])),
                                                                                                                 BinaryOp(
                                                                                                                     '-',
                                                                                                                     ArrayCell(
                                                                                                                         Id(
                                                                                                                             'a'),
                                                                                                                         [
                                                                                                                             Id(
                                                                                                                                 'i')]),
                                                                                                                     ArrayCell(
                                                                                                                         Id(
                                                                                                                             'b'),
                                                                                                                         [
                                                                                                                             Id(
                                                                                                                                 'i')])))))])),
                                                      CallStmt(Id('print'), [
                                                          BinaryOp('\.', BinaryOp('*', Id('sum'), Id('sum')),
                                                                   IntLiteral(2))])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 379))

    def test_case_81(self):
        input = """
        Var: arr[10][0o10] = {{1,2,3,4}, {1,2,3}, {2,3,4}};
        Function: main
        Body:
            For(i = 0, i < getlength(arr, axis(0)), 1) Do
                Var: j = 0;
                While (isvalid(arr, axis(1), j)) Do
                    print(arr[i][j] * 10);
                    j = j + 1;
                EndWhile.
            EndFor.
        EndBody."""
        expect = Program([VarDecl(Id('arr'), [10, 8], ArrayLiteral(
            [ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4)]),
             ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)]),
             ArrayLiteral([IntLiteral(2), IntLiteral(3), IntLiteral(4)])])), FuncDecl(Id('main'), [], ([], [
            For(Id('i'), IntLiteral(0),
                BinaryOp('<', Id('i'), CallExpr(Id('getlength'), [Id('arr'), CallExpr(Id('axis'), [IntLiteral(0)])])),
                IntLiteral(1), ([VarDecl(Id('j'), [], IntLiteral(0))], [
                    While(CallExpr(Id('isvalid'), [Id('arr'), CallExpr(Id('axis'), [IntLiteral(1)]), Id('j')]), ([], [
                        CallStmt(Id('print'),
                                 [BinaryOp('*', ArrayCell(Id('arr'), [Id('i'), Id('j')]), IntLiteral(10))]),
                        Assign(Id('j'), BinaryOp('+', Id('j'), IntLiteral(1)))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 380))

    def test_case_82(self):
        input = """
        Function: is_even
        Parameter: x
        Body:
            If x && 1 == 0 Then
                Return True;
            EndIf.
            Return False;
        EndBody."""
        expect = Program([FuncDecl(Id('is_even'), [VarDecl(Id('x'), [], None)], ([], [If([(BinaryOp('==', BinaryOp('&&',
                                                                                                                   Id(
                                                                                                                       'x'),
                                                                                                                   IntLiteral(
                                                                                                                       1)),
                                                                                                    IntLiteral(0)), [],
                                                                                           [Return(
                                                                                               BooleanLiteral(True))])],
                                                                                         ([], [])),
                                                                                      Return(BooleanLiteral(False))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 381))

    def test_case_83(self):
        input = """
        Function: test
        Body:
            Return "dasd" * asd  - {1,2,3} || 82 == False;
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [], ([], [Return(BinaryOp('==', BinaryOp('||', BinaryOp('-',
                                                                                                       BinaryOp('*',
                                                                                                                StringLiteral(
                                                                                                                    """dasd"""),
                                                                                                                Id(
                                                                                                                    'asd')),
                                                                                                       ArrayLiteral([
                                                                                                                        IntLiteral(
                                                                                                                            1),
                                                                                                                        IntLiteral(
                                                                                                                            2),
                                                                                                                        IntLiteral(
                                                                                                                            3)])),
                                                                                        IntLiteral(82)),
                                                                         BooleanLiteral(False)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 382))

    def test_case_84(self):
        input = """
        Function: t____
        Parameter: n
        Body:
            create(size, {400, 400});
            For(i = enum(), isend(i), steps(iter())) Do
                sub(n, 1, i + 1);
                im = coverted(read("path", "w"), type);
                b = im[1];
                While b Do
                    im = draw(im, figure);
                    pop(p, rand());
                EndWhile.
            EndFor.
        EndBody.
        """
        expect = Program([FuncDecl(Id('t____'), [VarDecl(Id('n'), [], None)], ([], [
            CallStmt(Id('create'), [Id('size'), ArrayLiteral([IntLiteral(400), IntLiteral(400)])]),
            For(Id('i'), CallExpr(Id('enum'), []), CallExpr(Id('isend'), [Id('i')]),
                CallExpr(Id('steps'), [CallExpr(Id('iter'), [])]), ([], [
                    CallStmt(Id('sub'), [Id('n'), IntLiteral(1), BinaryOp('+', Id('i'), IntLiteral(1))]),
                    Assign(Id('im'), CallExpr(Id('coverted'), [
                        CallExpr(Id('read'), [StringLiteral("""path"""), StringLiteral("""w""")]), Id('type')])),
                    Assign(Id('b'), ArrayCell(Id('im'), [IntLiteral(1)])), While(Id('b'), ([], [
                        Assign(Id('im'), CallExpr(Id('draw'), [Id('im'), Id('figure')])),
                        CallStmt(Id('pop'), [Id('p'), CallExpr(Id('rand'), [])])]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 383))

    def test_case_85(self):
        input = """
        Var: k = False;
        Var: str = "no thing";
        Var: d = 123;
        Function: t___k
        Body:
        EndBody."""
        expect = Program(
            [VarDecl(Id('k'), [], BooleanLiteral(False)), VarDecl(Id('str'), [], StringLiteral("""no thing""")),
             VarDecl(Id('d'), [], IntLiteral(123)), FuncDecl(Id('t___k'), [], ([], []))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 384))

    def test_case_86(self):
        input = """
        Function: mmmmmmm
        Body:
            For(i = 0, i < len(row), 1) Do
                For(j = 0, i < len(col), 1) Do
                    result[i][j] = row[i] * col[j];
                EndFor.
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('mmmmmmm'), [], ([], [
            For(Id('i'), IntLiteral(0), BinaryOp('<', Id('i'), CallExpr(Id('len'), [Id('row')])), IntLiteral(1), ([], [
                For(Id('j'), IntLiteral(0), BinaryOp('<', Id('i'), CallExpr(Id('len'), [Id('col')])), IntLiteral(1), (
                [], [Assign(ArrayCell(Id('result'), [Id('i'), Id('j')]),
                            BinaryOp('*', ArrayCell(Id('row'), [Id('i')]), ArrayCell(Id('col'), [Id('j')])))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 385))

    def test_case_87(self):
        input = """
        Var: arr[100];
        Var: x;
        Function: binary_search
        Parameter: low, high
        Body:
            Var: mid;
            If low > high Then Return False; EndIf.
            mid = (low + high) \ 2;
            If (arr[mid] == x) Then Return False; EndIf.
            If (arr[mid] < x) Then
                Return binary_search(mid + 1, high);
            Else
                Return binary_search(low, mid - 1);
            EndIf.
        EndBody."""
        expect = Program([VarDecl(Id('arr'), [100], None), VarDecl(Id('x'), [], None),
                          FuncDecl(Id('binary_search'), [VarDecl(Id('low'), [], None), VarDecl(Id('high'), [], None)], (
                          [VarDecl(Id('mid'), [], None)],
                          [If([(BinaryOp('>', Id('low'), Id('high')), [], [Return(BooleanLiteral(False))])], ([], [])),
                           Assign(Id('mid'), BinaryOp('\\', BinaryOp('+', Id('low'), Id('high')), IntLiteral(2))), If([(
                                                                                                                       BinaryOp(
                                                                                                                           '==',
                                                                                                                           ArrayCell(
                                                                                                                               Id(
                                                                                                                                   'arr'),
                                                                                                                               [
                                                                                                                                   Id(
                                                                                                                                       'mid')]),
                                                                                                                           Id(
                                                                                                                               'x')),
                                                                                                                       [],
                                                                                                                       [
                                                                                                                           Return(
                                                                                                                               BooleanLiteral(
                                                                                                                                   False))])],
                                                                                                                      (
                                                                                                                      [],
                                                                                                                      [])),
                           If([(BinaryOp('<', ArrayCell(Id('arr'), [Id('mid')]), Id('x')), [], [Return(
                               CallExpr(Id('binary_search'), [BinaryOp('+', Id('mid'), IntLiteral(1)), Id('high')]))])],
                              ([], [Return(CallExpr(Id('binary_search'),
                                                    [Id('low'), BinaryOp('-', Id('mid'), IntLiteral(1))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 386))

    def test_case_88(self):
        input = """
        Function: is_valid_index
        Parameter: arr[10], max_length, index
        Body:
            If index >= max_length Then raise(error());
            Else
                Return arr[index];
            EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('is_valid_index'),
                                   [VarDecl(Id('arr'), [10], None), VarDecl(Id('max_length'), [], None),
                                    VarDecl(Id('index'), [], None)], ([], [If([(BinaryOp('>=', Id('index'),
                                                                                         Id('max_length')), [], [
                                                                                    CallStmt(Id('raise'), [
                                                                                        CallExpr(Id('error'), [])])])],
                                                                              ([], [Return(ArrayCell(Id('arr'), [
                                                                                  Id('index')]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 387))

    def test_case_89(self):
        input = """
        Function: no_ideas
        Body:
            If x % 2 == y % f() Then
                print(a[2]);
            ElseIf f() % g(f()) > f() * 12 - f[123] Then
            ElseIf x % 12 == 1 Then
            EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('no_ideas'), [], ([], [If([(BinaryOp('==', BinaryOp('%', Id('x'), IntLiteral(2)),
                                                                           BinaryOp('%', Id('y'),
                                                                                    CallExpr(Id('f'), []))), [], [
                                                                      CallStmt(Id('print'),
                                                                               [ArrayCell(Id('a'), [IntLiteral(2)])])]),
                                                                 (BinaryOp('>', BinaryOp('%', CallExpr(Id('f'), []),
                                                                                         CallExpr(Id('g'), [
                                                                                             CallExpr(Id('f'), [])])),
                                                                           BinaryOp('-',
                                                                                    BinaryOp('*', CallExpr(Id('f'), []),
                                                                                             IntLiteral(12)),
                                                                                    ArrayCell(Id('f'),
                                                                                              [IntLiteral(123)]))), [],
                                                                  []), (
                                                                 BinaryOp('==', BinaryOp('%', Id('x'), IntLiteral(12)),
                                                                          IntLiteral(1)), [], [])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 388))

    def test_case_90(self):
        input = """
        Var: x, y, z, t;
        Function: test___
        Body:
            Var: a, b, c;
            Var: ksd[123][0x10][0o231340];
            Var: s = "132";
            Var: f = 0x13, sd = 123, s = "ad", k = 0.123, u = {1, 2, 4, 5, 6};
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None), VarDecl(Id('y'), [], None), VarDecl(Id('z'), [], None),
                          VarDecl(Id('t'), [], None), FuncDecl(Id('test___'), [], (
            [VarDecl(Id('a'), [], None), VarDecl(Id('b'), [], None), VarDecl(Id('c'), [], None),
             VarDecl(Id('ksd'), [123, 16, 78560], None), VarDecl(Id('s'), [], StringLiteral("""132""")),
             VarDecl(Id('f'), [], IntLiteral(19)), VarDecl(Id('sd'), [], IntLiteral(123)),
             VarDecl(Id('s'), [], StringLiteral("""ad""")), VarDecl(Id('k'), [], FloatLiteral(0.123)),
             VarDecl(Id('u'), [],
                     ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(4), IntLiteral(5), IntLiteral(6)]))], []))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 389))

    def test_case_91(self):
        input = """
        Var: x;
        Function: m
        Body:
            Break;
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None), FuncDecl(Id('m'), [], ([], [Break()]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 390))

    def test_case_92(self):
        input = """
        Function: m
        Body:
            f = (a + f(2 + 3, f + 2) * (f)[f((f[0]))[t]])[123] - 123;
            a[2 + f()] = f(f * k(a[0]));
            f()[2 + f()[2]] = "dasf" + f(2, 3 - f[2])[2];
            Continue;
        EndBody."""
        expect = Program([FuncDecl(Id('m'), [], ([], [Assign(Id('f'), BinaryOp('-', ArrayCell(BinaryOp('+', Id('a'),
                                                                                                       BinaryOp('*',
                                                                                                                CallExpr(
                                                                                                                    Id(
                                                                                                                        'f'),
                                                                                                                    [
                                                                                                                        BinaryOp(
                                                                                                                            '+',
                                                                                                                            IntLiteral(
                                                                                                                                2),
                                                                                                                            IntLiteral(
                                                                                                                                3)),
                                                                                                                        BinaryOp(
                                                                                                                            '+',
                                                                                                                            Id(
                                                                                                                                'f'),
                                                                                                                            IntLiteral(
                                                                                                                                2))]),
                                                                                                                ArrayCell(
                                                                                                                    Id(
                                                                                                                        'f'),
                                                                                                                    [
                                                                                                                        ArrayCell(
                                                                                                                            CallExpr(
                                                                                                                                Id(
                                                                                                                                    'f'),
                                                                                                                                [
                                                                                                                                    ArrayCell(
                                                                                                                                        Id(
                                                                                                                                            'f'),
                                                                                                                                        [
                                                                                                                                            IntLiteral(
                                                                                                                                                0)])]),
                                                                                                                            [
                                                                                                                                Id(
                                                                                                                                    't')])]))),
                                                                                              [IntLiteral(123)]),
                                                                               IntLiteral(123))), Assign(
            ArrayCell(Id('a'), [BinaryOp('+', IntLiteral(2), CallExpr(Id('f'), []))]),
            CallExpr(Id('f'), [BinaryOp('*', Id('f'), CallExpr(Id('k'), [ArrayCell(Id('a'), [IntLiteral(0)])]))])),
                                                      Assign(ArrayCell(CallExpr(Id('f'), []), [
                                                          BinaryOp('+', IntLiteral(2),
                                                                   ArrayCell(CallExpr(Id('f'), []), [IntLiteral(2)]))]),
                                                             BinaryOp('+', StringLiteral("""dasf"""), ArrayCell(
                                                                 CallExpr(Id('f'), [IntLiteral(2),
                                                                                    BinaryOp('-', IntLiteral(3),
                                                                                             ArrayCell(Id('f'), [
                                                                                                 IntLiteral(2)]))]),
                                                                 [IntLiteral(2)]))), Continue()]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 391))

    def test_case_93(self):
        input = """
        Function: blink
        Body:
            sys_call(3 * 2, sys(delete("path")));
            print();
            function();
            If "" Then EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('blink'), [], ([], [CallStmt(Id('sys_call'),
                                                                   [BinaryOp('*', IntLiteral(3), IntLiteral(2)),
                                                                    CallExpr(Id('sys'), [CallExpr(Id('delete'), [
                                                                        StringLiteral("""path""")])])]),
                                                          CallStmt(Id('print'), []), CallStmt(Id('function'), []),
                                                          If([(StringLiteral(""""""), [], [])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 392))

    def test_case_94(self):
        input = """
        Function: test
        Body:
            print();
        EndBody.
        Function: fn1
        Body: runfn(); EndBody.
        Function: fn2
        Body: EndBody.
        Function: main
        Body: Return test() + fn1() + fn2(); EndBody."""
        expect = Program([FuncDecl(Id('test'), [], ([], [CallStmt(Id('print'), [])])),
                          FuncDecl(Id('fn1'), [], ([], [CallStmt(Id('runfn'), [])])), FuncDecl(Id('fn2'), [], ([], [])),
                          FuncDecl(Id('main'), [], ([], [Return(
                              BinaryOp('+', BinaryOp('+', CallExpr(Id('test'), []), CallExpr(Id('fn1'), [])),
                                       CallExpr(Id('fn2'), [])))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 393))

    def test_case_95(self):
        input = """
        Function: t__________________________
        Body:
            Var: y;
            k = 120;
            x[12] = 123;
            x = {1, 2, 3, 4, {4, 5}, {{{{{}}}}}};
        EndBody."""
        expect = Program([FuncDecl(Id('t__________________________'), [], ([VarDecl(Id('y'), [], None)],
                                                                           [Assign(Id('k'), IntLiteral(120)),
                                                                            Assign(ArrayCell(Id('x'), [IntLiteral(12)]),
                                                                                   IntLiteral(123)), Assign(Id('x'),
                                                                                                            ArrayLiteral(
                                                                                                                [
                                                                                                                    IntLiteral(
                                                                                                                        1),
                                                                                                                    IntLiteral(
                                                                                                                        2),
                                                                                                                    IntLiteral(
                                                                                                                        3),
                                                                                                                    IntLiteral(
                                                                                                                        4),
                                                                                                                    ArrayLiteral(
                                                                                                                        [
                                                                                                                            IntLiteral(
                                                                                                                                4),
                                                                                                                            IntLiteral(
                                                                                                                                5)]),
                                                                                                                    ArrayLiteral(
                                                                                                                        [
                                                                                                                            ArrayLiteral(
                                                                                                                                [
                                                                                                                                    ArrayLiteral(
                                                                                                                                        [
                                                                                                                                            ArrayLiteral(
                                                                                                                                                [
                                                                                                                                                    ArrayLiteral(
                                                                                                                                                        [])])])])])]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 394))

    def test_case_96(self):
        input = """
        Function: tEEEEEEEEEEEEEE
        Body:
            While rand() Do
                print(rand());
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('tEEEEEEEEEEEEEE'), [], (
        [], [While(CallExpr(Id('rand'), []), ([], [CallStmt(Id('print'), [CallExpr(Id('rand'), [])])]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 395))

    def test_case_97(self):
        input = """
        Function: testttt
        Body:
            For(iter = 0, iter < max_iter, 1) Do
                If do_some_thing() == end Then
                    Return;
                EndIf.
                Continue; 
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('testttt'), [], ([], [
            For(Id('iter'), IntLiteral(0), BinaryOp('<', Id('iter'), Id('max_iter')), IntLiteral(1), ([], [
                If([(BinaryOp('==', CallExpr(Id('do_some_thing'), []), Id('end')), [], [Return(None)])], ([], [])),
                Continue()]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 396))

    def test_case_98(self):
        input = """Var: t;
        Function: t__Ddas
        Body:
            x = 2 -. 3 -. 4 + 123 + ((f() == 23) || 123) * 24 % (2 == 22);
        EndBody."""
        expect = Program([VarDecl(Id('t'), [], None), FuncDecl(Id('t__Ddas'), [], ([], [Assign(Id('x'), BinaryOp('+',
                                                                                                                 BinaryOp(
                                                                                                                     '+',
                                                                                                                     BinaryOp(
                                                                                                                         '-.',
                                                                                                                         BinaryOp(
                                                                                                                             '-.',
                                                                                                                             IntLiteral(
                                                                                                                                 2),
                                                                                                                             IntLiteral(
                                                                                                                                 3)),
                                                                                                                         IntLiteral(
                                                                                                                             4)),
                                                                                                                     IntLiteral(
                                                                                                                         123)),
                                                                                                                 BinaryOp(
                                                                                                                     '%',
                                                                                                                     BinaryOp(
                                                                                                                         '*',
                                                                                                                         BinaryOp(
                                                                                                                             '||',
                                                                                                                             BinaryOp(
                                                                                                                                 '==',
                                                                                                                                 CallExpr(
                                                                                                                                     Id(
                                                                                                                                         'f'),
                                                                                                                                     []),
                                                                                                                                 IntLiteral(
                                                                                                                                     23)),
                                                                                                                             IntLiteral(
                                                                                                                                 123)),
                                                                                                                         IntLiteral(
                                                                                                                             24)),
                                                                                                                     BinaryOp(
                                                                                                                         '==',
                                                                                                                         IntLiteral(
                                                                                                                             2),
                                                                                                                         IntLiteral(
                                                                                                                             22)))))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 397))

    def test_case_99(self):
        input = """
        Function: t_2937124
        Parameter: arr[100]
        Body:
            Var: sum = 0;
            create_multi_threads(num_threads);
            For (i = 0, i < len, 1) Do
                lock();
                sum = sum + arr[i];
                unlock();
            EndFor.
            destroy_all_resources();
        EndBody."""
        expect = Program([FuncDecl(Id('t_2937124'), [VarDecl(Id('arr'), [100], None)], (
        [VarDecl(Id('sum'), [], IntLiteral(0))], [CallStmt(Id('create_multi_threads'), [Id('num_threads')]),
                                                  For(Id('i'), IntLiteral(0), BinaryOp('<', Id('i'), Id('len')),
                                                      IntLiteral(1), ([], [CallStmt(Id('lock'), []), Assign(Id('sum'),
                                                                                                            BinaryOp(
                                                                                                                '+', Id(
                                                                                                                    'sum'),
                                                                                                                ArrayCell(
                                                                                                                    Id(
                                                                                                                        'arr'),
                                                                                                                    [Id(
                                                                                                                        'i')]))),
                                                                           CallStmt(Id('unlock'), [])])),
                                                  CallStmt(Id('destroy_all_resources'), [])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 398))

    def test_case_100(self):
        input = """
        Var: a, b = 120, c = "123", d[10] = {1,2,5};
        Var: f = {12, 3,4, {{}}};
        Function: test_
        Parameter: flag
        Body:
            If flag[0] && 1 Then
                For(i = 0, i < upp(upp(i)), s()) Do
                    update(f, i, d[i]);
                EndFor.
            ElseIf flag[2] && 2 Then
                Return;
            ElseIf all(flag, {0,1,2,3,4,5,6}) Then
                test_(flag[i]);
            ElseIf !flag Then
                Break;
            ElseIf is___(flag) Then
                flag = flag * ad - 123 + {1,2} % "124";
            Else
                println("da");
                delete(flag);
            EndIf.
        EndBody.
        Function: main
        Parameter: flags[100], len
        Body:
            For(i = 0, i < len, 1) Do
                test_(flags[i]);
            EndFor.
            Return 0;
        EndBody."""
        expect = Program([VarDecl(Id('a'), [], None), VarDecl(Id('b'), [], IntLiteral(120)),
                          VarDecl(Id('c'), [], StringLiteral("""123""")),
                          VarDecl(Id('d'), [10], ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(5)])),
                          VarDecl(Id('f'), [], ArrayLiteral(
                              [IntLiteral(12), IntLiteral(3), IntLiteral(4), ArrayLiteral([ArrayLiteral([])])])),
                          FuncDecl(Id('test_'), [VarDecl(Id('flag'), [], None)], ([], [If([(BinaryOp('&&', ArrayCell(
                              Id('flag'), [IntLiteral(0)]), IntLiteral(1)), [], [For(Id('i'), IntLiteral(0),
                                                                                     BinaryOp('<', Id('i'),
                                                                                              CallExpr(Id('upp'), [
                                                                                                  CallExpr(Id('upp'), [
                                                                                                      Id('i')])])),
                                                                                     CallExpr(Id('s'), []), ([], [
                                  CallStmt(Id('update'), [Id('f'), Id('i'), ArrayCell(Id('d'), [Id('i')])])]))]), (
                                                                                           BinaryOp('&&', ArrayCell(
                                                                                               Id('flag'),
                                                                                               [IntLiteral(2)]),
                                                                                                    IntLiteral(2)), [],
                                                                                           [Return(None)]), (
                                                                                           CallExpr(Id('all'),
                                                                                                    [Id('flag'),
                                                                                                     ArrayLiteral(
                                                                                                         [IntLiteral(0),
                                                                                                          IntLiteral(1),
                                                                                                          IntLiteral(2),
                                                                                                          IntLiteral(3),
                                                                                                          IntLiteral(4),
                                                                                                          IntLiteral(5),
                                                                                                          IntLiteral(
                                                                                                              6)])]),
                                                                                           [], [CallStmt(Id('test_'), [
                                                                                               ArrayCell(Id('flag'),
                                                                                                         [Id('i')])])]),
                                                                                           (
                                                                                           UnaryOp('!', Id('flag')), [],
                                                                                           [Break()]), (
                                                                                           CallExpr(Id('is___'),
                                                                                                    [Id('flag')]), [], [
                                                                                               Assign(Id('flag'),
                                                                                                      BinaryOp('+',
                                                                                                               BinaryOp(
                                                                                                                   '-',
                                                                                                                   BinaryOp(
                                                                                                                       '*',
                                                                                                                       Id(
                                                                                                                           'flag'),
                                                                                                                       Id(
                                                                                                                           'ad')),
                                                                                                                   IntLiteral(
                                                                                                                       123)),
                                                                                                               BinaryOp(
                                                                                                                   '%',
                                                                                                                   ArrayLiteral(
                                                                                                                       [
                                                                                                                           IntLiteral(
                                                                                                                               1),
                                                                                                                           IntLiteral(
                                                                                                                               2)]),
                                                                                                                   StringLiteral(
                                                                                                                       """124"""))))])],
                                                                                          ([], [CallStmt(Id('println'),
                                                                                                         [StringLiteral(
                                                                                                             """da""")]),
                                                                                                CallStmt(Id('delete'), [
                                                                                                    Id('flag')])]))])),
                          FuncDecl(Id('main'), [VarDecl(Id('flags'), [100], None), VarDecl(Id('len'), [], None)], ([], [
                              For(Id('i'), IntLiteral(0), BinaryOp('<', Id('i'), Id('len')), IntLiteral(1),
                                  ([], [CallStmt(Id('test_'), [ArrayCell(Id('flags'), [Id('i')])])])),
                              Return(IntLiteral(0))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 399))

    def test_simple_program_100(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    foo()[1] = 5;
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(ArrayCell(CallExpr(Id("foo"),[]),[IntLiteral(1)]),IntLiteral(5))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,400))

    def test_simple_program_101(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    a[1] = 5;
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(ArrayCell(Id("a"),[IntLiteral(1)]),IntLiteral(5))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,401))

    def test_simple_program_102(self):
        """Simple program: int main() {} """
        input = r"""
            Function: foo
                Body:
                    a[1][2] = 5;
                EndBody."""
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(ArrayCell(Id("a"),[IntLiteral(1), IntLiteral(2)]),IntLiteral(5))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,402))