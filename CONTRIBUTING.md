
# Contributing to Pydentity

First off, thank you for considering contributing to Pydentity! It's people like you that make Pydentity such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## What we're looking for

PyIdentity is an open source project and we love to receive contributions from our community. There are many ways to contribute, from writing tutorials or blog posts, improving the documentation, submitting bug reports and feature requests or writing code which can be incorporated into Pydentity itself.

## How to contribute

If you've never contributed to an open source project before, here are a few friendly tutorials:
http://makeapullrequest.com/ and http://www.firsttimersonly.com/

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Create a new branch: `git checkout -b my-branch-name`
4. Implement your changes
5. Push your work back up to your fork
6. Submit a Pull Request so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

## Development setup

To set up PyIdentity for local development:

1. Clone the repository
   ```
   git clone https://github.com/onlythompson/pydentity.git
   ```
2. Change into the Pydentity directory
   ```
   cd pydentity
   ```
3. Create a virtual environment
   ```
   python -m venv venv
   ```
4. Activate the virtual environment
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install the development dependencies
   ```
   pip install -r requirements-dev.txt
   ```

## Testing

We use `pytest` for our test suite. To run the tests:

```
pytest
```

Please ensure that any new functionality you add is covered by tests.

## Code style

We use `black` for code formatting and `flake8` for linting. Please ensure your code adheres to these standards before submitting a pull request.

To format your code:

```
black .
```

To check your code with flake8:

```
flake8 .
```

## Documentation

We use Google-style docstrings for function and method documentation. Please ensure any new code you write is properly documented.

## Reporting bugs

When reporting bugs, please include:

1. A clear and descriptive title
2. A detailed description of the issue
3. Steps to reproduce the behavior
4. What you expected to happen
5. What actually happened
6. Your environment (OS, Python version, PyIdentity version, etc.)

## Suggesting enhancements

We welcome suggestions for enhancements. When suggesting an enhancement, please:

1. Use a clear and descriptive title
2. Provide a detailed description of the suggested enhancement
3. Explain why this enhancement would be useful to most PyIdentity users
4. List some examples of how this enhancement would be used

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Questions?

If you have any questions, please feel free to contact the maintainers:

[Maintainer Name](mailto:codewiththompson@gmail.com)

Thank you for your interest in contributing to Pydentity!
```