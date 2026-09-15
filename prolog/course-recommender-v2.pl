% file: planes_puzzle.pl
% -----------------------------------------
% اشخاص/رنگ‌ها/مسافت‌ها
people([arman, elham, hananeh, amir, sara]).
colors([black, green, pink, silver, white]).
dists([5, 8, 14, 16, 17]).

% همه متفاوت
all_diff([]).
all_diff([H|T]) :- maplist(dif(H), T), all_diff(T).

% راه‌حل: ترتیب آرمان، الهام، حنانه، امیر، سارا
% X1..X5 رنگ‌ها، Y1..Y5 مسافت‌ها
solution(X1,X2,X3,X4,X5,  Y1,Y2,Y3,Y4,Y5) :-
    colors(Cs0),  permutation([X1,X2,X3,X4,X5], Cs0),
    dists(Ds0),   permutation([Y1,Y2,Y3,Y4,Y5], Ds0),

    % یکتایی (هم‌پوشانی برای اطمینان؛ permutation خودش تضمین می‌کند)
    all_diff([X1,X2,X3,X4,X5]),
    all_diff([Y1,Y2,Y3,Y4,Y5]),

    % --- قیود مسئله ---

    % سارا 17 متر
    Y5 = 17,

    % حنانه 14 متر
    Y3 = 14,

    % هواپیمای 8 متری نقره‌ای نبود
    % (رنگ متناظرِ مسافت 8 را پیدا کن و نقره‌ای نباشد)
    once( ( nth1(I8, [Y1,Y2,Y3,Y4,Y5], 8),
            nth1(I8, [X1,X2,X3,X4,X5], C8),
            dif(C8, silver) ) ),

    % هواپیمای 5 متری، صورتی بود
    once( ( nth1(I5, [Y1,Y2,Y3,Y4,Y5], 5),
            nth1(I5, [X1,X2,X3,X4,X5], pink) ) ),

    % مشکی بیشتر از صورتی پرواز کرد
    nth1(Ib, [X1,X2,X3,X4,X5], black),
    nth1(Ip, [X1,X2,X3,X4,X5], pink),
    nth1(Ib, [Y1,Y2,Y3,Y4,Y5], Db),
    nth1(Ip, [Y1,Y2,Y3,Y4,Y5], Dp),
    Db > Dp,

    % طرح حنانه بیشتر از الهام
    Y3 > Y2,

    % سبز یا برای امیر یا برای الهام
    ( X4 = green ; X2 = green ),

    % فقط یکی از «امیر» یا «سارا» سفید است (دقیقاً یکی)
    ( (X4 = white, dif(X5, white))
    ; (X5 = white, dif(X4, white)) ).

% چاپ خروجی به فرمتی شبیه تمپلیت شما
print_solution :-
    solution(X1,X2,X3,X4,X5,  Y1,Y2,Y3,Y4,Y5),
    write(arman),   write("  color: "), write(X1), write("  dist: "), write(Y1), nl,
    write(elham),   write("  color: "), write(X2), write("  dist: "), write(Y2), nl,
    write(hananeh), write("  color: "), write(X3), write("  dist: "), write(Y3), nl,
    write(amir),    write("  color: "), write(X4), write("  dist: "), write(Y4), nl,
    write(sara),    write("  color: "), write(X5), write("  dist: "), write(Y5), nl.
