for dir in micromagneticmodel joommfutil discretisedfield oommfodt oommfc; do
    echo $dir
    pushd $dir
    git pull -v
    popd
done



