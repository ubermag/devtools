# Release process

Order of release of Ubermag packages (internal dependencies):

1. ubermagutil
2. disretisedfield (ubermagutil)
3. ubermagtable (ubermagutil)
4. micromagneticmodel (disretisedfield)
5. micromagneticdata (disretisedfield, ubermagtable)
6. miromagetictests (micromagneticmodel)
7. oommfc (ubermagtable, micromagnetictests)
8. mag2exp (oommfc)
9. ubermag (mag2exp, micromagneticdata) [all package versions are specified explicitely]

## 1. PyPI

- Increase version and dependency versions in `setup.cfg` and `pyproject.toml`
  and commit changes.
- Run `invoke release`.

## 2. Release on Github

- Go to releases
- `Draft a new release` -> `Choose a tag` (Select new version tag, **not the
  latest tag**)
- [Release title can stay empty]
- Publish release

## 3. Conda-forge

- Wait for the bot to dectect the new release on PyPI (~some hours). A new PR in
  `conda-forge/<package>-feedstock` will be opened automatically.
- The package version is updated automatically.
- Update the versions of dependencies manually.
- Change any other metadata, e.g. code owners -> **add comment**
  `@conda-forge-admin please re-render`
- After tests pass the PR can be merged. This releases the new version on
  conda-forge. After merging it takes a few hours until the package index for
  `conda-forge` is updated and the package can be installed via `conda`. The
  next package of ubermag can be updated only after all dependencies are
  available via conda.
