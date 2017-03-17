# this scripts clones the required repositories to install oommfc
# using 'pip install --editable'.
#
# Useful if we want to be able to import the packages without
# having to manually set the PYTHONPATH but at the same time
# being able to edit the source.


# install dependencies first
git clone git@github.com:joommf/oommfc.git
git clone git@github.com:joommf/joommfutil.git
git clone git@github.com:joommf/discretisedfield.git
git clone git@github.com:joommf/micromagneticmodel.git
git clone git@github.com:joommf/oommfodt.git

git clone git@github.com:joommf/oommfdata.git

# then install

pushd joommfutil
pip install --editable .
popd

pushd oommfodt
pip install --editable .
popd


pushd discretisedfield
pip install --editable .
popd

pushd micromagneticmodel
pip install --editable .
popd

pushd oommfc
pip install --editable .
popd

pushd oommfdata
pip install --editable .
popd


# clean
# pip uninstall --yes micromagneticmodel discretisedfield oommfc micromagneticmodel joommfutil
