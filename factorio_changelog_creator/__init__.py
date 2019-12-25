import pkg_resources

from .creator import create_changelog, get_format_filename, get_format_template


def get_version():
    try:
        distribution = pkg_resources.get_distribution("factorio_changelog_creator")
    except pkg_resources.DistributionNotFound:
        return "dev"
    else:
        return distribution.version


__version__ = get_version()
name = "factorio_changelog_creator"
