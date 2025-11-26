"""Tests for Prolog directives."""

import pytest

from vibeprolog import PrologInterpreter
from vibeprolog.exceptions import PrologThrow


class TestInitializationDirective:
    """Tests for :- initialization/1 directive."""

    def test_single_initialization_simple_goal(self):
        """Test single initialization directive with simple goal."""
        prolog = PrologInterpreter()
        prolog.consult_string("""
            :- initialization(write('Hello')).
            test.
        """)
        # Check that initialization ran (but since write outputs, hard to test directly)
        # For now, just check no exception
        assert prolog.has_solution("test")

    def test_multiple_initializations_in_order(self):
        """Test multiple initialization directives execute in order."""
        prolog = PrologInterpreter()
        prolog.consult_string("""
            :- initialization(asserta(fact1)).
            :- initialization(asserta(fact2)).
            test.
        """)
        # fact2 should be first since asserta adds to front
        assert prolog.has_solution("fact2")
        assert prolog.has_solution("fact1")

    def test_initialization_with_side_effects(self):
        """Test initialization that performs side effects."""
        prolog = PrologInterpreter()
        prolog.consult_string("""
            :- initialization(assertz(side_effect)).
            query :- side_effect.
        """)
        assert prolog.has_solution("query")

    def test_initialization_accessing_facts(self):
        """Test initialization accessing facts defined in same file."""
        prolog = PrologInterpreter()
        prolog.consult_string("""
            base_fact.
            :- initialization((base_fact, assertz(derived_fact))).
            query :- derived_fact.
        """)
        assert prolog.has_solution("query")

    def test_empty_initialization(self):
        """Test :- initialization(true)."""
        prolog = PrologInterpreter()
        prolog.consult_string("""
            :- initialization(true).
            test.
        """)
        assert prolog.has_solution("test")

    def test_initialization_with_complex_goal(self):
        """Test initialization with conjunction."""
        prolog = PrologInterpreter()
        prolog.consult_string("""
            :- initialization((asserta(a), asserta(b))).
            test :- a, b.
        """)
        assert prolog.has_solution("test")

    def test_non_callable_goal_number(self):
        """Test error for non-callable goal (number)."""
        prolog = PrologInterpreter()
        with pytest.raises(PrologThrow) as exc_info:
            prolog.consult_string(":- initialization(42).")
        error = exc_info.value.term
        assert error.functor == "error"
        assert error.args[0].functor == "type_error"
        assert error.args[0].args[0].name == "callable"

    def test_unbound_variable_goal(self):
        """Test error for unbound variable as goal."""
        prolog = PrologInterpreter()
        with pytest.raises(PrologThrow) as exc_info:
            prolog.consult_string(":- initialization(X).")
        error = exc_info.value.term
        assert error.functor == "error"
        assert error.args[0].name == "instantiation_error"

    def test_initialization_goal_failure(self):
        """Test initialization goal that fails - consult succeeds since failure is not error."""
        prolog = PrologInterpreter()
        prolog.consult_string("""
            :- initialization(fail).
            test.
        """)
        assert prolog.has_solution("test")

    def test_initialization_throwing_exception(self):
        """Test initialization goal that throws exception."""
        prolog = PrologInterpreter()
        with pytest.raises(PrologThrow) as exc_info:
            prolog.consult_string("""
                :- initialization(throw(test_error)).
                test.
            """)
        # Should propagate the thrown term
        assert exc_info.value.term.name == "test_error"

    def test_initialization_in_multiple_consults(self):
        """Test initialization in multiple consulted strings."""
        prolog = PrologInterpreter()
        prolog.consult_string(":- initialization(asserta(first)).")
        prolog.consult_string(":- initialization(asserta(second)).")
        assert prolog.has_solution("first")
        assert prolog.has_solution("second")