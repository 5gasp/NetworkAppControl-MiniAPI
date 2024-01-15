# Debian Packaging of NetworkAppControl-MiniAPI

This file explains how to package the MiniAPI as a Debian package.

According to the [Debian packaging guidelines](https://wiki.debian.org/GitPackaging):
- The upstream code of the project lies in the `upstream/latest`
  branch. In our case, we'll use the `main` branch for that.
- The packaging code lies in the `debian/latest` branch. In this branch,
  - The `src/` directory contains the source code from upstream with
    slight modifications to make it easier to package. Basically:
    - The main code of MiniAPI is turned into a python module
    - We add an `__init__.py` to the `miniapi` module to let start the
      MiniAPI from the command line.
    - We use the python setup tools to package the python code. So that 
      debian helper (or dpkg-build) can easily build the package.
   - The `debian/` directory contains the files to set up the deb
     package (including the systemctl files to start the miniAPI as a
     linux daemon)



## Instal git-buildpackage and other dependencies for the build phase

```sh
sudo apt install -y git-buildpackage
sudo apt install -y dh-python python3-setuptools python3-pydantic
```


## Run git-buildpackage

*Note:* By default, git-buildpackage will try to sign the package with
the author's GPG key. For that:
* Either edit the author email in the `debian/changelog` of the
  `debian/latest` branch. This suppose that you have a GPG key for this 
  email already installed on your system...
* Or pass the `-uc -us` parameters to git-buildpackage to skip the 
  signature .

```sh
git checkout debian/latest
gbp buildpackage --git-ignore-branch --git-ignore-new
```
The compilation results (`.deb`, `.tgz`, etc) will be placed in the
parent folder. This can be changed with the `--git-export-dir=XXXX`
parameter.


## Rebasing when new version is available

```sh
# Retrieve the last upstream version
git checkout main
git pull

# Rebase the debian/latest on main
git checkout debian/latest
git rebase main
```