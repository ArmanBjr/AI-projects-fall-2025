select(ali, os, drnaghib).
grade(ali, os, 17).
select(ali, db, drkahani).
grade(ali, db, 19).
select(ali, ai, drharati).
grade(ali, ai, 20).
ta(ali, some_course_kahani, drkahani).

gt(N, M) :- N > M.

different(X, Y) :- dif(X, Y).

recommend(drnaghib, X) :-
    select(X, Y, drnaghib),
    grade(X, Y, N),
    gt(N, 18).

recommend(drkahani, X) :-
    select(X, Y1, drkahani),
    select(X, Y2, drkahani),
    different(Y1, Y2).

recommend(drharati, X) :-
    select(X, _Y1, drharati),
    ta(X, _Y2, drharati).

ta(X, Y, drharati) :-
    select(X, Y, drharati),
    grade(X, Y, 20).


who_recommends(Student, Prof) :-
    recommend(Prof, Student).