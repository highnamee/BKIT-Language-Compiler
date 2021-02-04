from BKITVisitor import BKITVisitor
from BKITParser import BKITParser
from AST import *


class ASTGeneration(BKITVisitor):

    # program         : var_declare* func_declare* EOF;
    def visitProgram(self, ctx: BKITParser.ProgramContext):
        var_declare_list = [x for item in ctx.var_declare() for x in self.visitVarDecl(item)]
        func_declare_list = [x for item in ctx.func_declare() for x in self.visitFuncDecl(item)]
        return Program(var_declare_list + func_declare_list)

    # -------------------------------------------------------------- #
    # -------------------VAR + FUNCTION VISITOR--------------------- #
    # -------------------------------------------------------------- #

    # var_declare     : VAR COLON var_declare_item (CM var_declare_item)* SEMI;
    def visitVarDecl(self, ctx: BKITParser.ProgramContext):
        if ctx.CM():
            return [self.visitVarDeclItem(item) for item in ctx.var_declare_item()]
        else:
            return [self.visitVarDeclItem(ctx.var_declare_item(0))]

    # var_declare_item: (var_id | var_init);
    def visitVarDeclItem(self, ctx: BKITParser.ProgramContext):
        if ctx.var_id():
            return self.visitVarId(ctx.var_id())
        else:
            return self.visitVarInit(ctx.var_init())

    # var_id          : ID (LSB INTLIT RSB)* ;
    def visitVarId(self, ctx: BKITParser.ProgramContext):
        int_list = [self.visitInt(item) for item in ctx.INTLIT()] if ctx.INTLIT() else []
        return VarDecl(self.visitId(ctx.ID()), int_list, None)

    # var_init        : ID (LSB INTLIT RSB)* ASSIGN all_literal;
    def visitVarInit(self, ctx: BKITParser.ProgramContext):
        int_list = [self.visitInt(item) for item in ctx.INTLIT()] if ctx.INTLIT() else []
        return VarDecl(self.visitId(ctx.ID()), int_list, self.visitAllLiteral(ctx.all_literal()))

    # func_declare    : (FUNC COLON ID) (PARAM COLON var_id (CM var_id)*)? BODY COLON statement_list END_BODY DOT ;
    def visitFuncDecl(self, ctx: BKITParser.ProgramContext):
        param_list = [self.visitVarId(item) for item in ctx.var_id()]
        statements = self.visitStatementList(ctx.statement_list())
        return [FuncDecl(self.visitId(ctx.ID()), param_list, statements)]

    # -------------------------------------------------------------- #
    # ---------------------EXPRESSION VISITOR----------------------- #
    # -------------------------------------------------------------- #

    # expression          : exp1 RELATIONAL exp1 | exp1 ;
    def visitExpression(self, ctx: BKITParser.ProgramContext):
        if ctx.RELATIONAL():
            return BinaryOp(ctx.RELATIONAL().getText(), self.visitExp1(ctx.exp1(0)), self.visitExp1(ctx.exp1(1)))
        else:
            return self.visitExp1(ctx.exp1(0))

    # exp1                : exp1 (BOOL_CONJ | BOOL_DISJ) exp2 | exp2 ;
    def visitExp1(self, ctx: BKITParser.ProgramContext):
        if ctx.exp1():
            return BinaryOp(ctx.getChild(1).getText(), self.visitExp1(ctx.exp1()), self.visitExp2(ctx.exp2()))
        else:
            return self.visitExp2(ctx.exp2())

    # exp2                : exp2 (ADD | SUB | F_ADD | F_SUB) exp3 | exp3 ;
    def visitExp2(self, ctx: BKITParser.ProgramContext):
        if ctx.exp2():
            return BinaryOp(ctx.getChild(1).getText(), self.visitExp2(ctx.exp2()), self.visitExp3(ctx.exp3()))
        else:
            return self.visitExp3(ctx.exp3())

    # exp3                : exp3 (MUL | DIV | F_MUL | F_DIV | REMAINDER) exp4 | exp4 ;
    def visitExp3(self, ctx: BKITParser.ProgramContext):
        if ctx.exp3():
            return BinaryOp(ctx.getChild(1).getText(), self.visitExp3(ctx.exp3()), self.visitExp4(ctx.exp4()))
        else:
            return self.visitExp4(ctx.exp4())

    # exp4                : BOOL_NEGA exp4 | exp5 ;
    def visitExp4(self, ctx: BKITParser.ProgramContext):
        if ctx.exp4():
            return UnaryOp(ctx.getChild(0).getText(), self.visitExp4(ctx.exp4()))
        else:
            return self.visitExp5(ctx.exp5())

    # exp5                : (SUB | F_SUB) exp5 | exp6 ;
    def visitExp5(self, ctx: BKITParser.ProgramContext):
        if ctx.exp5():
            return UnaryOp(ctx.getChild(0).getText(), self.visitExp5(ctx.exp5()))
        else:
            return self.visitExp6(ctx.exp6())

    # exp6                : exp6 (LSB expression RSB)+ | operand;
    def visitExp6(self, ctx: BKITParser.ProgramContext):
        if ctx.exp6():
            expression_list = [self.visitExpression(item) for item in ctx.expression()]
            return ArrayCell(self.visitExp6(ctx.exp6()), expression_list)
        else:
            return self.visitOperand(ctx.operand())

    # operand             : ID | all_literal | func_call_exp | LP expression RP ;
    def visitOperand(self, ctx: BKITParser.ProgramContext):
        if ctx.ID():
            return self.visitId(ctx.ID())
        if ctx.all_literal():
            return self.visitAllLiteral(ctx.all_literal())
        if ctx.func_call_exp():
            return self.visitFuncCallExp(ctx.func_call_exp())
        return self.visitExpression(ctx.expression())

    # func_call_exp       : ID LP (expression (CM expression)*)? RP ;
    def visitFuncCallExp(self, ctx: BKITParser.ProgramContext):
        expression_list = [self.visitExpression(item) for item in ctx.expression()]
        return CallExpr(self.visitId(ctx.ID()), expression_list)

    # -------------------------------------------------------------- #
    # ---------------------STATEMENT VISITOR------------------------ #
    # -------------------------------------------------------------- #

    # statement           : assign_stm | if_stm | for_stm | while_stm | dowhile_stm | call_stm | return_stm | break_stm | continue_stm ;
    def visitStatement(self, ctx: BKITParser.ProgramContext):
        if ctx.assign_stm():
            return self.visitAssign(ctx.assign_stm())
        if ctx.if_stm():
            return self.visitIf(ctx.if_stm())
        if ctx.for_stm():
            return self.visitFor(ctx.for_stm())
        if ctx.while_stm():
            return self.visitWhile(ctx.while_stm())
        if ctx.dowhile_stm():
            return self.visitDowhile(ctx.dowhile_stm())
        if ctx.call_stm():
            return self.visitCallStmt(ctx.call_stm())
        if ctx.return_stm():
            return self.visitReturn(ctx.return_stm())
        if ctx.break_stm():
            return self.visitBreak(ctx.break_stm())
        if ctx.continue_stm():
            return self.visitContinue(ctx.continue_stm())

    # lhs                 : (ID | func_call_exp) (LSB expression RSB)+ | ID;
    def visitLhs(self, ctx: BKITParser.ProgramContext):
        if ctx.expression():
            identify = self.visitId(ctx.ID()) if ctx.ID() else self.visitFuncCallExp(ctx.func_call_exp())
            expression_list = [self.visitExpression(item) for item in ctx.expression()]
            return ArrayCell(identify, expression_list)
        else:
            return self.visitId(ctx.ID())

    # assign_stm          : lhs ASSIGN expression SEMI;
    def visitAssign(self, ctx: BKITParser.ProgramContext):
        lhs = self.visitLhs(ctx.lhs())
        return Assign(lhs, self.visitExpression(ctx.expression()))

    # statement_list      : var_declare* statement* ;
    def visitStatementList(self, ctx: BKITParser.ProgramContext):
        var_declare_list = [x for item in ctx.var_declare() for x in self.visitVarDecl(item)]
        statement_list = [self.visitStatement(item) for item in ctx.statement()]
        return (var_declare_list, statement_list)

    # if_stm              : (IF expression THEN statement_list) (ELSEIF expression THEN statement_list)* (ELSE statement_list)? ENDIF DOT;
    def visitIf(self, ctx: BKITParser.ProgramContext):
        expression_list = [self.visitExpression(item) for item in ctx.expression()]
        statements = [self.visitStatementList(item) for item in ctx.statement_list()]
        if_statement = list(map(lambda x, y: (x, y[0], y[1]), expression_list, statements))
        else_statement = statements[-1] if ctx.ELSE() else ([], [])
        return If(if_statement, else_statement)

    # for_stm             : FOR LP (ID ASSIGN expression) CM expression CM expression RP DO statement_list ENDFOR DOT;
    def visitFor(self, ctx: BKITParser.ProgramContext):
        expression_list = [self.visitExpression(item) for item in ctx.expression()]
        statements = self.visitStatementList(ctx.statement_list())
        return For(self.visitId(ctx.ID()), expression_list[0], expression_list[1], expression_list[2], statements)

    # continue_stm        : CONTINUE SEMI ;
    def visitContinue(self, ctx: BKITParser.ProgramContext):
        return Continue()

    # break_stm           : BREAK SEMI ;
    def visitBreak(self, ctx: BKITParser.ProgramContext):
        return Break()

    # return_stm          : RETURN expression? SEMI ;
    def visitReturn(self, ctx: BKITParser.ProgramContext):
        expression = self.visitExpression(ctx.expression()) if ctx.expression() else None
        return Return(expression)

    # dowhile_stm         : DO statement_list WHILE expression ENDDO DOT;
    def visitDowhile(self, ctx: BKITParser.ProgramContext):
        return Dowhile(self.visitStatementList(ctx.statement_list()), self.visitExpression(ctx.expression()))

    # while_stm           : WHILE expression DO statement_list ENDWHILE DOT;
    def visitWhile(self, ctx: BKITParser.ProgramContext):
        return While(self.visitExpression(ctx.expression()), self.visitStatementList(ctx.statement_list()))

    # call_stm            : ID LP (expression (CM expression)*)? RP SEMI ;
    def visitCallStmt(self, ctx: BKITParser.ProgramContext):
        expression_list = [self.visitExpression(item) for item in ctx.expression()]
        return CallStmt(self.visitId(ctx.ID()), expression_list)

    # -------------------------------------------------------------- #
    # ---------------------ALL LITERAL VISITOR---------------------- #
    # -------------------------------------------------------------- #

    # all_literal: (INTLIT | FLOATLIT | BOOLEANLIT | STRINGLIT | array_literal);
    def visitAllLiteral(self, ctx: BKITParser.ProgramContext):
        if ctx.INTLIT():
            return self.visitIntLiteral(ctx.INTLIT())
        if ctx.FLOATLIT():
            return self.visitFloatLiteral(ctx.FLOATLIT())
        if ctx.BOOLEANLIT():
            return self.visitBooleanLiteral(ctx.BOOLEANLIT())
        if ctx.STRINGLIT():
            return self.visitStringLiteral((ctx.STRINGLIT()))
        if ctx.array_literal():
            return self.visitArrayLiteral(ctx.array_literal())

    def visitIntLiteral(self, ctx: BKITParser.ProgramContext):
        # int_text = str(ctx.getText())
        # if 'x' in int_text  or 'X' in int_text:
        #     return IntLiteral(int(int_text,16))
        # if 'o' in int_text or 'O' in int_text:
        #     return IntLiteral(int(int_text, 8))
        # return IntLiteral(int(int_text))
        return IntLiteral(self.visitInt(ctx))

    def visitInt(self, ctx: BKITParser.ProgramContext):
        int_text = str(ctx.getText())
        if 'x' in int_text or 'X' in int_text:
            return int(int_text, 16)
        if 'o' in int_text or 'O' in int_text:
            return int(int_text, 8)
        return int(int_text)

    def visitFloatLiteral(self, ctx: BKITParser.ProgramContext):
        return FloatLiteral(float(ctx.getText()))

    def visitBooleanLiteral(self, ctx: BKITParser.ProgramContext):
        return BooleanLiteral(True) if ctx.getText() == "True" else BooleanLiteral(False)

    def visitStringLiteral(self, ctx: BKITParser.ProgramContext):
        return StringLiteral(ctx.getText())

    # array_literal   : LB (all_literal (CM all_literal)*)? RB ;
    def visitArrayLiteral(self, ctx: BKITParser.ProgramContext):
        return ArrayLiteral([self.visitAllLiteral(x) for x in ctx.all_literal()])

    def visitId(self, ctx: BKITParser.ProgramContext):
        return Id(ctx.getText())