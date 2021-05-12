# this scripts clones the required repositories to install oommfc
# using 'pip install --editable'.
#
# Useful if we want to be able to import the packages without
# having to manually set the PYTHONPATH but at the same time
# being able to edit the source.


# install dependencies first


git clone git@github.com:ubermag/ubermagutil.git
git clone git@github.com:ubermag/discretisedfield.git
git clone git@github.com:ubermag/ubermagtable.git
git clone git@github.com:ubermag/micromagneticmodel.git 
git clone git@github.com:ubermag/micromagneticdata.git 
git clone git@github.com:ubermag/miromagnetictests.git
git clone git@github.com:ubermag/oommfc.git
git clone git@github.com:ubermag/ubermag.git 

# then install

pushd ubermagutil
pip install --editable .
popd

pushd discretisedfield
pip install --editable .
popd


pushd ubermagtable
pip install --editable .
popd

pushd micromagneticmodel
pip install --editable .
popd

pushd micromagneticdata
pip install --editable .
popd

pushd micromagnetictests
pip install --editable .
popd

pushd oommfc
pip install --editable .
popd

pushd ubermag
pip install --editable .
popd


# clean
pip uninstall ubermagutil discretisedfield ubermagtable micromagneticmodel micromagneticdata miromagnetictests oommfc ubermag.git 
