# Development installation

## 1. Install dependencies using conda
Install dependencies in the current environment:
```bash
conda env update --file environment.yml
```

OR

create a new environment called `ubermag-dev` with all dependencies:
```bash
conda create -f environment.yml
```
   
## 2. Install ubermag packages using `clone-and-install-repos.bat`

- Mac/Linux: `$ sh clone-and-install-repos.bat`
- Windows: `$ call clone-and-install-repos.bat`
   
## Optional: globally activate `conda-forge` channel

All dependencies are installed from `conda-forge` channel. To globally activate this channel use
```bash
$ conda config --add channels conda-forge
```
Results should be visible in `~/.condarc` (Mac, Linux) or `WHERE` (Windows).

## Uninstalling packages
```bash
$ pip uninstall ubermagutil discretisedfield ubermagtable micromagneticmodel micromagneticdata micromagnetictests oommfc ubermag
```