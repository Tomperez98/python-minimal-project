import contextlib

# import subprocess
from pathlib import Path
from typing import Generator, List, Tuple

REPO_BASE = (Path(__file__).parent / "..").resolve()

FILES_TO_REMOVE = [
    REPO_BASE / "scripts" / "setup_project.py",
    REPO_BASE / "Makefile",
]

FILES_TO_ROOT = [REPO_BASE / "scripts" / "Makefile"]

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
    from git.repo import Repo

    r = Repo(REPO_BASE)
    reader = r.config_reader()
    git_username = reader.get_value("user", "name")
    git_email = reader.get_value("user", "email")

    def move_file_to_root(path: Path) -> None:
        assert path.is_file()

        path.rename(REPO_BASE / path.name)

    def remove_file(path: Path) -> None:
        assert path.is_file()

        path.unlink()

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
        username: str = typer.Option(
            default=git_username,
            prompt="Project's author name",
        ),
        email: str = typer.Option(
            default=git_email,
            prompt="Project's author email",
        ),
    ):

        package_name = package_name.replace("-", "_")

        rich.print(f"Package name set to: [cyan]{package_name}[/]")
        rich.print(f"Project's author name set to: [cyan]{username}[/]")
        rich.print(f"Project's author email set to: [cyan]{email}[/]")

        typer.confirm("All good?", abort=True)

        (REPO_BASE / KEY_WORD_TO_REPLACE).replace(REPO_BASE / package_name)

        REPLACEMENTS = [
            (
                KEY_WORD_TO_REPLACE,
                package_name,
            ),
            (
                "author_name",
                username,
            ),
            (
                "author_email",
                email,
            ),
        ]
        for file in iterfiles(dir=REPO_BASE):
            format_file(path=file, replacements=REPLACEMENTS)

        # for file in FILES_TO_REMOVE:
        #     remove_file(path=file)

        for file in FILES_TO_ROOT:
            move_file_to_root(path=file)


if __name__ == "__main__":
    typer.run(main)
