# Devtools

Collection of scripts and additional information to help developers.

## Manage development installation

To clone/install/update all ubermag subpackages we use `invoke` (can be
installed via `pip` or `conda`, see below). Tasks are defined in `tasks.py`. To
get a list of all possible options run:

```bash
invoke --list
```

To get more detailed help on one specific `command`, run:

```bash
invoke --help <command>
```

We assume/create a directory structure where all subpackages are contained
within one base directory, here called `ubermag-devtools/repos`:

    ubermag-devtools
      +-- .git
      +-- ...
      +-- repometadata
      |     +-- ...
      +-- repos
      |     +-- discretisedfield
      |     |     +-- .git
      |     |     +-- ...
      |     +-- micromagneticdata
      |     |     +-- .git
      |     |     +-- ...
      |     +-- ...
      +-- tasks.py

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
location `ubermag-devtools` which is more explicit). Your directory layout
should then be similar to (not all content of the `devtools` repository is shown
here):

    ubermag-devtools
      +-- .git
      +-- repometadata
      |     +-- ...
      +-- tasks.py

#### 1. Create and activate `conda` environment

If required install `conda`. Suggestion: use [miniforge](https://github.com/conda-forge/miniforge).

Create a new `conda` environment, here called `ubermagdev312`, and install the most
basic packages (`python`, `pip`, `oommf`, `colorama` and `invoke`) from `conda-forge` channel using
`conda` (everything else later on will be installed via `pip`).
We use `conda` for this step because it simplifies the installation of `OOMMF`.

```bash
conda env create -f environment.yaml
conda activate ubermagdev312
```

We use Python version 3.12 to benefit from the performance improvements in
recent Python versions. Note that Python 3.8 is the oldest version currently
supported by `ubermag` so no features of newer Python versions can be used.

#### 2. Clone and install all packages in development mode

```bash
invoke clone -p ssh install
```

- `-p <ssh|https>` (`--protocol ...`) clone repositories using `ssh` or `https`

This will create a new directory `repos` and clone all repositories into that
directory using the specified protocol. Then all packages are installed in
development mode. Your directory tree should now look like outline in the
beginning.

#### 3. [Optional] Clone the additional repos

```bash
invoke clone-extras -p ssh
```

Clones the following additional repositories:

- `help`
- `mumax3c`
- `tutorials`
- `ubermag.github.io` (the website repository)
- `workshop`

#### 4. [Optional] Test installation

```bash
python -c "import ubermag; ubermag.test()"
```

### Execute command in multiple repos (e.g. pull)

Pull changes in all code repos:

```bash
invoke per-repo "git pull"
```

See `invoke --help per-repo` for available options.

### Set up pre-commit

```bash
invoke per-repo "pre-commit install"
```

### Uninstalling packages

```bash
invoke uninstall
```

## Update common metadata

`repometadata` contains templates and additional helper scripts to update
metadata common to all repositories. The metadata can be updated using the
`invoke` task `update-repometadata`

**The update will only work for the directory structure explained
above. Follow the instructions in the first section of this README.**

The repometadata can locally be updated using the `invoke` task
`update-repometadata`. The task can update one or multiple repositories at the
same time. Furthermore, it can work on different branches, both existing and
new ones. To get a list of available options and additional help, run

```bash
$ invoke --help update-repometadata
```

Available options are:
- `r <REPO>`/`--repo <REPO>` name of the repository; can be passed multiple
  times to update multiple repositories simultaneously; if omitted all
  repositories are updated
- `-f <FILE>`/`--file <FILE>` name of the file to update; can be passed multiple
  times ore omitted like `-r`
- `-b <BRANCH>`/`--branch <BRANCH>` name of the branch to use; can be an
  existing or a new one
- `-c`/`--create-branch` required if `-b` specifies a new branch that must be
  created (uses the `git` option `-B` so it will overwrite existing branches)
- `-o <MESSAGE>`/`--commit-message <MESSAGE>` custom commit message; if not
  specified the default is `"Update repository metadata"`
- `--[no-]push` push or do not push the changes; default is true, i.e. `push`
  changes

Examples:

1. Update all files in all repositories on a new (`-c`) branch
   `metadata-update` and push the changes:

   ```bash
   $ invoke update-repometadata -b metadata-update -c
   ```

2. Update all files in `ubermagutil` and `discretisedfield` on the `master` branch
   but do not push changes:

   ```bash
   $ invoke update-repometadata -r ubermagutil -r discretisedfield -b master --no-push
   ```

3. Update `README.md` in all repositories using a new (`-c`) branch
   `repo-metadata` with a special commit message and push the changes:

   ```bash
   $ invoke update-repometadata -f README.md -b repo-metadata -c --commit-message "Update README"
   ```
