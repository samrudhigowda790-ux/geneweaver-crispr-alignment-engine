import pytest

from geneweaver.pam_recognition import (
    find_pam_sites,
    reverse_complement,
    find_pam_sites_both_strands,
    find_protospacers,
)

def test_finds_spcas9_pam():
    result = find_pam_sites("ATCGATCGAGG")

    assert result == [
        {"position": 9, "pam_sequence": "AGG"}
    ]


def test_finds_multiple_pam_sites():
    result = find_pam_sites("AAGGCTGG")

    assert result == [
        {"position": 2, "pam_sequence": "AGG"},
        {"position": 6, "pam_sequence": "TGG"}
    ]


def test_returns_empty_when_no_pam_exists():
    assert find_pam_sites("ATATATAT") == []


def test_supports_lowercase_sequence():
    assert find_pam_sites("atcgatcgagg") == [
        {"position": 9, "pam_sequence": "AGG"}
    ]


def test_rejects_empty_sequence():
    with pytest.raises(ValueError):
        find_pam_sites("")


def test_rejects_invalid_sequence():
    with pytest.raises(ValueError):
        find_pam_sites("ATGXGG")


def test_rejects_empty_pam_pattern():
    with pytest.raises(ValueError):
        find_pam_sites("ATCG", "")


def test_rejects_invalid_pam_pattern():
    with pytest.raises(ValueError):
        find_pam_sites("ATCG", "XGG")


def test_pam_longer_than_sequence():
    assert find_pam_sites("AT", "NGG") == []

def test_reverse_complement():
    assert reverse_complement("AGTC") == "GACT"


def test_finds_reverse_strand_pam():
    result = find_pam_sites_both_strands("CCT")

    assert result == [
        {
            "position": 1,
            "pam_sequence": "AGG",
            "strand": "-"
        }
    ]


def test_finds_forward_strand_pam():
    result = find_pam_sites_both_strands("AGG")

    assert result == [
        {
            "position": 1,
            "pam_sequence": "AGG",
            "strand": "+"
        }
    ]

def test_finds_forward_strand_protospacer():
    sequence = "A" * 20 + "AGG"

    result = find_protospacers(sequence)

    assert len(result) == 1
    assert result[0]["protospacer_sequence"] == "A" * 20
    assert result[0]["protospacer_start"] == 1
    assert result[0]["protospacer_end"] == 20
    assert result[0]["pam_position"] == 21
    assert result[0]["strand"] == "+"


def test_finds_reverse_strand_protospacer():
    sequence = "CCT" + "A" * 20

    result = find_protospacers(sequence)

    assert len(result) == 1
    assert result[0]["protospacer_sequence"] == "T" * 20
    assert result[0]["protospacer_start"] == 4
    assert result[0]["protospacer_end"] == 23
    assert result[0]["pam_position"] == 1
    assert result[0]["strand"] == "-"


def test_skips_protospacer_with_insufficient_bases():
    result = find_protospacers("A" * 10 + "AGG")

    assert result == []


def test_supports_custom_protospacer_length():
    result = find_protospacers("AAAATGG", protospacer_length=4)

    assert len(result) == 1
    assert result[0]["protospacer_sequence"] == "AAAA"
    assert result[0]["protospacer_start"] == 1
    assert result[0]["protospacer_end"] == 4


@pytest.mark.parametrize("length", [0, -1, True, 2.5])
def test_rejects_invalid_protospacer_length(length):
    with pytest.raises(ValueError):
        find_protospacers("A" * 20 + "AGG", protospacer_length=length)