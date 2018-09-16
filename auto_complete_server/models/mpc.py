from .base import BaseAutoCompleteModel
import datrie
import string
import pandas as pd


class MostPopularCompletionModel(BaseAutoCompleteModel):
    """Most Popular Completion (Bar-Yossef Kraus 2011) trie based model."""

    def load(self, trie_file):
        """Load the trie data structure storing completions and frequencies."""
        df = pd.DataFrame()
        return df

    def build_trie(self, corpus_file):
        """Read a corpus file and build the trie data structure."""
        self.trie = datrie.Trie(string.printable)

    def generate_completions(self, prefix):
        """Generate completions for a given prefix."""
        pass
