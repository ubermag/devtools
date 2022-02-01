# Devtools

Collection of scripts and additional information to help developers.

## Manage development installation

To clone/install/update all ubermag subpackages we have a convenience script
`manage-repos.py`. To get a list of all possible options run:

```bash
python manage-repos.py -h
```

We assume/create a directory structure where all subpackages are contained
within one base directory, here called `ubermag-devtools/repos`:

    ubermag-devtools
      +-- .git
      +-- ...
      +-- repo-metadata
      |     +-- ...
      +-- repos
      |     +-- discretisedfield
      |     |     +-- .git
      |     |     +-- ...
      |     +-- micromagneticdata
      |     |     +-- .git
      |     |     +-- ...
      |     +-- ...
      +-- manage-repos.py

### Clone and install packages

To get started clone the `devtools` repository via `ssh`:

```bash
git clone git@github.com:ubermag/devtools.git ubermag-devtools
```

or `https` if you don't have an `ssh key`:

```bash
git clone https://github.com/ubermag/devtools.git ubermag-devtools
```

and change into that directory (we clone the `devtools` repository to a custom
location `ubermag-devtools` which is more expressive). Your directory layout
should then be similar to (not all content of the `devtools` repository is shown
here):

    ubermag-devtools
      +-- .gitignore
      +-- repo-metadata
      |     +-- ...
      +-- manage-repos.py

#### 1. Create and activate `conda` environment

Create a new `conda` environment, here called `ubermagdev`, and install the most basic
packages from `conda-forge` using `conda` (everything else will be installed via `pip`).

```bash
conda create -n ubermagdev -c conda-forge python=3.8 pip oommf
conda activate ubermagdev
```

We use `conda` for this step because simplifies the installation of `OOMMF`. (If
you don't have `conda` we suggest you install
[`miniconda`](https://docs.conda.io/en/latest/miniconda.html).) We use Python
version 3.8 as this is the oldest version that `ubermag` currently supports.

#### 2. Clone and install all packages in development mode

```bash
python manage-repos.py -e ubermagdev -c ssh -i
```

- `-e ...` (`--conda_env ...`) name of the conda environment to install to (has
  to be activated manually!), only used for basic sanity checks
- `-c <ssh|https>` (`--clone ...`) clone repositories using `ssh` or `https`
- `-i`(`--install`) install all packages in development mode

This will create a new directory `repos` and clone all repositories into
that directory using the specified protocol. Then all packages are installed in
development mode.

#### 3. [Optional] Test installation

```bash
python -c "import ubermag; ubermag.test()"
```

### Pull changes in all packages

```bash
python manage-repos.py --pull
```

### Set up pre-commit

```bash
python manage-repos.py --init_pre_commit
```

### Uninstalling packages

```bash
python manage-repos.py -e ubermagdev --uninstall
```

## Update common metadata

`repo-metadata` contains templates and additional helper scripts to update
metadata common to all repositories. To update metadata in the repositories run
the corresponding GitHub Action.
