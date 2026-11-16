def score_alignment(
    sequence_a,
    sequence_b,
    match_score=2,
    mismatch_penalty=-1,
    gap_penalty=-2
):
    """Calculate the score of two already-aligned DNA sequences."""

    if len(sequence_a) != len(sequence_b):
        raise ValueError("Aligned sequences must have equal lengths.")

    if not sequence_a:
        raise ValueError("Sequences cannot be empty.")

    score = 0

    for base_a, base_b in zip(sequence_a.upper(), sequence_b.upper()):
        if base_a == "-" or base_b == "-":
            score += gap_penalty
        elif base_a == base_b:
            score += match_score
        else:
            score += mismatch_penalty

    return score
