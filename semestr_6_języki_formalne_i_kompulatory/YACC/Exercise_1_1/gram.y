%{
  int yylex(void);
  void yyerror(const char *,...);
  int yyparse(void);
  extern int yylineno;
#include <stdio.h>
#include <stdlib.h>
%}
%union {
  int ival;
  char *text;
}
%token KWD_CHAR KWD_INT KWD_FLOAT KWD_DOUBLE IDENT INT_NUM KWD_STRUCT KWD_UNION
%type <ival> Type Decls Ide
%type <text> IDENT
%%

Input : Decls               {
                              printf("Global data size: %d", $1);
                            }
      ;
Decls : Type Ide ';'        { $$ = $2;         }
      | Decls Type Ide ';'  { $$ = $1 + $3;  }
      ;
Ide   : '*' IDENT           { $$ = 11; printf("%d\n", $$); }
      | IDENT           { $$ = $<ival>0;  printf("%d\n", $<ival>0);      }
      | IDENT ',' Ide   { $$ = $<ival>0 + $3; printf("A %d %d\n", $<ival>0, $3); }
      ;
Type  : KWD_CHAR    { $$ = 1; }
      | KWD_INT     { $$ = 4; }
      | KWD_FLOAT   { $$ = 6; }
      | KWD_DOUBLE  { $$ = 8; }
      |             { printf("syntax error in line %d\n", yylineno); exit(-1); }
      ;

%%
void yyerror(const char *fmt, ...) {
  printf("%s in line %d\n", fmt, yylineno);
}
int main() {
  return yyparse();
}
