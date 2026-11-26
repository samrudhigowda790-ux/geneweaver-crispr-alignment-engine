
import pytest

from geneweaver.cpu_aligner import align_sequences
from geneweaver.scheduler import align_batch


def test_batch_alignment_returns_all_results():
    pairs = [
        ("ATCG", "ATCG"),
        ("ATCG", "ATGG"),
        ("AAAA", "AAAT"),
    ]

    results = align_batch(pairs)

    assert len(results) == 3
    assert results[0].score == 8
    assert results[1].score == 5


def test_batch_results_match_cpu_aligner():
    pairs = [
        ("ATCG", "ATCG"),
        ("ATCG", "ATGG"),
        ("ATCG", "ATACG"),
    ]

    results = align_batch(pairs)

    for index, pair in enumerate(pairs):
        expected = align_sequences(pair[0], pair[1])
        assert results[index] == expected


def test_batch_preserves_input_order():
    pairs = [
        ("AAAA", "AAAA"),
        ("ATCG", "ATGG"),
        ("GGGG", "GGGG"),
    ]

    results = align_batch(pairs)

    assert results[0].score == 8
    assert results[1].score == 5
    assert results[2].score == 8


def test_batch_with_custom_scoring():
    pairs = [("ATCG", "ATGG")]

    results = align_batch(
        pairs,
        match_score=3,
        mismatch_penalty=-2,
        gap_penalty=-3,
    )

    expected = align_sequences(
        "ATCG",
        "ATGG",
        match_score=3,
        mismatch_penalty=-2,
        gap_penalty=-3,
    )

    assert results[0] == expected


def test_empty_batch_returns_empty_list():
    assert align_batch([]) == []


def test_invalid_pair_rejected():
    with pytest.raises(ValueError):
        align_batch([("ATCG",)])


def test_invalid_dna_sequence_rejected():
    with pytest.raises(ValueError):
        align_batch([("ATCX", "ATCG")])


def test_batch_with_multiple_workers():
    pairs = [
        ("ATCG", "ATCG"),
        ("AAAA", "AAAT"),
    ]

    results = align_batch(pairs, num_workers=2)

    assert len(results) == 2
    assert results[0].score == 8
