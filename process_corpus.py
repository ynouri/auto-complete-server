#!/usr/bin/env python3
"""Process a corpus file and generates a trie file."""

import logging
import click
from auto_complete_server.models.mpc import MostPopularCompletionModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M:%S",
)


@click.command()
@click.argument("corpus-file", type=click.Path(exists=True))
@click.argument("trie-file")
def process_corpus(corpus_file, trie_file):
    """Process a corpus file and generates a trie file."""
    mpc = MostPopularCompletionModel()
    mpc.build_trie(corpus_file)
    mpc.save(trie_file)


if __name__ == "__main__":
    process_corpus()  # pylint: disable=no-value-for-parameter
