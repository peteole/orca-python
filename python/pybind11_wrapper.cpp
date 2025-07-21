/*
 * Python bindings for ORCA (ORbit Counting Algorithm)
 *
 * Original ORCA algorithm: Tomaz Hocevar (https://github.com/thocevar/orca)
 * Python bindings: Ole Petersen (peteole2707@gmail.com)
 *
 * This file provides modern pybind11-based Python bindings for the ORCA
 * graphlet counting algorithm with NumPy integration.
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>
#include <string>
#include <sstream>
#include "../src/orca_declarations.h"

namespace py = pybind11;

// Wrapper function to interface with the existing C++ code
py::array_t<long long> count_orbits_wrapper(
    const std::string &orbit_type,
    int graphlet_size,
    py::array_t<int> edges_array,
    int n_nodes)
{
    // Validate inputs
    if (orbit_type != "node" && orbit_type != "edge")
    {
        throw std::invalid_argument("orbit_type must be 'node' or 'edge'");
    }
    if (graphlet_size != 4 && graphlet_size != 5)
    {
        throw std::invalid_argument("graphlet_size must be 4 or 5");
    }

    // Convert numpy array to internal format
    auto buf = edges_array.request();
    if (buf.ndim != 2 || buf.shape[1] != 2)
    {
        throw std::invalid_argument("edges must be a 2D array with shape (n_edges, 2)");
    }

    int n_edges = buf.shape[0];
    int *edges_ptr = static_cast<int *>(buf.ptr);

    // Create temporary file content as string
    std::stringstream graph_stream;
    graph_stream << n_nodes << " " << n_edges << "\n";
    for (int i = 0; i < n_edges; i++)
    {
        graph_stream << edges_ptr[i * 2] << " " << edges_ptr[i * 2 + 1] << "\n";
    }

    // Create temporary files
    std::string input_filename = "/tmp/orca_input.txt";
    std::string output_filename = "/tmp/orca_output.txt";

    // Write input file
    std::ofstream input_file(input_filename);
    input_file << graph_stream.str();
    input_file.close();

    // Call the ORCA algorithm
    std::string result_str;
    int success = motif_counts(orbit_type.c_str(), graphlet_size,
                               input_filename.c_str(), "std", result_str);

    if (!success)
    {
        throw std::runtime_error("ORCA computation failed");
    }

    // Parse results
    std::vector<std::vector<long long>> results;
    std::stringstream ss(result_str);
    std::string line;

    // Determine number of orbits based on type and size
    int n_orbits;
    if (orbit_type == "node")
    {
        int orbit_counts[] = {0, 0, 1, 4, 15, 73};
        n_orbits = orbit_counts[graphlet_size];
    }
    else
    {
        int orbit_counts[] = {0, 0, 0, 2, 12, 68};
        n_orbits = orbit_counts[graphlet_size];
    }

    // Parse the result string
    while (std::getline(ss, line))
    {
        if (line.empty())
            continue;
        std::vector<long long> row;
        std::stringstream line_ss(line);
        std::string value;
        while (line_ss >> value)
        {
            row.push_back(std::stoll(value));
        }
        if (!row.empty())
        {
            results.push_back(row);
        }
    }

    // Convert to numpy array
    int n_elements = (orbit_type == "node") ? n_nodes : n_edges;
    auto result_array = py::array_t<long long>(
        {n_elements, n_orbits},
        {sizeof(long long) * n_orbits, sizeof(long long)});

    auto buf_result = result_array.request();
    long long *ptr = static_cast<long long *>(buf_result.ptr);

    for (int i = 0; i < n_elements && i < results.size(); i++)
    {
        for (int j = 0; j < n_orbits && j < results[i].size(); j++)
        {
            ptr[i * n_orbits + j] = results[i][j];
        }
    }

    // Clean up temporary files
    std::remove(input_filename.c_str());

    return result_array;
}

// Python wrapper for easier graph format input
py::array_t<long long> count_node_orbits(
    py::array_t<int> edges,
    int n_nodes,
    int graphlet_size = 4)
{
    return count_orbits_wrapper("node", graphlet_size, edges, n_nodes);
}

py::array_t<long long> count_edge_orbits(
    py::array_t<int> edges,
    int n_nodes,
    int graphlet_size = 4)
{
    return count_orbits_wrapper("edge", graphlet_size, edges, n_nodes);
}

PYBIND11_MODULE(orca, m)
{
    m.doc() = "ORCA: Orbit Counting Algorithm for graphlet analysis";

    m.def("count_orbits", &count_orbits_wrapper,
          "Count node or edge orbits in a graph",
          py::arg("orbit_type"), py::arg("graphlet_size"),
          py::arg("edges"), py::arg("n_nodes"));

    m.def("count_node_orbits", &count_node_orbits,
          "Count node orbits in a graph",
          py::arg("edges"), py::arg("n_nodes"), py::arg("graphlet_size") = 4);

    m.def("count_edge_orbits", &count_edge_orbits,
          "Count edge orbits in a graph",
          py::arg("edges"), py::arg("n_nodes"), py::arg("graphlet_size") = 4);

    // Add version info
    m.attr("__version__") = "0.1.0";
}
