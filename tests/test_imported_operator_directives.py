import pytest

from vibeprolog import PrologInterpreter
from vibeprolog.parser import extract_op_directives


def test_clpz_operator_directives_loaded_before_parsing():
    prolog = PrologInterpreter()
    code = """
    :- use_module(library(clpz)).
    clpz_goal(X, Y) :- X in 0..1, Y #= X.
    """

    local_ops = extract_op_directives(code)
    imported_ops = prolog._collect_imported_operators(code, "string:1", local_ops)
    directive_ops = imported_ops + local_ops

    operator_names = {(spec, name) for _, spec, name in directive_ops}
    assert ("xfx", "#=") in operator_names
    assert any(name == ".." for _, name in operator_names)

    prolog.parser.parse(code, "consult/1", directive_ops=directive_ops)


def test_nested_imported_operator_directives_are_applied():
    prolog = PrologInterpreter()
    prolog.consult("tests/fixtures/operator_consumer.pl")

    operator_info = prolog.operator_table.lookup("<<<", "xfx")
    assert operator_info is not None

    consumer_module = prolog.modules.get("operator_consumer")
    assert consumer_module is not None
    assert ("uses_op", 2) in consumer_module.predicates
