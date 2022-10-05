import pathlib


def get_package_name() -> str:
    return pathlib.Path(__file__).parent.parent.parts[-1]
