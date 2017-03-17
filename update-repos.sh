for dir in micromagneticmodel joommfutil discretisedfield oommfodt oommfc oommfdata; do
    echo $dir
    pushd $dir
    git pull -v
    popd
done
