# Built-in Predicate Architecture (Phase 2)

Built-in predicates are being migrated toward a modular structure while keeping
existing behavior intact.

## Old Style (Temporary)
- Built-ins implemented as `PrologEngine` methods
- Registered in `_register_*_builtins()` methods during engine initialization

## New Style (Target)
- Built-ins implemented in `prolog/builtins/*.py` modules
- Each module exposes a class with static predicate handlers and a `register()`
  method adhering to the :class:`prolog.builtins.BuiltinPredicate` protocol
- Modules will be registered from `PrologEngine._build_builtin_registry()`

## Adding a New Built-in (Phase 3+)
1. Choose or create an appropriate module in `prolog/builtins/`
2. Implement the predicate handler using the `(args, subst, engine)` signature
3. Register it within the module's `register()` method via
   `prolog.builtins.register_builtin`
4. Add tests in `tests/` validating the new predicate
