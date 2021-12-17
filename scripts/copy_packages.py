import os
import shutil

import apt
import apt_pkg

# Import the apt cache.
cache = apt.Cache()

# Packages we do not want or need to install.
filter_packages = ["debconf", "debconf-2.0", "debianutils", "dpkg"]

# Alternative package choices.
alternatives = {"awk": "gawk", "python3.8-distutils": "python3-distutils"}

dpkg_status_file = "/var/lib/dpkg/status"


def find_direct_deps(p: str):
    """Return all direct dependencies for a given package, ignoring filter_packages."""
    deps = []
    pkg = cache.get(p)

    if pkg is None and p in alternatives:
        pkg = cache.get(alternatives[p])

    for v in pkg.versions:
        if not v.is_installed:
            continue

        for x in v.dependencies:
            for y in x.or_dependencies:
                pkg_name = y.name.split(":")[0]
                if pkg_name not in filter_packages and pkg_name not in alternatives:
                    if pkg_name in alternatives:
                        deps.append(alternatives[pkg_name])
                    else:
                        deps.append(pkg_name)

    return deps


def find_all_deps(packages: list):
    """Find all dependencies recursively for a given package."""
    found = []
    q = packages
    while len(q) > 0:
        pkg = q.pop()
        found.append(pkg)
        print("package: " + pkg)

        for d in find_direct_deps(pkg):
            if d not in found:
                q.append(d)
            print("  dependency: " + d)

    return found


def find_all_files(packages: list):
    """Find all files for a list of packages."""
    files = []
    for p in packages:
        package_files = cache.get(p).installed_files
        files += package_files

    return files


def copy_files(new_root: str, files: list):
    """Copy a list of files to a new root directory."""
    for f in files:
        src = f
        dst = new_root + f

        if not os.path.exists(src) or os.path.exists(dst):
            continue

        if os.path.isdir(src):
            os.mkdir(dst)
        else:
            shutil.copy2(f, new_root + f)
            # TODO add debug mode and print everything
            # print(f, new_root + f)


def write_status_file(new_root: str, packages: list):
    """Copy the apt status of all files in packages list to a new root."""
    with apt_pkg.TagFile(dpkg_status_file) as tagfile, open(
        new_root + dpkg_status_file, "w"
    ) as output:
        for section in tagfile:
            if section["Package"] in packages:
                output.write(str(section))


if __name__ == "__main__":
    # Get top level packages from environment.
    top_level_packages = os.environ.get("INSTALL_PACKAGES", "").split(" ")
    print("Top level packages:")
    for package in top_level_packages:
        print("  " + package)
    print()

    # Get list of packages we should ignore for this build.
    ignore_packages = os.environ.get("IGNORE_PACKAGES", "").split(" ")
    filter_packages = filter_packages + ignore_packages

    # Recursively find all dependencies for all top level packages.
    packages = list(set(find_all_deps(top_level_packages)))
    print("")
    print("Need to copy over the contents of these packages:")
    for package in sorted(packages):
        print("  " + package)
    print()

    # Find all the files contained in all packages found in the last step.
    files = find_all_files(packages)

    # Copy all the files from / to /new_root
    copy_files("/new_root", files)

    # Add all copied packages to the dpkg status file in /new_root
    new_root = "/new_root"
    new_status_file = new_root + "/var/lib/dpkg/status"
    os.makedirs(os.path.dirname(new_status_file), exist_ok=True)
    write_status_file(new_root, packages)
