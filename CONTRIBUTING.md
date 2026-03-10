# Contributing

Thank you for your interest in contributing!

<br>

## Setting up development environment with uv

We use uv for dependency management. You should follow instructions from the uv documentation for installing it onto your operating system.

To install the recorded environment (including python version from `.python-version` and dependencies from `uv.lock`) run:

```
uv sync
```

<br>

## Linting

We use Ruff for linting, with configuration in `pyproject.toml`. To run the Ruff linter:

```
uv run ruff check
```

Resolve "fixable" errors automatically:

```
uv run ruff check --fix
```

Once project is passing `ruff check`, run Ruff formatter:

```
uv run ruff format
```

<br>

## Release management

We follow the [GitHub guidelines](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/release-and-maintain-actions) for releasing and maintaining actions.

* Do feature work in branches off `main`.
* Have a CI workflow that runs on `push` and `pull_request` that runs tests and lints.
* Use semantic tags for releases, and keep moving major tag to point to the latest compatible release, so workflow users can safely do `uses: lintquarto/alt-text-linter@v1`. This is updated via `.github/workflows/release.yml` upon creating a new GitHub release.

### Instructions for creating a new release

1. Update `CHANGELOG.md`.

2. Create GitHub release.

3. Confirm that GitHub action `release.yml` has successfully run and updated tags.

<br>

## `all-contributors`

If your name or contributions are missing from the README, or if you contributed in ways not captured by the current role emojis, please create an issue and use: 

```
@all-contributors please add @githubuser for ...
```

Then list appropriate contribution types from [allcontributors.org/docs/en/emoji-key](https://allcontributors.org/docs/en/emoji-key) (e.g., code, review, doc, content, bug, ideas, infra).

Alternatively, you can update it from the command line. This may be preferable, as the bot will create GitHub issues that email people when they are added.

You'll need to install the [All-Contributors CLI tool](https://allcontributors.org/cli/installation/):

```
npm i -D all-contributors-cli
```

When we first set-up all-contributors, we called:

```
npx all-contributors init
```

You can then run the following and select/enter relevant information when prompted:

```
npx all-contributors
```

If you want to remove specific contributions or people, edit the `.all-contributorsrc` file then run the following to regenerate the table in `README.md`. (Don't edit `README.md`, as it is just generated based on `.all-contributorsrc`).

```
npx all-contributors generate
```
