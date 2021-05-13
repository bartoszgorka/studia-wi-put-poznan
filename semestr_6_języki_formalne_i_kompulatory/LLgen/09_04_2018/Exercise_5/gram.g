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

%token KWD_CHAR, KWD_INT, KWD_FLOAT, KWD_DOUBLE, IDENT, INT_NUM, KWD_STRUCT, KWD_UNION;

%start parse, Input;

Input {int size;}
  : Decls(&size) { printf("Global data size: %d",size); }
  ;
Decls(int *size) {int s1;}
  : { *size = 0; }
    [ Decl(&s1) { *size += s1; s1 = 0; } ] +
  ;
Decl(int *size) {*size = 0; int type_size = 0;}
  : Type(&type_size) IdentList(type_size, size) ';'
  ;

Type(int *size) { int value = 0; } : KWD_CHAR { *size = 1; }
                | KWD_INT { *size = 4; }
                | KWD_FLOAT { *size = 6; }
                | KWD_DOUBLE { *size = 8; }
                | KWD_STRUCT '{' Decls(&value) '}' { *size = value; }
                ;
IdentList(int type_size; int *list_size)
  : IDENT_CHAR(type_size, list_size) [ ',' IDENT_CHAR(type_size, list_size) ]*
  |
  ;

IDENT_CHAR(int type_size; int *var_size) { int elements_counter = 1;}
  : '*'+ IDENT ARRAY(&elements_counter)* { *var_size += elements_counter * 4; }
  | IDENT ARRAY(&elements_counter)* {*var_size += elements_counter * type_size; }
  ;

ARRAY(int *elements_counter)
  : '[' INT_NUM ']' { *elements_counter *= LLlval.ival; }
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
