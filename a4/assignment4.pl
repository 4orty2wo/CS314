/* YOUR CODE HERE (Prolem 1, delete the following line) */
range(S,E,M) :-
	S=<M,
	M=<E.

?- range(1,2,2).
?- not(range(1,2,3)).

/* YOUR CODE HERE (Prolem 2, delete the following line) */
reverseL(X,RevX) :-
	reverse(RevX, X).

?- reverseL([],X).
?- reverseL([1,2,3],X).
?- reverseL([a,b,c],X).

/* YOUR CODE HERE (Prolem 3, delete the following line) */
memberL(X,[H|T]) :-	
	X = H;
	memberL(X,T).

?- not(memberL(1, [])).
?- memberL(1,[1,2,3]).
?- not(memberL(4,[1,2,3])).
?- memberL(X, [1,2,3]).

/* YOUR CODE HERE (Prolem 4, delete the following line) */
zip(Xs, Ys, XYs) :- false.

?- zip([1,2],[a,b],Z).
?- zip([a,b,c,d], [1,X,y], Z).
?- zip([a,b,c],[1,X,y,z], Z).
?- length(A,2), length(B,2), zip(A, B, [1-a, 2-b]).

/* YOUR CODE HERE (Prolem 5, delete the following line) */
insert(X, Ys, Zs) :- false.

insert (X, [], [X]):- !.
insert(X, [H|T], [X, H|T]):- 
	X=<H, 
	!.
insert(X, [H|T], [H|TT]):- 
	insert(X, T, TT).

?- insert(3, [2,4,5], L).
?- insert(3, [1,2,3], L).
?- not(insert(3, [1,2,4], [1,2,3])).
?- insert(3, L, [2,3,4,5]).
?- insert(9, L, [1,3,6,9]).
?- insert(3, L, [1,3,3,5]).

/* YOUR CODE HERE (Prolem 6, delete the following line) */
remove_duplicates([H|T],L2) :-
	memberL(H, T),
	remove_duplicates(T, L2).

?- remove_duplicates([1,2,3,4,2,3],X).
?- remove_duplicates([1,4,5,4,2,7,5,1,3],X).
?- remove_duplicates([], X).

/* YOUR CODE HERE (Prolem 7, delete the following line) */
intersectionL(L1,L2,L3) :- 
	intersectionL([], [], []) :- !.
	intersectionL([], _, []) :-!.
	intersectionL(_, [], []) :-!.
intersectionL([_|T],L2, L3) :-
	intersectionL(T, L2, L3).
intersectionL( [H|T], L2, [H|TTT]) :-
	memberL(H, L2),
	intersectionL(T, L2, TTT), !.

?- intersectionL([1,2,3,4],[1,3,5,6],[1,3]).
?- intersectionL([1,2,3,4],[1,3,5,6],X).
?- intersectionL([1,2,3],[4,3],[3]).

/* YOUR CODE HERE (Prolem 8, delete the following line) */
prefix(P,L) :- append(P,_,L).
suffix(S,L) :- append(_,S,L).

partition(L,P,S) :- false.

?- partition([a],[a],[]).
?- partition([1,2,3],[1],[2,3]).
?- partition([a,b,c,d],X,Y).

/* YOUR CODE HERE (Prolem 9, delete the following line) */
merge(X,Y,Z) :-
	merge([], [], []):- !.
	merge([], Y, Z) :- !.
	merge(X, [], Z) :- !.
merge([X|T], [Y|TT], Z) :- X > Y,
	merge(T, TT, tempZ),
	append([Y],tempZ, Z), !.
merge(T, [Y|TT], Z :- X < Y,
	merge(T, [Y|TT]. tempZ),
	append([X],tempZ,Z], !.


?- merge([],[1],[1]).
?- merge([1],[],[1]).
?- merge([1,3,5],[2,4,6],X).

/* YOUR CODE HERE (Prolem 10, delete the following line) */
mergesort(L,SL) :- false.

?- mergesort([3,2,1],X).
?- mergesort([1,2,3],Y).
?- mergesort([],Z).
