%*
Author: Roland Kaminski

Encoding to calculate a permutation of a given portfolio on multiple cores to
minimize overall runtime.  This encoding uses aggregates with negative weights
to determine the fastest core.  Apart from this, no further optimizations are
applied.  Further optimizations like in roland-permutation-m.lp should be
applicable here too.  
*%

% transforming of old format
slice(C,S,T)     :- solverTimeCore(S,T,C).
slice(C,S)		 :- slice(C,S,_).

% auxiliary predicates
solver(C,S)      :- slice(C,S).
instance(I)      :- time(I,S,_), solver(_,S).
core(C)          :- slice(C,_,_).
cores(N)         :- N := { core(C) }.
solvers(C,N)     :- core(C), N := { solver(C,_) }.
first(C,M)       :- core(C), M := #min [ solver(C,S) = S ].
solved(C,S,I)    :- time(I,S,T), slice(C,S,TS), T <= TS.
solved(C,I)      :- solved(C,_,I).
capped(C,I,S,T)  :- time(I,S,T), solved(C,S,I).
capped(C,I,S,TS) :- time(I,S,T), slice(C,S,TS), T >  TS, solved(C,I).
capped(C,I,S,K)  :- first(C,S), kappa(K), instance(I), not solved(C,I).
capped(C,I,S,0)  :- solver(C,S), not first(C,S), instance(I), not solved(C,I).
capped(I,S,T)    :- capped(_,I,S,T).
timeouts(C,I,N)  :- core(C), instance(I), N = #count { not solved(C,S,I) : solver(C,S) }.

% guess an ordering
1 { order(C,S,U) : solver(C,S) } 1 :- solvers(C,N), U = 1..N.
1 { order(C,S,U) : solvers(C,N) : U = 1..N } 1 :- solver(C,S).

% mark at which point an instance is solved
solvedAt(C,I,U+1) :- slice(C,S,TS), time(I,S,T), T <= TS, order(C,S,U).
solvedAt(C,I,U+2) :- timeouts(C,I,U), solvers(C,N), U < N.
solvedAt(C,I,U+1) :- solvedAt(C,I,U), solvers(C,N), U <= N.

% linear search for minimum
layer(1,N)     :- cores(N).
layer(L+1,N/2) :- layer(L,N), N > 1.

offset(L,2*(1..N/2)-1) :- layer(L,N).

mark(1,C,I,S,T) :- capped(C,I,S,T), not solvedAt(C,I,U), order(C,S,U), solved(C,I).
mark(1,C,I,S,T) :- capped(C,I,S,T), not solved(C,I).

less(L,I,O) :- instance(I), layer(L,O), offset(L,O). % handle odd cases
less(L,I,O) :- not layer(L,O), offset(L,O), instance(I), [ mark(L,O,I,S1,T1) : capped(I,S1,T1) = T1, mark(L,O+1,I,S2,T2) : capped(I,S2,T2) = -T2  ] 0.

% choose the smaller one
mark(L,(O+1)/2,I,S,T) :- layer(L,_), less(L-1,I,O), mark(L-1,O,I,S,T).
mark(L,(O+1)/2,I,S,T) :- layer(L,_), not less(L-1,I,O), offset(L-1,O), mark(L-1,O+1,I,S,T).

mark(I,S,T) :- mark(L,1,I,S,T), layer(L,1).

#minimize [ mark(_,_,T) = T ].

#hide.
#show order/3.
