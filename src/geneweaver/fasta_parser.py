from dataclasses import dataclass
from pathlib import Path


VALID_DNA_BASES = set("ACGTRYSWKMBDHVN")


@dataclass(frozen=True)
class FastaRecord:
    id: str
    description: str
    sequence: str


def parse_fasta(file_path):
    """Read and validate DNA sequences from a FASTA file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"FASTA file not found: {path}")

    records = []
    current_description = None
    current_sequence = []

    def save_record():
        if current_description is None:
            return

        sequence = "".join(current_sequence).upper()

        if not sequence:
            raise ValueError(
                f"Sequence '{current_description}' is empty"
            )

        invalid_bases = set(sequence) - VALID_DNA_BASES

        if invalid_bases:
            raise ValueError(
                f"Invalid DNA characters in '{current_description}': "
                f"{''.join(sorted(invalid_bases))}"
            )

        identifier = current_description.split()[0]

        records.append(
            FastaRecord(
                id=identifier,
                description=current_description,
                sequence=sequence
            )
        )

    with path.open("r", encoding="utf-8-sig") as fasta_file:
        for line_number, line in enumerate(fasta_file, start=1):
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                save_record()
                current_description = line[1:].strip()

                if not current_description:
                    raise ValueError(
                        f"Missing FASTA header at line {line_number}"
                    )

                current_sequence = []

            else:
                if current_description is None:
                    raise ValueError(
                        f"Sequence found before FASTA header at line {line_number}"
                    )

                current_sequence.append("".join(line.split()))

    save_record()

    if not records:
        raise ValueError("The FASTA file contains no sequences")

    return records
