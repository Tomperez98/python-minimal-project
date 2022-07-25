import contextlib

# import subprocess
from pathlib import Path
from typing import Generator, List, Tuple

REPO_BASE = (Path(__file__).parent / "..").resolve()

FILES_TO_REMOVE = {
    REPO_BASE / "scripts" / "setup_project.py",
}

GITIGNORE_LIST = [
    line.strip()
    for line in (REPO_BASE / ".gitignore").open().readlines()
    if line.strip() and not line.startswith("#")
]

PATHS_TO_IGNORE = {
    REPO_BASE / ".git",
    REPO_BASE / "scripts" / "setup_project.py",
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

    def iterfiles(dir: Path) -> Generator[Path, None, None]:
        assert dir.is_dir()
        for path in dir.iterdir():
            if path in PATHS_TO_IGNORE:
                continue

            is_ignored_file = False
            for gitignore_entry in GITIGNORE_LIST:
                if path.relative_to(REPO_BASE).match(gitignore_entry):
                    is_ignored_file = True
                    break
            if is_ignored_file:
                continue

            if path.is_dir():
                yield from iterfiles(path)
            else:
                yield path

    def format_file(path: Path, replacements: List[Tuple[str, str]]):
        with path.open("r+t") as file:
            filedata = file.read()

        should_update = False
        for old, new in replacements:
            if filedata.count(old):
                should_update = True
                filedata = filedata.replace(old, new)

        if should_update:
            with path.open("w+t") as file:
                file.write(filedata)

    def main(
        package_name: str = typer.Option(
            ...,
            prompt="Python package name",
        ),
    ):

        package_name = package_name.replace("-", "_")

        rich.print(f"Package name set to: [cyan]{package_name}[/]")

        typer.confirm("All good?", abort=True)

        (REPO_BASE / KEY_WORD_TO_REPLACE).replace(REPO_BASE / package_name)

        REPLACEMENTS = [
            (
                KEY_WORD_TO_REPLACE,
                package_name,
            ),
        ]
        for file in iterfiles(dir=REPO_BASE):
            format_file(path=file, replacements=REPLACEMENTS)


if __name__ == "__main__":
    typer.run(main)
