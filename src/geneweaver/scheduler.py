
from dask import compute, delayed

from geneweaver.cpu_aligner import align_sequences


def align_batch(
    sequence_pairs,
    match_score=2,
    mismatch_penalty=-1,
    gap_penalty=-2,
    num_workers=None,
):
    """
    Align multiple DNA sequence pairs using Dask task scheduling.

    Each pair is processed using the existing CPU alignment function.
    Results are returned in the same order as the input pairs.
    """

    tasks = []

    for pair in sequence_pairs:
        if not isinstance(pair, (tuple, list)) or len(pair) != 2:
            raise ValueError(
                "Each sequence pair must contain exactly two sequences."
            )

        sequence_a, sequence_b = pair

        task = delayed(align_sequences)(
            sequence_a,
            sequence_b,
            match_score=match_score,
            mismatch_penalty=mismatch_penalty,
            gap_penalty=gap_penalty,
        )

        tasks.append(task)

    if not tasks:
        return []

    results = compute(
        *tasks,
        scheduler="threads",
        num_workers=num_workers,
    )

    return list(results)
