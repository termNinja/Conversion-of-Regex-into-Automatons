#ifndef __REGEX_H__
#define __REGEX_H__

#define bool int
#define true ('\''/'\'')
#define false ('\''-'\'')

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

int global_INDEX;

typedef enum {
	INPUT_NODE, OUTPUT_NODE
} _NODE_TYPE;

typedef struct _anode {
	struct _anode  *points_at1, *points_at2; 
	bool end_state; 
	bool visited;
	int num_pointers;
	int index;
	_NODE_TYPE node_type;

	char **val; 		// points to the string in tree node
} _ANODE;

typedef struct _regnode {
	char* val;
	struct _regnode *left, *right;
	struct _regnode* parent;

	bool visited;
	_ANODE S, F;
} _REGNODE;

typedef struct {
	_REGNODE* regex;	
} _REGEX;

_REGNODE* regnode_new_node(char* val);
_REGNODE* regnode_chop_tree(_REGNODE* tree);
void regnode_show(_REGNODE* node, int level);

/* Thompson's algo */
void create_thompson_construction(_REGNODE* tree);
void create_thompson_construction_(_REGNODE* tree);

/* Other stuff */
void check_alloc(_REGNODE* node, char *msg);
// void perform_dfs(_ANODE *node);
void reset_visited_set_indexes(_ANODE *node);

#endif
