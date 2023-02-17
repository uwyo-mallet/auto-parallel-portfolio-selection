import angr
import pickle
import networkx as nx
import statistics as stats
from collections import Counter
from scipy.stats import entropy
import os
import sys


def compute_features(net):
    features=[]
    #node degree
    degrees= [d for (n,d) in net.degree]
    #print(degrees)
    count = Counter(degrees)
    features = features + [min(degrees),max(degrees),stats.mean(degrees),stats.variance(degrees),entropy([count[i] for i in range(max(degrees))])]
    #transitivity
    features.append(nx.transitivity(net))
    #clustering
    clustering=[nx.clustering(net,n) for n in net.nodes]
    #print(clustering)
    count = Counter(clustering)
    features = features + [min(clustering),max(clustering),stats.mean(clustering),stats.variance(clustering)]
    
    # number of self loops
    features = features + [nx.number_of_selfloops(net)]

    # extract opereations from nodes
    nodes = net.nodes
    edges = net.edges

    node_sizes = []
    block_instructions = []
    insts_names = []
    operand_names = []
    syscalls = []
    
    # collect features
    for node in nodes:
        # size of nodes
        node_sizes.append(node.size)
        syscalls.append(node.is_syscall)
        if node.block is not None:
            # number of instructions in each block
            block_instructions.append(node.block.instructions)
            # get instruction names
            for ins in node.block.capstone.insns:
                insts_names.append(ins.insn.mnemonic)
                operand_names.append(ins.insn.op_str)


    # number of system calls
    features = features + [sum(syscalls)]

    # min, max, mean, median of above features
    features = features + [min(node_sizes),max(node_sizes),stats.mean(node_sizes),stats.variance(node_sizes)]

    features = features + [min(block_instructions),max(block_instructions),stats.mean(block_instructions),stats.variance(block_instructions)]

    # unique number of instructions
    features = features + [len(set(insts_names))]
    
    # frequency of every instruction 
    count_inst = {}
    for inst in insts_names: 
        count_inst[inst] = count_inst.get(inst, 0) + 1
        
    features = features + list(count_inst.values())
     
    # kinds of jumps
    jumpkind_names = []
    for (u, v, c) in edges.data('jumpkind'): 
        jumpkind_names.append(c)

    # unique number of jumpkinds 
    features = features + [len(set(jumpkind_names))]
    count_jumps = {}
    for jump in jumpkind_names: 
        count_jumps[jump] = count_jumps.get(jump, 0) + 1
        
    features = features + list(count_jumps.values())

    return [features, list(count_inst.keys()), list(count_jumps.keys())]

if __name__ =='__main__':
    # open abcd_graph.file
    file_obj = open(sys.argv[1], 'rb')
    cfg = pickle.load(file_obj)
    g = cfg.graph
    file_obj.close()
    
    features=[len(g.nodes),len(g.edges)]
    vals,inst_names,jump_names = compute_features(g)
    
    features=features+vals

    if sys.argv[2].lower() == 'true':
        print("solver,"
              +"nb_nodes,nb_edges,"
              +"degree_min,degree_max,degree_mean,degree_variance,degree_entropy,"
              +"transitivity,"
              +"clustering_min,clustering_max,clustering_mean,clustering_variance,"
              +"nb_selfloops," 
              +"nb_syscalls,"
              +"nodesize_min,nodesize_max,nodesize_mean,nodesize_variance,"
              +"blockinst_min,blockinstr_max,blockinstr_mean,blockinstr_variance,"
              +"nb_unique_inst,"
              +','.join(inst_names)
              +",nb_unique_jumps,"
              +','.join(jump_names))
    print(sys.argv[1]+","+",".join([str(f) for f in features]))
