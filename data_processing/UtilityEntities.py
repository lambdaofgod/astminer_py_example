# coding=utf-8
import torch


# Utility classes wrapping all entities generated by PathMiner.


class PathContext:
    def __init__(self, start_token, path, end_token):
        self.start_token = start_token
        self.path = path
        self.end_token = end_token

    @classmethod
    def fromstring(cls, s, sep=" "):
        return cls(*map(int, s.split(sep)))

    def resolve(self, dataset):
        return (
            dataset.get_token(self.start_token),
            dataset.get_path(self.path),
            dataset.get_token(self.end_token),
        )


class Path:
    def __init__(self, node_types):
        self.node_types = node_types

    @classmethod
    def fromstring(cls, s, sep=" "):
        return cls(list(map(int, s.split(sep))))

    def substitute_nodes(self, nodes):
        return list(map(lambda ind: nodes[ind], self.node_types))

    def prettyprint(self, nodes):
        return " ".join(
            map(lambda node: node.prettyprint(), self.substitute_nodes(nodes))
        )


class NodeType:
    def __init__(self, node_type, direction):
        self.node_type = node_type
        self.direction = direction

    @classmethod
    def fromstring(cls, s, sep=" "):
        return cls(*s.split(sep))

    def prettyprint(self):
        if self.direction == "UP":
            arrow = "↑"
        elif self.direction == "DOWN":
            arrow = "↓"
        else:
            arrow = " " + self.direction
        return self.node_type + arrow
