#begin_lua
ts = { }
function insert(i,s,t)
	if ts[s:name()] == nil then 
		ts[s:name()] = { }
	end
	table.insert(ts[s:name()], {i, t} )
	return 1
end
function order(s)
	table.sort(ts[s:name()], 
		function (x, y) 
			if x[2] ~= y[2] then return x[2] < y[2] end
			return Val.cmp(x[1], y[1]) < 0
		end )
	p = nil
	r = { }
	for i, v in ipairs(ts[s:name()]) do
		if p ~= nil then
		 	table.insert(r, Val.new(Val.FUNC, {p, v[1]}))
		end
		p = v[1]
	end
	return r
end
#end_lua.

#const cores=1.
#const maxsolver=3.
#const optMode=1.
#const maxPreSlice=1000000.
#const featTime=0.

solver(S)  :- time(_,S,_).
time(S,T)  :- time(_,S,T).
unit(1..cores).

insert :- time(I,S,T), @insert(I,S,T) == 1.
order(I,K,S) :- insert, solver(S), (I,K) := @order(S).

{ slice(U,S,T) : time(S,T) : T <= K : unit(U) } 1 :- 
  solver(S), kappa(K).
slice(S,T) :- slice(_,S,T).

 :- not [ slice(U,S,T) = T ] K, kappa(K), unit(U). 
 :- not [ slice(U,S,T) ] maxsolver. 
 :- not [ slice(1,S,T) = T : S != c0 ] maxPreSlice. %c0 is the encoded claspfolio
 :- not [ slice(U,S,T) = T : S != c0 ] maxPreSlice+featTime, unit(U). %c0 is the encoded claspfolio; on U > 1 feature time can be spend for pre-solving

solved(I,S) :- slice(S,T), time(I,S,T).
solved(I,S) :- solved(J,S), order(I,J,S).
solved(I)   :- solved(I,_).

#maximize { solved(I)@3 }.  
#maximize [ slice(c0,T) = T @2].
#minimize [ slice(S,T) = T*T @1 : optMode==1].
#maximize [ slice(S,T) = T*T @1 : optMode==2]. 
#minimize [ slice(S,T) = T @1 : optMode==3].
#maximize [ slice(S,T) = T @1 : optMode==4].
#minimize [ slice(S,T) @1 : T > 0 : optMode==5]. 
#maximize [ slice(S,T) @1 : T > 0 : optMode==6].

#hide.
#show slice/3.
