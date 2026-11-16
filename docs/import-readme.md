# Pseudorandom Number Generators and Statistical Tests

Academic project by Karawan and Adamek. Original attribution is retained in `PRNG_Karawan_Adamek.pdf`.

- `code/Generatory/`: LCG, generalized LCG, xorshift and RC4 implementations.
- `code/Analiza/`: analyses and comparisons, including tests of digit sequences.
- `code/Tests.py`, `code/transforms.py`: statistical tests and transformations.

Dependencies include NumPy, SciPy, pandas and matplotlib. These are educational implementations, not a cryptographic library.

## Reproduction limitations

The original scripts use sibling imports and hard-coded input/output paths. Some referenced helpers (`stirling`, `monobit_frequency_test`, `KS_test`, `chi_square_test`, `runs_test`) and digit-sequence inputs may be absent from the supplied source. They have not been replaced with invented implementations. Inspect each entry point and provide its inputs before running.

Python syntax was checked; statistical experiments were not rerun. No licence was assigned to the collaborative work.
