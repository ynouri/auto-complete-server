import pytest
from auto_complete_server.models.mpc import MostPopularCompletionModel
import os.path

TEST_CORPUS_FILE = os.path.join("data", "test_conversations.json")
TEST_SAVE_FILE = os.path.join("models", "test.trie")


def test_model_init():
    """Test the MPC model init."""
    mpc = MostPopularCompletionModel()
    assert mpc


@pytest.fixture(scope="module")
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
    expected_key = "I am sorry for the inconveniences."
    keys = mpc.trie.keys("I")
    assert expected_key in keys


def test_trie_value(mpc):
    """Test that a sentence frequency is correctly returned by the trie."""
    key = "How can I help you?"
    value = mpc.trie[key]
    expected_value = 4
    assert value == expected_value


def test_number_of_completions(mpc):
    """Test that MPC returns the max number of completions set in init."""
    completions = mpc.generate_completions("H")
    expected_len_completions = 3
    assert len(completions) == expected_len_completions


def test_top_completion(mpc):
    """Test the top completion returned by MPC."""
    top_completion = mpc.generate_completions("H")[0]
    expected_top_completion = "How can I help you?"
    assert top_completion == expected_top_completion


def test_no_completion(mpc):
    """Test the case where no completion is returned."""
    test_completions = mpc.generate_completions("1234$!@#$%^&*()_+=<>?[]{}")
    assert test_completions == []


def test_completion_blank_prefix(mpc):
    """Test that the blank prefix case returns nothing."""
    assert mpc.generate_completions("") == []


def test_save(mpc):
    """Test that the trie is correctly saved to a file."""
    mpc.save(TEST_SAVE_FILE)
    assert os.path.isfile(TEST_SAVE_FILE)


def test_save_and_reload(mpc):
    """Test that a saved trie can succesfully be reloaded."""
    mpc.save(TEST_SAVE_FILE)
    expected_items = mpc.trie.items()
    del mpc
    new_mpc = MostPopularCompletionModel()
    new_mpc.load(TEST_SAVE_FILE)
    assert new_mpc.trie.items() == expected_items
