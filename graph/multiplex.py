import networkx as nx
from enum import Enum


class EdgeDirection(Enum):
    A_TO_B = "a_to_b"
    B_TO_A = "b_to_a"
    BIDIRECTIONAL = "bidirectional"


class MultiplexGraph:
    def __init__(self):
        """
        A multiplex graph is a collection of layers, where each layer is a graph. The layers are connected by interdependencies, which are edges that connect nodes in different layers. The interdependencies can have weights and directions.
        """
        self.layers = {}
        self.interdependencies = []

    def add_layer(self, name, graph):
        """
        Add a layer to the multiplex graph.
        Args:
            name (str): The name of the layer.
            graph (networkx.Graph): The graph representing the layer.
        Raises:
            ValueError: If the layer already exists.
        """
        if name in self.layers:
            raise ValueError(f"`{name}` layer already exists")
        self.layers[name] = graph

    def add_interdependency(
        self,
        node_a,
        layer_a,
        node_b,
        layer_b,
        weight=1.0,
        direction=EdgeDirection.BIDIRECTIONAL,
    ):
        """
        Add an interdependency between two nodes in different layers.
        Args:
            node_a (str): The name of the node in layer_a.
            layer_a (str): The name of the layer containing node_a.
            node_b (str): The name of the node in layer_b.
            layer_b (str): The name of the layer containing node_b.
            weight (float, optional): The weight of the interdependency. Defaults to 1.0.
            direction (EdgeDirection, optional): The direction of the interdependency. Defaults to EdgeDirection.BIDIRECTIONAL.
        Raises:
            ValueError: If any of the layers or nodes do not exist.
        """
        if layer_a not in self.layers:
            raise ValueError(f"`{layer_a}` layer does not exist")
        if layer_b not in self.layers:
            raise ValueError(f"`{layer_b}` layer does not exist")
        if node_a not in self.layers[layer_a]:
            raise ValueError(f"`{node_a}` node does not exist in `{layer_a}` layer")
        if node_b not in self.layers[layer_b]:
            raise ValueError(f"`{node_b}` node does not exist in `{layer_b}` layer")
        if isinstance(direction, EdgeDirection):
            validated_direction = direction
        elif isinstance(direction, str):
            validated_direction = EdgeDirection(direction)
        else:
            raise ValueError(
                f"direction must be an EdgeDirection or string, got {type(direction)}"
            )
        # Using a dict to store interdependencies to allow for duplicate interdependencies between the same nodes and layers aa this may happen in real world infra for resilience purposes. If we used a set, we would lose this information.
        self.interdependencies.append(
            {
                "node_a": node_a,
                "layer_a": layer_a,
                "node_b": node_b,
                "layer_b": layer_b,
                "weight": weight,
                "direction": validated_direction,
            }
        )

    def get_layer(self, name):
        """
        Get a layer by name.
        Args:
            name (str): The name of the layer.
        Returns:
            networkx.Graph: The graph representing the layer.
        Raises:
            ValueError: If the layer does not exist.
        """
        if name not in self.layers:
            raise ValueError(f"`{name}` layer does not exist")
        return self.layers[name]

    def summary(self):
        """
        Get a summary of the multiplex graph.
        Returns:
            dict: A summary of the multiplex graph, including the number of layers, the number of nodes and edges in each layer, and the number of interdependencies.
        """
        summary = {
            "num_layers": len(self.layers),
            "layers": {},
            "num_interdependencies": len(self.interdependencies),
        }
        for layer_name, graph in self.layers.items():
            summary["layers"][layer_name] = {
                "num_nodes": graph.number_of_nodes(),
                "num_edges": graph.number_of_edges(),
            }
        return summary
