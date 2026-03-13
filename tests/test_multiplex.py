import networkx as nx
import pytest
from graph.multiplex import MultiplexGraph, EdgeDirection


def test_add_layer():
    g = MultiplexGraph()
    layer = nx.Graph()
    g.add_layer("power", layer)
    assert "power" in g.layers


def test_add_layer_duplicate():
    g = MultiplexGraph()
    layer = nx.Graph()
    g.add_layer("power", layer)
    with pytest.raises(ValueError, match="`power` layer already exists"):
        g.add_layer("power", layer)


def test_add_interdependency():
    g = MultiplexGraph()
    layer_a = nx.Graph()
    layer_b = nx.Graph()
    layer_a.add_node("A1")
    layer_b.add_node("B1")
    g.add_layer("power", layer_a)
    g.add_layer("communication", layer_b)
    g.add_interdependency(
        "A1", "power", "B1", "communication", weight=2.0, direction=EdgeDirection.A_TO_B
    )
    assert len(g.interdependencies) == 1
    interdependency = g.interdependencies[0]
    assert interdependency["node_a"] == "A1"
    assert interdependency["layer_a"] == "power"
    assert interdependency["node_b"] == "B1"
    assert interdependency["layer_b"] == "communication"
    assert interdependency["weight"] == 2.0
    assert interdependency["direction"] == EdgeDirection.A_TO_B


def test_summary():
    g = MultiplexGraph()
    layer_a = nx.Graph()
    layer_b = nx.Graph()
    layer_a.add_node("A1")
    layer_b.add_node("B1")
    g.add_layer("power", layer_a)
    g.add_layer("communication", layer_b)
    g.add_interdependency(
        "A1", "power", "B1", "communication", weight=2.0, direction=EdgeDirection.A_TO_B
    )
    summary = g.summary()
    assert summary["num_layers"] == 2
    assert summary["num_interdependencies"] == 1
