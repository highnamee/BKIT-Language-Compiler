# Generated from /Users/user/Desktop/HK201/PPL/Ass2/initial/src/main/bkit/parser/BKIT.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BKITParser import BKITParser
else:
    from BKITParser import BKITParser

# This class defines a complete listener for a parse tree produced by BKITParser.
class BKITListener(ParseTreeListener):

    # Enter a parse tree produced by BKITParser#program.
    def enterProgram(self, ctx:BKITParser.ProgramContext):
        pass

    # Exit a parse tree produced by BKITParser#program.
    def exitProgram(self, ctx:BKITParser.ProgramContext):
        pass


    # Enter a parse tree produced by BKITParser#var_declare.
    def enterVar_declare(self, ctx:BKITParser.Var_declareContext):
        pass

    # Exit a parse tree produced by BKITParser#var_declare.
    def exitVar_declare(self, ctx:BKITParser.Var_declareContext):
        pass


    # Enter a parse tree produced by BKITParser#var_declare_item.
    def enterVar_declare_item(self, ctx:BKITParser.Var_declare_itemContext):
        pass

    # Exit a parse tree produced by BKITParser#var_declare_item.
    def exitVar_declare_item(self, ctx:BKITParser.Var_declare_itemContext):
        pass


    # Enter a parse tree produced by BKITParser#var_init.
    def enterVar_init(self, ctx:BKITParser.Var_initContext):
        pass

    # Exit a parse tree produced by BKITParser#var_init.
    def exitVar_init(self, ctx:BKITParser.Var_initContext):
        pass


    # Enter a parse tree produced by BKITParser#var_id.
    def enterVar_id(self, ctx:BKITParser.Var_idContext):
        pass

    # Exit a parse tree produced by BKITParser#var_id.
    def exitVar_id(self, ctx:BKITParser.Var_idContext):
        pass


    # Enter a parse tree produced by BKITParser#all_literal.
    def enterAll_literal(self, ctx:BKITParser.All_literalContext):
        pass

    # Exit a parse tree produced by BKITParser#all_literal.
    def exitAll_literal(self, ctx:BKITParser.All_literalContext):
        pass


    # Enter a parse tree produced by BKITParser#array_literal.
    def enterArray_literal(self, ctx:BKITParser.Array_literalContext):
        pass

    # Exit a parse tree produced by BKITParser#array_literal.
    def exitArray_literal(self, ctx:BKITParser.Array_literalContext):
        pass


    # Enter a parse tree produced by BKITParser#func_declare.
    def enterFunc_declare(self, ctx:BKITParser.Func_declareContext):
        pass

    # Exit a parse tree produced by BKITParser#func_declare.
    def exitFunc_declare(self, ctx:BKITParser.Func_declareContext):
        pass


    # Enter a parse tree produced by BKITParser#expression.
    def enterExpression(self, ctx:BKITParser.ExpressionContext):
        pass

    # Exit a parse tree produced by BKITParser#expression.
    def exitExpression(self, ctx:BKITParser.ExpressionContext):
        pass


    # Enter a parse tree produced by BKITParser#exp1.
    def enterExp1(self, ctx:BKITParser.Exp1Context):
        pass

    # Exit a parse tree produced by BKITParser#exp1.
    def exitExp1(self, ctx:BKITParser.Exp1Context):
        pass


    # Enter a parse tree produced by BKITParser#exp2.
    def enterExp2(self, ctx:BKITParser.Exp2Context):
        pass

    # Exit a parse tree produced by BKITParser#exp2.
    def exitExp2(self, ctx:BKITParser.Exp2Context):
        pass


    # Enter a parse tree produced by BKITParser#exp3.
    def enterExp3(self, ctx:BKITParser.Exp3Context):
        pass

    # Exit a parse tree produced by BKITParser#exp3.
    def exitExp3(self, ctx:BKITParser.Exp3Context):
        pass


    # Enter a parse tree produced by BKITParser#exp4.
    def enterExp4(self, ctx:BKITParser.Exp4Context):
        pass

    # Exit a parse tree produced by BKITParser#exp4.
    def exitExp4(self, ctx:BKITParser.Exp4Context):
        pass


    # Enter a parse tree produced by BKITParser#exp5.
    def enterExp5(self, ctx:BKITParser.Exp5Context):
        pass

    # Exit a parse tree produced by BKITParser#exp5.
    def exitExp5(self, ctx:BKITParser.Exp5Context):
        pass


    # Enter a parse tree produced by BKITParser#exp6.
    def enterExp6(self, ctx:BKITParser.Exp6Context):
        pass

    # Exit a parse tree produced by BKITParser#exp6.
    def exitExp6(self, ctx:BKITParser.Exp6Context):
        pass


    # Enter a parse tree produced by BKITParser#operand.
    def enterOperand(self, ctx:BKITParser.OperandContext):
        pass

    # Exit a parse tree produced by BKITParser#operand.
    def exitOperand(self, ctx:BKITParser.OperandContext):
        pass


    # Enter a parse tree produced by BKITParser#func_call_exp.
    def enterFunc_call_exp(self, ctx:BKITParser.Func_call_expContext):
        pass

    # Exit a parse tree produced by BKITParser#func_call_exp.
    def exitFunc_call_exp(self, ctx:BKITParser.Func_call_expContext):
        pass


    # Enter a parse tree produced by BKITParser#statement.
    def enterStatement(self, ctx:BKITParser.StatementContext):
        pass

    # Exit a parse tree produced by BKITParser#statement.
    def exitStatement(self, ctx:BKITParser.StatementContext):
        pass


    # Enter a parse tree produced by BKITParser#assign_stm.
    def enterAssign_stm(self, ctx:BKITParser.Assign_stmContext):
        pass

    # Exit a parse tree produced by BKITParser#assign_stm.
    def exitAssign_stm(self, ctx:BKITParser.Assign_stmContext):
        pass


    # Enter a parse tree produced by BKITParser#statement_list.
    def enterStatement_list(self, ctx:BKITParser.Statement_listContext):
        pass

    # Exit a parse tree produced by BKITParser#statement_list.
    def exitStatement_list(self, ctx:BKITParser.Statement_listContext):
        pass


    # Enter a parse tree produced by BKITParser#if_stm.
    def enterIf_stm(self, ctx:BKITParser.If_stmContext):
        pass

    # Exit a parse tree produced by BKITParser#if_stm.
    def exitIf_stm(self, ctx:BKITParser.If_stmContext):
        pass


    # Enter a parse tree produced by BKITParser#for_stm.
    def enterFor_stm(self, ctx:BKITParser.For_stmContext):
        pass

    # Exit a parse tree produced by BKITParser#for_stm.
    def exitFor_stm(self, ctx:BKITParser.For_stmContext):
        pass


    # Enter a parse tree produced by BKITParser#while_stm.
    def enterWhile_stm(self, ctx:BKITParser.While_stmContext):
        pass

    # Exit a parse tree produced by BKITParser#while_stm.
    def exitWhile_stm(self, ctx:BKITParser.While_stmContext):
        pass


    # Enter a parse tree produced by BKITParser#dowhile_stm.
    def enterDowhile_stm(self, ctx:BKITParser.Dowhile_stmContext):
        pass

    # Exit a parse tree produced by BKITParser#dowhile_stm.
    def exitDowhile_stm(self, ctx:BKITParser.Dowhile_stmContext):
        pass


    # Enter a parse tree produced by BKITParser#break_stm.
    def enterBreak_stm(self, ctx:BKITParser.Break_stmContext):
        pass

    # Exit a parse tree produced by BKITParser#break_stm.
    def exitBreak_stm(self, ctx:BKITParser.Break_stmContext):
        pass


    # Enter a parse tree produced by BKITParser#continue_stm.
    def enterContinue_stm(self, ctx:BKITParser.Continue_stmContext):
        pass

    # Exit a parse tree produced by BKITParser#continue_stm.
    def exitContinue_stm(self, ctx:BKITParser.Continue_stmContext):
        pass


    # Enter a parse tree produced by BKITParser#call_stm.
    def enterCall_stm(self, ctx:BKITParser.Call_stmContext):
        pass

    # Exit a parse tree produced by BKITParser#call_stm.
    def exitCall_stm(self, ctx:BKITParser.Call_stmContext):
        pass


    # Enter a parse tree produced by BKITParser#return_stm.
    def enterReturn_stm(self, ctx:BKITParser.Return_stmContext):
        pass

    # Exit a parse tree produced by BKITParser#return_stm.
    def exitReturn_stm(self, ctx:BKITParser.Return_stmContext):
        pass



del BKITParser