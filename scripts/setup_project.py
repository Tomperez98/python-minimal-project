import contextlib

# import subprocess
from pathlib import Path
from typing import Generator

REPO_BASE = (Path(__file__).parent / "..").resolve()

FILES_TO_REMOVE = {
    REPO_BASE / "scripts" / "setup_project.py",
}

GITIGNORE_LIST = (
    line.strip()
    for line in (REPO_BASE / ".gitignore").open().readlines()
    if line.strip() and not line.startswith("#")
)

PATHS_TO_IGNORE = {
    REPO_BASE / ".git",
}

KEY_WORD_TO_REPLACE = "template_project"


@contextlib.contextmanager
def setup_dependencies():
    # subprocess.run(args=["poetry", "add", "typer[all]", "-D"])
    yield

    # subprocess.run(args=["poetry", "remove", "typer", "-D"])


with setup_dependencies():
    import rich
    import typer

    def main(
        github_owner: str = typer.Option(
            default="Tomperez98",
            prompt="Github Repo Organization or User (github.com/<github_owner>/*)",  # noqa flake8: E501
        ),
        github_repo: str = typer.Option(
            ..., prompt="Github repository name (github.com/*/<github_repo>)"
        ),
        package_name: str = typer.Option(
            ...,
            prompt="Python package name",
        ),
    ):
        repo_url = f"https://github.com/{github_owner}/{github_repo}"
        package_name = package_name.replace("-", "_")

        rich.print(f"Repository URL set to: [link={repo_url}]{repo_url}[/]")
        rich.print(f"Package name set to: [cyan]{package_name}[/]")

        typer.confirm("All good?", abort=True)

        _ = [
            (KEY_WORD_TO_REPLACE, package_name),
        ]

        (REPO_BASE / KEY_WORD_TO_REPLACE).replace(REPO_BASE / package_name)


def iterfiles(dir: Path) -> Generator[Path, None, None]:
    assert dir.is_dir()

    for path in dir.iterdir():
        if path in PATHS_TO_IGNORE:
            continue

        is_ignored_file = False
        for gitignore_entry in GITIGNORE_LIST:
            if path.relative_to(REPO_BASE).match(gitignore_entry):
                is_ignored_file = False
                break

        if is_ignored_file:
            continue

        if path.is_dir():
            yield from iterfiles(path)
        else:
            yield path


if __name__ == "__main__":
    typer.run(main)
