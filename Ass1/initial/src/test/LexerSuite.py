import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):
      
    def test_lower_identifier(self):
        """test identifiers"""
        self.assertTrue(TestLexer.checkLexeme("abc","abc,<EOF>",1))

    def test_lower_upper_id(self):
        self.assertTrue(TestLexer.checkLexeme("Var","Var,<EOF>",2))

    def test_wrong_token(self):
        self.assertTrue(TestLexer.checkLexeme("ab?svn","ab,Error Token ?",3))

    def test_integer(self):
        """test integers"""
        self.assertTrue(TestLexer.checkLexeme("Var x;","Var,x,;,<EOF>",4))

    def test_illegal_escape(self):
        """test illegal escape"""
        self.assertTrue(TestLexer.checkLexeme(""" "abc\\h def"  ""","""Illegal Escape In String: abc\\h""",5))

    def test_unterminated_string(self):
        """test unclosed string"""
        self.assertTrue(TestLexer.checkLexeme(""" "abc def  ""","""Unclosed String: abc def  """,6))

    def test_int_lit_1(self):
        """test integer literal"""
        self.assertTrue(TestLexer.checkLexeme("1234 00","1234,0,0,<EOF>",7))

    def test_int_lit_2(self):
        """test integer literal"""
        self.assertTrue(TestLexer.checkLexeme("0199 0xFF 0XABC 0o567 0O77","0,199,0xFF,0XABC,0o567,0O77,<EOF>",8))

    def test_int_lit_3(self):
        """test integer literal"""
        self.assertTrue(TestLexer.checkLexeme("0x0987","0,x0987,<EOF>",9))

    def test_int_lit_4(self):
        """test integer literal"""
        self.assertTrue(TestLexer.checkLexeme("0xEFGH","0xEF,Error Token G",10))

    def test_int_lit_5(self):
        """test integer literal"""
        self.assertTrue(TestLexer.checkLexeme("0o768","0o76,8,<EOF>",11))

    def test_float_lit_1(self):
        """test float literal"""
        self.assertTrue(TestLexer.checkLexeme("12.0e3 12e3 12.e5","12.0e3,12e3,12.e5,<EOF>",12))

    def test_float_lit_2(self):
        """test float literal"""
        self.assertTrue(TestLexer.checkLexeme("12.0e3 12000. 120000e-1","12.0e3,12000.,120000e-1,<EOF>",13))

    ########????????
    def test_float_lit_3(self):
        """test float literal"""
        self.assertTrue(TestLexer.checkLexeme("000.000","0,0,0.000,<EOF>",14))

    def test_float_lit_4(self):
        """test float literal"""
        self.assertTrue(TestLexer.checkLexeme("12E0","12E0,<EOF>",15))

    def test_boolean_lit_1(self):
        """test boolean literal"""
        self.assertTrue(TestLexer.checkLexeme("Var x = True","Var,x,=,True,<EOF>",16))

    def test_boolean_lit_2(self):
        """test boolean literal"""
        self.assertTrue(TestLexer.checkLexeme("Var x = False","Var,x,=,False,<EOF>",17))

    def test_boolean_lit_3(self):
        """test boolean literal"""
        self.assertTrue(TestLexer.checkLexeme("Var x = true","Var,x,=,true,<EOF>",18))

    def test_boolean_lit_4(self):
        "test boolean literal"
        self.assertTrue(TestLexer.checkLexeme("Var x = TRUE","Var,x,=,Error Token T",19))

    def test_string_lit_1(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen"  ""","hello my fen,<EOF>",20))

    def test_string_lit_2(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen \\t \\n"  ""","hello my fen \\t \\n,<EOF>",21))

    def test_string_lit_3(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen \\h"  ""","Illegal Escape In String: hello my fen \\h",22))

    def test_string_lit_4(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen '" hi"  ""","""hello my fen '" hi,<EOF>""",23))

    def test_string_lit_5(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen \\' hi"  ""","""hello my fen \\' hi,<EOF>""",24))

    def test_string_lit_6(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen ' hi"  ""","""Illegal Escape In String: hello my fen ' """,25))

    def test_string_lit_7(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen \\h hi"  ""","""Illegal Escape In String: hello my fen \\h""",26))

    def test_string_lit_8(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen \n"  ""","""Unclosed String: hello my fen """,27))

    def test_string_lit_9(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen \\\\c"  ""","""hello my fen \\\\c,<EOF>""",28))

    def test_string_lit_10(self):
        """test string literal"""
        self.assertTrue(TestLexer.checkLexeme(""" "hello my fen""  ""","""hello my fen,Unclosed String:   """,29))

    def test_comment_1(self):
        """test comment"""
        self.assertTrue(TestLexer.checkLexeme(" **hello my fen** ", "<EOF>", 30))

    def test_comment_2(self):
        """test comment"""
        self.assertTrue(TestLexer.checkLexeme(" **hello my fen\n*hi you** ", "<EOF>", 31))

    def test_comment_3(self):
        """test comment"""
        self.assertTrue(TestLexer.checkLexeme(" ***hello my fen*** ", "*,<EOF>", 32))

    def test_comment_4(self):
        """test comment"""
        self.assertTrue(TestLexer.checkLexeme(" **hello my fen ", "Unterminated Comment", 33))

    def test_keywords_1(self):
        """test keywords"""
        self.assertTrue(TestLexer.checkLexeme("BodyElseEndForIfVarEndDo", "Body,Else,EndFor,If,Var,EndDo,<EOF>", 34))

    def test_keywords_2(self):
        """test keywords"""
        self.assertTrue(TestLexer.checkLexeme("BreakElseIfEndWhileParameterWhile", "Break,ElseIf,EndWhile,Parameter,While,<EOF>", 35))

    def test_keywords_3(self):
        """test keywords"""
        self.assertTrue(TestLexer.checkLexeme("ContinueEndBodyForReturnTrue", "Continue,EndBody,For,Return,True,<EOF>", 36))

    def test_keywords_4(self):
        """test keywords"""
        self.assertTrue(TestLexer.checkLexeme("DoEndIfFunctionThenFalse", "Do,EndIf,Function,Then,False,<EOF>", 37))

    def test_operator_1(self):
        """test operators"""
        self.assertTrue(TestLexer.checkLexeme("+ * % == <= >.", "+,*,%,==,<=,>.,<EOF>", 38))

    def test_operator_2(self):
        """test operators"""
        self.assertTrue(TestLexer.checkLexeme("+. *. ! != >= <=.", "+.,*.,!,!=,>=,<=.,<EOF>", 39))

    def test_operator_3(self):
        """test operators"""
        self.assertTrue(TestLexer.checkLexeme("- \ && < =/= >=.", "-,\,&&,<,=/=,>=.,<EOF>", 40))

    def test_operator_5(self):
        """test operators"""
        self.assertTrue(TestLexer.checkLexeme("-. \\. || > <.", "-.,\\.,||,>,<.,<EOF>", 41))

    def test_id_1(self):
        """test id"""
        self.assertTrue(TestLexer.checkLexeme("x[1][2] = 3", "x,[,1,],[,2,],=,3,<EOF>", 42))

    def test_id_2(self):
        """test id"""
        self.assertTrue(TestLexer.checkLexeme("x[1][2] = {2, 3}", "x,[,1,],[,2,],=,{,2,,,3,},<EOF>", 43))

    def test_id_3(self):
        """test id"""
        self.assertTrue(TestLexer.checkLexeme("x = -3", "x,=,-,3,<EOF>", 44))

    def test_id_4(self):
        """test id"""
        self.assertTrue(TestLexer.checkLexeme("x = -.3.5 +. 12e4", "x,=,-.,3.5,+.,12e4,<EOF>", 45))

    def test_mix_1(self):
        """test mix"""
        self.assertTrue(TestLexer.checkLexeme(r"""
        Function: foo
            Body:
                x = 10;
                ok();
            EndBody.
        """, "Function,:,foo,Body,:,x,=,10,;,ok,(,),;,EndBody,.,<EOF>", 46))

    def test_mix_2(self):
        """test mix"""
        self.assertTrue(TestLexer.checkLexeme(r"""
        value = "string nay la value;
        value2 = "string string string";
        """, "value,=,Unclosed String: string nay la value;", 47))

    def test_mix_3(self):
        """test mix"""
        self.assertTrue(TestLexer.checkLexeme(r"""
        For (i = 1, i < 5, 2) Do
            writeln(i);
        EndFor.
        """, "For,(,i,=,1,,,i,<,5,,,2,),Do,writeln,(,i,),;,EndFor,.,<EOF>", 48))

    def test_mix_4(self):
        """test mix"""
        self.assertTrue(TestLexer.checkLexeme(r"""
        x = x+y-z*y\f-t1 && 123123;
        """, r"x,=,x,+,y,-,z,*,y,\,f,-,t1,&&,123123,;,<EOF>", 49))

    def test_mix_5(self):
        """test mix"""
        self.assertTrue(TestLexer.checkLexeme(r"""
        b[1+2] + int(3) + float_to_int(5.1) - 2 * 3 - 5 + 4 + f[a || b] % 2
        """, r"b,[,1,+,2,],+,int,(,3,),+,float_to_int,(,5.1,),-,2,*,3,-,5,+,4,+,f,[,a,||,b,],%,2,<EOF>", 50))

    def test_51_bool_mix_with_id_2(self):
        """test bool value mix with id, id first"""
        input = """someidFalse"""
        output = """someidFalse,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 51))

    ###################################################
    #   ARRAY TEST: 6 testcases
    def test_52_simple_array_lexer(self):
        """test simple array lexer"""
        input = """{1,2,3,4,5}"""
        output = """{,1,,,2,,,3,,,4,,,5,},<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 52))

    def test_53_empty_array_lexer(self):
        """test empty array lexer"""
        input = """{}"""
        output = """{,},<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 53))

    def test_54_array_in_array_lexer(self):
        """test array in array lexer"""
        input = """{{1,2,3},{3,2,1}}"""
        output = """{,{,1,,,2,,,3,},,,{,3,,,2,,,1,},},<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 54))

    def test_55_array_in_array_lexer(self):
        """test array in array lexer"""
        input = """{{1,2,3},{3,2,1}}"""
        output = """{,{,1,,,2,,,3,},,,{,3,,,2,,,1,},},<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 55))

    def test_56_array_with_various_type_lexer(self):
        """test array contains various types lexer"""
        input = """{{{{}}},   {1,2,3} ,1, 2,  "abc",99E-0,True}"""
        output = """{,{,{,{,},},},,,{,1,,,2,,,3,},,,1,,,2,,,abc,,,99E-0,,,True,},<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 56))

    def test_57_array_with_id_and_exp(self):
        """test array contains id and expression lexer"""
        input = """{id, funccall(param, param2), 1+2+3}"""
        output = """{,id,,,funccall,(,param,,,param2,),,,1,+,2,+,3,},<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 57))

    # Various func test
    def test_58_string_unclosed_lexer(self):
        input = \
            """Function: abc
                Body:
                    s = "abcde
                Endbody."""
        output = "Function,:,abc,Body,:,s,=,Unclosed String: abcde"
        self.assertTrue(TestLexer.checkLexeme(input, output, 58))

    def test_59_func_with_comment_lexer(self):
        """Check simple func decl with comments in lexer"""
        input = \
            """** some comment **
            Function: foo ** some more comment **
                Parameter: abc ** MuchM0re comment **
                Body:  ** LOTS of comment !@#$%^^&%&*() **
                EndBody **Here some too**. """
        output = "Function,:,foo,Parameter,:,abc,Body,:,EndBody,.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, output, 59))

    def test60_complex_exp_test_lexer(self):
        """Some complex expression in lexer"""
        input = \
            r"""Function: foo 
                Body: 
                    a = 1 + 1.23 *. abc \. id[12[123][2][moreid]];
                    b = 1.E-12 *. someThinG \ (-12.34) +. (!True) [False[moreid][more]]
            =/= (foo(123) || goo(-234 && ((f()[1 + 3][-2.99e-123] + 56%7))));
                EndBody."""
        output = r"""Function,:,foo,Body,:,a,=,1,+,1.23,*.,abc,\.,id,[,12,[,123,]""" + \
                 r""",[,2,],[,moreid,],],;,b,=,1.E-12,*.,someThinG,\,(,-,12.34,),+.,(,""" + \
                 r"""!,True,),[,False,[,moreid,],[,more,],],=/=,(,foo,(,123,),||,goo,(,""" + \
                 r"""-,234,&&,(,(,f,(,),[,1,+,3,],[,-,2.99e-123,],+,56,%,7,),),),),;,EndBody,.,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 60))

    def test_61_some_wrong_id_lexer_mix(self):
        """Some unrecognized id lexer in function"""
        input = \
            r"""Function: ThisNotTrue
                Body:
                    Do
                        Break;
                    While True
                    EndDo.
                EndBody."""
        output = "Function,:,Error Token T"
        self.assertTrue(TestLexer.checkLexeme(input, output, 61))

    def test_62_some_wrong_keyword_mix(self):
        """Some unrecognized keyword in function"""
        input = \
            r"""Funtion: foo
                Body:
                    Do
                        Break
                    While True
                    EndDo.
                EndBody."""
        output = "Error Token F"
        self.assertTrue(TestLexer.checkLexeme(input, output, 62))

    def test_63_dense_code_check(self):
        """Test no space code"""
        input = r"Var:a,b=123;Function:foo123 Parameter:a[99]Body:Var:x;" + \
                r"abc=321;WhileTrueDoEndWhile.If123ThenFor(abc=999,(13||31)&&" + \
                r"True-False,f())DoVar:def;EndFor.ElseVar:ghi;EndIf.EndBody."
        output = r"Var,:,a,,,b,=,123,;,Function,:,foo123,Parameter,:,a,[,99,]" + \
                 r",Body,:,Var,:,x,;,abc,=,321,;,While,True,Do,EndWhile,.,If,123,Then," + \
                 r"For,(,abc,=,999,,,(,13,||,31,),&&,True,-,False,,,f,(,),),Do,Var,:,def,;" + \
                 r",EndFor,.,Else,Var,:,ghi,;,EndIf,.,EndBody,.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, output, 63))

    def test_64_float_with_exp_missing_exp_number(self):
        """test float missing decimal after exp"""
        input = """123e"""
        output = """123,e,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 64))

    def test_65_float_with_both_missing_exp_number(self):
        """test float with both point and e but missing e decimal"""
        input = """123.123e"""
        output = """123.123,e,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 65))

    def test_66_float_dec_without_int_part(self):
        """test float"""
        input = """.123"""
        output = """.,123,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 66))

    def test_67_float_exp_without_int_part(self):
        """test float"""
        input = """E123"""
        output = """Error Token E"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 67))

    def test_68_float_end_with_dot(self):
        """test float has dot at the end"""
        input = """123."""
        output = """123.,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 68))

    def test_69_float_has_e0(self):
        """test float has exp 0"""
        input = """1.e-0 1.E0"""
        output = """1.e-0,1.E0,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 69))

    def test_70_float_has_e0(self):
        """test float has exp 0"""
        input = """1.e-0 1.000E0"""
        output = """1.e-0,1.000E0,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 70))

    def test_71_simple_exp_test(self):
        """A simple expression"""
        input = """      b = 1.E-12  =/= foo(123);"""
        output = "b,=,1.E-12,=/=,foo,(,123,),;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, output, 71))

    def test_72_string_int_float_keywords(self):
        self.assertTrue(TestLexer.checkLexeme("If (i_am_hand_some == True) Then \n killme();"
                                              "\n ElseIf (i_am_hand_some != notSo) Then \n makeUp();"
                                              "\n Else eatMore();"
                                              "\n EndIf.",
                                              "If,(,i_am_hand_some,==,True,),Then,killme,(,),;,"
                                              "ElseIf,(,i_am_hand_some,!=,notSo,),Then,makeUp,(,),;,"
                                              "Else,eatMore,(,),;,EndIf,.,<EOF>", 72))

    def test_73_string_int_float_keywords(self):
        self.assertTrue(TestLexer.checkLexeme("If (i_am_hand_some == True) Then \n killme();"
                                              "\n ElseIf (i_am_hand_some != NotSo) Then \n makeUp();"
                                              "\n Else eatMore();"
                                              "\n EndIf.",
                                              "If,(,i_am_hand_some,==,True,),Then,killme,(,),;,"
                                              "ElseIf,(,i_am_hand_some,!=,Error Token N", 73))

    def test_74_string(self):
        self.assertTrue(TestLexer.checkLexeme(""" "Hello\rHello" ""","Unclosed String: Hello", 74))

    def test_75_valid_string(self):
        """test valid string"""
        input = \
            """" This is a test !@#$%^^&*()?/|"
            " 1234567890 \\' ASD" abc 
            "KJFLDSK '" \\f asdasd "
            "\\b\\f\\r\\n\\t\\'\\\\"
             """
        output = \
            """ This is a test !@#$%^^&*()?/|, 1234567890 \\' ASD,abc,KJFLDSK '" \\f asdasd ,\\b\\f\\r\\n\\t\\'\\\\,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 75))

    def test_76_unclosed_string(self):
        """test unclosed string"""
        input = """" This is a test  asdsadasd \\f asdasd  """
        output = """Unclosed String:  This is a test  asdsadasd \\f asdasd  """
        self.assertTrue(TestLexer.checkLexeme(input, output, 76))

    def test_77_string_contains_illegal_escape_1(self):
        """test string which contains illegal escape: quote"""
        input = """" This is a test '" asdsadasd ' \\f asdasd " """
        output = """Illegal Escape In String:  This is a test '" asdsadasd ' """
        self.assertTrue(TestLexer.checkLexeme(input, output, 77))

    def test_78_string_contains_illegal_escape_2(self):
        """test string which contains illegal escape: unidentified backslash"""
        input = """" This is a test '" asdsadasd \\h asdasd " """
        output = """Illegal Escape In String:  This is a test '" asdsadasd \\h"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 78))

    def test_79_string_contains_illegal_escape_3(self):
        """test string which contains illegal escape: lone backslash"""
        input = """" This is a test '" asdsadasd \\ asdasd " """
        output = """Illegal Escape In String:  This is a test '" asdsadasd \\ """
        self.assertTrue(TestLexer.checkLexeme(input, output, 79))

    def test_80_string_contains_newline(self):
        """test string which contains newline character"""
        input = """" This is a test '" asdsa\ndasd \\ asdasd " """
        output = """Unclosed String:  This is a test '" asdsa"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 80))

    def test_81_empty_string(self):
        """test empty string"""
        input = """"" """
        output = """,<EOF>"""
        self.assertTrue(TestLexer.checkLexeme(input, output, 81))

    def test_82_unclose_string_contains_quote(self):
        """test string which contains quote and double quote"""
        input = """" This is a test '" """
        output = """Unclosed String:  This is a test '" """
        self.assertTrue(TestLexer.checkLexeme(input, output, 82))

    def test_83_unterminated_comment(self):
        self.assertTrue(TestLexer.checkLexeme(""" **This is a test *  """, """Unterminated Comment""", 83))

    def test_84_string_int_float(self):
        self.assertTrue(TestLexer.checkLexeme("**Hello world**\"This is a string: \\r\"12.0x1230o123",
                                              "This is a string: \\r,12.0,x1230o123,<EOF>", 84))

    def test_85_string_int_float(self):
        self.assertTrue(TestLexer.checkLexeme("**Hello \\t \t \ff world**\"This is a string: \\r\"12.0e120 0o123",
                                              "This is a string: \\r,12.0e120,0o123,<EOF>", 85))

    def test_86_string_int_float_keywords(self):
        self.assertTrue(TestLexer.checkLexeme("Var: a=5, arr[1][2]={{12e-6,12},{2,3}}",
                                              "Var,:,a,=,5,,,arr,[,1,],[,2,],=,"
                                              "{,{,12e-6,,,12,},,,{,2,,,3,},},<EOF>", 86))

    def test_87_string_int_float_keywords(self):
        self.assertTrue(TestLexer.checkLexeme("Var: a=5, arr[1][2]={{\"str\\t\",\"\'\"\"},"
                                              "{\"\\\\\",**comment**4}} 12..2",
                                              "Var,:,a,=,5,,,arr,[,1,],[,2,],=,"
                                              "{,{,str\\t,,,\'\",},,,{,\\\\,,,4,},},12.,.,2,<EOF>", 87))

    def test_88_string_int_float_keywords(self):
        self.assertTrue(TestLexer.checkLexeme("For (i=0,i<10,2) Do \n \t s=s+1;\n EndFor.",
                                              "For,(,i,=,0,,,i,<,10,,,2,),Do,s,=,s,+,1,;,EndFor,.,<EOF>", 88))

    def test_89_underscore_first(self):
        """fail because Underscore first"""
        self.assertTrue(TestLexer.checkLexeme("_aDH_198_bcdef", "Error Token _", 89))

    def test_90_hex(self):
        """success"""
        self.assertTrue(TestLexer.checkLexeme("0x123ABCD", "0x123ABCD,<EOF>", 90))

    def test_91_hex(self):
        """fail because no X in hex number"""
        self.assertTrue(TestLexer.checkLexeme("0x123ABCX", "0x123ABC,Error Token X", 91))

    def test_92_oc(self):
        """success"""
        self.assertTrue(TestLexer.checkLexeme("0O1234567", "0O1234567,<EOF>", 92))

    def test_93_oc(self):
        """fail because not int, hex or octal"""
        self.assertTrue(TestLexer.checkLexeme("0H1810198", "0,Error Token H", 93))

    def test_94_float(self):
        """success"""
        self.assertTrue(TestLexer.checkLexeme("1810.198", "1810.198,<EOF>", 94))

    def test_95_float(self):
        """success"""
        self.assertTrue(TestLexer.checkLexeme("1810.198E5", "1810.198E5,<EOF>", 95))

    def test_96_float(self):
        """success"""
        self.assertTrue(TestLexer.checkLexeme("1810E198", "1810E198,<EOF>", 96))

    def test_97_float(self):
        """success"""
        self.assertTrue(TestLexer.checkLexeme("1810.E198", "1810.E198,<EOF>", 97))

    def test_98_esc_str(self):
        """ Test Escape """
        self.assertTrue(TestLexer.checkLexeme("\"Single Quote   \\'\"", "Single Quote   \\',<EOF>", 98))

    def test_99_esc_str(self):
        """ Test Escape """
        self.assertTrue(TestLexer.checkLexeme("\"Single Quote    \\' \"", "Single Quote    \\' ,<EOF>", 99))

    def test_100_esc_str(self):
        """ Test Escape """
        self.assertTrue(TestLexer.checkLexeme("\"Single Quote    \' \"",
                                              "Illegal Escape In String: Single Quote    \' ", 100))