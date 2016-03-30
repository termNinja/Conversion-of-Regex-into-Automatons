#include "tree_map.h"

_TREENODE* tree_new_node(_REGEX* regex, char *name)
{
	_TREENODE* node = (_TREENODE*) malloc (sizeof(_TREENODE));
	if (node == NULL) {
		fprintf(stderr, "Failed mem alloc in tree_new_node function\n");
		exit(EXIT_FAILURE);
	}

	// node init
	node->name = strdup(name);
	if (node->name == NULL) {
		fprintf(stderr, "Failed strdup in tree_new_node function\n");
		exit(EXIT_FAILURE);
	}
	node->left = node->right = NULL;
	node->regex = *regex;

	return node;
}

_TREENODE* tree_add_into(_TREENODE* tree, _REGEX* regex, char *name)
{
	if (tree == NULL) 
		return tree_new_node(regex, name);

	int tmp = strcmp(name, tree->name);
	if (tmp == 0) {
		// we delete the old regex
		tree->regex.regex = regnode_chop_tree(tree->regex.regex);
		// and add a new one
		tree->regex = *regex;
	} else if (tmp < 0)
		tree->left = tree_add_into(tree->left, regex, name);
	else
		tree->right = tree_add_into(tree->right, regex, name);

	return tree;
}

_TREENODE* tree_find(_TREENODE* tree, char *name)
{
	if (tree == NULL) return NULL;
	int tmp = strcmp(name, tree->name);
	if (tmp == 0)
		return tree;
	else if (tmp < 0)
		return tree_find(tree->left, name);
	else
		return tree_find(tree->right, name);
}

_TREENODE* tree_chop_tree(_TREENODE *tree)
{
	if (tree != NULL) {
		tree_chop_tree(tree->left);
		tree_chop_tree(tree->right);
		free(tree->name);
		regnode_chop_tree(tree->regex.regex);
		free(tree);	
	}
	return NULL;
}

void tree_show_tree(_TREENODE *tree)
{
	if (tree != NULL) {
		printf("%s\n", tree->name);
		tree_show_tree(tree->left);
		tree_show_tree(tree->right);
	}
}
