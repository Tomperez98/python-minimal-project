# See https://semver.org/#is-v123-a-semantic-version%20for%20the%20semantics.

_MAJOR = "0"
_MINOR = "1"
# On main and in a nightly release the patch should be one ahead of the last
# released build.
_PATCH = "0"

_SUFFIX = "a"
VERSION_SHORT = f"{_MAJOR}.{_MINOR}"
VERSION = f"{_MAJOR}.{_MINOR}.{_PATCH}.{_SUFFIX}"
