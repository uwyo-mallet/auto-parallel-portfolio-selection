// This software has been written by Christine Solnon.
// It is distributed under the CeCILL-B FREE SOFTWARE LICENSE
// see http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html for more details

typedef struct{
	int *nbVal;    // nbVal[u] = number of values in D[u]
	int *firstVal; // firstVal[u] = pos in val of the first value of D[u]
	int *val;      // val[firstVal[u]..firstVal[u]+nbVal[u]-1] = values of D[u]
	int **posInVal; 
	// If v in D[u] then firstVal[u] <= posInVal[u][v] < firstVal[u]+nbVal[u] 
	//                   and val[posInVal[u][v]] = v
	// otherwise posInVal[u][v] >= firstVal[u]+nbVal[u] 
	int **firstMatch; // firstMatch[u][v] = pos in match of the first vertex of the covering matching of G_(u,v)
	int *matching; // matching[firstMatch[u][v]..firstMatch[u][v]+nbAdj[u]-1] = covering matching of G_(u,v)
	int nextOutToFilter; // position in toFilter of the next pattern node whose domain should be filtered (-1 if no domain to filter)
	int lastInToFilter; // position in toFilter of the last pattern node whose domain should be filtered
	int *toFilter;  // contain all pattern nodes whose domain should be filtered
	bool *markedToFilter;    // markedToFilter[u]=true if u is in toFilter; false otherwise
	int* globalMatchingP; // globalMatchingP[u] = node of Gt matched to u in globalAllDiff(Np)
	int* globalMatchingT; // globalMatchingT[v] = node of Gp matched to v in globalAllDiff(Np) or -1 if v is not matched
} Tdomain;

void printDomains(Tdomain *d, int n){
	int u, i;
	for (u=0; u<n; u++){
		printf("D[%d] = ",u);
		for (i=0; i<d->nbVal[u]; i++)
			printf("%d ",d->val[d->firstVal[u]+i]);
		printf("\n");
	}
		
}

bool toFilterEmpty(Tdomain* D){
	// return true if there is no more nodes in toFilter
	return (D->nextOutToFilter < 0);
}

void resetToFilter(Tdomain *D, int size){
	// empty to filter and unmark the vertices that are marked to be filtered
	memset(D->markedToFilter,false,size);
	D->nextOutToFilter = -1;
}

int nextToFilter(Tdomain* D, int size){
	// precondition: toFilterEmpty = false
	// remove a node from toFilter (FIFO)
	// unmark this node and return it
	int u = D->toFilter[D->nextOutToFilter];
	D->markedToFilter[u] = false;
	if (D->nextOutToFilter == D->lastInToFilter) 
		// u was the last node in tofilter
		D->nextOutToFilter = -1;
	else if (D->nextOutToFilter == size-1)
		D->nextOutToFilter = 0;
	else D->nextOutToFilter++;
	return u;
}

void addToFilter(int u, Tdomain* D, int size){
	// if u is not marked, then add it to toFilter and mark it
	if (D->markedToFilter[u]) return;
	D->markedToFilter[u] = true;
	if (D->nextOutToFilter < 0){
		D->lastInToFilter = 0;
		D->nextOutToFilter = 0;
	}
	else if (D->lastInToFilter == size-1)
		D->lastInToFilter = 0;
	else D->lastInToFilter++;
	D->toFilter[D->lastInToFilter] = u;
}

bool isInD(int u, int v, Tdomain* D){
	// returns true if v belongs to D(u); false otherwise
	return (D->posInVal[u][v]<D->firstVal[u]+D->nbVal[u]);
}

bool augmentingPath(int u, Tdomain* D, int nbV){
	// return true if there exists an augmenting path starting from u and ending on a free vertex v
	// in the bipartite directed graph G=(U,V,E) such that U=pattern nodes, V=target nodes, and 
	// E={(u,v), v in D(u)} U {(v,u), D->globalMatchingP[u]=v}
	// update D-globalMatchingP and D->globalMatchingT consequently
	int fifo[nbV];
	int pred[nbV];
	int nextIn = 0;
	int nextOut = 0;
	int i, v, v2, u2, j;
	bool marked[nbV];
	memset(marked,false,nbV);
	for (i=0; i<D->nbVal[u]; i++){
		v = D->val[D->firstVal[u]+i];// v in D(u)
		if (D->globalMatchingT[v]<0){// v is free => augmenting path found
			D->globalMatchingP[u]=v;
			D->globalMatchingT[v]=u;
			return true;
		}
		// v is not free => add it to fifo
		pred[v] = u;
		fifo[nextIn++] = v;
		marked[v] = true;
	}
	while (nextOut < nextIn){
		u2 = D->globalMatchingT[fifo[nextOut++]];
		for (i=0; i<D->nbVal[u2]; i++){
			v = D->val[D->firstVal[u2]+i];// v in D(u2)
			if (D->globalMatchingT[v]<0){// v is free => augmenting path found
				j=0;
				while (u2 != u){// update global matching wrt path
					if (j>100) exit(1); j++;
					v2 = D->globalMatchingP[u2];
					D->globalMatchingP[u2]=v;
					D->globalMatchingT[v]=u2;
					v = v2;
					u2 = pred[v];
				}
				D->globalMatchingP[u]=v;
				D->globalMatchingT[v]=u;
				return true;
			}
			if (!marked[v]){// v is not free and not marked => add it to fifo
				pred[v] = u2;
				fifo[nextIn++] = v;
				marked[v] = true;
			}
		}
	}
	return false;
}

bool removeAllValuesButOne(int u, int v, Tdomain* D, Tgraph* Gp, Tgraph* Gt){
	// remove all values but v from D(u) and add all successors of u in toFilter
	// return false if an inconsistency is detected wrt to global all diff
	int j, oldPos, newPos;
	// add all successors of u in toFilter
	for (j=0; j<Gp->nbAdj[u]; j++)
		addToFilter(Gp->adj[u][j], D, Gp->nbVertices);
	// remove all values but v from D[u]
	oldPos = D->posInVal[u][v];
	newPos = D->firstVal[u];
	D->val[oldPos] = D->val[newPos];
	D->val[newPos] = v;
	D->posInVal[u][D->val[newPos]] = newPos;
	D->posInVal[u][D->val[oldPos]] = oldPos;
	D->nbVal[u] = 1;
	// update global matchings that support the global all different constraint
	if (D->globalMatchingP[u]!=v){
		D->globalMatchingT[D->globalMatchingP[u]]=-1;
		D->globalMatchingP[u]=-1;
		return augmentingPath(u,D,Gt->nbVertices);
	}
	return true;
}


bool removeValue(int u, int v, Tdomain* D, Tgraph* Gp, Tgraph* Gt){
	// remove v from D(u) and add all successors of u in toFilter
	// return false if an inconsistency is detected wrt global all diff
	int j;

	// add all successors of u in toFilter
	for (j=0; j<Gp->nbAdj[u]; j++)
		addToFilter(Gp->adj[u][j], D, Gp->nbVertices);
	// remove v from D[u]
	int oldPos = D->posInVal[u][v];
	D->nbVal[u]--;
	int newPos = D->firstVal[u]+D->nbVal[u];
	D->val[oldPos] = D->val[newPos];
	D->val[newPos] = v;
	D->posInVal[u][D->val[oldPos]] = oldPos;
	D->posInVal[u][D->val[newPos]] = newPos;
	// update global matchings that support the global all different constraint
	if (D->globalMatchingP[u]==v){
		D->globalMatchingP[u]=-1;
		D->globalMatchingT[v]=-1;
		return augmentingPath(u,D,Gt->nbVertices);
	}
	return true;
}

bool isCompatible(bool induced, int dirGp, int dirGt){
	if (dirGp == dirGt) return true;
	if (induced) return false;
	if (dirGt == 3) return true;
	return false;
}


bool matchVertices(int nb, int* toBeMatched, bool induced, Tdomain* D, Tgraph* Gp, Tgraph* Gt){
	// for each u in toBeMatched[0..nb-1], match u to D->val[D->firstVal[u]
	// and filter domains of other non matched vertices wrt FC(Edges) and FC(diff)
	// (this is not mandatory, as LAD is stronger than FC(Edges) and GAC(allDiff) 
	// is stronger than FC(diff), but this speeds up the solution process).
	// return false if an inconsistency is detected by FC(Edges) or FC(diff); true otherwise;
	int j, u, v, u2, oldNbVal;
	while (nb>0){
		u = toBeMatched[--nb];
		v = D->val[D->firstVal[u]]; 
		// match u to v
		for (u2=0; u2<Gp->nbVertices; u2++){
			if (u != u2){
				oldNbVal = D->nbVal[u2];
				if (isInD(u2,v,D) && !removeValue(u2,v,D,Gp,Gt)) return false;
				if (Gp->edgeDirection[u][u2] != 0){// remove from D[u2] vertices which are not adjacent to v
					j=D->firstVal[u2]; 
					while (j<D->firstVal[u2]+D->nbVal[u2]){
						if ((!Gp->isLabelled || compatibleEdgeLabels(Gp->edgeLabel[u][u2], Gt->edgeLabel[v][D->val[j]]))
							&& (isCompatible(induced, Gp->edgeDirection[u][u2], Gt->edgeDirection[v][D->val[j]]))) j++;
						else if (!removeValue(u2,D->val[j],D,Gp,Gt)) return false;
					}
				}
				else if (induced){// (u,u2) is not an edge => remove neighbors of v from D[u2]
					j=D->firstVal[u2]; 
					while (j<D->firstVal[u2]+D->nbVal[u2]){
						if (Gt->edgeDirection[v][D->val[j]] == 0) j++;
						else if (!removeValue(u2,D->val[j],D,Gp,Gt)) return false;
					}
				}
				if (D->nbVal[u2] == 0) return false; // D[u2] is empty
				if ((D->nbVal[u2] == 1) && (oldNbVal > 1)) toBeMatched[nb++]=u2;
			}			
		}
	}
	return true;
}


bool matchVertex(int u, bool induced, Tdomain* D, Tgraph* Gp, Tgraph *Gt){
	// match u to D->val[D->firstVal[u]]
	// and filter domains of other non matched vertices wrt FC(Edges) and FC(diff)
	// (this is not mandatory, as LAD is stronger than FC(Edges) and GAC(allDiff) 
	// is stronger than FC(diff), but this speeds up the solution process).
	// return false if an inconsistency is detected by FC(Edges) or FC(diff); true otherwise;
	int toBeMatched[Gp->nbVertices];
	toBeMatched[0]=u;
	return matchVertices(1,toBeMatched,induced,D,Gp,Gt);
}


int qcompare (void const *a, void const *b){
	// function used by the qsort function
	int pa = *((int*)a) - *((int*)b);
	return pa;
}

bool compare(int size_mu, int* mu, int size_mv, int* mv){
	// return true if for every element u of mu there exists
	// a different element v of mv such that u <= v; 
	// return false otherwise
	int i, j;
	qsort(mu, size_mu, sizeof(int), qcompare);
	qsort(mv, size_mv, sizeof(int), qcompare);
	i = size_mv-1;
	for (j=size_mu-1; j>=0; j--){
		if (mu[j]>mv[i]) return false;
		i--;
	}
	return true;
}

bool compatibleVertices(bool induced, int u, int v, Tgraph* Gp, Tgraph* Gt){
    if (Gp->isLoop[u] != Gt->isLoop[v]){
        if ((induced) || (Gp->isLoop[u]))
            return false;
    }
	if (Gp->isLabelled && !compatibleVertexLabels(Gp->vertexLabel[u], Gt->vertexLabel[v]))
		return false;
	if (!Gp->isDirected && !Gt->isDirected){ // non directed graphs
		if (Gp->nbAdj[u] > Gt->nbAdj[v]) return false;
		int i, mu[Gp->nbAdj[u]], mv[Gt->nbAdj[v]];
		for (i=0; i<Gp->nbAdj[u]; i++) mu[i]=Gp->nbAdj[Gp->adj[u][i]];
		for (i=0; i<Gt->nbAdj[v]; i++) mv[i]=Gt->nbAdj[Gt->adj[v][i]];
		return compare(Gp->nbAdj[u], mu, Gt->nbAdj[v], mv);
	}
	// directed graphs
	if (induced){
		if (Gp->nbPred[u] > Gt->nbPred[v]) return false;
		if (Gp->nbSucc[u] > Gt->nbSucc[v]) return false;
		if (Gp->nbAdj[u] - Gp->nbPred[u] - Gp->nbSucc[u] > Gt->nbAdj[v] - Gt->nbPred[v] - Gt->nbSucc[v]) return false;
		return true;
	}
	if (Gp->nbAdj[u] > Gt->nbAdj[v]) return false;
	if (Gp->nbPred[u] > Gt->nbAdj[v] - Gt->nbSucc[v]) return false;
	if (Gp->nbSucc[u] > Gt->nbAdj[v] - Gt->nbPred[v]) return false;
	if (Gp->nbAdj[u] - Gp->nbPred[u] - Gp->nbSucc[u] > Gt->nbAdj[v] - Gt->nbPred[v] - Gt->nbSucc[v]) return false;
	return true;
}

Tdomain* createDomains(Tgraph* Gp, Tgraph* Gt){
	Tdomain* D = (Tdomain*)malloc(sizeof(Tdomain));
	D->globalMatchingP = (int*)malloc(sizeof(int)*Gp->nbVertices);
	memset(D->globalMatchingP,-1,sizeof(int)*Gp->nbVertices);
	D->globalMatchingT = (int*)malloc(sizeof(int)*Gt->nbVertices);
	memset(D->globalMatchingT,-1,sizeof(int)*Gt->nbVertices);
	D->nbVal = (int*)malloc(sizeof(int)*Gp->nbVertices);
	D->firstVal = (int*)malloc(sizeof(int)*Gp->nbVertices);
	D->posInVal = (int**)malloc(sizeof(int*)*Gp->nbVertices);  
	D->firstMatch = (int**)malloc(sizeof(int*)*Gp->nbVertices);  
	D->markedToFilter = (bool*)calloc(Gp->nbVertices,sizeof(bool));  
	D->toFilter = (int*)malloc(sizeof(int)*Gp->nbVertices);  
	return D;
}	

bool initDomains(bool induced, Tdomain* D, Tgraph* Gp, Tgraph* Gt){
	// for every pattern node u, initialize D(u) with every vertex v 
	// such that for every neighbor u' of u there exists a different 
	// neighbor v' of v such that degree(u) <= degree(v)
	// if initialDomains, then filter initial domains wrt compatibilities given in file
	// return false if a domain is empty and true otherwise
	int val[Gp->nbVertices*Gt->nbVertices];
	int matchingSize, u, v, i, valSize;
	matchingSize = 0;
	valSize = 0;
	for (u=0; u<Gp->nbVertices; u++){
		D->markedToFilter[u] = true;
		D->toFilter[u] = u;
		D->nbVal[u] = 0;
		D->posInVal[u] = (int*)malloc(sizeof(int)*Gt->nbVertices);
		D->firstMatch[u] = (int*)malloc(sizeof(int)*Gt->nbVertices);
		D->firstVal[u] = valSize;
		for (v=0; v<Gt->nbVertices; v++){
			if (!compatibleVertices(induced, u, v, Gp, Gt)) // v not in D(u)
				D->posInVal[u][v] = D->firstVal[u]+Gt->nbVertices;
			else { // v in D[u]
				D->firstMatch[u][v] = matchingSize;
				matchingSize += Gp->nbAdj[u];
				val[valSize] = v;
				D->nbVal[u]++;
				D->posInVal[u][v] = valSize++;
			}
		}
		if (D->nbVal[u]==0) return 0; // empty domain
	}
	D->val = (int*)malloc(sizeof(int)*valSize);
	for (i=0; i<valSize; i++) D->val[i] = val[i];
	D->matching = (int*)malloc(sizeof(int)*matchingSize);
	memset(D->matching,-1,sizeof(int)*matchingSize);
	D->nextOutToFilter = 0;
	D->lastInToFilter = Gp->nbVertices-1;
	return 1;
}

