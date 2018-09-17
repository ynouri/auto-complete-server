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
    mpc = MostPopularCompletionModel(max_completions=3)
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


def test_number_of_completions(mpc):
    """Test that MPC returns the max number of completions set in init."""
    test_completions = mpc.generate_completions('H')
    expected_len_completions = 3
    assert len(test_completions) == expected_len_completions


def test_top_completion(mpc):
    """Test the top completion returned by MPC."""
    test_top_completion = mpc.generate_completions('H')[0]
    expected_top_completion = 'How can I help you?'
    assert test_top_completion == expected_top_completion


def test_no_completion(mpc):
    """Test the case where no completion is returned."""
    test_completions = mpc.generate_completions('1234$!@#$%^&*()_+=<>?[]{}')
    assert test_completions == []


def test_completion_blank_prefix(mpc):
    """Test that the blank prefix case returns nothing."""
    assert mpc.generate_completions('') == []
