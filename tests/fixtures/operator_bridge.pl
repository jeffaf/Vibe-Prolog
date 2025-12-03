:- module(operator_bridge, [op(600, xfx, <<<), bridge_marker/0]).
:- use_module('operator_source.pl', [source_marker/0]).

bridge_marker :- source_marker.
