# PRNG generators and statistical tests

Academic work by Karawan and Adamek; original report and attribution are retained in `reports/`.

Install Python 3.11+ and `python -m pip install -e .`.

- `src/prng_tests/generators/`: LCG, generalized LCG, RC4 and xorshift, including distinct multiple-key RC4 code.
- `src/prng_tests/metrics.py` and `transforms.py`: original statistics and transformations.
- `scripts/`: RC4/xorshift analyses using `data/generated/` instead of the old F: drive.
- `archive/incomplete_analyses/`: original LCG/GLCG/digit analyses with unresolved helper/input dependencies, preserved verbatim.

Run `python -m prng_tests.generators.lcg --help` (or glcg/rc4/xorshift) for generation options. For analysis, generate a compatible dataset at `data/generated/rc4_1048576.pkl` or `xorshift_1048576.pkl`, then use `python -m scripts.rc4_analysis` or `scripts.xorshift_analysis` from the root. Generator output paths remain explicit CLI arguments. Do not load untrusted pickle files.

Known limitations: the original stirling helper is required for poker tests and is imported only when that test runs. Archived analyses reference monobit_frequency_test, KS_test, chi_square_test, runs_test and digit files which were not supplied. The multiple-key RC4 variant is retained as research code, not advertised as a validated entry point. Numerical algorithms are unchanged; these are educational generators, not a cryptographic library. `docs/file-migration.json` records old paths. No licence was assigned.

## Migration checks

After installation: `python -m unittest discover -s tests -v`. These small checks do not run the full research experiments.
