
VALID_BASES = set("ACGT")


def find_pam_sites(sequence, pam_pattern="NGG"):
    """
    Find PAM sites in a DNA sequence.

    Currently supports exact matching and N as
    a wildcard representing any standard DNA base.

    Positions returned are 1-based.
    """

    sequence = sequence.upper()
    pam_pattern = pam_pattern.upper()

    if not sequence:
        raise ValueError("DNA sequence must not be empty")

    if set(sequence) - VALID_BASES:
        raise ValueError("Sequence must contain only A, C, G and T")

    if not pam_pattern:
        raise ValueError("PAM pattern must not be empty")

    if any(base not in VALID_BASES | {"N"} for base in pam_pattern):
        raise ValueError("Invalid PAM pattern")

    pam_length = len(pam_pattern)
    matches = []

    for i in range(len(sequence) - pam_length + 1):
        candidate = sequence[i:i + pam_length]

        is_match = all(
            pattern_base == "N" or pattern_base == sequence_base
            for pattern_base, sequence_base in zip(pam_pattern, candidate)
        )

        if is_match:
            matches.append({
                "position": i + 1,
                "pam_sequence": candidate
            })

    return matches

def reverse_complement(sequence):
    sequence = sequence.upper()

    if not sequence:
        raise ValueError("DNA sequence must not be empty")

    if set(sequence) - VALID_BASES:
        raise ValueError("Sequence must contain only A, C, G and T")

    complement = str.maketrans("ACGT", "TGCA")
    return sequence.translate(complement)[::-1]


def find_pam_sites_both_strands(sequence, pam_pattern="NGG"):
    sequence = sequence.upper()

    if not sequence:
        raise ValueError("DNA sequence must not be empty")

    forward_matches = find_pam_sites(sequence, pam_pattern)

    reverse_sequence = reverse_complement(sequence)
    reverse_matches = find_pam_sites(reverse_sequence, pam_pattern)

    results = []

    for match in forward_matches:
        results.append({
            **match,
            "strand": "+"
        })

    for match in reverse_matches:
        original_position = (
            len(sequence) - match["position"] - len(pam_pattern) + 2
        )

        results.append({
            "position": original_position,
            "pam_sequence": match["pam_sequence"],
            "strand": "-"
        })

    return sorted(results, key=lambda item: item["position"])
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