from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fastapi import UploadFile, File
from geneweaver.fasta_parser import parse_fasta
import tempfile

from geneweaver.cpu_aligner import align_sequences
from geneweaver.scoring import score_alignment

app = FastAPI(
    title="GeneWeaver API",
    description="DNA sequence alignment and scoring API",
    version="1.0.0"
)

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)


@app.get("/", include_in_schema=False)
def homepage():
    return FileResponse(FRONTEND_DIR / "index.html")


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
@app.post("/api/fasta")
async def upload_fasta(file: UploadFile = File(...)):
    allowed_extensions = {".fasta", ".fa", ".fna"}

    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only .fasta, .fa, and .fna files are supported"
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded FASTA file is empty"
        )

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=extension,
            delete=False
        ) as temp_file:
            temp_file.write(content)
            temp_path = Path(temp_file.name)

        try:
            records = parse_fasta(temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

        return {
            "filename": file.filename,
            "sequence_count": len(records),
            "sequences": [
                {
                    "id": record.id,
                    "description": record.description,
                    "sequence": record.sequence
                }
                for record in records
            ]
        }

    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))
    finally:
        await file.close()
