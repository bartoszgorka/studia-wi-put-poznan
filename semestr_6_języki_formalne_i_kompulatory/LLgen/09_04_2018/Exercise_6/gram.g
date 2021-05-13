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
Decl2(int *size) {*size = 0; int type_size = 0;}
  : Type(&type_size) IdentList2(type_size, size) ';'
  ;

Type(int *size) { int value = 0; int max_value = 0; } : KWD_CHAR { *size = 1; }
                | KWD_INT { *size = 4; }
                | KWD_FLOAT { *size = 6; }
                | KWD_DOUBLE { *size = 8; }
                | KWD_STRUCT '{' Decls(&value) '}' { *size = value; }
                | KWD_UNION '{' [ Decl2(&value) { if(value >= max_value) { max_value = value; value = 0; } printf("%d\n", max_value); } ]+ '}' { *size = max_value; }
                ;
IdentList(int type_size; int *list_size)
  : IDENT_CHAR(type_size, list_size) [ ',' IDENT_CHAR(type_size, list_size) ]*
  |
  ;

IdentList2(int type_size; int *list_size) { int max_value = 0; }
  : IDENT_CHAR(type_size, list_size) { max_value = *list_size; } [ ',' { *list_size = 0;} IDENT_CHAR(type_size, list_size) { if(*list_size >= max_value) { max_value = *list_size; }} ]*
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
