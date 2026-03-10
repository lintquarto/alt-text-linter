# Alt text linter
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

This repository stores a **GitHub action for linting alternative (alt) text in Quarto markdown (`.qmd`) files**.

Alt text provides meaningful descriptions for images so that screen readers, text-based browsers, and users with low vision or limited bandwidth can understand their content. Including clear alt text improves accessibility, meets WCAG standards, and ensures research outputs are inclusive and comprehensible to all audiences.

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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/amyheather"><img src="https://avatars.githubusercontent.com/u/92166537?v=4?s=100" width="100px;" alt="Amy Heather"/><br /><sub><b>Amy Heather</b></sub></a><br /><a href="https://github.com/lintquarto/alt-text-linter/commits?author=amyheather" title="Code">💻</a> <a href="https://github.com/lintquarto/alt-text-linter/commits?author=amyheather" title="Documentation">📖</a> <a href="#maintenance-amyheather" title="Maintenance">🚧</a> <a href="https://github.com/lintquarto/alt-text-linter/commits?author=amyheather" title="Tests">⚠️</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!