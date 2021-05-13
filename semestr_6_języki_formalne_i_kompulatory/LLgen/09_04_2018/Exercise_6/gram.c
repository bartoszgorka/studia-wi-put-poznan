/* LLgen generated code from source gram.g */
#include "Lpars.h"
#define LL_LEXI yylex
#define LLNOFIRSTS
#if __STDC__ || __cplusplus
#define LL_ANSI_C 1
#endif
#define LL_LEXI yylex
/* $Id: incl,v 2.13 1997/02/21 15:44:09 ceriel Exp $ */
#ifdef LL_DEBUG
#include <assert.h>
#include <stdio.h>
#define LL_assert(x)	assert(x)
#else
#define LL_assert(x)	/* nothing */
#endif

extern int LLsymb;

#define LL_SAFE(x)	/* Nothing */
#define LL_SSCANDONE(x)	if (LLsymb != x) LLsafeerror(x)
#define LL_SCANDONE(x)	if (LLsymb != x) LLerror(x)
#define LL_NOSCANDONE(x) LLscan(x)
#ifdef LL_FASTER
#define LLscan(x)	if ((LLsymb = LL_LEXI()) != x) LLerror(x)
#endif

extern unsigned int LLscnt[];
extern unsigned int LLtcnt[];
extern int LLcsymb;

#if LL_NON_CORR
extern int LLstartsymb;
#endif

#define LLsdecr(d)	{LL_assert(LLscnt[d] > 0); LLscnt[d]--;}
#define LLtdecr(d)	{LL_assert(LLtcnt[d] > 0); LLtcnt[d]--;}
#define LLsincr(d)	LLscnt[d]++
#define LLtincr(d)	LLtcnt[d]++

#if LL_ANSI_C
extern int LL_LEXI(void);
extern void LLread(void);
extern int LLskip(void);
extern int LLnext(int);
extern void LLerror(int);
extern void LLsafeerror(int);
extern void LLnewlevel(unsigned int *);
extern void LLoldlevel(unsigned int *);
#ifndef LL_FASTER
extern void LLscan(int);
#endif
#ifndef LLNOFIRSTS
extern int LLfirst(int, int);
#endif
#if LL_NON_CORR
extern void LLnc_recover(void);
#endif
#else /* not LL_ANSI_C */
extern LLread();
extern int LLskip();
extern int LLnext();
extern LLerror();
extern LLsafeerror();
extern LLnewlevel();
extern LLoldlevel();
#ifndef LL_FASTER
extern LLscan();
#endif
#ifndef LLNOFIRSTS
extern int LLfirst();
#endif
#if LL_NON_CORR
extern LLnc_recover();
#endif
#endif /* not LL_ANSI_C */
# line 1 "gram.g"

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
#if LL_ANSI_C
static void LL1_Decls(
# line 21 "gram.g"
int *size) ;
static void LL2_Decl(
# line 25 "gram.g"
int *size) ;
static void LL3_Type(
# line 32 "gram.g"
int *size) ;
static void LL4_IdentList(
# line 39 "gram.g"
int type_size ,int *list_size) ;
static void LL5_Decl2(
# line 28 "gram.g"
int *size) ;
static void LL6_IdentList2(
# line 44 "gram.g"
int type_size ,int *list_size) ;
static void LL7_IDENT_CHAR(
# line 50 "gram.g"
int type_size ,int *var_size) ;
static void LL8_ARRAY(
# line 55 "gram.g"
int *elements_counter) ;
#else
static LL1_Decls();
static LL2_Decl();
static LL3_Type();
static LL4_IdentList();
static LL5_Decl2();
static LL6_IdentList2();
static LL7_IDENT_CHAR();
static LL8_ARRAY();
#endif
#if LL_ANSI_C
void
#endif
LL0_Input(
#if LL_ANSI_C
void
#endif
) {
# line 18 "gram.g"
int size;
LL1_Decls(
# line 19 "gram.g"
&size);
# line 19 "gram.g"
{ printf("Global data size: %d",size); }
}
static
#if LL_ANSI_C
void
#endif
LL1_Decls(
#if LL_ANSI_C
# line 21 "gram.g"
int *size)  
#else
# line 21 "gram.g"
 size) int *size;
#endif
{
# line 21 "gram.g"
int s1;
LLsincr(0);
# line 22 "gram.g"
{ *size = 0; }
LLsdecr(0);
LLsincr(1);
for (;;) {
LL2_Decl(
# line 23 "gram.g"
&s1);
# line 23 "gram.g"
{ *size += s1; s1 = 0; }
LLread();
goto L_1;
L_1 : {switch(LLcsymb) {
case /*  EOFILE  */ 0 : ;
case /* '}' */ 12 : ;
break;
default:{int LL_1=LLnext(-3);
;if (!LL_1) {
break;
}
else if (LL_1 & 1) goto L_1;}
case /*  KWD_CHAR  */ 2 : ;
case /*  KWD_INT  */ 3 : ;
case /*  KWD_FLOAT  */ 4 : ;
case /*  KWD_DOUBLE  */ 5 : ;
case /*  KWD_STRUCT  */ 8 : ;
case /*  KWD_UNION  */ 9 : ;
continue;
}
}
LLsdecr(1);
break;
}
}
static
#if LL_ANSI_C
void
#endif
LL2_Decl(
#if LL_ANSI_C
# line 25 "gram.g"
int *size)  
#else
# line 25 "gram.g"
 size) int *size;
#endif
{
# line 25 "gram.g"
*size = 0; int type_size = 0;
LLsincr(1);
LLsincr(2);
LLtincr(10);
LL3_Type(
# line 26 "gram.g"
&type_size);
LLread();
LL4_IdentList(
# line 26 "gram.g"
type_size, size);
LLtdecr(10);
LL_SCANDONE(';');
}
static
#if LL_ANSI_C
void
#endif
LL5_Decl2(
#if LL_ANSI_C
# line 28 "gram.g"
int *size)  
#else
# line 28 "gram.g"
 size) int *size;
#endif
{
# line 28 "gram.g"
*size = 0; int type_size = 0;
LLsincr(1);
LLsincr(2);
LLtincr(10);
LL3_Type(
# line 29 "gram.g"
&type_size);
LL6_IdentList2(
# line 29 "gram.g"
type_size, size);
LLtdecr(10);
LL_SCANDONE(';');
}
static
#if LL_ANSI_C
void
#endif
LL3_Type(
#if LL_ANSI_C
# line 32 "gram.g"
int *size)  
#else
# line 32 "gram.g"
 size) int *size;
#endif
{
# line 32 "gram.g"
 int value = 0; int max_value = 0; 
goto L_2; /* so that the label is used for certain */
L_2: ;
switch(LLcsymb) {
case /*  KWD_CHAR  */ 2 : ;
goto L_3;
L_3: ;
LLsdecr(1);
LL_SSCANDONE(KWD_CHAR);
# line 32 "gram.g"
{ *size = 1; }
break;
default: if (LLskip()) goto L_2;
goto L_3;
case /*  KWD_INT  */ 3 : ;
LLsdecr(1);
LL_SAFE(KWD_INT);
# line 33 "gram.g"
{ *size = 4; }
break;
case /*  KWD_FLOAT  */ 4 : ;
LLsdecr(1);
LL_SAFE(KWD_FLOAT);
# line 34 "gram.g"
{ *size = 6; }
break;
case /*  KWD_DOUBLE  */ 5 : ;
LLsdecr(1);
LL_SAFE(KWD_DOUBLE);
# line 35 "gram.g"
{ *size = 8; }
break;
case /*  KWD_STRUCT  */ 8 : ;
LLsdecr(1);
LLsincr(0);
LLtincr(12);
LL_SAFE(KWD_STRUCT);
LL_NOSCANDONE('{');
LLread();
LLsdecr(0);
LL1_Decls(
# line 36 "gram.g"
&value);
LLtdecr(12);
LL_SCANDONE('}');
# line 36 "gram.g"
{ *size = value; }
break;
case /*  KWD_UNION  */ 9 : ;
LLsdecr(1);
LLsincr(0);
LLtincr(12);
LL_SAFE(KWD_UNION);
LL_NOSCANDONE('{');
LLread();
LLsdecr(0);
LLsincr(1);
for (;;) {
LL5_Decl2(
# line 37 "gram.g"
&value);
# line 37 "gram.g"
{ if(value >= max_value) { max_value = value; value = 0; } printf("%d\n", max_value); }
LLread();
goto L_4;
L_4 : {switch(LLcsymb) {
case /* '}' */ 12 : ;
break;
default:{int LL_2=LLnext(-3);
;if (!LL_2) {
break;
}
else if (LL_2 & 1) goto L_4;}
case /*  KWD_CHAR  */ 2 : ;
case /*  KWD_INT  */ 3 : ;
case /*  KWD_FLOAT  */ 4 : ;
case /*  KWD_DOUBLE  */ 5 : ;
case /*  KWD_STRUCT  */ 8 : ;
case /*  KWD_UNION  */ 9 : ;
continue;
}
}
LLsdecr(1);
break;
}
LLtdecr(12);
LL_SSCANDONE('}');
# line 37 "gram.g"
{ *size = max_value; }
break;
}
}
static
#if LL_ANSI_C
void
#endif
LL4_IdentList(
#if LL_ANSI_C
# line 39 "gram.g"
int type_size ,int *list_size)  
#else
# line 39 "gram.g"
 type_size,list_size) int type_size; int *list_size;
#endif
{
goto L_2; /* so that the label is used for certain */
L_2: ;
switch(LLcsymb) {
case /*  IDENT  */ 6 : ;
case /* '*' */ 14 : ;
LLsdecr(2);
LLsincr(3);
LLtincr(13);
LL7_IDENT_CHAR(
# line 40 "gram.g"
type_size, list_size);
for (;;) {
goto L_4;
L_4 : {switch(LLcsymb) {
case /* ';' */ 10 : ;
break;
default:{int LL_3=LLnext(44);
;if (!LL_3) {
break;
}
else if (LL_3 & 1) goto L_4;}
case /* ',' */ 13 : ;
LLsincr(3);
LL_SAFE(',');
LLread();
LL7_IDENT_CHAR(
# line 40 "gram.g"
type_size, list_size);
continue;
}
}
LLtdecr(13);
break;
}
break;
case /* ';' */ 10 : ;
goto L_3;
L_3: ;
LLsdecr(2);
break;
default: if (LLskip()) goto L_2;
goto L_3;
}
}
static
#if LL_ANSI_C
void
#endif
LL6_IdentList2(
#if LL_ANSI_C
# line 44 "gram.g"
int type_size ,int *list_size)  
#else
# line 44 "gram.g"
 type_size,list_size) int type_size; int *list_size;
#endif
{
# line 44 "gram.g"
 int max_value = 0; 
LLread();
goto L_2; /* so that the label is used for certain */
L_2: ;
switch(LLcsymb) {
case /*  IDENT  */ 6 : ;
case /* '*' */ 14 : ;
LLsdecr(2);
LLsincr(3);
LLtincr(13);
LL7_IDENT_CHAR(
# line 45 "gram.g"
type_size, list_size);
# line 45 "gram.g"
{ max_value = *list_size; }
for (;;) {
goto L_4;
L_4 : {switch(LLcsymb) {
case /* ';' */ 10 : ;
break;
default:{int LL_4=LLnext(44);
;if (!LL_4) {
break;
}
else if (LL_4 & 1) goto L_4;}
case /* ',' */ 13 : ;
LLsincr(3);
LL_SAFE(',');
# line 45 "gram.g"
{ *list_size = 0;}
LLread();
LL7_IDENT_CHAR(
# line 45 "gram.g"
type_size, list_size);
# line 45 "gram.g"
{ if(*list_size >= max_value) { max_value = *list_size; }}
continue;
}
}
LLtdecr(13);
break;
}
break;
case /* ';' */ 10 : ;
goto L_3;
L_3: ;
LLsdecr(2);
break;
default: if (LLskip()) goto L_2;
goto L_3;
}
}
static
#if LL_ANSI_C
void
#endif
LL7_IDENT_CHAR(
#if LL_ANSI_C
# line 50 "gram.g"
int type_size ,int *var_size)  
#else
# line 50 "gram.g"
 type_size,var_size) int type_size; int *var_size;
#endif
{
# line 50 "gram.g"
 int elements_counter = 1;
goto L_2; /* so that the label is used for certain */
L_2: ;
switch(LLcsymb) {
case /* '*' */ 14 : ;
LLsdecr(3);
LLtincr(14);
LLtincr(6);
LLtincr(15);
for (;;) {
LL_SAFE('*');
LLread();
goto L_4;
L_4 : {switch(LLcsymb) {
case /*  IDENT  */ 6 : ;
break;
default:{int LL_5=LLnext(42);
;if (!LL_5) {
break;
}
else if (LL_5 & 1) goto L_4;}
case /* '*' */ 14 : ;
continue;
}
}
LLtdecr(14);
break;
}
LLtdecr(6);
LL_SSCANDONE(IDENT);
LLread();
for (;;) {
goto L_5;
L_5 : {switch(LLcsymb) {
case /* ';' */ 10 : ;
case /* ',' */ 13 : ;
break;
default:{int LL_6=LLnext(91);
;if (!LL_6) {
break;
}
else if (LL_6 & 1) goto L_5;}
case /* '[' */ 15 : ;
LL8_ARRAY(
# line 51 "gram.g"
&elements_counter);
LLread();
continue;
}
}
LLtdecr(15);
break;
}
# line 51 "gram.g"
{ *var_size += elements_counter * 4; }
break;
case /*  IDENT  */ 6 : ;
goto L_3;
L_3: ;
LLsdecr(3);
LLtincr(15);
LL_SSCANDONE(IDENT);
LLread();
for (;;) {
goto L_6;
L_6 : {switch(LLcsymb) {
case /* ';' */ 10 : ;
case /* ',' */ 13 : ;
break;
default:{int LL_7=LLnext(91);
;if (!LL_7) {
break;
}
else if (LL_7 & 1) goto L_6;}
case /* '[' */ 15 : ;
LL8_ARRAY(
# line 52 "gram.g"
&elements_counter);
LLread();
continue;
}
}
LLtdecr(15);
break;
}
# line 52 "gram.g"
{*var_size += elements_counter * type_size; }
break;
default: if (LLskip()) goto L_2;
goto L_3;
}
}
static
#if LL_ANSI_C
void
#endif
LL8_ARRAY(
#if LL_ANSI_C
# line 55 "gram.g"
int *elements_counter)  
#else
# line 55 "gram.g"
 elements_counter) int *elements_counter;
#endif
{
LLtincr(16);
LL_SAFE('[');
LL_NOSCANDONE(INT_NUM);
LLtdecr(16);
LL_NOSCANDONE(']');
# line 56 "gram.g"
{ *elements_counter *= LLlval.ival; }
}

# line 59 "gram.g"

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

