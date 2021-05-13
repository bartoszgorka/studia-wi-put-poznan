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
# line 29 "gram.g"
int *size) ;
static void LL4_IdentList(
# line 34 "gram.g"
int type_size ,int *list_size) ;
static void LL5_IDENT_CHAR(
# line 38 "gram.g"
int type_size ,int *var_size) ;
#else
static LL1_Decls();
static LL2_Decl();
static LL3_Type();
static LL4_IdentList();
static LL5_IDENT_CHAR();
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
break;
default:{int LL_1=LLnext(-2);
;if (!LL_1) {
break;
}
else if (LL_1 & 1) goto L_1;}
case /*  KWD_CHAR  */ 2 : ;
case /*  KWD_INT  */ 3 : ;
case /*  KWD_FLOAT  */ 4 : ;
case /*  KWD_DOUBLE  */ 5 : ;
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
LLsdecr(2);
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
LL3_Type(
#if LL_ANSI_C
# line 29 "gram.g"
int *size)  
#else
# line 29 "gram.g"
 size) int *size;
#endif
{
goto L_2; /* so that the label is used for certain */
L_2: ;
switch(LLcsymb) {
case /*  KWD_CHAR  */ 2 : ;
goto L_3;
L_3: ;
LLsdecr(1);
LL_SSCANDONE(KWD_CHAR);
# line 29 "gram.g"
{ *size = 1; }
break;
default: if (LLskip()) goto L_2;
goto L_3;
case /*  KWD_INT  */ 3 : ;
LLsdecr(1);
LL_SAFE(KWD_INT);
# line 30 "gram.g"
{ *size = 4; }
break;
case /*  KWD_FLOAT  */ 4 : ;
LLsdecr(1);
LL_SAFE(KWD_FLOAT);
# line 31 "gram.g"
{ *size = 6; }
break;
case /*  KWD_DOUBLE  */ 5 : ;
LLsdecr(1);
LL_SAFE(KWD_DOUBLE);
# line 32 "gram.g"
{ *size = 8; }
break;
}
}
static
#if LL_ANSI_C
void
#endif
LL4_IdentList(
#if LL_ANSI_C
# line 34 "gram.g"
int type_size ,int *list_size)  
#else
# line 34 "gram.g"
 type_size,list_size) int type_size; int *list_size;
#endif
{
LLsincr(3);
LLtincr(11);
LL5_IDENT_CHAR(
# line 35 "gram.g"
type_size, list_size);
LLread();
for (;;) {
goto L_1;
L_1 : {switch(LLcsymb) {
case /* ';' */ 10 : ;
break;
default:{int LL_2=LLnext(44);
;if (!LL_2) {
break;
}
else if (LL_2 & 1) goto L_1;}
case /* ',' */ 11 : ;
LLsincr(3);
LL_SAFE(',');
LLread();
LL5_IDENT_CHAR(
# line 35 "gram.g"
type_size, list_size);
LLread();
continue;
}
}
LLtdecr(11);
break;
}
}
static
#if LL_ANSI_C
void
#endif
LL5_IDENT_CHAR(
#if LL_ANSI_C
# line 38 "gram.g"
int type_size ,int *var_size)  
#else
# line 38 "gram.g"
 type_size,var_size) int type_size; int *var_size;
#endif
{
goto L_2; /* so that the label is used for certain */
L_2: ;
switch(LLcsymb) {
case /* '*' */ 12 : ;
LLsdecr(3);
LLtincr(12);
LLtincr(6);
for (;;) {
LL_SAFE('*');
LLread();
goto L_4;
L_4 : {switch(LLcsymb) {
case /*  IDENT  */ 6 : ;
break;
default:{int LL_3=LLnext(42);
;if (!LL_3) {
break;
}
else if (LL_3 & 1) goto L_4;}
case /* '*' */ 12 : ;
continue;
}
}
LLtdecr(12);
break;
}
LLtdecr(6);
LL_SSCANDONE(IDENT);
# line 39 "gram.g"
{*var_size += 4; }
break;
case /*  IDENT  */ 6 : ;
goto L_3;
L_3: ;
LLsdecr(3);
LL_SSCANDONE(IDENT);
# line 40 "gram.g"
{*var_size += type_size; }
break;
default: if (LLskip()) goto L_2;
goto L_3;
}
}

# line 43 "gram.g"

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

