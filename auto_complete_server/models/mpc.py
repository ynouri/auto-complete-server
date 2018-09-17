from .base import BaseAutoCompleteModel
import datrie
import string
import pandas as pd
import json
import nltk
import operator


class MostPopularCompletionModel(BaseAutoCompleteModel):
    """Most Popular Completion (Bar-Yossef Kraus 2011) trie based model."""

    def load(self, trie_file):
        """Load the trie data structure storing completions and frequencies."""
        df = pd.DataFrame()
        return df

    def build_trie(self, corpus_file):
        """Read a corpus file and build the trie data structure."""
        # Deserialize the corpus file into a dict
        with open(corpus_file, encoding='utf8') as f:
            corpus_json = json.loads(f.read())

        # Create a dataframe of messages from the corpus dict
        df_messages = pd.io.json.json_normalize(
            data=corpus_json,
            record_path=['Issues', 'Messages'],
            meta=[
                ['Issues', 'CompanyGroupId'],
                ['Issues', 'IssueId']
            ]
        )

        # Rename columns for simplicity of usage
        new_columns = {
            'Issues.IssueId': 'IssueId',
            'Issues.CompanyGroupId': 'CompanyGroupId'
        }
        df_messages.rename(columns=new_columns, inplace=True)

        # Instantiate a Punkt tokenizer from the english pickle
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

        # Split each message row into its different sentences and create a
        # dataframe of sentences. Note: the creation of the sentences dataframe
        # might not be scalable for a corpus of a billion messages with this
        # implementation. A clever usage of pandas stack() and joins might
        # enable to do it in a more efficient fashion.
        columns = ['IssueId', 'CompanyGroupId', 'IsFromCustomer', 'SentenceId',
                   'Sentence']
        df_sentences = pd.DataFrame(columns=columns)
        for message in df_messages.itertuples():
            sentences = tokenizer.tokenize(message.Text)
            for i, sentence in enumerate(sentences):
                new_row = [message.IssueId, message.CompanyGroupId,
                           message.IsFromCustomer, i, sentence]
                df_sentences = df_sentences.append(
                    dict(zip(columns, new_row)),
                    ignore_index=True
                )

        # Computes the frequencies for each non-customer sentence in the corpus
        not_customer = df_sentences.IsFromCustomer == False  # noqa: E712
        sentences_freq = df_sentences[not_customer].Sentence.value_counts()

        # Create and build the trie by inserting each sentence and its freq
        self.trie = datrie.Trie(string.printable)
        for sentence, freq in sentences_freq.iteritems():
            self.trie[sentence] = freq
        return self.trie

    def generate_completions(self, prefix):
        """Generate completions for a given prefix."""
        # Return empty list if prefix is empty
        if prefix == '':
            return []

        # Else, get sentences with their frequencies from the trie
        sentences_freq = self.trie.items(prefix)
        sorted_d = sorted(
            dict(sentences_freq).items(),
            key=operator.itemgetter(1),
            reverse=True
        )

        # Return only a maximum number of completions set during model init
        n_results = min(len(sorted_d), self.max_completions)

        # Return only sentences, not the frequencies
        completions = list(dict(sorted_d[:n_results]).keys())

        return completions
