echo "conda-forge needs to be activated as additional channel"
echo "using"
echo "conda config --add channels conda-forge"
echo "Results should be visible in ~/.condarc."
echo "your ~/.condarc looks like this:"
cat ~/.condarc
echo "Press return to proceed or CTRL+C to interrupt"
read
# oommfc
conda install numpy matplotlib pytest pytest-cov sarge oommf scipy
# conda install numpy matplotlib ipywidgets pytest pytest-cov
# pip install sarge

# We generally also want ipython and the notebook
conda install ipython notebook
