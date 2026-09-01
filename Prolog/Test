
my_member(X, [X | _]).
my_member(X, [_ | T]) :-
    my_member(X, T).

not_in(_, []).
not_in(X, [H | T]) :-
    X \= H,
    not_in(X, T).

my_reverse(L, R) :-
    my_rev_acc(L, [], R).

my_rev_acc([], Acc, Acc).
my_rev_acc([H | T], Acc, R) :-
    my_rev_acc(T, [H | Acc], R).

edge_weight([], _, _, _) :- fail.
edge_weight([edge(A, B, W) | _], A, B, W).
edge_weight([_ | T], A, B, W) :-
    edge_weight(T, A, B, W).

findPath(Graph, Start, End, Path, Length) :-
    travel(Graph, Start, End, [Start], RevPath, 0, Length),
    my_reverse(RevPath, Path).

travel(_, Node, Node, Path, Path, Length, Length).

travel(Graph, Current, Dest, Visited, Path, AccLen, Length) :-
    edge_weight(Graph, Current, Next, W),
    not_in(Next, Visited),
    NewAcc is AccLen + W,
    travel(Graph, Next, Dest, [Next | Visited], Path, NewAcc, Length).

findAndPrint(Graph, Start, End) :-
    findPath(Graph, Start, End, Path, Length),
    write('Path = '), write(Path), nl,
    write('Length = '), write(Length), nl, nl,
    fail.
findAndPrint(_, _, _) :-
    write('--- No more paths. ---'), nl.


?- G = [edge(1,2,5), edge(1,3,2), edge(2,3,7), edge(2,4,8),
        edge(3,4,3), edge(3,5,4), edge(4,6,4), edge(5,6,5)],
   findAndPrint(G, 1, 6).