for dir in ubermagutil discretisedfield ubermagtable micromagneticmodel micromagneticdata micromagnetictests oommfc ubermag; do
    echo $dir
    pushd repos/$dir
    git pull -v
    popd
done
