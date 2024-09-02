# Release process

Order of release of Ubermag packages (internal dependencies):

1. ubermagutil
2. disretisedfield (ubermagutil)
3. ubermagtable (ubermagutil)
4. micromagneticmodel (discretisedfield)
5. micromagneticdata (disretisedfield, ubermagtable)
6. miromagetictests (micromagneticmodel, micromagneticdata)
7. oommfc (ubermagtable, micromagnetictests, micromagneticdata)
8. mumax3c (ubermagtable, micromagnetictests, micromagneticmodel)
9. mag2exp (oommfc)
10. ubermag (mag2exp, micromagneticdata) [all package versions are specified explicitely]

## 1. PyPI

- Increase version and dependency versions in `pyproject.toml`
- Commit changes
- Run `invoke release`. (This task will run the unittests and doctests before
  releasing the package).

## 2. Release on Github

- Go to releases
- `Draft a new release` -> `Choose a tag` (Select new version tag, **not** the
  *latest* tag)
- Put release version as title
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
- Update the ubermag version in `ubermag.github.io/environment.yml`.
- Update the changelog (`source/changelog.rst` in the `ubermag.github.io`
  repository) and add the release date (of the `ubermag` conda package).
- Merge the PR for the changelog updates (this automatically triggers a re-build of the website).

## 5. Mailing list

Announce the new version on the mailing list (ubermag-users@lists.mpg.de).
