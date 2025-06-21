# Contributing to Event and Festival Promotion Backend

Thank you for your interest in contributing to this project! We welcome contributions of all kinds — whether it's bug reports, feature requests, code, documentation, or tests.

---

## Table of Contents

- [How to Contribute](#how-to-contribute)
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Submit Changes](#how-to-submit-changes)
- [Coding Guidelines](#coding-guidelines)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)
- [Community and Support](#community-and-support)

---

## How to Contribute

There are many ways to contribute:

- **Reporting bugs** — Please open an issue with detailed information.
- **Suggesting enhancements** — Feature requests and improvements are welcome.
- **Submitting code** — Fix bugs, add features, improve documentation.
- **Improving documentation** — Make docs clearer or more comprehensive.
- **Testing** — Help us test new features and report issues.

---

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to foster a welcoming and respectful community.

---

## Getting Started

1. **Fork the repository** and clone your fork locally.
2. **Create a virtual environment** and install dependencies:
   python -m venv venv
   source venv/bin/activate # Windows: venv\Scripts\activate
   pip install -r requirements.txt

text 3. **Set up environment variables** as described in the README. 4. **Run migrations**:
python manage.py migrate

text 5. **Run the development server**:
python manage.py runserver

text

---

## How to Submit Changes

1. Create a new branch for your work:
   git checkout -b feature/your-feature-name

text 2. Make your changes with clear, concise commits. 3. Write tests and ensure existing tests pass. 4. Push your branch to your fork:
git push origin feature/your-feature-name

text 5. Open a Pull Request against the `main` branch of this repository. 6. Fill out the PR template with details about your changes. 7. Be responsive to feedback and update your PR as needed.

---

## Coding Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
- Write clear, maintainable, and well-documented code.
- Include tests for new features and bug fixes.
- Keep commits focused and descriptive.

---

## Reporting Bugs

Please include:

- A clear and descriptive title.
- Steps to reproduce the issue.
- Expected and actual behavior.
- Screenshots or logs if applicable.
- Your environment details (OS, Python version, Django version).

---

## Requesting Features

Please provide:

- A clear description of the feature.
- Why it would be useful.
- Any alternatives you have considered.
- Any additional context or screenshots.

---

## Community and Support

If you have questions or want to discuss ideas:

- Open an issue.
- Join our mailing list or chat (add links here if available).
- Check existing issues and pull requests for similar topics.

---

Thank you for helping make this project better!

---

