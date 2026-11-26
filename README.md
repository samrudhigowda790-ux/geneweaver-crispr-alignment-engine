# GeneWeaver – GPU-Accelerated CRISPR Alignment Engine

GeneWeaver is an individual Python engineering project focused on accelerating genomic sequence alignment using GPU computing.

## Project Objective

The project aims to develop a computational engine that processes FASTA genomic sequences, identifies potential CRISPR off-target matches and improves alignment performance through GPU acceleration.

## Technology Stack

- Python
- BioPython
- Numba CUDA
- NumPy
- Dask
- Textual

## Core Modules

1. Genomic FASTA Parser
2. Sequence Chunking
3. CPU Alignment Engine
4. GPU Alignment Engine
5. Biological Scoring
6. Distributed Scheduler
7. Terminal Dashboard

## Project Structure

- `src/` – Main application source code
- `tests/` – Automated tests
- `benchmarks/` – CPU and GPU performance benchmarks
- `data/` – Sample genomic datasets
- `docs/` – Technical documentation
- `reports/` – Project reports
- `results/` – Generated outputs

## Development Status

**Current phase:** Core sequence analysis and batch scheduling development.

### Implemented
- FASTA sequence parsing and upload API.
- Needleman–Wunsch CPU sequence alignment.
- Sequence chunking with configurable overlap.
- Biological alignment scoring.
- PAM recognition on forward and reverse DNA strands.
- Protospacer identification on both DNA strands.
- FastAPI endpoints for alignment, FASTA upload, PAM recognition and protospacer identification.
- Dask-based batch scheduling for independent sequence alignment tasks.

### Testing
- Automated project test suite: 85 passed.
- Dask scheduler tests: 8 passed.
- No test failures in the latest full test run.

### In Progress
- GPU alignment implementation and verification.
- Frontend integration for PAM and protospacer analysis.
- Performance benchmarking.
- Further dashboard and workflow development.

GPU execution and performance improvements have not yet been verified.

Development progress and implementation details are maintained in `docs/development_log.md`.