#! /bin/sh
flex -l scan.l &&\
LLgen gram.g &&\
gcc lex.yy.c Lpars.c gram.c &&\
rm -f lex.yy.c && rm -f Lpars.c && rm -f Lpars.h && rm -f gram.c
