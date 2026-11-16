import pytest
from geneweaver.scoring import score_alignment


def test_exact_match():
    assert score_alignment("ATCG", "ATCG") == 8


def test_single_mismatch():
    assert score_alignment("ATCG", "ATGG") == 5


def test_gap_penalty():
    assert score_alignment("AT-CG", "ATTCG") == 6


def test_custom_scoring():
    assert score_alignment("ATCG", "ATGG", 3, -2, -4) == 7


def test_unequal_lengths_rejected():
    with pytest.raises(ValueError):
        score_alignment("ATCG", "ATC")


def test_empty_sequences_rejected():
    with pytest.raises(ValueError):
        score_alignment("", "")


def test_lowercase_sequences():
    assert score_alignment("atcg", "ATCG") == 8
