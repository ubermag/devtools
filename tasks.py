"""Tasks to set up ubermag for development."""
import os
import shutil

from colorama import Fore, init
from invoke import task

REPODIR = 'repos'

# order is important
REPOLIST = [
    'ubermagutil',
    'discretisedfield',
    'ubermagtable',
    'micromagneticmodel',
    'micromagneticdata',
    'micromagnetictests',
    'oommfc',
    'mag2exp',
    'ubermag',
]

EXTRA_REPOS = [
    'help',
    'mumax3c',
    'tutorials',
    'ubermag.github.io',
    'workshop',
]

# for coloured output in print
init(autoreset=True)


@task(help={'protocol': 'Protocol to use, either "ssh" or "https".'})
def clone(c, protocol):
    """Clone all repositories."""
    _clone_repos(c, protocol, REPOLIST)


@task(help={'protocol': 'Protocol to use, either "ssh" or "https".'})
def clone_extras(c, protocol):
    """Clone extra repositories.

    Clones the following additional repositories that are part of Ubermag:
    - help
    - mumax3c
    - ubermag.github.io (website repository)
    - tutorials
    - workshop
    """
    _clone_repos(c, protocol, EXTRA_REPOS)


@task(
    help={
        'command': 'Command to be executed in all packages.',
        'repo': ('List of repos to execute command in. If not specified all '
                 'package repos are used by default.'),
        'include_extras': ('Include extra repositories (see clone-extras).'
                           ' This is has no effect if repos are given'
                           ' explicitely.')},
    iterable=['repo'])
def per_repo(c, command, repo, include_extras=False):
    """Execute command in multiple repositories.

    The ``command`` will be executed in multiple repositories, by default in
    all package repositories. To also include the extra repositories pass the
    flag ``--include-extras``. Alternatively, a custom list of repositories can
    be specified with ``--repo <REPO1> --repo <REPO2> ...``.

    Example (pull changes in all package repos):

    ``per-repo "git pull"``
    """
    if repo == []:
        repo = REPOLIST + EXTRA_REPOS if include_extras else REPOLIST
    for r in repo:
        print(f'{Fore.BLUE}==> {r}')
        with c.cd(f'{REPODIR}/{r}'):
            c.run(command)


@task
def install(c):
    """Install all packages in development mode.

    Installs all Ubermag packages with additional development dependencies
    using pip.

    WARNING: Installs into the current environment without any tests.
    """
    per_repo(c, 'pip install -e .[dev]', REPOLIST)


@task
def uninstall(c):
    """Uninstall all ubermag subpackages."""
    for pkg in reversed(REPOLIST):
        c.run(f'pip uninstall {pkg} -y')


@task
def init_pre_commit(c):
    """Initialise pre-commit for all subpackages."""
    per_repo(c, 'pre-commit install', REPOLIST)


@task(
    help={
        'repo': 'List of repos to update; all are updated if not specified',
        'file': 'List of files to update; all are updated if not specified',
        'branch': ('Name of the branch to work on. If the branch does not'
                   ' exist --create-branch must be passed.'),
        'create-branch': ('Create the specified branch. Overwrites existing'
                          ' branches [git option -B is used].'),
        'commit_message': 'Optionally pass a custom commit message.',
        'push': 'Push changes; defaults to true.'},
    iterable=['file', 'repo'])
def update_repometadata(c,
                        repo,
                        file,
                        branch,
                        create_branch=False,
                        commit_message='Update repository metadata',
                        push=True):
    """Update repo-metadata locally.

    The updates are done on the specified ``branch``. The branch is created if
    necessary. The task does NOT switch back to the previous branch.
    """
    from repometadata.repometadata import generate_files
    if len(file) == 0:
        file = ['all']
    if len(repo) == 0:
        repo = REPOLIST

    with c.cd('repometadata'):
        for repo in repo:
            with c.cd(f'../{REPODIR}/{repo}'):
                cmd = '-B' if create_branch else ''
                c.run(f'git checkout {cmd} {branch}')
                if not create_branch:
                    c.run('git pull')

            generate_files(
                repository=repo,
                files=file,
                pyproject_path=f'../{REPODIR}/{repo}/pyproject.toml')

            shutil.copytree(src=f'{repo}',
                            dst=f'../{REPODIR}/{repo}',
                            dirs_exist_ok=True)

            shutil.rmtree(f'{repo}')
            with c.cd(f'../{REPODIR}/{repo}'):
                for f in file:
                    c.run(f'git add {os.path.relpath(f)}')
                c.run(f'git commit -m "{commit_message}"')
                if push:
                    push = f'-u origin {branch}' if branch is not None else ''
                    c.run(f'git push {push}')


def _clone_repos(c, protocol, repolist):
    os.makedirs(REPODIR, exist_ok=True)
    if protocol == 'ssh':
        base_url = 'git@github.com:ubermag/'
    elif protocol == 'https':
        base_url = 'https://github.com/ubermag/'
    else:
        raise ValueError(f'Unknown protocol {protocol}.')
    with c.cd(REPODIR):
        for repo in repolist:
            c.run(f'git clone {base_url}{repo}.git')
