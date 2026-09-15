% اگر لیست اول خالی است، نتیجه همان لیست دوم است
append([], L, L).

% در غیر این صورت، سرِ لیست اول را به ابتدای خروجی اضافه کن
append([H|T], L2, [H|R]) :-
    append(T, L2, R).

% اگر X سرِ لیست باشد
member(X, [X|_]).

% در غیر این صورت در بقیه لیست جستجو کن
member(X, [_|T]) :-
    member(X, T).

length([], 0).

length([_|T], N) :-
    length(T, N1),
    N is N1 + 1.


reverse([], []).

reverse([H|T], R) :-
    reverse(T, RevT),
    append(RevT, [H], R).

max_list([X], X).

max_list([H|T], Max) :-
    max_list(T, TailMax),
    (H > TailMax -> Max = H ; Max = TailMax).

sum_list([], 0).

sum_list([H|T], S) :-
    sum_list(T, Rest),
    S is H + Rest.

factorial(0, 1).

factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.

even(X) :- 0 is X mod 2.
odd(X)  :- 1 is X mod 2.

flatten([], []).

flatten([H|T], flatList) :-
    flatten(H, FlatH),
    flatten(T, FlatT),
    append(FlatH, FlatT, flatList).

flatten(X, [X]) :-
    \+ is_list(X).


count(_, [], 0).

count(X, [X|T], N) :-
    count(X, T, N1),
    N is N1 + 1.

count(X, [_|T], N) :-
    count(X, T, N).




% حالت پایه: لیست خالی، مجموعه خالی
list_to_set([], []).

% اگر Head در Tail نیست، آن را اضافه کن
list_to_set([H|T], [H|R]) :-
    \+ member(H, T),         % اگر H در بقیه نیست
    list_to_set(T, R).

% اگر Head تکراری است، آن را رد کن
list_to_set([H|T], R) :-
    member(H, T),
    list_to_set(T, R).

list_to_sorted_set(List, Set) :-
    sort(List, Set).

% ---------- دامنه ----------
person(arman). person(elham). person(hanane). person(amir). person(sara).
color(black). color(green). color(pink). color(silver). color(white).
dist(5). dist(8). dist(14). dist(16). dist(17).

% ---------- همه متفاوت ----------
all_diff([]).
all_diff([H|T]) :- maplist(dif(H), T), all_diff(T).

% ---------- نگاشت یک‌به‌یک (مدل‌سازی تخصیص‌ها) ----------
solution(C1,D1, C2,D2, C3,D3, C4,D4, C5,D5) :-
    % آرمان/الهام/حنانه/امیر/سارا
    color(C1), dist(D1),
    color(C2), dist(D2),
    color(C3), dist(D3),
    color(C4), dist(D4),
    color(C5), dist(D5),

    all_diff([C1,C2,C3,C4,C5]),
    all_diff([D1,D2,D3,D4,D5]),

    % --- قیود مسئله (اینجا بنویس) ---
    % مثال‌ها:
    D5 = 17,                 % سارا 17
    D3 = 14,                 % حنانه 14
    D1 = 5, C1 = pink,       % 5 متر صورتی (فرض: نفر اول آرمان)
    % سیاه > صورتی:
    nth1(I_black,[C1,C2,C3,C4,C5], black),
    nth1(I_pink, [C1,C2,C3,C4,C5], pink),
    nth1(I_black,[D1,D2,D3,D4,D5], DB),
    nth1(I_pink, [D1,D2,D3,D4,D5], DP),
    DB > DP,
    % ... سایر قیود ...

    true.

% ---------- چاپ خروجی ----------
print_solution :-
    solution(C1,D1, C2,D2, C3,D3, C4,D4, C5,D5),
    writeln(arman  - C1 - D1),
    writeln(elham  - C2 - D2),
    writeln(hanane - C3 - D3),
    writeln(amir   - C4 - D4),
    writeln(sara   - C5 - D5).
