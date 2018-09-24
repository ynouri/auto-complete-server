"""Most Popular Completion model classes."""

import operator
import string
import json
import logging
import pandas as pd
import nltk
import datrie
from .base import BaseAutoCompleteModel


class MostPopularCompletionModel(BaseAutoCompleteModel):
    """Most Popular Completion (Bar-Yossef Kraus 2011) trie based model."""

    def __init__(self, max_completions=5):
        """Init the model with a maximum number of returned completions."""
        self.max_completions = max_completions
        self.trie = None

    def save(self, file):
        """Save the trie data structure to a file."""
        logging.info("Saving trie to %s", file)
        self.trie.save(file)

    def load(self, file):
        """Load the trie data structure storing completions and frequencies."""
        logging.info("Loading trie from %s", file)
        self.trie = datrie.Trie.load(file)
        return self.trie

    @staticmethod
    def _read_corpus(corpus_file):
        """Read a corpus file and return a dataframe of messages."""
        logging.info("Start reading corpus from %s", corpus_file)
        # Deserialize the corpus file into a dict
        with open(corpus_file, encoding="utf8") as file:
            corpus_json = json.loads(file.read())

        # Create a dataframe of messages from the corpus dict
        df_messages = pd.io.json.json_normalize(
            data=corpus_json,
            record_path=["Issues", "Messages"],
            meta=[["Issues", "CompanyGroupId"], ["Issues", "IssueId"]],
        )

        # Rename columns for simplicity of usage
        new_columns = {
            "Issues.IssueId": "IssueId",
            "Issues.CompanyGroupId": "CompanyGroupId",
        }
        df_messages.rename(columns=new_columns, inplace=True)
        logging.info("Finished reading corpus.")
        return df_messages

    @staticmethod
    def _split_into_sentences(df_messages):
        """Split a dataframe of messages into a dataframe of sentences."""
        logging.info("Start split messages into sentences...")
        # Instantiate a Punkt tokenizer from the english pickle
        tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")

        # Split each message row into its different sentences and create a
        # dataframe of sentences. Note: the creation of the sentences dataframe
        # might not be scalable for a corpus of a billion messages with this
        # implementation. A clever usage of pandas stack() and joins might
        # enable to do it in a more efficient fashion.
        columns = [
            "IssueId",
            "CompanyGroupId",
            "IsFromCustomer",
            "SentenceId",
            "Sentence",
        ]
        df_sentences = pd.DataFrame(columns=columns)
        for message in df_messages.itertuples():
            sentences = tokenizer.tokenize(message.Text)
            for i, sentence in enumerate(sentences):
                new_row = [
                    message.IssueId,
                    message.CompanyGroupId,
                    message.IsFromCustomer,
                    i,
                    sentence,
                ]
                df_sentences = df_sentences.append(
                    dict(zip(columns, new_row)), ignore_index=True
                )
        logging.info("Finished split messages into sentences.")
        return df_sentences

    @staticmethod
    def _insert_into_trie(items):
        """Insert items into a datrie trie."""
        logging.info("Start inserting into trie...")
        trie = datrie.Trie(string.printable)  # noqa
        for key, val in items.iteritems():
            trie[key] = val
        logging.info("Finished inserting into trie.")
        return trie

    def build_trie(self, corpus_file):
        """Read a corpus file and build the trie data structure."""
        df_messages = self._read_corpus(corpus_file)
        # pylint: disable=C0121
        not_customer = df_messages.IsFromCustomer == False  # noqa: E712
        df_sentences = self._split_into_sentences(df_messages[not_customer])
        sentences_freq = df_sentences.Sentence.value_counts()
        self.trie = self._insert_into_trie(sentences_freq)
        return self.trie

    def generate_completions(self, prefix):
        """Generate completions for a given prefix."""
        # Return empty list if prefix is empty
        if prefix == "":
            return []

        # Else, get sentences with their frequencies from the trie
        sentences_freq = self.trie.items(prefix)
        sorted_d = sorted(
            dict(sentences_freq).items(),
            key=operator.itemgetter(1),
            reverse=True,
        )

        # Return only a maximum number of completions set during model init
        n_results = min(len(sorted_d), self.max_completions)

        # Return only sentences, not the frequencies
        completions = list(dict(sorted_d[:n_results]).keys())

        return completions
