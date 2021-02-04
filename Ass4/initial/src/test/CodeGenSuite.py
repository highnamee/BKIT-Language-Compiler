import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    # def test_int(self):
    #     """Simple program: int main() {} """
    #     input = """Function: main
    #                Body: 
    #                     print(string_of_int(120));
    #                EndBody."""
    #     expect = "120"
    #     self.assertTrue(TestCodeGen.test(input,expect,500))

    # def test_int_ast(self):
    # 	input = Program([
    # 		FuncDecl(Id("main"),[],([],[
    # 			CallStmt(Id("print"),[
    #                 CallExpr(Id("string_of_int"),[IntLiteral(120)])])]))])
    # 	expect = "120"
    # 	self.assertTrue(TestCodeGen.test(input,expect,501))

    # def test_int_1(self):
    #     """Simple program: int main() {} """
    #     input = """Function: main
    #                Body: 
    #                     Var: x = 2;
    #                     Return;
    #                EndBody."""
    #     expect = ""
    #     self.assertTrue(TestCodeGen.test(input,expect,502))

    # def test_2(self):
    #     input = """
    #             Var: x = 2;
    #             Function: y  
    #                 Body:
    #                     Return x;
    #                 EndBody.
    #             Function: main
    #                 Body:
    #                 EndBody."""
    #     expect = ""
    #     self.assertTrue(TestCodeGen.test(input,expect,503))

    # def test_3(self):
    #     input = """
    #             Var: x = 2;
    #             Function: y  
    #                 Parameter: t
    #                 Body:
    #                     Var: a = 3, b = 4;
    #                     t = 3;
    #                     Return 3;
    #                 EndBody.
    #             Function: main
    #                 Body:
    #                 EndBody."""
    #     expect = ""
    #     self.assertTrue(TestCodeGen.test(input,expect,504))

    # def test_4(self):
    #     input = """
    #             Var: x = 2, y = 3;
    #             Function: main
    #                 Body:
    #                     print(string_of_int(x));
    #                 EndBody."""
    #     expect = "2"
    #     self.assertTrue(TestCodeGen.test(input,expect,505))

    # def test_5(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: x = 2, y = 3;
    #                     print(string_of_int(x));
    #                 EndBody."""
    #     expect = "2"
    #     self.assertTrue(TestCodeGen.test(input,expect,506))

    # def test_6(self):
    #     input = """
    #             Var: x = 2;
    #             Function: foo
    #                 Body:
    #                     Return x;
    #                 EndBody.
    #             Function: main
    #                 Body:
    #                 EndBody."""
    #     expect = ""
    #     self.assertTrue(TestCodeGen.test(input,expect,507))

    # def test_7(self):
    #     input = """
    #             Var: x = 2, y = 3;
    #             Function: main
    #                 Body:
    #                     Var: x = 5;
    #                     x = y;
    #                     print(string_of_int(x));
    #                 EndBody."""
    #     expect = "3"
    #     self.assertTrue(TestCodeGen.test(input,expect,508))

    # def test_8(self):
    #     input = """
    #             Var: x = 2, y = 3;
    #             Function: foo
    #                 Body:
    #                     print(string_of_int(x));
    #                 EndBody.
    #             Function: main
    #                 Body:
    #                     Var: x = 5;
    #                     x = y;
    #                     print(string_of_int(x));
    #                     foo();
    #                 EndBody."""
    #     expect = "32"
    #     self.assertTrue(TestCodeGen.test(input,expect,509))

    # def test_9(self):
    #     input = """
    #             Var: x = 2, y = 3;
    #             Function: main
    #                 Body:
    #                     x = y + 5;
    #                     print(string_of_int(x));
    #                 EndBody."""
    #     expect = "8"
    #     self.assertTrue(TestCodeGen.test(input,expect,510))

    # def test_10(self):
    #     input = """
    #             Var: x = 2, y = 3;
    #             Function: main
    #                 Body:
    #                     print(string_of_int(1 + 3 - 5 + 1*4 - 4\\3));
    #                 EndBody."""
    #     expect = "2"
    #     self.assertTrue(TestCodeGen.test(input,expect,511))

    # def test_11(self):
    #     input = """
    #             Var: x = 2, y = 3;
    #             Function: main
    #                 Body:
    #                     print(string_of_int(13%3 + -4 - y*x));
    #                 EndBody."""
    #     expect = "-9"
    #     self.assertTrue(TestCodeGen.test(input,expect,512))

    # def test_12(self):
    #     input = """
    #             Var: x = 2.0, y = 3.0;
    #             Function: main
    #                 Body:
    #                     print(string_of_float(1.0 +. 2*.3 -. 4 +. 3\\.2));
    #                 EndBody."""
    #     expect = "4.5"
    #     self.assertTrue(TestCodeGen.test(input,expect,513))

    # def test_13(self):
    #     input = """
    #             Var: x = 2.0, y = 3;
    #             Function: main
    #                 Body:
    #                     print(string_of_float(1.0 +. 2*.3 -. 4 +. 3\\.2 +. y\\.x));
    #                 EndBody."""
    #     expect = "6.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,514))

    # def test_14(self):
    #     input = """
    #             Var: x = 2, y = 3;
    #             Function: main
    #                 Body:
    #                     print(string_of_bool((x > y) && True || False));
    #                 EndBody."""
    #     expect = "false"
    #     self.assertTrue(TestCodeGen.test(input,expect,515))

    # def test_15(self):
    #     input = """
    #             Var: x = 0xA, y = 0o10;
    #             Function: main
    #                 Body:
    #                     print(string_of_int(x*y));
    #                 EndBody."""
    #     expect = "80"
    #     self.assertTrue(TestCodeGen.test(input,expect,516))

    # def test_16(self):
    #     input = """
    #             Var: x = 2.0, y = 3;
    #             Function: main
    #                 Body:
    #                     print(string_of_bool((x >. y) && True || False));
    #                 EndBody."""
    #     expect = "false"
    #     self.assertTrue(TestCodeGen.test(input,expect,517))

    # def test_17(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     print(string_of_bool(False && True || False));
    #                 EndBody."""
    #     expect = "false"
    #     self.assertTrue(TestCodeGen.test(input,expect,518))

    # def test_18(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: x = 1, y = 1.0;
    #                     x = -(-1 - 2);
    #                     y = -.1.0 *. 7.0;
    #                     print(string_of_int(x));
    #                     print(string_of_float(y));
    #                 EndBody."""
    #     expect = "3-7.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,519))

    # def test_19(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     print(string_of_bool(!True || !False));
    #                 EndBody."""
    #     expect = "true"
    #     self.assertTrue(TestCodeGen.test(input,expect,520))

    # def test_20(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     foo(2,2,3);
    #                 EndBody.
    #             Function: foo
    #                 Parameter: x, y, z
    #                 Body:
    #                     x = 2*3;
    #                     print(string_of_int(x));
    #                     print(string_of_int(y));
    #                     print(string_of_int(z));
    #                 EndBody."""
    #     expect = "623"
    #     self.assertTrue(TestCodeGen.test(input,expect,521))

    # def test_21(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0.0;
    #                     While (i <. 4.0) Do
    #                         print(string_of_float(i));
    #                         i = i +. 1.0;
    #                     EndWhile. 
    #                     While (i <. 4.0) Do
    #                         print(string_of_float(i));
    #                         i = i +. 1.0;
    #                     EndWhile.
    #                 EndBody."""
    #     expect = "0.01.02.03.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,522))

    # def test_22(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0.0, value = 0;
    #                     While (i <. 4.0) Do
    #                         Var: value = 2;
    #                         print(string_of_int(value));
    #                         i = i +. 1.0;
    #                     EndWhile.
    #                     print(string_of_int(value));
    #                 EndBody."""
    #     expect = "22220"
    #     self.assertTrue(TestCodeGen.test(input,expect,523))

    # def test_23(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0.0, value = 0;
    #                     Do
    #                         print(string_of_float(i));
    #                         i = i +. 2.0;
    #                     While (i <. 4.0)
    #                     EndDo. 
    #                 EndBody."""
    #     expect = "0.02.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,524))

    # def test_24(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0.0, value = 0;
    #                     Do
    #                         print(string_of_float(i));
    #                         i = i +. 2.0;
    #                     While (i <. 4.0)
    #                     EndDo.
    #                     Do
    #                         print(string_of_float(i));
    #                         i = i +. 2.0;
    #                     While (i <. 4.0)
    #                     EndDo.  
    #                 EndBody."""
    #     expect = "0.02.04.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,525))

    # def test_25(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0.0, value = 0;
    #                     Do
    #                         print(string_of_float(i));
    #                         Break;
    #                         i = i +. 2.0;
    #                     While (i <. 4.0)
    #                     EndDo. 
    #                 EndBody."""
    #     expect = "0.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,526))

    # def test_26(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0.0, value = 0;
    #                     Do
    #                         print(string_of_float(i));
    #                         Return;
    #                         i = i +. 2.0;
    #                     While (i <. 4.0)
    #                     EndDo. 
    #                 EndBody."""
    #     expect = "0.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,527))

    # def test_27(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0;
    #                     For (i = 0, i <= 4, 1*1) Do 
    #                         print(string_of_int(i));
    #                     EndFor.
    #                 EndBody."""
    #     expect = "01234"
    #     self.assertTrue(TestCodeGen.test(input,expect,528))

    # def test_28(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0.0;
    #                     For (i = 6.0, i >. 0.0, -.2.0) Do 
    #                         print(string_of_float(i));
    #                     EndFor.
    #                 EndBody."""
    #     expect = "6.04.02.0"
    #     self.assertTrue(TestCodeGen.test(input,expect,529))

    # def test_29(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: x = 3;
    #                     If x == 1 Then 
    #                         print("1");
    #                     ElseIf x == 2 Then
    #                         print("2");
    #                     ElseIf x == 3 Then
    #                         print("3");
    #                     Else
    #                         print("Do_not_know");
    #                     EndIf.
    #                     print(" Out");
    #                 EndBody."""
    #     expect = "3 Out"
    #     self.assertTrue(TestCodeGen.test(input,expect,530))

    # def test_30(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: x = 8;
    #                     If x == 1 Then 
    #                         print("1");
    #                     ElseIf x == 2 Then
    #                         print("2");
    #                     ElseIf x == 3 Then
    #                         print("3");
    #                     Else
    #                         print("Do_not_know");
    #                     EndIf.
    #                     print(" Out");
    #                 EndBody."""
    #     expect = "Do_not_know Out"
    #     self.assertTrue(TestCodeGen.test(input,expect,531))

    # def test_31(self):
    #     input = """
    #             **Var: y[2] = {1,2};**
    #             Function: main
    #                 Body:
    #                     Var: x[2] = {1,2};
    #                     x[0] = 10;
    #                     print(string_of_int(x[0]));
    #                 EndBody."""
    #     expect = "10"
    #     self.assertTrue(TestCodeGen.test(input,expect,532))

    # def test_32(self):
    #     input = """
    #             Var: check = True;
    #             Var: y[2] = {1,2};
    #             Var: x = 4;
    #             Function: main
    #                 Body:
    #                     print(string_of_int(y[0]));
    #                 EndBody."""
    #     expect = "1"
    #     self.assertTrue(TestCodeGen.test(input,expect,533))

    # def test_33(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: x[2] = {1,2};
    #                     foo(x);
    #                 EndBody.
    #             Function: foo
    #                 Parameter: t[2]
    #                 Body:
    #                     print(string_of_int(t[0]));
    #                 EndBody."""
    #     expect = "1"
    #     self.assertTrue(TestCodeGen.test(input,expect,534))

    # def test_34(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: x[2] = {1,2};
    #                     foo(x);
    #                     print(string_of_int(x[0]));
    #                 EndBody.
    #             Function: foo
    #                 Parameter: t[2]
    #                 Body:
    #                     t[0] = 10;
    #                 EndBody."""
    #     expect = "10"
    #     self.assertTrue(TestCodeGen.test(input,expect,535))

    # def test_bubble_sort(self):
    #     input = """
    #         Function: main
    #         Body:
    #             Var: x[5] = {1, 5, 2, 7, 4};
    #             bubbleSort(x);
    #         EndBody.
    #         Function: bubbleSort
    #             Parameter: x[5]
    #             Body:
    #                 Var: iter = 0, innerIter = 0;
    #                 For(iter = 0, iter < 5, 1) Do
    #                     For(innerIter = iter, innerIter < 5, 1) Do
    #                         If x[iter] > x[innerIter] Then
    #                             Var: temp = 0;
    #                             temp = x[iter];
    #                             x[iter] = x[innerIter];
    #                             x[innerIter] = temp;
    #                         EndIf.
    #                     EndFor.
    #                 EndFor.
    #                 For(iter = 0, iter < 5, 1) Do
    #                     print(string_of_int(x[iter]));
    #                 EndFor.
    #             EndBody.
    #     """
    #     expect = "12457"
    #     self.assertTrue(TestCodeGen.test(input,expect,536))

    # def test_35(self):
    #     input = """ Function: main
    #                 Body: 
    #                     print(string_of_bool(120. =/= 120.));
    #                 EndBody.
    #                 """
    #     expect = "false"
    #     self.assertTrue(TestCodeGen.test(input,expect,537))

    # def test_36(self):
    #     input = """ Var: x = 120;

    #                 Function: foo 
    #                 Body:
    #                     x = 110;
    #                     Return True;
    #                 EndBody.
        
    #                 Function: main
    #                 Body:
    #                     If True || foo() Then 
    #                     EndIf.
    #                     print(string_of_int(x));
    #                 EndBody.
    #                 """
    #     expect = "120"
    #     self.assertTrue(TestCodeGen.test(input,expect,538))
    
    # def test_37(self):
    #     input = """ Var: x = 110;

    #                 Function: foo 
    #                 Body:
    #                     x = 120;
    #                     Return True;
    #                 EndBody.
        
    #                 Function: main
    #                 Body: 
    #                     If True && foo() Then 
    #                     EndIf.
    #                     print(string_of_int(x));
    #                 EndBody.
    #                 """
    #     expect = "120"
    #     self.assertTrue(TestCodeGen.test(input,expect,539))

    # def test_38(self):
    #     input = """ Var: x = 120;

    #                 Function: foo 
    #                 Body:
    #                     x = 110;
    #                     Return True;
    #                 EndBody.
        
    #                 Function: main
    #                 Body: 
    #                     If False && foo() Then 
    #                     EndIf.
    #                     print(string_of_int(x));
    #                 EndBody.
    #                 """
    #     expect = "120"
    #     self.assertTrue(TestCodeGen.test(input,expect,540))

    # def test_39(self):
    #     input = """ Var: x = 110;

    #                 Function: foo 
    #                 Body:
    #                     x = 120;
    #                     Return True;
    #                 EndBody.
        
    #                 Function: main
    #                 Body: 
    #                     If False || foo() Then 
    #                     EndIf.
    #                     print(string_of_int(x));
    #                 EndBody.
    #                 """
    #     expect = "120"
    #     self.assertTrue(TestCodeGen.test(input,expect,541))

    # def test_40(self):
    #     input = """ Function: main
    #                 Body: 
    #                     Var: x = 0;
    #                     For (x = 0, x < 5, 1) Do 
    #                         If x == 2 Then
    #                             Continue;
    #                         EndIf.
    #                         print(string_of_int(x));
    #                     EndFor.
    #                 EndBody.
    #                 """
    #     expect = "0134"
    #     self.assertTrue(TestCodeGen.test(input,expect,542))

    # def test_41(self):
    #     input = """ Function: main
    #                 Body: 
    #                     Var: x = 0;
    #                     For (x = 0, x < 5, 1) Do 
    #                         If x == 2 Then
    #                             Break;
    #                         EndIf.
    #                         print(string_of_int(x));
    #                     EndFor.
    #                 EndBody.
    #                 """
    #     expect = "01"
    #     self.assertTrue(TestCodeGen.test(input,expect,543))

    # def test_42(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0;
    #                     While (i < 4) Do
    #                         Var: value = 2;
    #                         print(string_of_int(value));
    #                         If i == 2 Then
    #                             Break;
    #                         EndIf.
    #                         i = i + 1;
    #                     EndWhile.
    #                 EndBody."""
    #     expect = "222"
    #     self.assertTrue(TestCodeGen.test(input,expect,544))

    # def test_43(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: i = 0;
    #                     While (i < 4) Do
    #                         Var: value = 2;
    #                         i = i + 1;
    #                         If i == 2 Then
    #                             Continue;
    #                         EndIf.
    #                         print(string_of_int(value));
    #                     EndWhile.
    #                 EndBody."""
    #     expect = "222"
    #     self.assertTrue(TestCodeGen.test(input,expect,545))

    # def test_44(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: x = 3;
    #                     foo(x);
    #                     print(string_of_int(x));
    #                 EndBody.
    #             Function: foo
    #                 Parameter: t
    #                 Body:
    #                     t = 4;
    #                 EndBody."""
    #     expect = "3"
    #     self.assertTrue(TestCodeGen.test(input,expect,546))

    # def test_45(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: x = 3;
    #                     x = foo(5);
    #                     print(string_of_int(x));
    #                 EndBody.
    #             Function: foo
    #                 Parameter: t
    #                 Body:
    #                     t = 4;
    #                     Return t;
    #                 EndBody."""
    #     expect = "4"
    #     self.assertTrue(TestCodeGen.test(input,expect,547))

    # def test_46(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     print(string_of_int(foo(5)));
    #                 EndBody.
    #             Function: foo
    #                 Parameter: t
    #                 Body:
    #                     t = 4;
    #                     Return t;
    #                 EndBody."""
    #     expect = "4"
    #     self.assertTrue(TestCodeGen.test(input,expect,548))

    # def test_47(self):
    #     input = """
    #             Var: x[1] = {3.5}, y[1] = {True}, z[1] = {"Hello"};
    #             Function: main
    #                 Body:
    #                     print(string_of_float(x[0]));
    #                     print(string_of_bool(y[0]));
    #                     print(z[0]);
    #                 EndBody."""
    #     expect = "3.5trueHello"
    #     self.assertTrue(TestCodeGen.test(input,expect,549))

    # def test_48(self):
    #     input = """
    #             Function: main
    #                 Body:
    #                     Var: x[1] = {3.5}, y[1] = {True}, z[1] = {"Hello"};
    #                     print(string_of_float(x[0]));
    #                     print(string_of_bool(y[0]));
    #                     print(z[0]);
    #                 EndBody."""
    #     expect = "3.5trueHello"
    #     self.assertTrue(TestCodeGen.test(input,expect,550))

    # def test_49(self):
    #     input = """
    #             Function: main
    #             Body:
    #                 Var: a[3] = {1,2,3}, b = 0;
    #                 foo(a, b);
    #                 print(string_of_int(a[0]));
    #                 print(string_of_int(a[1]));
    #                 print(string_of_int(a[2]));
    #                 print(string_of_int(b));
    #             EndBody.

    #             Function: foo
    #             Parameter: a[3], b
    #             Body:
    #                 a = {4,5,6};
    #                 b = 1;
    #             EndBody.
    #             """
    #     expect = "4560"
    #     self.assertTrue(TestCodeGen.test(input,expect,551))

    # def test_50(self):
    #     input = """
    #             Function: main
    #             Body:
    #                 print(string_of_int(foo()[0]));
    #             EndBody.

    #             Function: foo
    #             Body:
    #                 Var: a[3] = {4,5,6};
    #                 Return a;
    #             EndBody.
    #             """
    #     expect = "4"
    #     self.assertTrue(TestCodeGen.test(input,expect,552))

    # def test_51(self):
    #     input = """
    #             Function: main
    #             Body:
    #                 Var: a[3] = {1,2,3}, b[3] = {5,6,7};
    #                 a = b;
    #                 print(string_of_int(a[0]));
    #                 print(string_of_int(a[1]));
    #                 print(string_of_int(a[2]));
    #             EndBody.
    #             """
    #     expect = "567"
    #     self.assertTrue(TestCodeGen.test(input,expect,553))

    # def test_52(self):
    #     input = """
    #             Function: main
    #             Body:
    #                 Var: a[3] = {1,2,3}, b[3] = {5,6,7};
    #                 b = a;
    #                 print(string_of_int(b[0]));
    #                 print(string_of_int(b[1]));
    #                 print(string_of_int(b[2]));
    #             EndBody.
    #             """
    #     expect = "123"
    #     self.assertTrue(TestCodeGen.test(input,expect,554))

    def test_53(self):
        input = """
            Function: isPrimeNumber
            Parameter: x
            Body:   
                If ((x==2) || (x==3)) Then
                    Return True;
                Else
                    Var: i=1, mid =0;
                    mid = x\\2+1;
                    For(i=2, i<mid, 1) Do
                        If(x%i==0) Then
                            Return False;
                        EndIf.
                    EndFor.
                EndIf.
                Return True;
            EndBody.
            Function: main
            Body:  
                Var: x=0;
                For(x=2, x<20, 1)Do
                    If(isPrimeNumber(x)) Then
                        print(string_of_int(x));
                        print("\\n");
                    EndIf.
                EndFor.
            EndBody.
        """
        expect = "2\n3\n5\n7\n11\n13\n17\n19\n"
        self.assertTrue(TestCodeGen.test(input,expect,555))
