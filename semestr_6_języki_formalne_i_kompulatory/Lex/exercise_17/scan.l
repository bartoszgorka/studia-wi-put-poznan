%{
  #include <stdio.h>
  int yywrap(void);
  int yylex(void);

  int counter_if = 0;
  int counter_while = 0;
  int comment_depth = 0;
%}
%s LINE_COMMENT
%s COMMENT
%%

<INITIAL>\/\/     { BEGIN LINE_COMMENT; }
<LINE_COMMENT>\n  { BEGIN INITIAL; }

\/\*              { comment_depth++; BEGIN COMMENT; }
<COMMENT>\*\/     { comment_depth--; if(comment_depth == 0) BEGIN INITIAL; }

<INITIAL>^(if\/\*)|([\ ]+if\/\*)            { counter_if++; comment_depth++; BEGIN COMMENT; }
<INITIAL>^(if\/\/)|([\ ]+if\/\/)            { counter_if++; BEGIN LINE_COMMENT; }
<INITIAL>^(if[\n\(\ ]+)|([\ ]+if[\n\(\ ]+)  { counter_if++; }

<<EOF>> {
  printf("Instrukcji \"if\": %d \n", counter_if);
  printf("Instrukcji \"while\": %d \n", counter_while);
  printf("Łącznie instrukcji \"if\" i \"while\": %d \n", counter_if + counter_while);
  return 1;
}

.|\n ;

%%
int yywrap(void) { return 1; }
int main() { return yylex(); }
