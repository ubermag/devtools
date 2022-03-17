# Release process

Order of release of Ubermag packages (internal dependencies):

1. ubermagutil
2. disretisedfield (ubermagutil)
3. ubermagtable (ubermagutil)
4. micromagneticmodel (disretisedfield)
5. micromagneticdata (disretisedfield, ubermagtable)
6. miromagetictests (micromagneticmodel)
7. oommfc (ubermagtable, micromagnetictests, micromagneticdata)
8. mag2exp (oommfc)
9. ubermag (mag2exp, micromagneticdata) [all package versions are specified
   explicitely]

## 1. PyPI

- Increase version and dependency versions in `setup.cfg` and `pyproject.toml`
- Commit changes
- Run `invoke release`. (This task will run the unittests and doctests before
  releasing the package).

## 2. Release on Github

- Go to releases
- `Draft a new release` -> `Choose a tag` (Select new version tag, **not** the
  *latest* tag)
- [Release title can stay empty]
- Publish release

## 3. Conda-forge

- Wait for the bot to dectect the new release on PyPI (~some hours). A new PR in
  `conda-forge/<package>-feedstock` will be opened automatically.
- If new versions of the dependencies of the `<package>` have been released
  earlier on `conda-forge`, wait a few hours for them to be indexed. Check for the
  latest version of an indexed dependency with `conda search <dependency>`.
- [The package version is updated automatically by the bot in PR.]
- Update the versions of dependencies manually in `recipe/meta.yaml`.
- Change any other metadata, e.g. code owners
  - **add comment** `@conda-forge-admin please re-render`
  - If the `<package>` version did not change update the `build number` in
    `recipe/meta.yaml`.
- After tests pass the PR can be merged. This releases the new version on
  conda-forge.
- Again, after merging it takes a few hours until the package index
  for `conda-forge` is updated and the package can be installed via `conda`.

## 4. Website

- Wait until all packages can be installed via `conda`.
- Update the changelog (`source/changelog.rst` in the `ubermag.github.io`
  repository) and add the release date (of the `ubermag` `conda` package).
- Merge the PR for the changelog updates.
- Manually trigger the action `publish website`.
