import pytest
from geneweaver.chunking import split_sequence


def test_split_sequence_into_equal_chunks():
    assert split_sequence("ATCGATCG", 4) == ["ATCG", "ATCG"]


def test_split_sequence_with_remainder():
    assert split_sequence("ATCGATCGA", 4) == ["ATCG", "ATCG", "A"]


def test_split_sequence_with_overlap():
    assert split_sequence("ATCGATCG", 4, 2) == ["ATCG", "CGAT", "ATCG"]


def test_sequence_shorter_than_chunk():
    assert split_sequence("ATCG", 10) == ["ATCG"]


def test_lowercase_sequence():
    assert split_sequence("atcgatcg", 4) == ["ATCG", "ATCG"]


def test_empty_sequence_rejected():
    with pytest.raises(ValueError):
        split_sequence("")


def test_zero_chunk_size_rejected():
    with pytest.raises(ValueError):
        split_sequence("ATCG", 0)


def test_invalid_overlap_rejected():
    with pytest.raises(ValueError):
        split_sequence("ATCGATCG", 4, 4)


def test_negative_overlap_rejected():
    with pytest.raises(ValueError):
        split_sequence("ATCGATCG", 4, -1)


def test_non_string_sequence_rejected():
    with pytest.raises(TypeError):
        split_sequence(None)
