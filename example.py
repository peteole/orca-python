"""
Example usage of ORCA Python bindings
"""

import numpy as np


def example_usage():
    """
    Demonstrate basic usage of ORCA for graphlet analysis
    """
    print("ORCA Python Bindings Example")
    print("=" * 40)

    # Create a simple graph: triangle with an additional node
    # Graph structure:
    #   0---1
    #   |\ /
    #   | 2
    #   |
    #   3

    edges = np.array(
        [
            [0, 1],  # edge 0-1
            [1, 2],  # edge 1-2
            [2, 0],  # edge 2-0 (completes triangle)
            [0, 3],  # edge 0-3 (pendant edge)
        ],
        dtype=np.int32,
    )

    n_nodes = 4
    n_edges = len(edges)

    print(f"Graph: {n_nodes} nodes, {n_edges} edges")
    print(f"Edges: {edges.tolist()}")
    print()

    try:
        import orca

        # Count 4-node graphlet orbits for each node
        print("Node Orbit Analysis (4-node graphlets)")
        print("-" * 40)
        node_orbits = orca.count_node_orbits(edges, n_nodes, graphlet_size=4)

        print(f"Shape: {node_orbits.shape} (nodes × orbits)")
        for i in range(n_nodes):
            print(f"Node {i}: {node_orbits[i][:10]}...")  # Show first 10 orbits
        print()

        # Count edge orbits
        print("Edge Orbit Analysis (4-node graphlets)")
        print("-" * 40)
        edge_orbits = orca.count_edge_orbits(edges, n_nodes, graphlet_size=4)

        print(f"Shape: {edge_orbits.shape} (edges × orbits)")
        for i in range(n_edges):
            edge = edges[i]
            print(
                f"Edge {edge[0]}-{edge[1]}: {edge_orbits[i][:8]}..."
            )  # Show first 8 orbits
        print()

        # Try 5-node graphlets (more computationally intensive)
        print("5-node Graphlet Analysis")
        print("-" * 25)
        node_orbits_5 = orca.count_node_orbits(edges, n_nodes, graphlet_size=5)
        print(f"5-node orbits shape: {node_orbits_5.shape}")
        print(f"Node 0 (5-node): {node_orbits_5[0][:15]}...")
        print()

        # Summary statistics
        print("Summary Statistics")
        print("-" * 18)
        print(f"Total 4-node orbit counts per node: {np.sum(node_orbits, axis=1)}")
        print(f"Most active node (4-node): {np.argmax(np.sum(node_orbits, axis=1))}")
        print(f"Total 4-node orbit counts per edge: {np.sum(edge_orbits, axis=1)}")
        print(f"Most active edge (4-node): {np.argmax(np.sum(edge_orbits, axis=1))}")

    except ImportError:
        print("❌ ORCA module not available. Please build the package first:")
        print("   python setup.py build_ext --inplace")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    example_usage()
