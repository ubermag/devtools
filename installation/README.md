# [NEW] Development installation

## 1. Create and activate conda environment

Create a new environment `ubermagdev` and install the most basic packages
using conda (everything else will be installed via `pip`).

```bash
conda create -n ubermagdev python=3.8 pip oommfc
conda activate ubermagdev
```

## 2. Clone and install all packages in development mode
```bash
python setup-ubermag.py -d ubermag -e ubermagdev -c ssh i
```

- `-d ...` name of the base directory to install to (will be created if it does not exist).
- `e ...` name of the conda environment to install to (has to be activated manually!)
- `-c <ssh|https>` clone repositories using `ssh` or `https`
- `-i` install all packages in development mode

# [OLD] Development installation

## 1. Install dependencies using conda
Install dependencies in the current environment:
```bash
conda env update --file environment.yml
```

OR

Create a new environment with all dependencies:
```bash
conda env create -n ENVIRONMENT_NAME -f environment.yml
conda activate ENVIRONMENT_NAME
```

## 2. Install ubermag packages

- Mac/Linux: `$ sh clone-and-install-METHOD.bat`
- Windows: `$ call clone-and-install-METHOD.bat`

Choose either `METHOD=https` or `METHOD=ssh`.
   
# Optional: globally activate `conda-forge` channel

All dependencies are installed from `conda-forge` channel. To globally activate this channel use
```bash
conda config --add channels conda-forge
```
Results should be visible in `~/.condarc` (Mac, Linux) or `C:\Users\Username\.condarc` (Windows).

# Uninstalling packages
```bash
pip uninstall ubermagutil discretisedfield ubermagtable micromagneticmodel micromagneticdata micromagnetictests oommfc mag2exp ubermag
```
