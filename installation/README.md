# [NEW] Development installation

## 1. Create and activate conda environment

Create a new environment `ubermagdev` and install the most basic packages
using conda (everything else will be installed via `pip`).

```bash
conda create -n ubermagdev -c conda-forge python=3.8 pip oommf
conda activate ubermagdev
```

## 2. Clone and install all packages in development mode
```bash
python setup-ubermag.py -d ubermag -e ubermagdev -c ssh -i
```

- `-d ...` name of the base directory to install to (will be created if it does not exist).
- `-e ...` ( name of the conda environment to install to (has to be activated manually!)
- `-c <ssh|https>` (`--clone`) clone repositories using `ssh` or `https`
- `-i`(`--install`) install all packages in development mode


## 3. [Optional] Test installation
```bash
python -c "import ubermag; ubermag.test()"
```

# Pull changes in all packages
```bash
python setup-ubermag.py -d ubermag -e ubermagdev --pull
```

# Set up pre-commit
```bash
python setup-ubermag.py -d ubermag -e ubermagdev --pre-commit
```

# Uninstalling packages
```bash
python setup-ubermag.py -d ubermag -e ubermagdev --uninstall
```
