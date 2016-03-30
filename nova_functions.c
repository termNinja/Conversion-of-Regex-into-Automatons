#include "nova_functions.h"

void nova_show_help_menu()
{
	printf(MAGENTA "Commands end with ;\n");
	printf("Allowed regex operations:\n");
	printf("\tOR operator -> |\n");
	printf("\tCLEENE operator -> *\n");
	printf(GREEN "Example: (a|b)|(c|d)*\n\n");
	printf("vars;\t\t -> shows memory and variables.\n");
	printf("clear;\t\t -> clears the screen.\n");
	printf("print E;\t -> shows expression value.\n");
	printf("leave;\t\t -> leaves the program.\n");
	printf("E;\t\t -> shows expression value.\n");
	printf("x := E;\t\t -> Create/redefine variable x as regex E.\n");
	printf(RED "\t\tVariable name must start with $ (like in PHP).\n");
	printf("\n" RESET);
}

void nova_clear_screen()
{
	printf("\033[2J\033[1;1H");	
}

void nova_leave_program()
{
	printf("\033[2J\033[1;1H");	
	printf(BOLDRED "FAREWELL!\n" RESET);
	exit(EXIT_SUCCESS);
}

extern void yyerror(const char *errmsg)
{
	fprintf(stderr, "%s\n", errmsg);
	exit(EXIT_FAILURE);
}

void nova_export_thompson(_REGEX *regex, int filenum)
{
	FILE *f;
	char shellcmd[100];
	char graph_name[50];
	sprintf(graph_name, "graphs/%d_01_thompson.gv", filenum);
	f = fopen(graph_name, "w");
	if (! f) {
		fprintf(stderr, "Failed creating/writing into file %s!", graph_name);
		exit(EXIT_FAILURE);
	}
	
	fprintf(f, "digraph finite_state_machine {\n");
	fprintf(f, "graph [fontname = \"lmroman12\"];\n");
	fprintf(f, "node [fontname = \"lmroman12\"];\n");
	fprintf(f, "edge [fontname = \"lmroman12\"];\n");
	fprintf(f, "\trankdir=LR;\n");
	fprintf(f, "\tsize=\"8,5\"\n");
	fprintf(f, "\tnode [shape = doublecircle]; 1;\n");
	fprintf(f, "\tnode [shape = circle];\n");

	generate_thompson(f, &(regex->regex->S));

	fprintf(f, "}\n");
	fclose(f);

	reset_nodes(regex->regex);
	
	sprintf(shellcmd, "dot -Tpdf graphs/%d_01_thompson.gv -o graphs/%d_01_thompson.pdf", filenum, filenum);
	system(shellcmd);
	sprintf(shellcmd, "python2 pyscripts/pygraph.py %s", graph_name);
	system(shellcmd);
}

void reset_nodes(_REGNODE *regex)
{
	regex->visited = false;
	regex->S.visited = false;
	regex->F.visited = false;
	if (regex->left != NULL)
		reset_nodes(regex->left);
	if (regex->right != NULL)
		reset_nodes(regex->right);
}

void generate_thompson(FILE *f, _ANODE *node)
{
	// we mark the current node as visited
	node->visited = true;

	// we check if the node has a adjacent node and we write required edges into file
	if (node->points_at1 != NULL) {
		fprintf(f, "\t\"%d\" -> \"%d\"", node->index, node->points_at1->index);	
		if (strcmp(*(node->val), *(node->points_at1->val)) == 0 
			&& node->node_type == INPUT_NODE
			&& strcmp("|", *(node->val)) != 0 
			&& strcmp("*", *(node->val)) != 0) {
				fprintf(f, " [label=\"%s\"];", *(node->val));
		}
		fprintf(f, "\n");

		// if adjacent vertex wasn't visited, we visit it
		if (! node->points_at1->visited) {
			generate_thompson(f, node->points_at1);
		}
	}

	// we check if the node has a adjacent node and we write required edges into file
	if (node->points_at2 != NULL) {
		fprintf(f, "\t\"%d\" -> \"%d\"", node->index, node->points_at2->index);	
		if (strcmp(*(node->val), *(node->points_at2->val)) == 0 
			&& node->node_type == INPUT_NODE
			&& strcmp("|", *(node->val)) != 0 
			&& strcmp("*", *(node->val)) != 0) {
				fprintf(f, " [label=\"%s\"];", *(node->val));
		}
		fprintf(f, "\n");

		// if adjacent vertex wasn't visited, we visit it
		if (! node->points_at2->visited) {
			generate_thompson(f, node->points_at2);
		}
	}
}
