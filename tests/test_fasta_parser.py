import pytest

from geneweaver.fasta_parser import parse_fasta


def test_parse_single_sequence(tmp_path):
    fasta = tmp_path / "sample.fasta"
    fasta.write_text(">gene1\nATCGATCG\n")

    records = parse_fasta(fasta)

    assert len(records) == 1
    assert records[0].id == "gene1"
    assert records[0].sequence == "ATCGATCG"


def test_parse_multiple_sequences(tmp_path):
    fasta = tmp_path / "sample.fasta"
    fasta.write_text(">gene1\nATCG\n>gene2\nGGTA\n")

    records = parse_fasta(fasta)

    assert len(records) == 2
    assert records[1].id == "gene2"
    assert records[1].sequence == "GGTA"


def test_sequence_is_converted_to_uppercase(tmp_path):
    fasta = tmp_path / "sample.fasta"
    fasta.write_text(">gene1\natcg\n")

    records = parse_fasta(fasta)

    assert records[0].sequence == "ATCG"


def test_invalid_dna_character(tmp_path):
    fasta = tmp_path / "sample.fasta"
    fasta.write_text(">gene1\nATCX\n")

    with pytest.raises(ValueError):
        parse_fasta(fasta)


def test_missing_header(tmp_path):
    fasta = tmp_path / "sample.fasta"
    fasta.write_text("ATCGATCG\n")

    with pytest.raises(ValueError):
        parse_fasta(fasta)


def test_empty_file(tmp_path):
    fasta = tmp_path / "empty.fasta"
    fasta.write_text("")

    with pytest.raises(ValueError):
        parse_fasta(fasta)


def test_empty_sequence(tmp_path):
    fasta = tmp_path / "empty_sequence.fasta"
    fasta.write_text(">gene1\n>gene2\nATCG\n")

    with pytest.raises(ValueError):
        parse_fasta(fasta)


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        parse_fasta("missing_file.fasta")


def test_header_description(tmp_path):
    fasta = tmp_path / "sample.fasta"
    fasta.write_text(">gene1 human chromosome\nATCG\n")

    records = parse_fasta(fasta)

    assert records[0].id == "gene1"
    assert records[0].description == "gene1 human chromosome"
