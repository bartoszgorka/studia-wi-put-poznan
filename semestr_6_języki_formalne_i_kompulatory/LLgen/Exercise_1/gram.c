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

# line 13 "gram.g"

  int main()
  {

    parse();
    return 0;
  }

  void LLmessage(int tk)
  {
    printf("LLmessage: ");
    switch(tk)
    {
      case -1 : if(isprint(LLsymb))printf("expected EOF not encountered, unexpected token (%c) found, skipping extra input\n", LLsymb);
                else printf("expected EOF not encountered, unexpected token (%d) found, skipping extra input\n", LLsymb);
                break;
      case 0  : if(isprint(LLsymb))printf("unexpected token (%c) deleted\n",LLsymb);
                else printf("unexpected token (%d) deleted\n",LLsymb);
                exit(-1);
      default : if(isprint(tk))printf("expected token (%c) not found, ", tk);
                else printf("expected token (%d) not found, ", tk);
                if(isprint(LLsymb))printf("token (%c) encountered\n", LLsymb);
                else printf("token (%d) encountered\n", LLsymb);
                exit(-1);
    }
  }

