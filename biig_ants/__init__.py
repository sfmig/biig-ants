from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("biig-ants")
except PackageNotFoundError:
    # package is not installed
    pass
