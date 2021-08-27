# Development installation

## 1. Install dependencies using conda
Install dependencies in the current environment:
```bash
conda env update --file environment.yml
```

OR

Create a new environment with all dependencies:
```bash
conda env create -n ENVINORMENT_NAME -f environment.yml
conda activate ENVIRONMENT_NAME
```
   
## 2. Install ubermag packages using `clone-and-install-repos.bat`

- Mac/Linux: `$ sh clone-and-install-repos.bat`
- Windows: `$ call clone-and-install-repos.bat`
   
## Optional: globally activate `conda-forge` channel

All dependencies are installed from `conda-forge` channel. To globally activate this channel use
```bash
conda config --add channels conda-forge
```
Results should be visible in `~/.condarc` (Mac, Linux) or `WHERE` (Windows).

## Uninstalling packages
```bash
pip uninstall ubermagutil discretisedfield ubermagtable micromagneticmodel micromagneticdata micromagnetictests oommfc mag2exp ubermag
```
