/* vim: set sw=4 sts=4 et foldmethod=syntax : */

#ifndef GUARD_SEQUENTIAL_HH
#define GUARD_SEQUENTIAL_HH 1

#include "params.hh"
#include "result.hh"
#include "graph.hh"

auto glasgow_1_subgraph_isomorphism(const std::pair<Graph, Graph> & graphs, const Params & params) -> Result;
auto glasgow_2_subgraph_isomorphism(const std::pair<Graph, Graph> & graphs, const Params & params) -> Result;
auto glasgow_3_subgraph_isomorphism(const std::pair<Graph, Graph> & graphs, const Params & params) -> Result;
auto glasgow_4_subgraph_isomorphism(const std::pair<Graph, Graph> & graphs, const Params & params) -> Result;

#endif
