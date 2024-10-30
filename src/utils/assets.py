import pathlib

ASSETS_DIRECTORY = (
    # "../../../assets"
    pathlib.Path(__file__)
    .parent.parent.parent.resolve()
    .joinpath("assets")
)


def assets(path: str):
    return ASSETS_DIRECTORY.joinpath(path)
