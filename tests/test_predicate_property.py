"""Tests for predicate_property/2 ISO compliance.

This test module verifies that predicate_property/2 returns simple atoms
for property names as required by ISO Prolog, not compound terms.
"""

import pytest

from vibeprolog import PrologInterpreter


class TestPredicatePropertyFormat:
    """Test that predicate_property/2 returns ISO-compliant atom properties."""

    def test_builtin_returns_atom(self):
        """built_in property should be returned as simple atom."""
        prolog = PrologInterpreter()
        result = prolog.query_once("predicate_property(append(_,_,_), P)")
        assert result is not None
        assert result["P"] == "built_in"

    def test_static_returns_atom(self):
        """static property should be returned as simple atom, not static(pred/arity)."""
        prolog = PrologInterpreter()
        results = list(prolog.query("predicate_property(append(_,_,_), P)"))
        props = [r["P"] for r in results]
        assert "static" in props
        # Verify it's a simple string/atom, not a dict or compound
        for prop in props:
            assert isinstance(prop, str), f"Property should be string, got {type(prop)}: {prop}"

    def test_dynamic_returns_atom(self):
        """dynamic property should be returned as simple atom."""
        prolog = PrologInterpreter()
        prolog.consult_string(":- dynamic(foo/1). foo(a).")
        result = prolog.query_once("predicate_property(foo(_), P)")
        assert result is not None
        assert result["P"] == "dynamic"

    def test_multifile_returns_atom(self):
        """multifile property should be returned as simple atom."""
        prolog = PrologInterpreter()
        prolog.consult_string(":- dynamic(bar/1). :- multifile(bar/1). bar(x).")
        results = list(prolog.query("predicate_property(bar(_), P)"))
        props = [r["P"] for r in results]
        assert "multifile" in props

    def test_discontiguous_returns_atom(self):
        """discontiguous property should be returned as simple atom."""
        prolog = PrologInterpreter()
        prolog.consult_string(":- discontiguous(baz/1). baz(1). other(x). baz(2).")
        results = list(prolog.query("predicate_property(baz(_), P)"))
        props = [r["P"] for r in results]
        assert "discontiguous" in props


class TestPredicatePropertyChecking:
    """Test checking specific properties with bound second argument."""

    def test_check_dynamic_succeeds(self):
        """predicate_property(Pred, dynamic) should succeed for dynamic predicates."""
        prolog = PrologInterpreter()
        prolog.consult_string(":- dynamic(test_dyn/1). test_dyn(1).")
        assert prolog.has_solution("predicate_property(test_dyn(_), dynamic)")

    def test_check_dynamic_fails_for_static(self):
        """predicate_property(Pred, dynamic) should fail for static predicates."""
        prolog = PrologInterpreter()
        prolog.consult_string("test_static(1).")
        assert not prolog.has_solution("predicate_property(test_static(_), dynamic)")

    def test_check_static_succeeds(self):
        """predicate_property(Pred, static) should succeed for static predicates."""
        prolog = PrologInterpreter()
        prolog.consult_string("my_static(42).")
        assert prolog.has_solution("predicate_property(my_static(_), static)")

    def test_check_static_fails_for_dynamic(self):
        """predicate_property(Pred, static) should fail for dynamic predicates."""
        prolog = PrologInterpreter()
        prolog.consult_string(":- dynamic(my_dyn/1). my_dyn(1).")
        assert not prolog.has_solution("predicate_property(my_dyn(_), static)")

    def test_check_builtin_succeeds(self):
        """predicate_property(Pred, built_in) should succeed for builtins."""
        prolog = PrologInterpreter()
        assert prolog.has_solution("predicate_property(member(_,_), built_in)")
        assert prolog.has_solution("predicate_property(append(_,_,_), built_in)")
        assert prolog.has_solution("predicate_property(length(_,_), built_in)")

    def test_check_builtin_fails_for_user(self):
        """predicate_property(Pred, built_in) should fail for user predicates."""
        prolog = PrologInterpreter()
        prolog.consult_string("user_pred(x).")
        assert not prolog.has_solution("predicate_property(user_pred(_), built_in)")


class TestPredicatePropertyEnumeration:
    """Test enumerating all properties of a predicate."""

    def test_enumerate_builtin_properties(self):
        """Builtins should enumerate both built_in and static."""
        prolog = PrologInterpreter()
        results = list(prolog.query("predicate_property(append(_,_,_), P)"))
        props = set(r["P"] for r in results)
        assert "built_in" in props
        assert "static" in props

    def test_enumerate_dynamic_properties(self):
        """Dynamic predicates should enumerate dynamic but not static."""
        prolog = PrologInterpreter()
        prolog.consult_string(":- dynamic(dyn_test/1). dyn_test(a).")
        results = list(prolog.query("predicate_property(dyn_test(_), P)"))
        props = set(r["P"] for r in results)
        assert "dynamic" in props
        assert "static" not in props

    def test_enumerate_multiple_properties(self):
        """Predicates with multiple declarations should enumerate all."""
        prolog = PrologInterpreter()
        prolog.consult_string(
            ":- dynamic(multi/1). :- multifile(multi/1). :- discontiguous(multi/1). multi(1)."
        )
        results = list(prolog.query("predicate_property(multi(_), P)"))
        props = set(r["P"] for r in results)
        assert "dynamic" in props
        assert "multifile" in props
        assert "discontiguous" in props
        assert "static" not in props


class TestPredicatePropertyWithIndicator:
    """Test predicate_property with Name/Arity indicator format."""

    def test_indicator_format_works(self):
        """predicate_property(name/arity, Prop) should work."""
        prolog = PrologInterpreter()
        result = prolog.query_once("predicate_property(append/3, P)")
        assert result is not None
        assert result["P"] == "built_in"

    def test_indicator_dynamic(self):
        """Dynamic predicate with indicator format."""
        prolog = PrologInterpreter()
        prolog.consult_string(":- dynamic(ind_test/2). ind_test(a, b).")
        assert prolog.has_solution("predicate_property(ind_test/2, dynamic)")

    def test_indicator_static(self):
        """Static predicate with indicator format."""
        prolog = PrologInterpreter()
        prolog.consult_string("static_ind(1).")
        assert prolog.has_solution("predicate_property(static_ind/1, static)")


class TestPredicatePropertyEdgeCases:
    """Test edge cases for predicate_property/2."""

    def test_nonexistent_predicate_defaults_to_static(self):
        """Non-existent predicates default to static property.

        This is consistent with Prolog semantics where any predicate indicator
        that could exist is considered static by default (until declared dynamic).
        """
        prolog = PrologInterpreter()
        result = prolog.query_once("predicate_property(nonexistent_pred(_), P)")
        # Non-existent predicates are considered static by default
        assert result is not None
        assert result["P"] == "static"
        # Should not be built_in
        assert not prolog.has_solution("predicate_property(nonexistent_pred(_), built_in)")

    def test_atom_predicate(self):
        """Test with zero-arity predicate (atom)."""
        prolog = PrologInterpreter()
        # true/0 is a built-in
        assert prolog.has_solution("predicate_property(true, built_in)")

    def test_cut_builtin(self):
        """Cut should be recognized as built-in."""
        prolog = PrologInterpreter()
        result = prolog.query_once("predicate_property(!/0, P)")
        assert result is not None
        assert result["P"] == "built_in"
