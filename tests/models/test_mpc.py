from auto_complete_server.models.mpc import MostPopularCompletionModel


def test_model_init():
    """Test the MPC model init."""
    mpc = MostPopularCompletionModel()
    assert mpc
