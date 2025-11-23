"""Dummy built-ins used to validate the modular registration infrastructure."""

from __future__ import annotations

from prolog.unification import Substitution


class DummyBuiltins:
    """Dummy built-ins for testing infrastructure."""

    @staticmethod
    def dummy_test(_args, subst: Substitution, engine):
        """dummy_test/0 - Always succeeds for testing and returns the current substitution."""
        assert engine is not None
        return subst

    @staticmethod
    def register(registry, engine_ref=None):
        """Register dummy built-ins in the provided registry."""
        from prolog.builtins import register_builtin
        register_builtin(registry, "dummy_test", 0, DummyBuiltins.dummy_test)
