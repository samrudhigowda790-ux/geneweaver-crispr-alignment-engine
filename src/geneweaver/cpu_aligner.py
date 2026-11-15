from dataclasses import dataclass

VALID_DNA_BASES = set("ACGTRYSWKMBDHVN")

@dataclass(frozen=True)
class AlignmentResult:
    aligned_sequence_a: str
    aligned_sequence_b: str
    score: int
    mismatch_positions: tuple
    gap_count: int

def align_sequences(
    sequence_a,
    sequence_b,
    match_score=2,
    mismatch_penalty=-1,
    gap_penalty=-2
):
    """
    Perform global DNA sequence alignment using Needleman-Wunsch.
    Mismatch positions are reported as 1-based alignment columns.
    """

    sequence_a = sequence_a.upper()
    sequence_b = sequence_b.upper()

    if not sequence_a or not sequence_b:
        raise ValueError("DNA sequences must not be empty")

    if set(sequence_a) - VALID_DNA_BASES:
        raise ValueError("Sequence A contains invalid DNA characters")

    if set(sequence_b) - VALID_DNA_BASES:
        raise ValueError("Sequence B contains invalid DNA characters")

    rows = len(sequence_a) + 1
    columns = len(sequence_b) + 1

    # Create score and traceback matrices.
    scores = [[0] * columns for _ in range(rows)]
    traceback = [[None] * columns for _ in range(rows)]

    # Initialize first column and row with gap penalties.
    for i in range(1, rows):
        scores[i][0] = i * gap_penalty
        traceback[i][0] = "up"

    for j in range(1, columns):
        scores[0][j] = j * gap_penalty
        traceback[0][j] = "left"

    # Fill the dynamic programming matrices.
    for i in range(1, rows):
        for j in range(1, columns):
            if sequence_a[i - 1] == sequence_b[j - 1]:
                diagonal_score = scores[i - 1][j - 1] + match_score
            else:
                diagonal_score = (
                    scores[i - 1][j - 1] + mismatch_penalty
                )

            up_score = scores[i - 1][j] + gap_penalty
            left_score = scores[i][j - 1] + gap_penalty

            best_score = max(diagonal_score, up_score, left_score)
            scores[i][j] = best_score

            # Deterministic tie-breaking: diagonal, then up, then left.
            if best_score == diagonal_score:
                traceback[i][j] = "diagonal"
            elif best_score == up_score:
                traceback[i][j] = "up"
            else:
                traceback[i][j] = "left"

    # Trace back to construct the aligned sequences.
    aligned_a = []
    aligned_b = []
    i = len(sequence_a)
    j = len(sequence_b)

    while i > 0 or j > 0:
        direction = traceback[i][j]

        if direction == "diagonal":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append(sequence_b[j - 1])
            i -= 1
            j -= 1

        elif direction == "up":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append("-")
            i -= 1

        elif direction == "left":
            aligned_a.append("-")
            aligned_b.append(sequence_b[j - 1])
            j -= 1

    aligned_a.reverse()
    aligned_b.reverse()

    aligned_a = "".join(aligned_a)
    aligned_b = "".join(aligned_b)

    # Find mismatch columns and count gap columns.
    mismatch_positions = []
    gap_count = 0

    for position, (base_a, base_b) in enumerate(
        zip(aligned_a, aligned_b), start=1
    ):
        if base_a == "-" or base_b == "-":
            gap_count += 1
        elif base_a != base_b:
            mismatch_positions.append(position)

    return AlignmentResult(
        aligned_sequence_a=aligned_a,
        aligned_sequence_b=aligned_b,
        score=scores[-1][-1],
        mismatch_positions=tuple(mismatch_positions),
        gap_count=gap_count
    )
