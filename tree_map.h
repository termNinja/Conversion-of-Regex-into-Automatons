#ifndef _TREE_MAP_H
#define _TREE_MAP_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "regex.h"

typedef struct _treenode {
	_REGEX regex;
	struct _treenode *left, *right;
	char* name;
} _TREENODE;

_TREENODE* tree_new_node(_REGEX* regex, char *name);
_TREENODE* tree_add_into(_TREENODE* tree, _REGEX* regex, char *name);
_TREENODE* tree_find(_TREENODE* tree, char *name);
_TREENODE* tree_chop_tree(_TREENODE *tree);
void tree_show_tree(_TREENODE *tree);

#endif
