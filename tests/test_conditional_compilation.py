import pytest

from vibeprolog import PrologInterpreter
from vibeprolog.exceptions import PrologThrow


def test_if_true_loads_block():
    prolog = PrologInterpreter()
    prolog.consult_string(
        """
        :- if(true).
        active_fact.
        :- endif.
        """
    )

    assert prolog.has_solution("active_fact")


def test_if_false_skips_block():
    prolog = PrologInterpreter()
    prolog.consult_string(
        """
        :- if(fail).
        skipped_fact.
        :- endif.
        """
    )

    assert not prolog.has_solution("skipped_fact")
    assert not prolog.has_solution("current_predicate(skipped_fact/0)")


def test_if_else_true_branch_used():
    prolog = PrologInterpreter()
    prolog.consult_string(
        """
        :- if(true).
        chosen(yes).
        :- else.
        chosen(no).
        :- endif.
        """
    )

    assert prolog.has_solution("chosen(yes)")
    assert not prolog.has_solution("chosen(no)")


def test_if_else_false_branch_used():
    prolog = PrologInterpreter()
    prolog.consult_string(
        """
        :- if(fail).
        branch(false).
        :- else.
        branch(true).
        :- endif.
        """
    )

    assert prolog.has_solution("branch(true)")
    assert not prolog.has_solution("branch(false)")


def test_nested_conditionals_respect_parent_state():
    prolog = PrologInterpreter()
    prolog.consult_string(
        """
        :- if(fail).
        outer_inactive.
        :- if(true).
        nested_active.
        :- endif.
        :- else.
        outer_active.
        :- endif.
        """
    )

    assert prolog.has_solution("outer_active")
    assert not prolog.has_solution("outer_inactive")
    assert not prolog.has_solution("nested_active")


def test_condition_can_query_current_predicate():
    prolog = PrologInterpreter()
    prolog.consult_string(
        """
        :- if(current_predicate(member/2)).
        uses_member(X) :- member(X, [1, 2]).
        :- else.
        uses_member(none).
        :- endif.
        """
    )

    assert prolog.has_solution("uses_member(1)")
    assert not prolog.has_solution("uses_member(none)")


def test_else_without_if_errors():
    prolog = PrologInterpreter()

    with pytest.raises(PrologThrow):
        prolog.consult_string(":- else.")


def test_endif_without_if_errors():
    prolog = PrologInterpreter()

    with pytest.raises(PrologThrow):
        prolog.consult_string(":- endif.")


def test_multiple_else_in_same_block_errors():
    prolog = PrologInterpreter()
    prolog_code = """
    :- if(true).
    a.
    :- else.
    b.
    :- else.
    c.
    :- endif.
    """

    with pytest.raises(PrologThrow):
        prolog.consult_string(prolog_code)


def test_unclosed_if_errors():
    prolog = PrologInterpreter()

    with pytest.raises(PrologThrow):
        prolog.consult_string(":- if(true). fact.")
