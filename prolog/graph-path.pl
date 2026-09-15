% edge lookup: gets weight between two nodes
edge_weight(Graph, A, B, W) :-
    member(edge(A,B,W), Graph).

% findPath(Graph, Start, End, Path, Length)
findPath(Graph, Start, End, Path, Length) :-
    travel(Graph, Start, End, [Start], RevPath, 0, Length),
    reverse(RevPath, Path).

% Base case: reached destination
travel(_, Node, Node, Path, Path, Length, Length).

% Recursive expansion
travel(Graph, Current, Dest, Visited, Path, AccLen, Length) :-
    edge_weight(Graph, Current, Next, W),
    \+ member(Next, Visited),               % avoid cycles
    NewAcc is AccLen + W,
    travel(Graph, Next, Dest, [Next|Visited], Path, NewAcc, Length).
