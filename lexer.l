%option noyywrap
%option noinput
%option nounput
%{
#include <stdio.h>
#include <stdlib.h>

#include "regex.h"
#include "y.tab.h"
%}

ID 		[$][a-zA-Z_][a-zA-Z_0-9]*
WORD	[a-zA-Z0-9]+
%%
leave {
	return leave_token;
}

clear {
	return clear_token;
}

help {
	return help_token;
}

print {
	return print_token;
}

vars {
	return vars_token;
}

thompson {
	return thompson_token;
}

[*+|():=;] {
	return *yytext;
}

{ID} {
	yylval.name = strdup(yytext);
	if (yylval.name == NULL) {
		fprintf(stderr, "Failed string duplication at lexer.l\n");
		exit(EXIT_FAILURE);
	}
	return id_token;
}

{WORD} {	
	yylval.word = strdup(yytext);
	if (yylval.word == NULL) {
		fprintf(stderr, "Failed string duplication at lexer.l\n");
		exit(EXIT_FAILURE);
	}
	return word_token;
}

[ \n\t] { }

. {
	fprintf(stderr, "Lexical error at character %s\n", yytext);
	exit(EXIT_FAILURE);
}
%%
