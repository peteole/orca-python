"""
Test script for ORCA Python bindings
"""

import numpy as np


def test_basic_functionality():
    try:
        import orca

        print("✓ ORCA module imported successfully")
        print(f"Version: {orca.__version__}")
    except ImportError as e:
        print(f"✗ Failed to import ORCA: {e}")
        return False

    # Create a simple test graph (triangle + one extra node)
    edges = np.array([[0, 1], [1, 2], [2, 0], [0, 3]], dtype=np.int32)

    n_nodes = 4

    try:
        # Test node orbits
        print("\nTesting node orbits...")
        node_orbits = orca.count_node_orbits(edges, n_nodes, graphlet_size=4)
        print(f"✓ Node orbits computed: shape {node_orbits.shape}")
        print(f"Sample values: {node_orbits[0][:5]}")

        # Test edge orbits
        print("\nTesting edge orbits...")
        edge_orbits = orca.count_edge_orbits(edges, n_nodes, graphlet_size=4)
        print(f"✓ Edge orbits computed: shape {edge_orbits.shape}")
        print(f"Sample values: {edge_orbits[0][:5]}")

        # Test general function
        print("\nTesting general function...")
        node_orbits_alt = orca.count_orbits("node", 4, edges, n_nodes)
        print(f"✓ General function works: shape {node_orbits_alt.shape}")

        # Verify results are consistent
        if np.array_equal(node_orbits, node_orbits_alt):
            print("✓ Results are consistent between functions")
        else:
            print("✗ Results differ between functions")
            return False

        return True

    except Exception as e:
        print(f"✗ Error during computation: {e}")
        return False


if __name__ == "__main__":
    success = test_basic_functionality()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Tests failed!")
        exit(1)
