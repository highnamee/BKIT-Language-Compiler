// 1810340
grammar BKIT;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()

    if tk == self.UNCLOSE_STRING:
        y = str(result.text)
        if y[-1] == '\n' or y[-1] == '\r':
            raise UncloseString(y[1:-1])
        else:
            raise UncloseString(y[1:])

    elif tk == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(result.text[1:])

    elif tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)

    elif tk == self.UNTERMINATED_COMMENT:
        raise UnterminatedComment()
    else:
        return result;
}

options{
	language=Python3;
}

/*-----------------------------------------------------------------------*/
/*------------------------------- Parser --------------------------------*/
/*-----------------------------------------------------------------------*/

program         : var_declare* func_declare* EOF;

var_declare     : VAR COLON (var_id | var_init) (CM (var_id | var_init))* SEMI;
var_init        : var_id ASSIGN all_literal;
var_id          : ID (LSB INTLIT RSB)* ;

all_literal     : (INTLIT | FLOATLIT | BOOLEANLIT | STRINGLIT | array_literal) ;
array_literal   : LB (all_literal (CM all_literal)*)? RB ;

func_declare    : func_begin func_body ;
func_begin      : (FUNC COLON ID) (PARAM COLON var_id (CM var_id)*)? ;
func_body       : BODY COLON var_declare* statement* END_BODY DOT;

/*------------------------------- Expression --------------------------------*/
expression          : exp1 RELATIONAL exp1 | exp1 ;
exp1                : exp1 (BOOL_CONJ | BOOL_DISJ) exp2 | exp2 ;
exp2                : exp2 (ADD | SUB | F_ADD | F_SUB) exp3 | exp3 ;
exp3                : exp3 (MUL | DIV | F_MUL | F_DIV | REMAINDER) exp4 | exp4 ;
exp4                : BOOL_NEGA exp4 | exp5 ;
exp5                : (SUB | F_SUB) exp5 | exp6 ;
exp6                : exp6 index_operator | operand;

operand             : ID | all_literal | func_call_exp | LP expression RP ;
index_operator      : (LSB expression RSB)+ ;

func_call_exp       : ID LP (expression (CM expression)*)? RP ; // | buil_in_func_call | type_coer;
//buil_in_func_call   : 'printLn' LP RP
//                    | 'print' LP expression RP
//                    | 'printStrLn' LP expression RP
//                    | 'read' LP RP ;
//
//type_coer           : 'int_of_ﬂoat' LP expression RP
//                    | 'ﬂoat_to_int' LP expression RP
//                    | 'int_of_string' LP expression RP
//                    | 'string_of_int' LP expression RP
//                    | 'ﬂoat_of_string' LP expression RP
//                    | 'string_of_ﬂoat' LP expression RP
//                    | 'bool_of_string' LP expression RP
//                    | 'string_of_bool' LP expression RP ;

/*------------------------------- Statement --------------------------------*/
//statement_list      : var_declare* statement* ;
statement           : assign_stm | if_stm | for_stm | while_stm | dowhile_stm | call_stm | return_stm | break_stm | continue_stm ;

// Var declare => var_declare
//var_declare_stm     : VAR COLON (var_id_stm | var_init_stm) (CM (var_id_stm | var_init_stm))* SEMI;
var_init_stm        : var_id_stm ASSIGN expression;
var_id_stm          : exp6;

// Assignment Statement
assign_stm          : var_init_stm SEMI;

// If Statement
if_stm              : (IF expression THEN var_declare* statement*) (ELSEIF expression THEN var_declare* statement*)* (ELSE var_declare* statement*)? ENDIF DOT;

// For Statement
for_stm             : FOR LP (ID ASSIGN expression) CM expression CM expression RP DO var_declare* statement* ENDFOR DOT;

// While Statement
while_stm           : WHILE expression DO var_declare* statement* ENDWHILE DOT;

// Do-while Statement
dowhile_stm         : DO var_declare* statement* WHILE expression ENDDO DOT;

// Break Statement
break_stm           : BREAK SEMI ;

// Continue Statement
continue_stm        : CONTINUE SEMI ;

// Call Statement
call_stm            : func_call_exp SEMI ;

// Return Statement
return_stm          : RETURN expression? SEMI ;


/*-----------------------------------------------------------------------*/
/*------------------------------- Lexer ---------------------------------*/
/*-----------------------------------------------------------------------*/

// Separators
CM      : ',' ;
SEMI    : ';' ;
COLON   : ':' ;
LB      : '{' ;
RB      : '}' ;
LP      : '(' ;
RP      : ')' ;
LSB     : '[' ;
RSB     : ']' ;
ASSIGN  : '=' ;
DOT     : '.' ;


// Keywords
VAR         : 'Var' ;
FUNC        : 'Function' ;
PARAM       : 'Parameter' ;
BODY        : 'Body' ;
END_BODY    : 'EndBody' ;
IF          : 'If' ;
ELSEIF      : 'ElseIf' ;
THEN        : 'Then' ;
ELSE        : 'Else' ;
ENDIF       : 'EndIf' ;
FOR         : 'For' ;
ENDFOR      : 'EndFor' ;
DO          : 'Do' ;
ENDDO       : 'EndDo' ;
BREAK       : 'Break' ;
WHILE       : 'While' ;
ENDWHILE    : 'EndWhile' ;
CONTINUE    : 'Continue' ;
RETURN      : 'Return' ;

// Operators
//INT_OPERATER        : ADD | SUB | MUL | DIV | REMAINDER | EQUAL | NOT_EQUAL | LESS_THAN | GREATER_THAN | LESS_THAN_EQ | GREATER_THAN_EQ ;
//FLOAT_OPERATER      : F_ADD | F_SUB | F_MUL | F_DIV | F_NOT_EQUAL | F_LESS_THAN | F_GREATER_THAN | F_LESS_THAN_EQ | F_GREATER_THAN_EQ ;
//BOOL_OPERATOR       : BOOL_NEGA | BOOL_CONJ | BOOL_DISJ ;
RELATIONAL          : EQUAL | NOT_EQUAL | LESS_THAN | GREATER_THAN | LESS_THAN_EQ | GREATER_THAN_EQ | F_NOT_EQUAL | F_LESS_THAN
                    | F_GREATER_THAN | F_LESS_THAN_EQ | F_GREATER_THAN_EQ ;

ADD                 : '+' ;
SUB                 : '-' ;
MUL                 : '*' ;
DIV                 : '\\' ;
REMAINDER           : '%' ;
F_ADD               : '+.' ;
F_SUB               : '-.' ;
F_MUL               : '*.' ;
F_DIV               : '\\.' ;

BOOL_NEGA           : '!' ;
BOOL_CONJ           : '&&' ;
BOOL_DISJ           : '||' ;

EQUAL               : '==' ;
NOT_EQUAL           : '!=' ;
LESS_THAN           : '<' ;
GREATER_THAN        : '>' ;
LESS_THAN_EQ        : '<=' ;
GREATER_THAN_EQ     : '>=' ;
F_NOT_EQUAL         : '=/=' ;
F_LESS_THAN         : '<.' ;
F_GREATER_THAN      : '>.' ;
F_LESS_THAN_EQ      : '<=.' ;
F_GREATER_THAN_EQ   : '>=.' ;


// Identifers
ID      : [a-z] [a-z_A-Z0-9]* ;

// Integer literal
INTLIT      : DEC | HEX | OTC ;
DEC         : [1-9][0-9]* | '0' ;
HEX         : '0'[xX][1-9A-F][0-9A-F]* ;
OTC         : '0'[oO][1-7][0-7]* ;

// Float literal
FLOATLIT            : DEC '.' [0-9]* EXP? | DEC EXP ;
fragment EXP        : [Ee][+-]?[0-9]+ ;

// Boolean literal
BOOLEANLIT      : 'True' | 'False' ;

// String literal
STRINGLIT                   : '"' STRING_CHAR* '"'
{
    y = str(self.text)
    self.text = y[1:-1]
};
fragment STRING_CHAR        : ~[\n\r'"\\] | ESCAPE | SINGLEQUOTE | DOUBLEQUOTE ;
fragment ESCAPE             : '\\' [bfntr\\] ;
fragment ILLEGAL_ESC        : '\\' ~[btnfr'\\] | '\'' ~["];
fragment SINGLEQUOTE        : '\\\'' ;
fragment DOUBLEQUOTE        : '\'"' ;

// Array literal
fragment LITERALS  : INTLIT | FLOATLIT | BOOLEANLIT | STRINGLIT;

// Skip tokens
WS                 : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
BLOCK_CMT          : '**' (~('*') | '*'(~('*')))* '**' -> skip;

ERROR_CHAR: .;
UNCLOSE_STRING: '"' STRING_CHAR* ([\n\r] |EOF);
ILLEGAL_ESCAPE: '"' STRING_CHAR* ILLEGAL_ESC ;
UNTERMINATED_COMMENT: '**' (~('*') | '*'(~('*')))* '*'? EOF;