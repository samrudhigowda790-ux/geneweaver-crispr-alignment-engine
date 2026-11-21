# GeneWeaver - Development Roadmap

## Project Overview
GeneWeaver is a CRISPR DNA sequence alignment and analysis prototype.
The project aims to combine sequence processing, alignment, PAM recognition,
GPU acceleration, distributed execution and a simple user interface.

## Current Implementation
- FASTA file parsing and validation.
- Support for multiple FASTA records.
- CPU-based Needleman-Wunsch global alignment.
- Configurable match, mismatch and gap scores.
- Alignment score verification.
- DNA sequence chunking with overlap.
- FastAPI backend for sequence alignment.
- Web interface for manual sequence alignment.
- FASTA upload and sequence selection.
- FASTA upload size validation (5 MB limit).
- Automated tests for implemented modules.
- CPU alignment benchmark.

## Planned Development

### 1. PAM Recognition
- Implement PAM sequence detection.
- Begin with the SpCas9 NGG PAM pattern.
- Support wildcard matching using N.
- Identify PAM locations in input sequences.
- Add automated tests for PAM recognition.
- Handle invalid and empty DNA sequences.
- Extend scanning to reverse-complement sequences.
- Document PAM position conventions and limitations.

### 2. CRISPR Target Analysis
- Define the protospacer region relative to a PAM.
- Associate candidate target regions with PAM sites.
- Identify sequence mismatches against a guide sequence.
- Record mismatch positions.
- Add configurable candidate scoring.
- Test target identification using synthetic DNA examples.

### 3. GPU Acceleration
- Review the existing GPU alignment module.
- Implement GPU-compatible alignment operations using Numba CUDA.
- Handle GPU availability and unsupported environments.
- Compare GPU results against the CPU baseline.
- Measure memory transfer and execution time.
- Benchmark multiple sequence lengths.
- Report speedup only when supported by measurements.

### 4. Distributed Processing
- Review the existing scheduling module.
- Explore Dask-based task scheduling.
- Divide larger sequence workloads into manageable tasks.
- Execute independent alignment tasks.
- Collect and validate distributed results.
- Test error handling and task completion.

### 5. Backend and Interface Improvements
- Integrate PAM recognition into the API.
- Add endpoints for relevant analysis operations.
- Display PAM locations in the web interface.
- Display alignment and mismatch information.
- Improve input validation and error messages.
- Test API responses and frontend integration.

### 6. Testing and Validation
- Add unit tests for every new module.
- Test empty and invalid inputs.
- Test different sequence lengths.
- Compare CPU and GPU outputs.
- Test PAM recognition on known synthetic examples.
- Run the complete test suite after changes.
- Record test results and known limitations.

### 7. Benchmarking and Evaluation
- Maintain a reproducible CPU benchmark.
- Add GPU benchmark measurements.
- Compare CPU and GPU execution times.
- Evaluate performance across input sizes.
- Record hardware and software environment.
- Store benchmark results in the reports directory.
- Avoid unsupported performance claims.

### 8. Documentation and Final Submission
- Update the project architecture document.
- Maintain the development log.
- Document installation and execution steps.
- Document API endpoints.
- Explain algorithm design and scoring assumptions.
- Record limitations and future improvements.
- Prepare the final project report.
- Prepare presentation slides.
- Prepare a working final demonstration.

## Development Principles
- Implement features incrementally.
- Keep code modular and maintainable.
- Validate new functionality with automated tests.
- Preserve reproducible benchmark results.
- Clearly distinguish implemented features from planned work.
- Do not claim unverified GPU acceleration or biological accuracy.
- Use synthetic or permitted public DNA sequences for testing.
