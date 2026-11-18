from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from geneweaver.cpu_aligner import align_sequences
from geneweaver.scoring import score_alignment

app = FastAPI(
    title="GeneWeaver API",
    description="DNA sequence alignment and scoring API",
    version="1.0.0"
)


class AlignmentRequest(BaseModel):
    sequence_a: str = Field(min_length=1)
    sequence_b: str = Field(min_length=1)
    match_score: int = 2
    mismatch_penalty: int = -1
    gap_penalty: int = -2


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "application": "GeneWeaver"
    }


@app.post("/api/align")
def perform_alignment(request: AlignmentRequest):
    try:
        result = align_sequences(
            request.sequence_a,
            request.sequence_b,
            match_score=request.match_score,
            mismatch_penalty=request.mismatch_penalty,
            gap_penalty=request.gap_penalty
        )

        final_score = score_alignment(
            result.aligned_sequence_a,
            result.aligned_sequence_b,
            request.match_score,
            request.mismatch_penalty,
            request.gap_penalty
        )

        return {
            "aligned_sequence_a": result.aligned_sequence_a,
            "aligned_sequence_b": result.aligned_sequence_b,
            "alignment_score": result.score,
            "verified_score": final_score,
            "mismatch_positions": list(result.mismatch_positions),
            "gap_count": result.gap_count
        }

    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))
