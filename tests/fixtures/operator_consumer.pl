:- module(operator_consumer, [uses_op/2, bridge_marker/0]).
:- use_module('operator_bridge.pl').

uses_op(X, Y) :- X <<< Y.
