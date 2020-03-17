
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BLOCKCOMMENT COLON EOL FLOAT IDENTIFIER INTEGER LANGLE LBRACE LBRACKET LET LINECOMMENT LOOP MACRO MAP PIPE RANGLE RBRACE RBRACKET REG SEMICOLONprogram : header_statements body_statementsprogram : EOL programheader_statements : header_statement seq_sep header_statementsheader_statements : header_statement \n\t\t\t\t\t\t | header_statement seq_sepheader_statement : register_statement\n\t\t\t\t\t\t| map_statement\n\t\t\t\t\t\t| let_statementregister_statement : REG array_declarationmap_statement : MAP map_target map_sourcemap_target : IDENTIFIERmap_source : IDENTIFIERmap_source : array_slicelet_statement : LET IDENTIFIER numberbody_statements : body_statement seq_sep body_statementsbody_statements : body_statement\n\t\t\t\t\t   | body_statement seq_sepbody_statement : gate_statement\n\t\t\t\t\t  | macro_definition\n\t\t\t\t\t  | loop_statement\n\t\t\t\t\t  | gate_blockgate_statement : IDENTIFIER gate_arg_listgate_arg_list : gate_arg gate_arg_listgate_arg_list : gate_arg : array_elementgate_arg : IDENTIFIERgate_arg : numbermacro_definition : MACRO IDENTIFIER gate_def_list gate_blockgate_def_list : IDENTIFIER gate_def_listgate_def_list : loop_statement : LOOP let_or_integer gate_blockgate_block : sequential_gate_block\n\t\t\t\t  | parallel_gate_blocksequential_gate_block : LBRACE sequential_statements RBRACEsequential_gate_block : LBRACE EOL sequential_statements RBRACEparallel_gate_block : LANGLE parallel_statements RANGLEparallel_gate_block : LANGLE EOL parallel_statements RANGLEsequential_statements : sequential_statement seq_sep sequential_statementssequential_statements : sequential_statement\n\t\t\t\t\t\t\t | sequential_statement seq_sepsequential_statement : gate_statement\n\t\t\t\t\t\t\t| parallel_gate_block\n\t\t\t\t\t\t\t| loop_statementparallel_statements : parallel_statement par_sep parallel_statementsparallel_statements : parallel_statement\n\t\t\t\t\t\t   | parallel_statement par_sepparallel_statement : gate_statement\n\t\t\t\t\t\t  | sequential_gate_blockarray_declaration : IDENTIFIER LBRACKET let_or_integer RBRACKETarray_element : IDENTIFIER LBRACKET let_or_integer RBRACKETarray_slice : IDENTIFIER LBRACKET slice_indexing RBRACKETslice_indexing : let_or_integerslice_indexing : let_or_integer COLON let_or_integerslice_indexing : let_or_integer COLON let_or_integer COLON let_or_integerlet_or_integer : IDENTIFIER\n\t\t\t\t\t  | INTEGERseq_sep : SEMICOLON\n\t\t\t   | EOL\n\t\t\t   | seq_sep EOLpar_sep : PIPE\n\t\t\t   | EOL\n\t\t\t   | par_sep EOLnumber : INTEGER\n\t\t\t  | FLOAT'
    
_lr_action_items = {'EOL':([0,3,4,5,6,7,12,13,14,15,16,17,20,21,22,23,25,26,27,28,33,34,35,36,37,38,39,40,47,48,49,50,53,54,55,57,59,60,61,62,65,68,69,71,72,74,75,76,81,82,84,86,87,90,91,],[3,3,27,-6,-7,-8,27,-18,-19,-20,-21,-24,-32,-33,46,52,57,-57,-58,-9,57,-26,-22,-24,-25,-27,-63,-64,27,-41,-42,-43,76,-47,-48,-59,-10,-12,-13,-14,-23,-31,-34,57,-36,86,-60,-61,-28,-35,-37,-62,-49,-50,-51,]),'REG':([0,3,25,26,27,57,],[8,8,8,-57,-58,-59,]),'MAP':([0,3,25,26,27,57,],[9,9,9,-57,-58,-59,]),'LET':([0,3,25,26,27,57,],[10,10,10,-57,-58,-59,]),'$end':([1,11,12,13,14,15,16,17,20,21,24,26,27,33,34,35,36,37,38,39,40,57,63,65,68,69,72,81,82,84,90,],[0,-1,-16,-18,-19,-20,-21,-24,-32,-33,-2,-57,-58,-17,-26,-22,-24,-25,-27,-63,-64,-59,-15,-23,-31,-34,-36,-28,-35,-37,-50,]),'IDENTIFIER':([2,4,5,6,7,8,9,10,17,18,19,22,23,25,26,27,28,30,31,33,34,36,37,38,39,40,41,46,52,56,57,58,59,60,61,62,64,66,71,74,75,76,78,86,87,90,91,92,94,],[17,-4,-6,-7,-8,29,31,32,34,41,43,17,17,-5,-57,-58,-9,60,-11,17,-26,34,-25,-27,-63,-64,66,17,17,-3,-59,43,-10,-12,-13,-14,43,66,17,17,-60,-61,43,-62,-49,-50,-51,43,43,]),'MACRO':([2,4,5,6,7,25,26,27,28,33,39,40,56,57,59,60,61,62,87,91,],[18,-4,-6,-7,-8,-5,-57,-58,-9,18,-63,-64,-3,-59,-10,-12,-13,-14,-49,-51,]),'LOOP':([2,4,5,6,7,22,25,26,27,28,33,39,40,46,56,57,59,60,61,62,71,87,91,],[19,-4,-6,-7,-8,19,-5,-57,-58,-9,19,-63,-64,19,-3,-59,-10,-12,-13,-14,19,-49,-51,]),'LBRACE':([2,4,5,6,7,23,25,26,27,28,33,39,40,41,42,43,44,52,56,57,59,60,61,62,66,67,74,75,76,80,86,87,91,],[22,-4,-6,-7,-8,22,-5,-57,-58,-9,22,-63,-64,-30,22,-55,-56,22,-3,-59,-10,-12,-13,-14,-30,22,22,-60,-61,-29,-62,-49,-51,]),'LANGLE':([2,4,5,6,7,22,25,26,27,28,33,39,40,41,42,43,44,46,56,57,59,60,61,62,66,67,71,80,87,91,],[23,-4,-6,-7,-8,23,-5,-57,-58,-9,23,-63,-64,-30,23,-55,-56,23,-3,-59,-10,-12,-13,-14,-30,23,23,-29,-49,-51,]),'SEMICOLON':([4,5,6,7,12,13,14,15,16,17,20,21,28,34,35,36,37,38,39,40,47,48,49,50,59,60,61,62,65,68,69,72,81,82,84,87,90,91,],[26,-6,-7,-8,26,-18,-19,-20,-21,-24,-32,-33,-9,-26,-22,-24,-25,-27,-63,-64,26,-41,-42,-43,-10,-12,-13,-14,-23,-31,-34,-36,-28,-35,-37,-49,-50,-51,]),'RBRACE':([17,20,21,26,27,34,35,36,37,38,39,40,45,47,48,49,50,57,65,68,69,70,71,72,82,83,84,90,],[-24,-32,-33,-57,-58,-26,-22,-24,-25,-27,-63,-64,69,-39,-41,-42,-43,-59,-23,-31,-34,82,-40,-36,-35,-38,-37,-50,]),'PIPE':([17,34,35,36,37,38,39,40,53,54,55,65,69,82,90,],[-24,-26,-22,-24,-25,-27,-63,-64,75,-47,-48,-23,-34,-35,-50,]),'RANGLE':([17,34,35,36,37,38,39,40,51,53,54,55,65,69,73,74,75,76,82,85,86,90,],[-24,-26,-22,-24,-25,-27,-63,-64,72,-45,-47,-48,-23,-34,84,-46,-60,-61,-35,-44,-62,-50,]),'INTEGER':([17,19,32,34,36,37,38,39,40,58,64,78,90,92,94,],[39,44,39,-26,39,-25,-27,-63,-64,44,44,44,-50,44,44,]),'FLOAT':([17,32,34,36,37,38,39,40,90,],[40,40,-26,40,-25,-27,-63,-64,-50,]),'LBRACKET':([29,34,60,],[58,64,78,]),'RBRACKET':([43,44,77,79,88,89,93,95,],[-55,-56,87,90,91,-52,-53,-54,]),'COLON':([43,44,89,93,],[-55,-56,92,94,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,3,],[1,24,]),'header_statements':([0,3,25,],[2,2,56,]),'header_statement':([0,3,25,],[4,4,4,]),'register_statement':([0,3,25,],[5,5,5,]),'map_statement':([0,3,25,],[6,6,6,]),'let_statement':([0,3,25,],[7,7,7,]),'body_statements':([2,33,],[11,63,]),'body_statement':([2,33,],[12,12,]),'gate_statement':([2,22,23,33,46,52,71,74,],[13,48,54,13,48,54,48,54,]),'macro_definition':([2,33,],[14,14,]),'loop_statement':([2,22,33,46,71,],[15,50,15,50,50,]),'gate_block':([2,33,42,67,],[16,16,68,81,]),'sequential_gate_block':([2,23,33,42,52,67,74,],[20,55,20,20,55,20,55,]),'parallel_gate_block':([2,22,33,42,46,67,71,],[21,49,21,21,49,21,49,]),'seq_sep':([4,12,47,],[25,33,71,]),'array_declaration':([8,],[28,]),'map_target':([9,],[30,]),'gate_arg_list':([17,36,],[35,65,]),'gate_arg':([17,36,],[36,36,]),'array_element':([17,36,],[37,37,]),'number':([17,32,36,],[38,62,38,]),'let_or_integer':([19,58,64,78,92,94,],[42,77,79,89,93,95,]),'sequential_statements':([22,46,71,],[45,70,83,]),'sequential_statement':([22,46,71,],[47,47,47,]),'parallel_statements':([23,52,74,],[51,73,85,]),'parallel_statement':([23,52,74,],[53,53,53,]),'map_source':([30,],[59,]),'array_slice':([30,],[61,]),'gate_def_list':([41,66,],[67,80,]),'par_sep':([53,],[74,]),'slice_indexing':([78,],[88,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> header_statements body_statements','program',2,'p_program','parser.py',7),
  ('program -> EOL program','program',2,'p_program_blanks','parser.py',65),
  ('header_statements -> header_statement seq_sep header_statements','header_statements',3,'p_header_statements','parser.py',69),
  ('header_statements -> header_statement','header_statements',1,'p_header_statements_s','parser.py',73),
  ('header_statements -> header_statement seq_sep','header_statements',2,'p_header_statements_s','parser.py',74),
  ('header_statement -> register_statement','header_statement',1,'p_header_statement','parser.py',78),
  ('header_statement -> map_statement','header_statement',1,'p_header_statement','parser.py',79),
  ('header_statement -> let_statement','header_statement',1,'p_header_statement','parser.py',80),
  ('register_statement -> REG array_declaration','register_statement',2,'p_register_statement','parser.py',84),
  ('map_statement -> MAP map_target map_source','map_statement',3,'p_map_statement','parser.py',88),
  ('map_target -> IDENTIFIER','map_target',1,'p_map_target_id','parser.py',92),
  ('map_source -> IDENTIFIER','map_source',1,'p_map_source_id','parser.py',100),
  ('map_source -> array_slice','map_source',1,'p_map_source_array','parser.py',104),
  ('let_statement -> LET IDENTIFIER number','let_statement',3,'p_let_statement','parser.py',108),
  ('body_statements -> body_statement seq_sep body_statements','body_statements',3,'p_body_statements','parser.py',112),
  ('body_statements -> body_statement','body_statements',1,'p_body_statements_s','parser.py',116),
  ('body_statements -> body_statement seq_sep','body_statements',2,'p_body_statements_s','parser.py',117),
  ('body_statement -> gate_statement','body_statement',1,'p_body_statement','parser.py',121),
  ('body_statement -> macro_definition','body_statement',1,'p_body_statement','parser.py',122),
  ('body_statement -> loop_statement','body_statement',1,'p_body_statement','parser.py',123),
  ('body_statement -> gate_block','body_statement',1,'p_body_statement','parser.py',124),
  ('gate_statement -> IDENTIFIER gate_arg_list','gate_statement',2,'p_gate_statement','parser.py',128),
  ('gate_arg_list -> gate_arg gate_arg_list','gate_arg_list',2,'p_gate_arg_list','parser.py',132),
  ('gate_arg_list -> <empty>','gate_arg_list',0,'p_gate_arg_list_empty','parser.py',136),
  ('gate_arg -> array_element','gate_arg',1,'p_gate_arg_array','parser.py',140),
  ('gate_arg -> IDENTIFIER','gate_arg',1,'p_gate_arg_id','parser.py',144),
  ('gate_arg -> number','gate_arg',1,'p_gate_arg_number','parser.py',148),
  ('macro_definition -> MACRO IDENTIFIER gate_def_list gate_block','macro_definition',4,'p_macro_definition','parser.py',152),
  ('gate_def_list -> IDENTIFIER gate_def_list','gate_def_list',2,'p_gate_def_list','parser.py',156),
  ('gate_def_list -> <empty>','gate_def_list',0,'p_gate_def_list_empty','parser.py',160),
  ('loop_statement -> LOOP let_or_integer gate_block','loop_statement',3,'p_loop_statement','parser.py',164),
  ('gate_block -> sequential_gate_block','gate_block',1,'p_gate_block','parser.py',168),
  ('gate_block -> parallel_gate_block','gate_block',1,'p_gate_block','parser.py',169),
  ('sequential_gate_block -> LBRACE sequential_statements RBRACE','sequential_gate_block',3,'p_sequential_gate_block','parser.py',173),
  ('sequential_gate_block -> LBRACE EOL sequential_statements RBRACE','sequential_gate_block',4,'p_sequential_gate_block_blanks','parser.py',177),
  ('parallel_gate_block -> LANGLE parallel_statements RANGLE','parallel_gate_block',3,'p_parallel_gate_block','parser.py',181),
  ('parallel_gate_block -> LANGLE EOL parallel_statements RANGLE','parallel_gate_block',4,'p_parallel_gate_block_blanks','parser.py',185),
  ('sequential_statements -> sequential_statement seq_sep sequential_statements','sequential_statements',3,'p_sequential_statements','parser.py',189),
  ('sequential_statements -> sequential_statement','sequential_statements',1,'p_sequential_statements_s','parser.py',193),
  ('sequential_statements -> sequential_statement seq_sep','sequential_statements',2,'p_sequential_statements_s','parser.py',194),
  ('sequential_statement -> gate_statement','sequential_statement',1,'p_sequential_statement','parser.py',198),
  ('sequential_statement -> parallel_gate_block','sequential_statement',1,'p_sequential_statement','parser.py',199),
  ('sequential_statement -> loop_statement','sequential_statement',1,'p_sequential_statement','parser.py',200),
  ('parallel_statements -> parallel_statement par_sep parallel_statements','parallel_statements',3,'p_parallel_statements','parser.py',204),
  ('parallel_statements -> parallel_statement','parallel_statements',1,'p_parallel_statements_s','parser.py',208),
  ('parallel_statements -> parallel_statement par_sep','parallel_statements',2,'p_parallel_statements_s','parser.py',209),
  ('parallel_statement -> gate_statement','parallel_statement',1,'p_parallel_statement','parser.py',213),
  ('parallel_statement -> sequential_gate_block','parallel_statement',1,'p_parallel_statement','parser.py',214),
  ('array_declaration -> IDENTIFIER LBRACKET let_or_integer RBRACKET','array_declaration',4,'p_array_declaration','parser.py',218),
  ('array_element -> IDENTIFIER LBRACKET let_or_integer RBRACKET','array_element',4,'p_array_element','parser.py',222),
  ('array_slice -> IDENTIFIER LBRACKET slice_indexing RBRACKET','array_slice',4,'p_array_slice','parser.py',226),
  ('slice_indexing -> let_or_integer','slice_indexing',1,'p_slice_indexing_one','parser.py',230),
  ('slice_indexing -> let_or_integer COLON let_or_integer','slice_indexing',3,'p_slice_indexing_two','parser.py',234),
  ('slice_indexing -> let_or_integer COLON let_or_integer COLON let_or_integer','slice_indexing',5,'p_slice_indexing_three','parser.py',238),
  ('let_or_integer -> IDENTIFIER','let_or_integer',1,'p_let_or_integer','parser.py',242),
  ('let_or_integer -> INTEGER','let_or_integer',1,'p_let_or_integer','parser.py',243),
  ('seq_sep -> SEMICOLON','seq_sep',1,'p_seq_sep','parser.py',247),
  ('seq_sep -> EOL','seq_sep',1,'p_seq_sep','parser.py',248),
  ('seq_sep -> seq_sep EOL','seq_sep',2,'p_seq_sep','parser.py',249),
  ('par_sep -> PIPE','par_sep',1,'p_par_sep','parser.py',253),
  ('par_sep -> EOL','par_sep',1,'p_par_sep','parser.py',254),
  ('par_sep -> par_sep EOL','par_sep',2,'p_par_sep','parser.py',255),
  ('number -> INTEGER','number',1,'p_number','parser.py',259),
  ('number -> FLOAT','number',1,'p_number','parser.py',260),
]
