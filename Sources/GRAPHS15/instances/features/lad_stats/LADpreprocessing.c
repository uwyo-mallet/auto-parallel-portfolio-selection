// This software has been written by Christine Solnon.
// It is distributed under the CeCILL-B FREE SOFTWARE LICENSE
// see http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html for more details

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <getopt.h>
#include <sys/time.h>
#include <sys/resource.h>

// define boolean type as char
#define true 1
#define false 0
#define bool char


void usage(int status){
	// print usage notice and exit with status code status
	printf("Usage:\n");
	printf("  -p FILE  Input pattern graph (mandatory)\n");
	printf("  -t FILE  Input target graph (mandatory)\n\n"); 
	printf("  -h       Print this help message\n");
	exit(status);
}

void parse(char* fileNameGp, char* fileNameGt, char* argv[], int argc){
	// get parameter values
	// return false if an error occurs; true otherwise
	char ch;
	extern char* optarg;
	while ( (ch = getopt(argc, argv, "lvfs:ip:t:d:h"))!=-1 ) {
		switch(ch) {
			case 'p': strncpy(fileNameGp, optarg, 254); break;
			case 't': strncpy(fileNameGt, optarg, 254); break;
			case 'h': usage(0);
			default:
				printf("Unknown option: %c.\n", ch);
				usage(2);
		}
	}
	if (fileNameGp[0] == 0){
		printf("Error: no pattern graph given.\n");
		usage(2);
	}
	if (fileNameGt[0] == 0){
		printf("Error: no target graph given.\n");
		return usage(2);
	}
}

typedef struct{
    bool* isLoop; // isLoop[i] = true if there is a loop on vertex i
    int nbVertices; // Number of vertices
    int* nbAdj;    // nbAdj[i] = number of vertices j such that (i,j) or (j,i) is an edge
    int** adj;     // forall j in [0..nbAdj[i]-1], adj[i][j] = jth vertex adjacent to i
    int maxDegree;
    int minDegree;
} Tgraph;


Tgraph* createGraph(char* fileName){
    // reads data in fileName and create the corresponding graph
    FILE* fd;
    int i, j, k;
    Tgraph* graph = (Tgraph*)malloc(sizeof(Tgraph));
    
    if ((fd=fopen(fileName, "r"))==NULL){
        printf("ERROR: Cannot open ascii input file %s\n", fileName);
        exit(1);
    }
    if (fscanf(fd,"%d",&(graph->nbVertices)) != 1){
        printf("ERROR while reading input file %s\n", fileName);
        exit(1);
    }
    graph->isLoop = (bool*)calloc(graph->nbVertices,sizeof(bool));
    graph->nbAdj = (int*)calloc(graph->nbVertices,sizeof(int));
    graph->adj = (int**)malloc(graph->nbVertices*sizeof(int*));
    for (i=0; i<graph->nbVertices; i++){
        graph->adj[i] = (int*)malloc(graph->nbVertices*sizeof(int));
    }
    graph->maxDegree = 0;
    graph->minDegree = graph->nbVertices;
    for (i=0; i<graph->nbVertices; i++){
        // read degree of vertex i
        if ((fscanf(fd,"%d",&(graph->nbAdj[i])) != 1) || (graph->nbAdj[i] < 0) || (graph->nbAdj[i]>=graph->nbVertices) || (feof(fd))) {
            printf("ERROR while reading input file %s: Vertex %d has an illegal number of successors (%d should be between 0 and %d)\n",
                   fileName, i, graph->nbAdj[i], graph->nbVertices);
            exit(1);
        }
        if (graph->nbAdj[i] > graph->maxDegree)
            graph->maxDegree = graph->nbAdj[i];
        if (graph->nbAdj[i] < graph->minDegree)
            graph->minDegree = graph->nbAdj[i];
        for (j=0; j<graph->nbAdj[i]; j++){
            // read jth successor of i
            if ((fscanf(fd,"%d",&k) != 1) || (k<0) || (k>=graph->nbVertices) || (feof(fd))){
                printf("ERROR while reading input file %s: Successor %d of vertex %d has an illegal value %d (should be between 0 and %d)\n",
                       fileName, j, i, k, graph->nbVertices);
                exit(1);
            }
            if (i == k){ // The edge is a loop
                graph->isLoop[i] = true;
            }
            else{
                graph->adj[i][j] = k;
            }
        }
    }
    fclose(fd);
    return graph;
}

bool compare(int* mu, int* mv, int size){
    int total = 0;
    for (int j=size; j>=0; j--){
        total += mv[j] - mu[j];
        if (total < 0) return false;
    }
    return true;
}



int main(int argc, char* argv[]){
	// Parameters
	char fileNameGp[1024]; // Name of the file that contains the pattern graph
	char fileNameGt[1024]; // Name of the file that contains the target graph
	fileNameGp[0] = 0;
	fileNameGt[0] = 0;
	parse(fileNameGp, fileNameGt, argv, argc);
	
	// Initialize graphs
	Tgraph *Gp = createGraph(fileNameGp);       // Pattern graph
	Tgraph *Gt = createGraph(fileNameGt);       // Target graph
    
    struct rusage ru;     // reusable structure to get CPU time usage
    
    float minReduction = 100.0;
    float maxReduction = 0.0;
    if ((Gp->nbVertices > Gt->nbVertices) || (Gp->maxDegree > Gt->maxDegree)){
        getrusage(RUSAGE_SELF, &ru);
        printf("Inconsistency detected in %d.%06d seconds\n",
               (int) ru.ru_utime.tv_sec, (int) ru.ru_utime.tv_usec);
    }
    else if (Gp->maxDegree <= Gt->minDegree){
        getrusage(RUSAGE_SELF, &ru);
        printf("0 removed values (percentage = 0) in %d.%06d seconds\n",(int) ru.ru_utime.tv_sec, (int) ru.ru_utime.tv_usec);
    }
    else{
        int cpt = 0;
        int mu[Gt->maxDegree+1];
        int** mv = (int**)malloc(Gt->nbVertices*sizeof(int*));
        bool isUsed[Gt->nbVertices];
        memset(isUsed,false,(Gt->nbVertices)*sizeof(bool));
        for (int v=0; v<Gt->nbVertices; v++){
            mv[v] = (int*)calloc(Gt->maxDegree+1,sizeof(int));
            memset(mv[v],0,(Gt->maxDegree+1)*sizeof(int));
            for (int i=0; i<Gt->nbAdj[v]; i++) mv[v][Gt->nbAdj[Gt->adj[v][i]]]++;
        }
        for (int u=0; u<Gp->nbVertices; u++){
            int domainSize = 0;
            int val;
            memset(mu,0,(Gt->maxDegree+1)*sizeof(int));
            for (int i=0; i<Gp->nbAdj[u]; i++) mu[Gp->nbAdj[Gp->adj[u][i]]]++;
            for (int v=0; v<Gt->nbVertices; v++){
                if ((Gp->nbAdj[u] > Gt->nbAdj[v]) || (Gp->isLoop[u] != Gt->isLoop[v]) || (isUsed[v]) || (!compare(mu, mv[v], Gt->maxDegree))){
                    cpt++;
                }
                else{
                    domainSize++;
                    val = v;
                }
           }
            if (domainSize == 0){
                getrusage(RUSAGE_SELF, &ru);
                printf("Inconsistency detected in %d.%06d seconds\n",
                       (int) ru.ru_utime.tv_sec, (int) ru.ru_utime.tv_usec);
                return 0;
            }
            if (domainSize == 1)
                isUsed[val] = true;
            float reduction = 100.0*(Gt->nbVertices - domainSize)/Gt->nbVertices;
            if (reduction > maxReduction)
                maxReduction = reduction;
            if (reduction < minReduction)
                minReduction = reduction;
        }
        getrusage(RUSAGE_SELF, &ru);
        printf("%d removed values (percentage = %f, min = %f, max = %f) in %d.%06d seconds\n",cpt,100.0*cpt/(Gp->nbVertices*Gt->nbVertices), minReduction, maxReduction, (int) ru.ru_utime.tv_sec, (int) ru.ru_utime.tv_usec);
    }
    return 0;
}
