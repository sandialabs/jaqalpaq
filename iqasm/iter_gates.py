"""Functions for iterating over gates in a Jaqal file"""

from .parse import parse_with_lark, ParseTreeVisitor
from .let_visitor import expand_let_values
from .map_visitor import expand_map_values
from .macro_expansion_visitor import expand_macros
from .block_normalizer import normalize_blocks_with_unitary_timing


def parse_unitary_timed_gates(jaqal_text):
    """Given the text of a Jaqal file, iterate over all gate objects. Macros are expanded, but loops are not.
    """

    tree = parse_with_lark(jaqal_text)
    tree = expand_let_values(tree)
    tree = expand_map_values(tree)
    tree = expand_macros(tree)
    tree = normalize_blocks_with_unitary_timing(tree)

    visitor = IterateGatesAndLoopsVisitor()
    return visitor.visit(tree)


class IterateGatesAndLoopsVisitor(ParseTreeVisitor):
    """Parse tree visitor that takes a simplified Jaqal parse tree and returns a list of JaqalObject's."""

    def visit_program(self, header_statements, body_statements):
        return body_statements

    def visit_register_statement(self, array_declaration):
        return None

    def visit_map_statement(self, target, source):
        raise ValueError(f"Map statements should have been removed by now")

    def visit_let_statement(self, identifier, number):
        raise ValueError(f"Let statements should have been removed by now")

    def visit_gate_statement(self, gate_name, gate_args):
        return Gate(gate_name, gate_args)

    def visit_macro_definition(self, name, arguments, block):
        raise ValueError(f"Macro definition should have been removed by now")

    def visit_loop_statement(self, repetition_count, block):
        return Loop(repetition_count, block)

    def visit_sequential_gate_block(self, statements):
        return SequentialGateBlock(statements)

    def visit_parallel_gate_block(self, statements):
        return ParallelGateBlock(statements)

    def visit_array_declaration(self, identifier, size):
        return None

    def visit_array_element(self, identifier, index):
        return (identifier, index)

    def visit_array_slice(self, identifier, index_slice):
        return None

    def visit_let_identifier(self, identifier):
        return identifier

    def visit_let_or_map_identifier(self, identifier):
        return identifier


# Define the objects we return when iterating over gates. Having the `is_*` methods really just allows us
# to check the type without having to import the classes into the user's namespace. I'm not sure if it's a
# good idea but it seems like one.

class JaqalObject:
    """Base class for objects to be returned from parsing Jaqal."""

    # Class-level variables to be selectively overridden by derived classes.
    is_gate = False
    is_loop = False
    is_parallel_gate_block = False
    is_sequential_gate_block = False

    @property
    def is_gate_block(self):
        return self.is_parallel_gate_block or self.is_sequential_gate_block


class Gate(JaqalObject):

    is_gate = True

    def __init__(self, gate_name, gate_args):
        # gate_args are either numbers or (register_name, index) tuples.
        self.gate_name = gate_name
        self.gate_args = gate_args

    def __eq__(self, other):
        return self.gate_name == other.gate_name and self.gate_args == other.gate_args


class Loop(JaqalObject):

    is_loop = True

    def __init__(self, repetition_count, block):
        self.repetition_count = repetition_count
        self.block = block

    def __eq__(self, other):
        return self.repetition_count == other.repetition_count and self.block == other.block


class ParallelGateBlock(JaqalObject):

    is_parallel_gate_block = True

    def __init__(self, gates):
        self.gates = gates

    def __eq__(self, other):
        return self.gates == other.gates


class SequentialGateBlock(JaqalObject):

    is_sequential_gate_block = True

    def __init__(self, gates):
        self.gates = gates

    def __eq__(self, other):
        return self.gates == other.gates
