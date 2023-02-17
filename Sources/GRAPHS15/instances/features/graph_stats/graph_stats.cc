/* vim: set sw=4 sts=4 et foldmethod=syntax : */

#include "lad.hh"

#include <boost/program_options.hpp>

#include <iostream>
#include <exception>
#include <cstdlib>
#include <chrono>
#include <thread>
#include <mutex>
#include <condition_variable>

namespace po = boost::program_options;

using std::chrono::steady_clock;
using std::chrono::duration_cast;
using std::chrono::milliseconds;

namespace
{
    struct VertexDistance
    {
        int distance;
        int next;
    };

    struct VertexInformation
    {
        std::vector<int> firsts;
        std::vector<VertexDistance> distances;
    };
}

auto main(int argc, char * argv[]) -> int
{
    try {
        po::options_description display_options{ "Program options" };
        display_options.add_options()
            ("help",                                  "Display help information")
            ("distances",                             "Also calculate distance information")
            ;

        po::options_description all_options{ "All options" };
        all_options.add_options()
            ("graph-file", "Specify the graph file (LAD format)")
            ;

        all_options.add(display_options);

        po::positional_options_description positional_options;
        positional_options
            .add("graph-file", 1)
            ;

        po::variables_map options_vars;
        po::store(po::command_line_parser(argc, argv)
                .options(all_options)
                .positional(positional_options)
                .run(), options_vars);
        po::notify(options_vars);

        /* --help? Show a message, and exit. */
        if (options_vars.count("help")) {
            std::cout << "Usage: " << argv[0] << " [options] graph-file" << std::endl;
            std::cout << std::endl;
            std::cout << display_options << std::endl;
            return EXIT_SUCCESS;
        }

        /* No algorithm or no input file specified? Show a message and exit. */
        if (! options_vars.count("graph-file")) {
            std::cout << "Usage: " << argv[0] << " [options] graph-file" << std::endl;
            return EXIT_FAILURE;
        }

        /* Read in the graph */
        auto graph = read_lad(options_vars["graph-file"].as<std::string>());

        /* Start the clock. */
        auto start_time = steady_clock::now();

        unsigned edges = 0;
        unsigned loops = 0;
        unsigned max_deg = 0;
        unsigned total_deg = 0;
        int fixed_degree = -2;

        bool is_connected = true;
        unsigned distancege2 = 0;
        unsigned distancege3 = 0;
        unsigned distancege4 = 0;
        unsigned sum_distances = 0;
        unsigned max_distance = 0;
        unsigned distance_count = 0;

        for (int i = 0 ; i < graph.size() ; ++i) {
            if (graph.adjacent(i, i)) {
                ++edges;
                ++loops;
            }

            auto deg = graph.degree(i);
            total_deg += deg;
            max_deg = std::max<unsigned>(max_deg, deg);
            edges += deg;

            if (-2 == fixed_degree)
                fixed_degree = deg;
            else if (deg != fixed_degree)
                fixed_degree = -1;
        }

        if (0 != edges % 2)
            throw 0;
        edges /= 2;

        if (options_vars.count("distances")) {
            std::vector<VertexInformation> vertices(graph.size());

            for (auto & d : vertices) {
                d.firsts.resize(graph.size() + 1);
                for (auto & f : d.firsts)
                    f = -1;

                d.distances.resize(graph.size());
            }

            /* build up distance 1 lists */
            for (int i = 0 ; i < graph.size() ; ++i) {
                int prev = -1;
                for (int j = 0 ; j < graph.size() ; ++j) {
                    if (i == j) {
                        vertices[i].firsts[0] = i;
                        vertices[i].distances[j].distance = 0;
                        vertices[i].distances[j].next = -1;
                    }
                    else if (graph.adjacent(i, j)) {
                        if (-1 == vertices[i].firsts[1]) {
                            vertices[i].firsts[1] = j;
                            vertices[i].distances[j].distance = 1;
                            vertices[i].distances[j].next = -1;
                            prev = j;
                        }
                        else {
                            vertices[i].distances[prev].next = j;
                            vertices[i].distances[j].distance = 1;
                            vertices[i].distances[j].next = -1;
                            prev = j;
                        }
                    }
                    else {
                        vertices[i].distances[j].distance = -1;
                        vertices[i].distances[j].next = -1;
                    }
                }
            }

            /* build up distance k lists */
            for (int k = 2 ; k <= graph.size() ; ++k) {
                // for each vertex i...
                for (int i = 0 ; i < graph.size() ; ++i) {
                    int prev = -1;
                    // for each vertex a at distance k - 1 from i...
                    for (int a = vertices[i].firsts[k - 1] ; a != -1 ; a = vertices[i].distances[a].next) {
                        // for each vertex j at distance 1 from a...
                        for (int j = vertices[a].firsts[1] ; j != -1 ; j = vertices[a].distances[j].next) {
                            // are i and j currently infinitely far apart?
                            if (vertices[i].distances[j].distance == -1) {
                                // distance from i to j is now k, via a.
                                vertices[i].distances[j].distance = k;
                                if (-1 == prev)
                                    vertices[i].firsts[k] = j;
                                else
                                    vertices[i].distances[prev].next = j;
                                prev = j;
                            }
                        }
                    }
                }
            }

            for (int i = 0 ; i < graph.size() ; ++i)
                for (int j = 0 ; j < graph.size() ; ++j) {
                    int dist = vertices[i].distances[j].distance;
                    if (0 == dist) {
                    }
                    else if (dist < 0)
                        is_connected = false;
                    else {
                        ++distance_count;
                        sum_distances += dist;
                        max_distance = std::max(max_distance, unsigned(dist));
                        if (dist >= 2) ++distancege2;
                        if (dist >= 3) ++distancege3;
                        if (dist >= 4) ++distancege4;
                    }
                }
        }

        /* Stop the clock. */
        auto overall_time = duration_cast<milliseconds>(steady_clock::now() - start_time);

        std::cout << "time = " << overall_time.count() << std::endl;
        std::cout << "vertices = " << graph.size() << std::endl;
        std::cout << "edges = " << edges << std::endl;
        std::cout << "loops = " << loops << std::endl;
        std::cout << "meandeg = " << ((0.0 + total_deg) / (0.0 + graph.size())) << std::endl;
        std::cout << "maxdeg = " << max_deg << std::endl;
        std::cout << "degisfixed = " << (fixed_degree >= 0) << std::endl;
        std::cout << "density = " << ((0.0 + 2 * edges) / (graph.size() * (graph.size() - 1))) << std::endl;

        if (options_vars.count("distances")) {
            std::cout << "isconnected = " << is_connected << std::endl;
            std::cout << "meandistance = " << ((0.0 + sum_distances) / (0.0 + distance_count)) << std::endl;
            std::cout << "maxdistance = " << max_distance << std::endl;
            std::cout << "proportiondistancege2 = " << ((0.0 + distancege2) / (graph.size() * graph.size() + 0.0)) << std::endl;
            std::cout << "proportiondistancege3 = " << ((0.0 + distancege3) / (graph.size() * graph.size() + 0.0)) << std::endl;
            std::cout << "proportiondistancege4 = " << ((0.0 + distancege4) / (graph.size() * graph.size() + 0.0)) << std::endl;
        }

        return EXIT_SUCCESS;
    }
    catch (const po::error & e) {
        std::cerr << "Error: " << e.what() << std::endl;
        std::cerr << "Try " << argv[0] << " --help" << std::endl;
        return EXIT_FAILURE;
    }
    catch (const std::exception & e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }
}

