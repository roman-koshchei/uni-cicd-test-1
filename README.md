# uni-cicd-test-1

Middle Test for CI/CD courses

## Notes

I use `pyproject.toml` instead of `requirements.txt`.
It's new superiour format to keep dependencies information about project.
As well I use [uv](https://docs.astral.sh/uv/) package manager.

I use [black](https://github.com/psf/black) formatter to format code.
It's very good and simple to use. It follows PEP8 rules.

There are 2 workflows: lint and test.
Lint checks formatting and test runs tests with report.
