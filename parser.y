%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "regex.h"
#include "tree_map.h"
#include "nova_functions.h"
#include "colors.h"

int yylex(void);
int global_FILE_EXPORT_NUM;

_TREENODE* mem_map = NULL;

%}

%union {
	char* name;
	char* word;
	_REGEX regex;
}

%token <name> id_token;
%token <word> word_token;
%token leave_token print_token vars_token clear_token help_token thompson_token

%type <regex> E

%left '|'
%right '*' '+'

%%
Program	: Program Command ';'
		| Command ';'
		;

Command	: leave_token {
	nova_leave_program();
}
		| id_token ':' '=' E {
	mem_map = tree_add_into(mem_map, &$4, $1);	
}
		| print_token E {
	regnode_show($2.regex, 0);
	system("python2 pyscripts/pygraph.py hello world");
}
		| vars_token {
	printf(BLUE "**********************\n" RESET);
	printf(BOLDRED "Declared variables:\n" RESET);
	printf(BLUE "**********************\n" RESET);
	tree_show_tree(mem_map);
	printf(BLUE "**********************\n\n" RESET);
}
		| clear_token {
	nova_clear_screen();
}
		| help_token {
	nova_show_help_menu();
}
		| thompson_token  E {
	create_thompson_construction($2.regex);
	// perform_dfs(&(mem_map->regex.regex->S), 0);
	nova_export_thompson(&($2), global_FILE_EXPORT_NUM);

	global_FILE_EXPORT_NUM++;

}
;

E 	:	E '*' {
	_REGEX obj;

	// Alloc a new node
	_REGNODE* root = regnode_new_node("*");

	// Connect $1 to it
	root->left = $1.regex;
	obj.regex = root;

	$$ = obj;
}
/*
TODO: implement later
E 	:	E '+' {
	_REGEX obj;

	// Alloc a new node
	_REGNODE* root = regnode_new_node("+");

	// Connect $1 to it
	root->left = $1.regex;
	obj.regex = root;

	$$ = obj;
}
*/
	|	E '|' E {
	_REGEX obj;
	_REGNODE* root;

	// We alloc a new node
	root = regnode_new_node("|");

	// Connect $1 and $3 to it
	root->left = $1.regex;
	root->right = $3.regex;
	obj.regex = root;
	$$ = obj;
}
	|	word_token {
	_REGEX obj;
	char* word = strdup($1);
	if (word == NULL) {
		fprintf(stderr, "stdrup failed in parser.y\n");
		exit(EXIT_FAILURE);
	}
	free($1);
	obj.regex = regnode_new_node(word);
	$$ = obj;
}
	| '(' E ')' {
	$$ = $2;
}
	| id_token {
	_TREENODE* pointer = tree_find(mem_map, $1);
	if (pointer == NULL) {
		fprintf(stderr, "Variable %s doesn't exist!\n", $1);
		free($1);
		tree_chop_tree(mem_map);
		exit(EXIT_FAILURE);
	}
	$$ = pointer->regex;
	free($1);
}
%%
int main(int argc, char *argv[])
{
	if (argc == 2)
		global_FILE_EXPORT_NUM = atoi(argv[1]);
	yyparse();
	tree_chop_tree(mem_map);
	return 0;
}
