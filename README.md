# ORCA Python Package

A Python wrapper for the ORCA (ORbit Counting Algorithm) library for graphlet analysis in networks.

**Original ORCA Algorithm**: [Tomaz Hocevar](https://github.com/thocevar/orca)  
**Python Bindings**: Ole Petersen (peteole2707@gmail.com)

ORCA is an efficient algorithm for counting graphlets in networks. It computes node- and edge-orbits (of 4- and 5-node graphlets) for each node in the network.

## Installation

```bash
pip install orca-graphlets
```

> **Note**: This package provides pre-built wheels for Linux (x86_64), macOS (x86_64, arm64), and Windows (x64) for Python 3.8+. No compilation required!

## Usage

```python
import numpy as np
import orca

# Define a simple graph as edge list
edges = np.array([
    [0, 1],
    [1, 2], 
    [2, 0],
    [0, 3]
], dtype=np.int32)

n_nodes = 4

# Count 4-node graphlet orbits for each node
node_orbits = orca.count_node_orbits(edges, n_nodes, graphlet_size=4)
print("Node orbits shape:", node_orbits.shape)  # (4, 15) for 4 nodes, 15 orbits

# Count 4-node graphlet orbits for each edge  
edge_orbits = orca.count_edge_orbits(edges, n_nodes, graphlet_size=4)
print("Edge orbits shape:", edge_orbits.shape)  # (4, 11) for 4 edges, 11 orbits

# You can also use the general function
node_orbits_alt = orca.count_orbits("node", 4, edges, n_nodes)
```

## API Reference

### `count_node_orbits(edges, n_nodes, graphlet_size=4)`

Count node orbits in a graph.

**Parameters:**

- `edges`: numpy array of shape (n_edges, 2) with node indices
- `n_nodes`: number of nodes in the graph
- `graphlet_size`: size of graphlets to count (4 or 5)

**Returns:**

- numpy array of shape (n_nodes, n_orbits) with orbit counts

### `count_edge_orbits(edges, n_nodes, graphlet_size=4)`

Count edge orbits in a graph.

**Parameters:**

- `edges`: numpy array of shape (n_edges, 2) with node indices  
- `n_nodes`: number of nodes in the graph
- `graphlet_size`: size of graphlets to count (4 or 5)

**Returns:**

- numpy array of shape (n_edges, n_orbits) with orbit counts

### `count_orbits(orbit_type, graphlet_size, edges, n_nodes)`

General function to count orbits.

**Parameters:**

- `orbit_type`: "node" or "edge"
- `graphlet_size`: 4 or 5
- `edges`: numpy array of shape (n_edges, 2)
- `n_nodes`: number of nodes

**Returns:**

- numpy array with orbit counts

## About ORCA

ORCA (ORbit Counting Algorithm) is a tool for counting graphlets and their orbits in networks. Graphlets are small connected subgraphs, and orbits represent different structural roles that nodes or edges can have within these graphlets.

This is useful for:

- Network analysis and comparison
- Node importance ranking
- Graph classification
- Biological network analysis

## Original Implementation

This package provides Python bindings for the original ORCA implementation by Tomaz Hocevar:
<https://github.com/thocevar/orca>

## License

This package is licensed under GPL-3.0, maintaining compatibility with the original ORCA implementation.

## Requirements

- Python 3.8+
- NumPy

## Development

This package uses [uv](https://astral.sh/uv/) for package management and development.

### Quick Start

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/peteole/orca-python
cd orca-python

# Create virtual environment and install dependencies
uv venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements-dev.txt

# Build the package
make build

# Run tests
make test

# Run example
make example
```

### Available Commands

```bash
make help          # Show all available commands
make dev           # Install development dependencies  
make build         # Build package for development
make test          # Run tests
make wheel         # Build wheel
make clean         # Clean build artifacts
make ci-wheels     # Build wheels for all platforms (Linux, macOS, Windows)
```

### Building Cross-Platform Wheels

This package uses [cibuildwheel](https://cibuildwheel.readthedocs.io/) to build wheels for multiple platforms:

```bash
# Build wheels for all platforms (requires Docker for Linux builds)
make ci-wheels

# Or run cibuildwheel directly
uv run python -m cibuildwheel --output-dir wheelhouse
```

The wheels are automatically built for:
- **Linux**: manylinux_2_28_x86_64 (Python 3.8-3.12)
- **macOS**: x86_64 and arm64 (Python 3.8-3.12)  
- **Windows**: x64 (Python 3.8-3.12)

## Citation

If you use this software in your research, please cite the original ORCA paper:

**Tomaz Hocevar and Janez Demsar.** A combinatorial approach to graphlet counting. 
*Bioinformatics*, 2014. DOI: 10.1093/bioinformatics/btu245

## Credits

- **Original ORCA Algorithm**: Tomaz Hocevar - [GitHub](https://github.com/thocevar/orca)
- **Python Bindings**: Ole Petersen (peteole2707@gmail.com) - Created modern pybind11-based Python bindings with NumPy integration
