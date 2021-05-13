# makefile for flex + LLgen project

SCANNER_DESC_FILE=scan.l
PARSER_DESC_FILE=gram.g
PARSER_EXEC_FILE=gram.x

all: $(PARSER_EXEC_FILE)

$(PARSER_EXEC_FILE): lex.yy.c gram.c
	gcc -o $(PARSER_EXEC_FILE) lex.yy.c Lpars.c gram.c

lex.yy.c: $(SCANNER_DESC_FILE)
	flex -l $(SCANNER_DESC_FILE)

gram.c: $(PARSER_DESC_FILE)
	LLgen $(PARSER_DESC_FILE)

clean:
	rm -f lex.yy.c
	rm -f Lpars.c
	rm -f Lpars.h
	rm -f gram.c
