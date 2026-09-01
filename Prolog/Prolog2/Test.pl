member(Element, [Element | Tail]).

member(Element, [Head | Tail]) :-
	member(Element, Tail).


union([],[],[]).
union(List1,[],List1).


union(List1, [Head2|Tail2], [Head2|Output]):-
    not(member(Head2,List1)), union(List1,Tail2,Output).


union(List1, [Head2|Tail2], Output):-
    member(Head2,List1), union(List1,Tail2,Output).  



?- union([5, 9, 1, 6, 4], [8, 6, 2, 5], U), write(U).
