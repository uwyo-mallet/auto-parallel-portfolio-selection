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

solver(S)  :- time(_,S,_).
time(S,T)  :- time(_,S,T).
unit(1..cores).

insert :- time(I,S,T), @insert(I,S,T) == 1.
order(I,K,S) :- insert, solver(S), (I,K) := @order(S).

{ slice(U,S,T) : time(S,T) : T <= K : unit(U) } 1 :- 
  solver(S), kappa(K).
slice(S,T) :- slice(_,S,T).

 :- not [ slice(U,S,T) = T ] K, kappa(K), unit(U).

solved(I,S) :- slice(S,T), time(I,S,T).
solved(I,S) :- solved(J,S), order(I,J,S).
solved(I)   :- solved(I,_).

#maximize { solved(I)@2 }.  
#minimize [ slice(c1,T) = T @1 ].

#hide.
#show slice/2.
