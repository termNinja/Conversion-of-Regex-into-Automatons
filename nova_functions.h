#ifndef __NOVA_FUNCTIONS_H__
#define __NOVA_FUNCTIONS_H__

#include <stdio.h>
#include <stdlib.h>
#include "regex.h"
#include "colors.h"

void nova_show_help_menu();
void nova_clear_screen();
void nova_leave_program();
void nova_export_thompson(_REGEX *regex, int filenum);
void generate_thompson(FILE *f, _ANODE *node);
void reset_nodes(_REGNODE *regex);
extern void yyerror(const char *errmsg);

#endif
