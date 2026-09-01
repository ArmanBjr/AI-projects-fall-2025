%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Utilities
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
my_member(X, [X | _]).
my_member(X, [_ | T]) :- my_member(X, T).

not_member(_, []).
not_member(X, [H | T]) :- X \= H, not_member(X, T).

my_reverse(L, R) :- my_rev_acc(L, [], R).
my_rev_acc([], Acc, Acc).
my_rev_acc([H | T], Acc, R) :- my_rev_acc(T, [H | Acc], R).

append([], L, L).
append([H | T], L, [H | R]) :- append(T, L, R).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Edge lookup
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
edge_w([], _, _, _) :- fail.
edge_w([edge(A,B,W) | _], A, B, W).
edge_w([_ | T], A, B, W) :- edge_w(T, A, B, W).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find all neighbors manually (no findall)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
neighbors(_, _, [], []).
neighbors(Graph, Node, [edge(Node,B,W) | T], [(B, W) | R]) :-
    neighbors(Graph, Node, T, R).
neighbors(Graph, Node, [_ | T], R) :-
    neighbors(Graph, Node, T, R).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Dijkstra core
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
dijkstra(Graph, Start, Result) :-
    dijkstra_loop(Graph, [(Start,0,[Start])], [], Result).

% When queue is empty ? done
dijkstra_loop(_, [], Visited, Visited).

dijkstra_loop(Graph, [(Node,Dist,Path) | Rest], Visited, Result) :-

    ( my_member((Node,_), Visited) ->
        dijkstra_loop(Graph, Rest, Visited, Result)
    ;
        neighbors(Graph, Node, Graph, Nbs),
        add_new_paths(Nbs, Node, Dist, Path, Rest, NewQueue),
        dijkstra_loop(Graph, NewQueue, [(Node,Dist,Path) | Visited], Result)
    ).

% Add neighbors manually
add_new_paths([], _, _, _, Q, Q).
add_new_paths([(N,W) | T], Node, Dist, Path, Q, R) :-
    N \= Node,  % avoid self-loops
    NewDist is Dist + W,
    add_new_paths(T, Node, Dist, Path, [(N,NewDist,[N|Path]) | Q], R).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Printing results
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print_paths([]).
print_paths([(Node, Dist, RevPath) | T]) :-
    my_reverse(RevPath, Path),
    write('Node: '), write(Node), nl,
    write('Dist: '), write(Dist), nl,
    write('Path: '), write(Path), nl, nl,
    print_paths(T).

run(Graph, Start) :-
    dijkstra(Graph, Start, Result),
    print_paths(Result).


?- G = [edge(1,2,5), edge(1,3,2), edge(2,3,7), edge(2,4,8),
        edge(3,4,3), edge(3,5,4), edge(4,6,4), edge(5,6,5)],
   run(G, 1).