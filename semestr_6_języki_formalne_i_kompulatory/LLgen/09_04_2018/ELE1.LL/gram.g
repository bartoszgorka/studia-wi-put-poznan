{
  #include <stdio.h>
  #include <stdlib.h>
  #include <ctype.h>
  extern int yylineno;
  void parse(void);
  union
  {
    char *text;
    int ival;
  } LLlval;
}

%token KWD_CHAR, KWD_INT, KWD_FLOAT, KWD_DOUBLE, IDENT, INT_NUM, KWD_STRUCT, KWD_UNION ;

%start parse, Input ;

Input :
      ;
{
  int main()
  {
    parse();
    return 0;
  }

  void LLmessage(int tk)
  {
    printf("syntax error in line %d\n",yylineno);
    exit(1);
  }
}
