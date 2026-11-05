"""Check that every package in a requirements file actually EXISTS.

DIY 3. You are completing this, not reading a finished answer.

Why this script needs to exist: an assistant will confidently suggest a
package that was never published. That used to be a harmless dead end --
the install fails and you move on. It stopped being harmless when
attackers noticed the invented names REPEAT, and started registering them.
By the time a bad install fails, their code has already run.

So the check has to happen BEFORE installation, which is why this is a
separate script and not something you notice in pip's output.

Usage:
    python verify_deps.py suspect-requirements.txt
"""
import sys
import urllib.error
import urllib.request

PYPI = "https://pypi.org/pypi/{name}/json"
TIMEOUT = 10


def package_names(path: str) -> list[str]:
    """Read a requirements file and return bare package names.

    Skips blank lines and comments, and strips version specifiers so that
    `redis>=5.0` is looked up as `redis`.
    """
    names = []
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # TODO (DIY 3, step 4): strip everything from the first version
        # specifier onwards. The specifiers you need to handle are
        # >=  <=  ==  !=  ~=  >  <  and a trailing [extras] marker.
        #
        #   "redis>=5.0"      -> "redis"
        #   "uvicorn[standard]" -> "uvicorn"
        names.append(line)
    return names


def exists_on_pypi(name: str) -> bool:
    """True if `name` is a real package on PyPI.

    PyPI answers with 200 for a package that exists and 404 for one that
    does not, so a 404 is an ANSWER, not an error -- catch it and return
    False rather than letting it propagate.
    """
    # TODO (DIY 3, step 4): request PYPI.format(name=name) and return
    # True on success. Catch urllib.error.HTTPError; treat 404 as False
    # and re-raise anything else, because "the network is down" must not
    # look like "this package is fake".
    raise NotImplementedError("Complete exists_on_pypi() -- see DIY 3")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1])
        return 2

    path = sys.argv[1]
    names = package_names(path)
    print(f"Checking {path} ({len(names)} packages)\n")

    missing = []
    for name in names:
        ok = exists_on_pypi(name)
        print(f"  {'OK        ' if ok else 'NOT FOUND '} {name}")
        if not ok:
            missing.append(name)

    print()
    if missing:
        print(f"{len(missing)} package(s) could not be found on PyPI. "
              f"Do not install this file.")
        return 1
    print("Every package exists. That is necessary, not sufficient -- a real "
          "package can still be malicious.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
