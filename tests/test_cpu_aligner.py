import pytest

from geneweaver.cpu_aligner import align_sequences

def test_exact_match():
    result = align_sequences("ATCG", "ATCG")

    assert result.aligned_sequence_a == "ATCG"
    assert result.aligned_sequence_b == "ATCG"
    assert result.score == 8
    assert result.mismatch_positions == ()
    assert result.gap_count == 0

def test_single_mismatch():
    result = align_sequences("ATCG", "ATGG")

    assert result.aligned_sequence_a == "ATCG"
    assert result.aligned_sequence_b == "ATGG"
    assert result.score == 5
    assert result.mismatch_positions == (3,)
    assert result.gap_count == 0

def test_insertion_or_deletion():
    result = align_sequences("ATCG", "ATACG")

    assert len(result.aligned_sequence_a) == len(
        result.aligned_sequence_b
    )
    assert "-" in result.aligned_sequence_a or "-" in result.aligned_sequence_b
    assert result.gap_count >= 1

def test_custom_scoring():
    result = align_sequences(
        "ATCG",
        "ATGG",
        match_score=3,
        mismatch_penalty=-2,
        gap_penalty=-3
    )

    assert result.score == 7

def test_empty_sequence_rejected():
    with pytest.raises(ValueError):
        align_sequences("", "ATCG")

def test_invalid_dna_character_rejected():
    with pytest.raises(ValueError):
        align_sequences("ATCX", "ATCG")

def test_lowercase_sequences():
    result = align_sequences("atcg", "ATCG")

    assert result.score == 8
    assert result.mismatch_positions == ()

def test_alignment_lengths_are_equal():
    result = align_sequences("ATCG", "AG")

    assert len(result.aligned_sequence_a) == len(
        result.aligned_sequence_b
    )
