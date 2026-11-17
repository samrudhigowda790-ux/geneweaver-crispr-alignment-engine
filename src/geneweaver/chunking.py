def split_sequence(sequence, chunk_size=100, overlap=0):
    """Split a DNA sequence into chunks with optional overlap."""

    if not isinstance(sequence, str):
        raise TypeError("Sequence must be a string.")

    if not sequence:
        raise ValueError("Sequence cannot be empty.")

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be non-negative and smaller than chunk size.")

    sequence = sequence.upper()
    step = chunk_size - overlap
    chunks = []
    start = 0

    while start < len(sequence):
        chunk = sequence[start:start + chunk_size]
        chunks.append(chunk)

        if start + chunk_size >= len(sequence):
            break

        start += step

    return chunks
