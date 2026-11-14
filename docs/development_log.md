# GeneWeaver Development Log

## Day 1 – November 12, 2026

### Objective
Initialize the individual GeneWeaver project.

### Work Completed
- Created individual GitHub repository.
- Cloned repository to local development environment.
- Established modular Python project architecture.
- Created source code modules for parsing, CPU alignment,
  GPU alignment, scoring and scheduling.
- Created test and benchmark directories.
- Established documentation structure.

### Next Steps
- Implement FASTA sequence parsing.
- Develop CPU-based alignment algorithm.
- Establish baseline performance benchmarks.

### Status
Initial project setup completed.
## Day 2 – November 14, 2026

### Objective
Implement FASTA parsing and DNA sequence validation.

### Work Completed
- Implemented a FASTA parser using Python.
- Added support for multiple FASTA records.
- Extracted sequence identifiers and descriptions.
- Normalized DNA sequences to uppercase.
- Added validation for standard and IUPAC ambiguity DNA symbols.
- Added error handling for missing files, empty sequences, malformed headers and invalid characters.
- Created 9 unit tests covering parser functionality and error cases.

### Testing
- Command: python -m pytest tests/test_fasta_parser.py -v
- Result: 9 passed in 0.09 seconds.

### Next Steps
- Implement a CPU-based sequence alignment algorithm.
- Add alignment-specific test cases.
- Establish baseline performance measurements.

### Status
FASTA parser implementation and focused unit testing completed.
