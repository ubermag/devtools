# Devtools

Collection of scripts and additional information to help developers.

## Manage development installation

To clone/install/update all ubermag subpackages we have a convenience script
`manage-ubermag.py`. To get a list of all possible options run:

```bash
python manage-ubermag.py -h
```

We assume a directory structure where all subpackages are contained within one
base directory:

    ubermag
      +-- discretisedfield
      |     +-- .github
      |     +-- ...
      |
      +-- micromagneticdata
      |     +-- .github
      |     +-- ...
      |
      +-- setup-ubermag.py

To get started create the base-directory, here called `ubermag`, copy
`setup-ubermag.py` to that directory, and change into that directory.

### Clone and install packages

#### 1. Create and activate conda environment ####

Create a new environment, here called `ubermagdev`, and install the most basic
packages using `conda` (everything else will be installed via `pip`).

```bash
conda create -n ubermagdev -c conda-forge python=3.8 pip oommf
conda activate ubermagdev
```

#### 2. Clone and install all packages in development mode ####

```bash
python manage-ubermag.py -e ubermagdev -c ssh -i
```

- `-e ...` (`--conda_env ...`) name of the conda environment to install to (has
  to be activated manually!), only used for basic sanity checks
- `-c <ssh|https>` (`--clone ...`) clone repositories using `ssh` or `https`
- `-i`(`--install`) install all packages in development mode

#### 3. [Optional] Test installation ####

```bash
python -c "import ubermag; ubermag.test()"
```

### Pull changes in all packages ###

```bash
python manage-ubermag.py --pull
```

### Set up pre-commit ###

```bash
python manage-ubermag.py --pre-commit
```

### Uninstalling packages ###

```bash
python manage-ubermag.py -e ubermagdev --uninstall
```

## Update common metadata

`repo-metadata` contains templates and additional helper scripts to update
metadata common to all repositories. To update metadata in the repositories run
the corresponding GitHub Action.
