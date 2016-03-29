#include "regex.h"

_REGNODE* regnode_new_node(char* val)
{
	_REGNODE* node = (_REGNODE*) malloc (sizeof(_REGNODE));
	check_alloc(node, "Failed memory alloc in new_node\n");

	// init the node
	node->parent = node->left = node->right = NULL;
	node->val = strdup(val);
	if (node->val == NULL) {	
		fprintf(stderr, "Failed stdrup in new_node!\n");
		exit(EXIT_FAILURE);
	}

	node->visited = false;

	node->S.num_pointers = 0;
	node->S.points_at1 = NULL;
	node->S.points_at2 = NULL;
	node->S.end_state = false;
	node->S.val = &(node->val);
	node->S.visited = false;
	node->S.node_type = INPUT_NODE;

	node->F.num_pointers = 0;
	node->F.points_at1 = NULL;
	node->F.points_at2 = NULL;
	node->F.end_state = false;
	node->F.val = &(node->val);
	node->F.visited = false;
	node->F.node_type = OUTPUT_NODE;

	return node;
}

_REGNODE* regnode_chop_tree(_REGNODE* tree)
{
	if (tree != NULL) {
		regnode_chop_tree(tree->left);
		regnode_chop_tree(tree->right);
	 	free(tree->val);
		free(tree);
		printf("IM FINE DUDE!\n");
	}
	return NULL;
}

void check_alloc(_REGNODE* node, char *msg)
{
	if (node == NULL) {
		fprintf(stderr, "%s\n", msg);
		exit(EXIT_FAILURE);
	}
}

void regnode_show(_REGNODE* node, int level)
{
	int i;
	if (node != NULL) {
		for (i = 0; i < level; ++i)
			printf("  ");
		printf("%s\n", node->val);
		regnode_show(node->left, level + 1);
		regnode_show(node->right, level + 1);
	}
}

void create_thompson_construction(_REGNODE* tree)
{
	global_INDEX = 0;
	tree->F.end_state = true; 						// thompson's algo produces automaton with 1 final state
	create_thompson_construction_(tree);
}

// TODO is variable num_pointers needed? Marked it for later -> UPDATE: NOT NEEDED, remove it later
void create_thompson_construction_(_REGNODE* tree)
{
	tree->S.index = global_INDEX;
	tree->F.index = global_INDEX + 1;
	global_INDEX += 2;

	// if our regex is a simple word (tree has only 1 node)
	if(tree->left == NULL && tree->right == NULL) {
		tree->S.num_pointers = 1;
		tree->S.points_at1 = &(tree->F);
		return;
	}
	// If we have a * or | operator in our node, then there
	// must exist a child.
	assert(tree->left != NULL || tree->right != NULL);

	// handling * operator
	if (! strcmp(tree->val, "*")) {
		// root S
		tree->S.num_pointers = 2;
		tree->S.points_at1 = &(tree->F);
		tree->S.points_at2 = &(tree->left->S);

		_REGNODE *child = tree->left;
		// child: S
		child->S.num_pointers = 0;
		
		// child: F
		child->F.num_pointers = 2;
		child->F.points_at1 = &(child->S);
		child->F.points_at2 = &(tree->F);

		//		printf("calling rec: %s\n", tree->left->val);
		create_thompson_construction_(tree->left);
	}

	// handling | operator
	if(! strcmp(tree->val, "|")) {
		// root: S
		tree->S.num_pointers = 2;
		tree->S.points_at1 = &(tree->left->S);
		tree->S.points_at2 = &(tree->right->S);

		// left child: F
		tree->left->F.num_pointers = 1;
		tree->left->F.points_at1 = &(tree->F);

		// right child: F
		tree->right->F.num_pointers = 1;
		tree->right->F.points_at1 = &(tree->F);

		create_thompson_construction_(tree->left);
		create_thompson_construction_(tree->right);
	}

	// handling . operator
	if (! strcmp(tree->val, ".")) {
		tree->S.num_pointers = 1;
		tree->S.points_at1 = &(tree->left->S);

		// left child
		tree->left->S.num_pointers = 1;
		tree->left->S.points_at1 = &(tree->left->F);
		tree->left->F.num_pointers = 1;
		tree->left->F.points_at1 = &(tree->right->S);

		// right child
		tree->right->S.num_pointers = 1;
		tree->right->S.points_at1 = &(tree->right->F);
		tree->right->F.num_pointers = 1;
		tree->right->F.points_at1 = &(tree->F);
		
		create_thompson_construction_(tree->left);
		create_thompson_construction_(tree->right);
	}
}

void reset_visited_set_indexes(_ANODE *node)
{
	node->visited = false;
//	node->index = global_INDEX;
//	global_INDEX++;
	if (node->points_at1 != NULL) reset_visited_set_indexes(node->points_at1);
	if (node->points_at2 != NULL) reset_visited_set_indexes(node->points_at2);
}
