import pandas as pd
from os import path
import parse

from data_processing.UtilityEntities import PathContext, Path, NodeType


# Loads all .csv files generated by PathMiner in pd.Series or pd.Dataframe
class PathMinerLoader:

    def __init__(self, tokens_file, paths_file, node_types_file, path_contexts_file):
        self.unit_sep = " "
        self.path_sep = ","
        self.tokens = self._load_tokens(tokens_file)
        self.node_types = self._load_node_types(node_types_file)
        self.paths = self._load_paths(paths_file)
        self.path_contexts = self._load_path_contexts(path_contexts_file)

    @classmethod
    def from_folder(cls, dataset_folder):
        return cls(path.join(dataset_folder, 'tokens.csv'),
                   path.join(dataset_folder, 'paths.csv'),
                   path.join(dataset_folder, 'node_types.csv'),
                   path.join(dataset_folder, "data", 'path_contexts.c2s'))

    # Token loading is slightly complex because tokens can contain any symbols
    @staticmethod
    def _load_tokens(tokens_file):
        fstring = '{:d},{}'
        with open(tokens_file, 'r') as f:
            indices = []
            tokens = []
            for line in f.readlines()[1:]:
                parsed = parse.parse(fstring, line)
                if parsed is not None:
                    ind, token = parsed
                    indices.append(ind)
                    tokens.append(token)
                else:
                    tokens[-1] += line

        # Remove line breaks at the end of tokens
        for i in range(len(tokens)):
            tokens[i] = tokens[i][:-1]

        return pd.Series(data=tokens, index=indices)

    def _load_paths(self, paths_file):
        paths = pd.read_csv(paths_file, sep=",", index_col=0, squeeze=True)
        paths = paths.map(Path.fromstring)
        return paths

    def _load_node_types(self, node_types_file):
        node_types = pd.read_csv(node_types_file, sep=self.unit_sep, index_col=0, squeeze=True)
        node_types = node_types.map(NodeType.fromstring)
        return node_types

    def _load_path_contexts(self, path_contexts_file):
        contexts = pd.read_csv(path_contexts_file, sep=".py")
        contexts.columns = ["file_name", "path_contexts"]


        contexts['path_contexts'] = contexts['path_contexts'].fillna('').str.strip()
        ex_ctx = contexts['path_contexts'].iloc[0]
        import ipdb; ipdb.set_trace()
        contexts['path_contexts'] = contexts['path_contexts'].str.split(self.unit_sep).map(
            lambda ctx: list(map(PathContext.fromstring, ctx.split(self.path_sep))) if ctx else list()
        )
        return contexts
