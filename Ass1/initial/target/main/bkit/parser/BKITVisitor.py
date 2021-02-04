# Generated from main/bkit/parser/BKIT.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BKITParser import BKITParser
else:
    from BKITParser import BKITParser

# This class defines a complete generic visitor for a parse tree produced by BKITParser.

class BKITVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BKITParser#program.
    def visitProgram(self, ctx:BKITParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#var_declare.
    def visitVar_declare(self, ctx:BKITParser.Var_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#var_init.
    def visitVar_init(self, ctx:BKITParser.Var_initContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#var_id.
    def visitVar_id(self, ctx:BKITParser.Var_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#all_literal.
    def visitAll_literal(self, ctx:BKITParser.All_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#array_literal.
    def visitArray_literal(self, ctx:BKITParser.Array_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#func_declare.
    def visitFunc_declare(self, ctx:BKITParser.Func_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#func_begin.
    def visitFunc_begin(self, ctx:BKITParser.Func_beginContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#func_body.
    def visitFunc_body(self, ctx:BKITParser.Func_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#expression.
    def visitExpression(self, ctx:BKITParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp1.
    def visitExp1(self, ctx:BKITParser.Exp1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp2.
    def visitExp2(self, ctx:BKITParser.Exp2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp3.
    def visitExp3(self, ctx:BKITParser.Exp3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp4.
    def visitExp4(self, ctx:BKITParser.Exp4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp5.
    def visitExp5(self, ctx:BKITParser.Exp5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#exp6.
    def visitExp6(self, ctx:BKITParser.Exp6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#operand.
    def visitOperand(self, ctx:BKITParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#index_operator.
    def visitIndex_operator(self, ctx:BKITParser.Index_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#func_call_exp.
    def visitFunc_call_exp(self, ctx:BKITParser.Func_call_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#statement.
    def visitStatement(self, ctx:BKITParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#var_init_stm.
    def visitVar_init_stm(self, ctx:BKITParser.Var_init_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#var_id_stm.
    def visitVar_id_stm(self, ctx:BKITParser.Var_id_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#assign_stm.
    def visitAssign_stm(self, ctx:BKITParser.Assign_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#if_stm.
    def visitIf_stm(self, ctx:BKITParser.If_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#for_stm.
    def visitFor_stm(self, ctx:BKITParser.For_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#while_stm.
    def visitWhile_stm(self, ctx:BKITParser.While_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#dowhile_stm.
    def visitDowhile_stm(self, ctx:BKITParser.Dowhile_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#break_stm.
    def visitBreak_stm(self, ctx:BKITParser.Break_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#continue_stm.
    def visitContinue_stm(self, ctx:BKITParser.Continue_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#call_stm.
    def visitCall_stm(self, ctx:BKITParser.Call_stmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BKITParser#return_stm.
    def visitReturn_stm(self, ctx:BKITParser.Return_stmContext):
        return self.visitChildren(ctx)



del BKITParser