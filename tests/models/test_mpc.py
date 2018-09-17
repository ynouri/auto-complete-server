import pytest
from auto_complete_server.models.mpc import MostPopularCompletionModel
import os

TEST_CORPUS_FILE = os.path.join('data', 'test_conversations.json')


def test_model_init():
    """Test the MPC model init."""
    mpc = MostPopularCompletionModel()
    assert mpc


@pytest.fixture(scope='module')
def mpc():
    """Set up a MPC model and build trie from a test corpus file."""
    mpc = MostPopularCompletionModel()
    mpc.build_trie(TEST_CORPUS_FILE)
    yield mpc


def test_trie_is_built(mpc):
    """Test if the trie exists."""
    assert mpc.trie


def test_trie_keys(mpc):
    """Test that a key is the trie."""
    test_key = 'I am sorry for the inconveniences.'
    test_keys = mpc.trie.keys('I')
    assert test_key in test_keys


def test_trie_value(mpc):
    """Test that a sentence frequency is correctly returned by the trie."""
    test_key = 'How can I help you?'
    test_value = mpc.trie[test_key]
    expected_value = 4
    assert test_value == expected_value
