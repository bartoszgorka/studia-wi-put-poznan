%{
  int yylex(void);
  void yyerror(const char *,...);
  int yyparse(void);
  extern int yylineno;
#include <stdio.h>
#include <stdlib.h>
%}
%union
{
  int ival;
  char *text;
}
%token KWD_CHAR KWD_INT KWD_FLOAT KWD_DOUBLE IDENT INT_NUM KWD_STRUCT KWD_UNION
%%
Input :
      ;
%%
void yyerror(const char *fmt, ...)
{
  printf("%s in line %d\n", fmt, yylineno);
}
int main() { return yyparse(); }
