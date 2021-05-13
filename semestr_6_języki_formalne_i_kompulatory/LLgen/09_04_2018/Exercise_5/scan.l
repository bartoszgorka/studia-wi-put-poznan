%{
  #include <stdio.h>
  int yywrap(void);
  int yylex(void);
  #include "Lpars.h"
  extern union
  {
    char *text;
    int ival;
  } LLlval;
%}
%%
char                       { return KWD_CHAR; }
int                        { return KWD_INT; }
float                      { return KWD_FLOAT; }
double                     { return KWD_DOUBLE; }
struct                     { return KWD_STRUCT; }
union                      { return KWD_UNION; }
[_a-zA-Z][_a-zA-Z0-9]*     { LLlval.text = strdup(yytext);
                             return IDENT;
                           }
[0-9]+                     { LLlval.ival = atoi(yytext);
                             return INT_NUM;
                           }
\*                         { return '*'; }
,                          { return ','; }
;                          { return ';'; }
\[                         { return '['; }
\]                         { return ']'; }
\{                         { return '{'; }
\(                         { return '('; }
\)                         { return ')'; }
\}                         { return '}'; }
[ \t\n]                    { ; }
%%
int yywrap(void) { return 1; }
