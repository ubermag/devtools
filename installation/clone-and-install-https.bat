git clone https://github.com/ubermag/ubermagutil.git
git clone https://github.com/ubermag/discretisedfield.git
git clone https://github.com/ubermag/ubermagtable.git
git clone https://github.com/ubermag/micromagneticmodel.git
git clone https://github.com/ubermag/micromagneticdata.git
git clone https://github.com/ubermag/micromagnetictests.git
git clone https://github.com/ubermag/oommfc.git
git clone https://github.com/ubermag/mag2exp.git
git clone https://github.com/ubermag/ubermag.git

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

pushd mag2exp
pip install --editable .
popd

pushd ubermag
pip install --editable .
popd
