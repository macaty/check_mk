import os
import subprocess
import re
import pytest


@pytest.mark.parametrize("what", [
    ("rpm"),
    ("deb"),
    ("cma"),
])
def test_package_built(version_path, what):
    files = os.listdir(version_path)
    count = len([e for e in files if e.startswith("check-mk-") and e.endswith("." + what)])
    assert count > 0, "Found no %s package in %s" % (what.upper(), version_path)


def _get_package_paths(version_path, what):
    for filename in os.listdir(version_path):
        if filename.startswith("check-mk-") and filename.endswith(".%s" % what):
            yield os.path.join(version_path, filename)


# In case packages grow/shrink this check has to be changed.
@pytest.mark.parametrize("what,min_size,max_size", [
    ("rpm", 160 * 1024 * 1024, 235 * 1024 * 1024),
    ("deb", 128 * 1024 * 1024, 139 * 1024 * 1024),
    ("cma", 230 * 1024 * 1024, 241 * 1024 * 1024),
    ("tar.gz", 358 * 1024 * 1024, 428 * 1024 * 1024),
])
def test_package_sizes(version_path, what, min_size, max_size):
    for pkg in _get_package_paths(version_path, what):
        size = os.stat(pkg).st_size
        assert min_size <= size <= max_size, \
            "Package %s size %s not between %s and %s bytes." % \
                (pkg, size, min_size, max_size)


@pytest.mark.parametrize("what", [
    ("rpm"),
    ("deb"),
])
def test_files_not_in_version_path(version_path, what):
    allowed_patterns = {
        "rpm": [
            "/opt$",
            "/opt/omd$",
            "/opt/omd/apache$",
            "/opt/omd/sites$",
            "/opt/omd/versions",
        ],
        "deb": [
            "/$",
            "/opt/$",
            "/opt/omd/$",
            "/opt/omd/apache/$",
            "/opt/omd/sites/$",
            "/opt/omd/versions/",  # All files below this are allowed
            "/usr/$",
            "/usr/share/$",
            "/usr/share/man/$",
            "/usr/share/man/man8/$",
            "/usr/share/doc/$",
            "/usr/share/doc/check-mk-(raw|enterprise|managed)-.*/$",
            "/usr/share/doc/check-mk-(raw|enterprise|managed)-.*/changelog.gz$",
            "/usr/share/doc/check-mk-(raw|enterprise|managed)-.*/COPYING.gz$",
            "/usr/share/doc/check-mk-(raw|enterprise|managed)-.*/TEAM$",
            "/usr/share/doc/check-mk-(raw|enterprise|managed)-.*/copyright$",
            "/usr/share/doc/check-mk-(raw|enterprise|managed)-.*/README$",
            "/etc/$",
            "/etc/init.d/$",
            "/etc/init.d/check-mk-(raw|enterprise|managed)-.*$",
        ],
    }

    for pkg in _get_package_paths(version_path, what):
        print "Testing %s" % pkg

        if what == "rpm":
            paths = subprocess.check_output(["rpm", "-qlp", pkg]).splitlines()

        elif what == "deb":
            paths = []
            for line in subprocess.check_output(["dpkg", "-c", pkg]).splitlines():
                paths.append(line.split()[5].lstrip("."))

        for path in paths:
            if not path.startswith("/opt/omd/versions/"):
                is_allowed = any(re.match(p, path) for p in allowed_patterns[what])
                assert is_allowed, "Found unexpected global file: %s in %s" % (path, pkg)


def test_cma_only_contains_version_paths(version_path):
    for pkg in _get_package_paths(version_path, "cma"):
        version = os.path.basename(pkg).split("-")[3]
        for line in subprocess.check_output(["tar", "tvf", pkg]).splitlines():
            path = line.split()[5]
            assert not path.startswith(version + "/")


def test_src_only_contains_relative_version_paths(version_path):
    for pkg in _get_package_paths(version_path, "tar.gz"):
        prefix = pkg.replace(".tar.gz", "")
        for line in subprocess.check_output(["tar", "tvf", pkg]).splitlines():
            path = line.split()[5]
            assert not path.startswith(prefix + "/")
