# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------
GOAL	= project_nova
CC		= gcc
OPT		= -Wall
asOBJ	= -c
AS		= -o
YACC	= yacc -d
LEX		= flex
PFiles  = *.c *.h *.l *.y pyscripts graphs
# -----------------------------------------------------------------------------
# GOAL
# -----------------------------------------------------------------------------
$(GOAL): y.tab.o lex.yy.o regex.o tree_map.o nova_functions.o
	$(CC) $(OPT) $(AS) $@ $^

# -----------------------------------------------------------------------------
# Object files
# -----------------------------------------------------------------------------
y.tab.o: y.tab.c y.tab.h tree_map.h regex.h colors.h nova_functions.h regex.h
	$(CC) $(OPT) $(asOBJ) $(AS) $@ $<

lex.yy.o: lex.yy.c
	$(CC) $(OPT) $(asOBJ) $(AS) $@ $<

regex.o: regex.c regex.h
	$(CC) $(OPT) $(asOBJ) $(AS) $@ $<

tree_map.o: tree_map.c tree_map.h regex.h
	$(CC) $(OPT) $(asOBJ) $(AS) $@ $<

nova_functions.o: nova_functions.c nova_functions.h colors.h regex.h
	$(CC) $(OPT) $(asOBJ) $(AS) $@ $<

# -----------------------------------------------------------------------------
# C (H) files
# -----------------------------------------------------------------------------
y.tab.c y.tab.h: parser.y
	$(YACC) $<	

lex.yy.c: lexer.l
	$(LEX) $<	

# -----------------------------------------------------------------------------
# Additional stuff
# -----------------------------------------------------------------------------
.PHONY: help clear dance lines dist

help:
	@echo "make help 	-> shows help menu"
	@echo "make clear 	-> clears workspace"
	@echo "make dance 	-> performs a dance"
	@echo "make lines 	-> counts file lines"

clear:
	@rm -rf *~ *.o lex.yy.* $(GOAL) y.tab.*
	@clear
	@echo "Project dir has been cleaned sire!"

dance:
	@clear
	@echo "OPPA REGEX STYLE!"

dist:
	@zip -r project_aurora.zip $(PFiles)

lines:
	@make clear
	@echo "C files:"
	@wc -l *.c *.h *.y *.l 
	@echo
	@echo "Python files:"
	@wc -l pyscripts/pygraph.py pyscripts/classes/resources.py
