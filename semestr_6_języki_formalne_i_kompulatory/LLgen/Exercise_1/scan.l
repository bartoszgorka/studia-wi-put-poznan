%{
  #include <stdio.h>
  int yywrap(void);
  int yylex(void);
  #include "Lpars.h"
%}
%%
 /* == rules == */
.|\n     { printf("Lexical error: unexpected character in input file\n");
           return -1;    
         }
%%
int yywrap(void) { return 1; }
