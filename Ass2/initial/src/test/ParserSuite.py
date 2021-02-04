import unittest
from TestUtils import TestParser


class ParserSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """Var: x;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 201))

    def test_wrong_miss_close(self):
        """Miss variable"""
        input = """Var: ;"""
        expect = "Error on line 1 col 5: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 202))

    def test_var_global_declare_1(self):
        """Global variable declaration"""
        input = """Var: b[2][3] = {{2,3,4},{4,5,6}};"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 203))

    def test_var_global_declare_2(self):
        """Global variable declaration"""
        input = """Var: c, d = 6, e, f;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 204))

    def test_var_global_declare_3(self):
        """Global variable declaration"""
        input = """Var: m, n[10];"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 205))

    def test_var_global_declare_4(self):
        """Global variable declaration"""
        input = """Var: m, n[10], b[2][3] = {{2,3,4},{4,5,6};"""
        expect = "Error on line 1 col 41: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 206))

    def test_func_declare_1(self):
        """Global variable declaration"""
        input = r"""
        Var: x;
        Function: fact
            Parameter: n 
            Body:
                If n == 0 Then Return 1; 
                Else Return n * fact (n - 1); 
                EndIf.
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 207))

    def test_func_declare_2(self):
        """Global variable declaration"""
        input = r"""
        Var: x;
        Function: main 
            Body:
                x = 10;
                fact (x); 
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 208))

    # ?????????????
    def test_func_declare_3(self):
        """Global variable declaration"""
        input = r"""
        Var: x;
        ** hihi **
        Function: main 
            Body:
                x = 10;
                fact (x); 
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 209))

    def test_func_declare_4(self):
        """Global variable declaration"""
        input = r"""
        Function: foo 
        Parameter: a[5], b 
            Body:
                Var: i = 0;
                While (i < 5) Do
                    a[i] = b +. 1.0;
                    i = i + 1;
                EndWhile. 
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 210))

    def test_func_declare_5(self):
        """Global variable declaration"""
        input = r"""
        Function: foo 
        Parameter: a[5], b 
            Body:
                Var: r = 10., v;
                v = (4. \. 3.) *. 3.14 *. r *. r *. r;
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 211))

    def test_func_declare_6(self):
        """Global variable declaration"""
        input = r"""
        Function: foo 
        Parameter: a[5], b 
            Body:
                foo (2 + x, 4. \. y);
                goo ();
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 212))

    def test_func_declare_7(self):
        """Global variable declaration"""
        input = r"""
        Function:f
            Body:
            EnDBody."""
        expect = "E"
        self.assertTrue(TestParser.checkParser(input, expect, 213))

    def test_func_declare_8(self):
        """Global variable declaration"""
        input = r"""
        Function:f
            Body:
                For (i = 0, i < 10, 2) Do 
                    writeln(i); 
                EndFor.
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 214))

    def test_func_declare_9(self):
        """Global variable declaration"""
        input = r"""
        Function: foo 
        Parameter: a[5], b 
            Body:
                Var: i = 0;
                Do
                    a[i] = b +. 1.0;
                    i = i + 1;
                While (i < 5) 
                EndDo. 
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 215))

    def test_func_declare_10(self):
        """Global variable declaration"""
        input = r"""
        Function: foo
            Body:
                Var: i = 0;
                Do
                    a[i] = b +. 1.0;
                    i = i + 1;
                    Break;
                    Continue;
                While (i < 5) 
                EndDo. 
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 216))

    def test_mix_1(self):
        """Global variable declaration"""
        input = r"""
        Function: foo
            Body:
                Var: i = 0, a[6][5];
                Do
                    a[i][1] = a[3][4] + 5 \ (2 * 3) -  a[6][b[1]];
                    i = i + 1;
                While (i < 5) 
                EndDo. 
                Return a[4][2];
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 217))

    def test_mix_2(self):
        """Global variable declaration"""
        input = r"""
        Var x = 5, y[3][3], z = "Hello";
        Function: foo
            Body:
            EndBody."""
        expect = "Error on line 2 col 12: x"
        self.assertTrue(TestParser.checkParser(input, expect, 218))

    def test_mix_3(self):
        """Global variable declaration"""
        input = r"""
        Var: x = 5, y[3][3], z = "Hello";
        Function: foo
            Body:
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 219))

    def test_mix_4(self):
        """Global variable declaration"""
        input = r"""
        Var: x = 5, y[3][3], z = "Hello";
        x = 6;
        Function: foo
            Body:
            EndBody."""
        expect = "Error on line 3 col 8: x"
        self.assertTrue(TestParser.checkParser(input, expect, 220))

    def test_mix_5(self):
        """Global variable declaration"""
        input = r"""
        Function: foo
            Body:
            If bool_of_string ("True") Then 
                a = int_of_string (read ());
                b = float_of_int (a) +. 2.0;
            EndIf.
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 221))

    def test_mix_6(self):
        """Global variable declaration"""
        input = r"""
        Function: foo
            Body:
            If bool_of_string ("True") Then 
                a = int_of_string (read (b));
                b = float_of_int (a) +. 2.0;
            EndIf.
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 222))

    def test23(self):
        input = """ Function: main
                    Body:
                        Var: a[5][5][9], b = 1.55, c = -10;
                    EndBody.
                    """
        expect = "Error on line 3 col 55: -"
        self.assertTrue(TestParser.checkParser(input, expect, 223))

    def test24(self):
        input = """ Function: testIfStatement
                        Parameter: x, a, b, c
                        Body:
                            If(x == ((False||True) && (a > b + c))) Then
                                a = b - c;
                            Else
                                a = b + c;
                                x = True;
                            EndIf.
                        EndBody.
                    """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 224))

    def test25(self):
        """ test for_stmt """
        input = """Function: foo
                        Parameter: x
                        Body:
                            For (i = 1, i <= x*x*x,i + x ) Do
                                writeln(i);
                            EndFor.
                        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 225))

    def test26(self):
        """ Test while stmt """
        input = """Function: foo 
        Parameter: n
        Body: 
            While(1) Do
                While(!x) Do
                    x = True;
                EndWhile.
            EndWhile.
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 226))

    def test27(self):
        """ Test miss endwhile stmt """
        input = """Function: foo 
        Parameter: n
        Body: 
            While((x > a) && (x < b)) Do
                While((x >= b) || (x >= a)) Do
                    While((x > c * b) && (x < b*b)) Do
                        x = x - 1;
                        c = 2 * c;
                        While( !False ) Do
                            a = a * 1;
                        EndWhile.
                    EndWhile.
                EndWhile.
        EndBody."""
        expect = "Error on line 14 col 8: EndBody"
        self.assertTrue(TestParser.checkParser(input, expect, 227))

    def test28(self):
        """ Test miss EndDo."""
        input = """Function: foo 
        Parameter: n
        Body: 
            Do
                x = a + b;
                writeln(x);
            While(True || False || True || (a > b))
        EndBody."""
        expect = "Error on line 8 col 8: EndBody"
        self.assertTrue(TestParser.checkParser(input, expect, 228))

    def test29(self):
        """  """
        input = """Function: foo 
        Parameter: n
        Body: 
            Do
            While();
            EndDo.
        EndBody."""
        expect = "Error on line 5 col 18: )"
        self.assertTrue(TestParser.checkParser(input, expect, 229))

    def test30(self):
        """  """
        input = """Function: foo 
        Parameter: n
        Body: 
            Do
                Do
                    While(b!=4);
                While(a!=3);
                EndDo.
            EndDo.
        EndBody."""
        expect = "Error on line 6 col 31: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 230))

    def test31(self):
        """ Test break stmt """
        input = """Function: foo 
        Parameter: n
        Body: 
            Break;
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 231))

    def test32(self):
        """ Test continue stmt """
        input = """Function: foo 
        Parameter: n
        Body: 
            Continue;
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 232))

    def test33(self):
        """ Test complex func_call """
        input = """Function: foo 
        Parameter: n
        Body: 
            test(a,3*7,y[1],z[2] + 5,"string",True);
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 233))

    def test34(self):
        """ Test return stmt  """
        input = """Function: foo 
        Parameter: n
        Body: 
            Do  
                Return foo(x,y);
            While (True)
            EndDo.
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 234))

    def test35(self):
        """ test relational arithmetic """
        input = """Function: foo 
        Parameter: n
        Body: 
            a= (a==b)!= c ;
            x= (x =/= y) <. z >.t;
        EndBody."""
        expect = "Error on line 5 col 30: >."
        self.assertTrue(TestParser.checkParser(input, expect, 235))

    def test36(self):
        """ test adding operator  """
        input = """Function: foo 
        Parameter: n
        Body: 
            x= (y+3)+. 0.e3 - (z -. -9);
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 236))

    def test37(self):
        """ test multiplying operator  """
        input = """Function: foo 
        Parameter: n
        Body: 
            x= (x*3)*. 0x3E \ (y \. 0.123) % 5;
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 237))

    def test38(self):
        """ test sign operator """
        input = """Function: foo 
        Parameter: n
        Body:
            a= -3;
            b= -0x123;
            c= -0o77;
            d= -a;
            c= -foo(x); 
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 238))

    def test39(self):
        """ test boolean operator """
        input = """Function: foo 
        Parameter: n
        Body: 
            x = !(True);
            y = (False || True) && True;
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 239))

    def test40(self):
        """ Test boolean and expression """
        input = """Function: foo 
        Parameter: n
        Body: 
            x = !(!(!(y) && z) || (x > 3) !(y < 2));
        EndBody."""
        expect = "Error on line 4 col 42: !"
        self.assertTrue(TestParser.checkParser(input, expect, 240))

    def test41(self):
        """ test index operator """
        input = """Function: foo 
        Parameter: n
        Body: 
            a[a[3 + foo(2)][b||True]][b[b[1+0x369]]] = a[b[2][b[12E-9]*3]] + 4;
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 241))

    def test42(self):
        """ Test func_call expression """
        input = """Function: foo 
        Parameter: n
        Body: 
            a= foo(a,b) + goo (x);
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 242))

    def test43(self):
        """ Test funcall_expr  """
        input = """Function: foo 
        Parameter: n
        Body: 
            foo(2.34,"string",-9.2e11);
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 243))

    def test44(self):
        """ test simple program """
        input = """Function: foo 
            Parameter: n
            Body: 
            Var : a;
            EndBody.

            Function: program1
            Parameter: e
            Body:
            EndBody.

            Function: main
            Body:
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 244))

    def test45(self):
        """ Test relational operator """
        input = """Function: foo 
        Parameter: n
        Body: 
            If (x == y) || (x != y) Then
                x = ((a >=. 2.3e-13) || (x =/= 2e-35));
            EndIf.
            z = (x < 3) && (y > 4);
            a = (x != z);
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 245))

    def test46(self):
        """ Test func_call + expression"""
        input = """Function: foo 
        Parameter: n
        Body: 
            a =(foo(3) != foo(4))* 0.e2;
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 246))

    def test47(self):
        """ Test array with comment"""
        input = """Var: x = {{1,2,3}, **Comment here** "abc"};"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 247))

    def test48(self):
        """ Test array """
        input = """Function: foo 
        Parameter: n
        Body: 
            a[123]={};
            b[1]={{{}}};
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 248))

    def test49(self):
        """ Check wrong composite type """
        input = """
        Var: x[]=1;
        """
        expect = "Error on line 2 col 15: ]"
        self.assertTrue(TestParser.checkParser(input, expect, 249))

    def test50(self):
        """Check wrong composite type  """
        input = """
        Var: x[12.e3]=1;
        """
        expect = "Error on line 2 col 15: 12.e3"
        self.assertTrue(TestParser.checkParser(input, expect, 250))

    def test51(self):
        """ Check wrong inital-values """
        input = """Var:x[1]=1+2;"""
        expect = "Error on line 1 col 10: +"
        self.assertTrue(TestParser.checkParser(input, expect, 251))

    def test52(self):
        """ Check var_decl with comment """
        input = """Var **some COMMENT**: ****someid = 3
        **more more**;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 252))

    def test53(self):
        """ Check mix"""
        input = """Function: foo 
                Parameter: n, a[3][4]
                Body: 
                    a[3 + foo(2)] = a[b[2][3]] + 4;
                EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 253))

    def test54(self):
        """ Check mix"""
        input = """Function: foo 
                Parameter: n = 3, a[3][4]
                Body: 
                EndBody."""
        expect = "Error on line 2 col 29: ="
        self.assertTrue(TestParser.checkParser(input, expect, 254))

    def test55(self):
        """Global variable declaration"""
        input = r"""
        Var: x;
        Function: fact
            Parameter: n 
            Body:
                If n == 0 Then Return 1; 
                ElseIf n>2 Then Return n * fact (n - 1); 
                ElseIf n>20 Then Return n * fact (n - 1); 
                EndIf.
            EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 255))

    def test56(self):
        """ Check mix"""
        input = """Function: foo 
                Parameter: n, a[3][4]
                Body: 
                    For (i[2] = 0, i < 10, 2) Do writeln(); 
                    EndFor.
                EndBody."""
        expect = "Error on line 4 col 26: ["
        self.assertTrue(TestParser.checkParser(input, expect, 256))

    def test57(self):
        """ Check mix"""
        input = r"""Function: foo 
                Parameter: n = 3, a[3][4]
                Body: 
                    x = (x+2)[3 - b[2]] % 2 * (2.0 \. 8)
                EndBody."""
        expect = "Error on line 2 col 29: ="
        self.assertTrue(TestParser.checkParser(input, expect, 257))

    def test58(self):
        """ Check mix"""
        input = r"""Function: foo 
                    Parameter: n, a[3][4]
                    Body: 
                        x = a[!-2 * 3 + b[1]] ;
                    EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 258))

    def test59(self):
        """ Check mix"""
        input = r"""Function: foo 
                    Parameter: n, a[3][4]
                    Body: 
                        x = a[!-2 * 3 + b[1]]
                    EndBody."""
        expect = "Error on line 5 col 20: EndBody"
        self.assertTrue(TestParser.checkParser(input, expect, 259))

    def test60(self):
        """ Check mix"""
        input = r"""Function: foo 
                    Parameter: n, a[3][4]
                    Body: 
                        x = a[!-2 * 3 + b[1]]
                    EndBody"""
        expect = "Error on line 5 col 20: EndBody"
        self.assertTrue(TestParser.checkParser(input, expect, 260))

    def test61(self):
        """ Check mix"""
        input = r"""Function: foo 
                    Parameter: n, a[3][4]
                    Body: 
                        int_of_float(12);
                        While float_to_int(0) Do
                            int_of_string();
                            string_of_int();
                            float_of_string();
                            string_of_float()  ;
                        EndWhile.
                    EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 261))

    def test62(self):
        """ Check mix"""
        input = r"""Function: foo 
                    Parameter: n, a[3][4]
                    Body: 
                        int_of_float(12);
                        While float_to_int(0) Do
                            int_of_string();
                            string_of_int();
                            float_of_string;
                            string_of_float()  ;
                        EndWhile.
                    EndBody."""
        expect = "Error on line 8 col 43: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 262))

    def test_case_63(self):
        input = """
        Function: main
        Body:
            blu = 123 * 23 - 123 - -.--.- "dads";
            While (print(blu[123]) = 123, i < 10, 10)
                test();
            EndWhile.
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 5 col 35: =", 263))

    def test64(self):
        """ Check mix"""
        input = r"""Function: foo 
                    Parameter: n, a[3][4]
                    Body: 
                        x[2+b[3]] = a[!-2 * 3 + b[1]] ;
                    EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 264))

    def test_65(self):
        input = """
        Var: hihi ;
        Function: foo
        Body:
            Var: array[0X1810198ABCD];
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "successful", 265))

    def test_66(self):
        input = """
        Var: hihi ;
        Function: foo
        Body:
            Var: array[0O1234567];
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "successful", 266))

    def test_67_wrong_return(self):
        input = """
        Var: hihi ;
        Function: foo
        Body:
            Return Break;
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 5 col 19: Break", 267))

    def test_68_neg_num_in_array(self):
        input = """
        ** Hana **
        Function: foo
        Body:
            Var: x = {{{1,  8 ,1e-0198, "abc" , -1 }, {  4 , **erty**  5}  },  {{ 6  ,  7  },{ 8,9}}};
            Return 0 ;
        EndBody.
        ** **
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 5 col 48: -", 268))

    def test_69_wrong_param(self):
        input = """
        ** Hana **
        Function: foo
        Parameter: arr[1 + 2 * 3]
        Body:
            While True Do
                ** nothing **
            EndWhile.
            Return ;
        EndBody.
        ** **
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 4 col 25: +", 269))

    def test_70_wrong_param(self):
        input = """
        ** Hana **
        Function: main
        Parameter: 1810[198]
        Body:
            While True Do
                ** nothing **
            EndWhile.
            Return ;
        EndBody.
        ** **
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 4 col 19: 1810", 270))

    def test_71_wrong_param(self):
        input = """
        ** Hana **
        Function: main
        Parameter: array[size]
        Body:
            While i < 5 Do
                ** nothing **
            EndWhile.
        EndBody.
        ** **
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 4 col 25: size", 271))

    def test_72(self):
        input = """ Function: foo
        Parameter: x, a[2] , arr[1][2][3]
        Body:
            For (i = 0, i < 10, 2) Do
                If (x) Then Break; EndIf.
            EndFor.
            If (a) Then Break; EndIf.
            Return 0;
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "successful", 272))

    def test_73_wrong_keyword(self):
        input = """Function: a_b
            Parameter: y,v
            Bxdy:
            EndBody."""
        self.assertTrue(TestParser.checkParser(input, "B", 273))

    def test_74(self):
        input = """Function: a_b
            Parameter: y,v
            Body:
            x[2] = x[2+x[2]];
            EndBody."""
        self.assertTrue(TestParser.checkParser(input, "successful", 274))

    def test_75(self):
        input = """Function: a_b
               Parameter: y,v
               Body:
               x[2 +x[2]] = x[2+x[2]];
               EndBody."""
        self.assertTrue(TestParser.checkParser(input, "successful", 275))

    def test_76(self):
        input = """Function: a_b
               Parameter: y,v
               Body:
               "ab"[2 +x[2]] = x[2+x[2]];
               EndBody."""
        self.assertTrue(TestParser.checkParser(input, "successful", 276))

    def test_77(self):
        input = """Function: a_b
               Parameter: y,v
               Parameter: y,v
               Body:
               EndBody."""
        self.assertTrue(TestParser.checkParser(input, "Error on line 3 col 15: Parameter", 277))

    def test_78(self):
        input = """Function: foo
        Parameter: a , v , asd[5][12][4]
        Body:
            If True Then a = 1;
            ElseIf False Then a = 2;
            Else (a == v) Then a = v;
            EndIf.
        EndBody."""
        self.assertTrue(TestParser.checkParser(input, "Error on line 6 col 26: Then", 278))

    def test_79(self):
        input = """Function: a_b
               Parameter: y,v
               Body:
               EndBody.
               Body:
               EndBody."""
        self.assertTrue(TestParser.checkParser(input, "Error on line 5 col 15: Body", 279))

    def test_80(self):
        input = """Function: a_b
               Parameter: y,v
               Body:
               {1,2}[2 +x[2]] = x[2+x[2]];
               EndBody."""
        self.assertTrue(TestParser.checkParser(input, "successful", 280))

    def test_81(self):
        input = """Function: a_b
               Parameter: y,v
               Body:
               1 + x[2 +x[2]] = x[2+x[2]];
               EndBody."""
        self.assertTrue(TestParser.checkParser(input, "Error on line 4 col 17: +", 281))

    def test_82(self):
        input = """Function: a_b
               Parameter: y,v
               Body:
               For (i[0] = 0, i < 10, 2) Do 
                    writeln(i); 
               EndFor.
               EndBody."""
        self.assertTrue(TestParser.checkParser(input, "Error on line 4 col 21: [", 282))

    def test_83(self):
        input = """
        ** This is a 
        multiline
        comment
        ** 
        Function: main
        Body:
            While True Do
                Do
                    If i = 1 Then
                        ** nothing **
                    EndIf.
                While True EndDo.
            EndWhile.
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 10 col 25: =", 283))

    def test_84(self):
        input = """
        Function: main
        Body:
            Var: x = 1810.340, y = 0.;
            While (x =/= y) Do
                x = x -. 10;
                y = y +. 10;
            EndWhile.
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "successful", 284))

    def test_85(self):
        input = """
        Var: a,b[1],c[1][2];
        Function: foo
        Body:
           Var: d;
           a = d = 1810198;
           Return ;
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 6 col 17: =", 285))

    def test_86(self):
        input = """
        Function: main
        Parameter: a b c d e
        Body:
            ** nothing **
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 3 col 21: b", 286))

    def test_87(self):
        input = """
        Function: main
        Body:
            Var: x = {2 + 1, foo(2), fact(4)};
            Return 0;
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 4 col 24: +", 287))

    def test_88(self):
        input = """
        ** this is a comment **
        Function: foo
        Body:
            Var: a,b[1],c[1][2];
            If i == 1810198 Then
            Else
                writeln(i);
            ElseIf i == 1810 Then
                Break;
            EndIf.
            Return 0;
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 9 col 12: ElseIf", 288))

    def test_89(self):
        input = """Var: a,b[1],c[1][2][3];
        Function: foo
        Body:
            func(18)[b[10][19]]=8;
        EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 289))

    def test_90(self):
        input = """ Function: foo
        Body:
            x = 18[10] + 198;
        EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 290))

    def test_91(self):
        input = """ Function: foo
        Body:
            x = (1 + f() * 2 + arr[3])[4] * 5 \\ 6;
            Return 0;
        EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 291))

    def test_92(self):
        input = """ Function: foo
        Body:
            array[[2]] = 3; 
            Return 0;
        EndBody.
        """
        expect = "Error on line 3 col 18: ["
        self.assertTrue(TestParser.checkParser(input, expect, 292))

    def test_93(self):
        input = """ Function: foo
        Body:
            x = (func(func))[1810198]; 
        EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 293))

    def test_94(self):
        input = """ Function: foo
        Body:
            x ="ahihi
        EndBody.
        """
        expect = "ahihi"
        self.assertTrue(TestParser.checkParser(input, expect, 294))

    def test_95(self):
        input = """ Function: foo
        Parameter: x, a[2] , arr[1][2][3]
        Body:
            For (i = 0, i < 10, 2) Do
                If (x) Then Break; EndIf.
            EndFor.
            If (a) Then Break; EndIf.
            Return 0;
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "successful", 295))

    def test_96(self):
        input = """
        Var: tmp;
        Function: foo
        Body:
           Var: array[18];
           array[foo(10) + 18] = a[b[1][9]] + 8;
           Return 0;
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "successful", 296))

    def test_97(self):
        input = """
        Var: a = {1,2,{2};
        Function: foo
        Body:
        ** nothing **
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "Error on line 2 col 25: ;", 297))

    def test_98(self):
        input = """
        Function: max
        Parameter: array[10]
        Body:
            Return array[random(1, 9, False)];
        EndBody.
        Function: main
        Body:
            print(max({1,8,1,0,1,9,8}));
            Return ;
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "successful", 298))

    def test_99(self):
        input = """Function: fact
                Body:
                    For (i = 1, i < 10, 1) Do
                        If i == 5 Then
                            Break ;
                        EndIf.
                    EndFor.
                EndBody.
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 299))

    def test_100(self):
        input = """Function: fact
                Body:
                    For (i = 1, i < 10, 1) Do
                        If i < 5 Then
                            Continue ;
                        Else 
                            i = i + 1 ;
                        EndIf.
                    EndFor.
                EndBody.
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 300))

    def test_101(self):
        input = """Function: fact
                Body:
                    Return a ;
                EndBody.
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 301))
