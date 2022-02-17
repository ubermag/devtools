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
      +-- .git
      +-- repometadata
      |     +-- ...
      +-- manage-repos.py

#### 1. Create and activate `conda` environment

Create a new `conda` environment, here called `ubermagdev`, and install the most
basic packages (`python`, `pip`, `oommf`, and `invoke`) from `conda-forge` using
`conda` (everything else will be installed via `pip`).

```bash
conda create -n ubermagdev -c conda-forge -y python=3.8 pip oommf invoke
conda activate ubermagdev
```

We use `conda` for this step because it simplifies the installation of `OOMMF`.
(If you don't have `conda` we suggest you install
[`miniconda`](https://docs.conda.io/en/latest/miniconda.html).) We use Python
version 3.8 as this is the oldest version that `ubermag` currently supports.

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
- `ubermag.github.io` (the website repository)
- `workshop`

#### 4. [Optional] Test installation

```bash
python -c "import ubermag; ubermag.test()"
```

### Pull changes in all packages

```bash
invoke pull
```

### [SKIP - Not yet fully set up] Set up pre-commit

```bash
invoke init-pre-commit
```

### Uninstalling packages

```bash
invoke uninstall
```

## Update common metadata

`repometadata` contains templates and additional helper scripts to update
metadata common to all repositories. The metadata can be updated:
- on GitHub using the action in the `devtools` repository
- locally using the `invoke` task `update-repometadata`

The local update provides more functionallity.

### on GitHub

The action can only update one repository at a time. It needs:
- the name of the repository
- [optionally] the name of the files to update; if no files are specified all files are updated

The action can only update one repository at a time. Therefore, it is necessary to run the action for all repositories individually.

**Note** The action creates a new branch `metadata-update` and opens a PR. It will fail *if the branch does already exist*

PRs are opened using the `ubermagbot` account.

### locally

The repometadata can locally be updated using the `invoke` task `update-repometadata`. It can update one ore multiple repositories at the same time. Furthermore, it can work on different branches, both, existing and new ones. To get a list of available options and additional help, run
```bash
$ invoke --help update-repometadata
```

Available options are:
- `r`/`--repo` name of the repository; can be passed multiple times to update multiple repositories simultaneously; if omitted all repositories are updated
- `-f`/`--file` name of the file to update; can be passed multiple times ore omitted like `-r`
- `-b`/`--branch` name of the branch to use; can be an existing or a new one
- `-c`/`--create-branch` required if `-b` specifies a new branch that must be created (uses the `git` option `-B` so it will overwrite existing branches)
- `-o`/`--commit-message` custom commit-message; if not specified the default is `Update repository metadata`
- `--[no-]push` switch to push or not push the changes; default is true, i.e. `push` changes

Examples:

1. Update all files in `ubermagutil` and `discretisedfield` on the master branch but do not push changes:
   ```bash
   $ invoke update-repometadata -r ubermagutil -r discretisedfield -b master --no-push
   ```
   
2. Update `README.md` in all repositories using a new (-> `-c`) branch `repo-metadata` with a special commit message and push the changes:
   ```bash
   $ invoke update-repometadata -f README.md -b repo-metadata -c --commit-message "Update README.md"
   ```
   
3. Update all files in all repositories on a new (-> `-c`) branch `metadata-update` and push the changes:
   ```bash
   $ invoke update-repometadata -b metadata-update -c
   ```
