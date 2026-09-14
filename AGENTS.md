# AGENTS.md

## Project focus
This repository is primarily a Python learning and practice workspace. Most development work should be Python-first, with supporting files such as SQL, HTML, and Access data files kept intact unless a task specifically requires changing them.

## General guidance
- Prefer Python 3.x code and keep scripts simple, readable, and beginner-friendly.
- Place new Python logic in the `test/` directory unless a task clearly belongs elsewhere.
- Use UTF-8 text and keep Hungarian/ASCII content compatible with existing project files.
- Favor clear variable names, small functions, and straightforward logic over complexity.
- Preserve existing project structure and naming patterns unless the task requires refactoring.
- If anything is unclear, ask first!

## Coding standards
- Write maintainable, self-contained scripts that can be run directly with Python.
- Prefer standard-library modules before adding external dependencies.
- If a task involves data files, read and write them in a way that matches the repo's current conventions.
- Keep outputs concise and user-friendly; this is a learning-focused repo.

## Validation
- After editing Python code, run the smallest relevant validation command possible.
- For standalone scripts, prefer executing the script directly with Python to confirm it works.
- If a task introduces a bug fix or feature, verify the changed behavior with a focused run rather than broad test execution.

## Repository conventions
- Root-level folders like `Python/`, `erettsegi/`, and `adatbazis/` are meaningful project areas; keep changes scoped to the relevant area.
- Avoid unrelated cleanup while fixing a task.
- Do not delete or overwrite data files without a clear requirement.

## Preferred workflow
1. Read the relevant file and surrounding context before editing.
2. Make the smallest change that solves the task.
3. Validate with a focused Python execution or script run.
4. Keep the solution consistent with the repository’s educational and practical style.
