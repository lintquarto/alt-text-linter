# Alt-text linter

This repository stores a GitHub action for linting alt-text in Quarto markdown (`.qmd`) files.

## Usage

This is currently in early development with no major tags yet, so for now you should pin to `main`:

```
uses: lintquarto/alt-text-linter@main
```

<!--
We recommend pinning to a major tag if you want non-breaking updates:

```
uses: lintquarto/alt-text-linter@v1
```
-->

## Example

```
name: Check Alt Text
run-name: Check Alt Text

on:
  push:
    paths:
      - '**.qmd'
  pull_request:
    paths:
      - '**.qmd'
  workflow_dispatch:

jobs:
  check-alt-text:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lintquarto/alt-text-linter@main
```

## Release management

We follow the [GitHub guidelines](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/release-and-maintain-actions) for releasing and maintaining actions.

* Do feature work in branches off `main`.
* Have a CI workflow that runs on `push` and `pull_request` that runs tests and lints.
* Use semantic tags for releases, and keep moving major tag to point to the latest compatible release, so workflow users can safely do `uses: lintquarto/alt-text-linter@v1`. This is updated via `.github/workflows/release.yml` upon creating a new GitHub release.
