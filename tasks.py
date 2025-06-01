"""Tasks to set up ubermag for development."""
import os
import shutil

from colorama import Fore, init
from invoke import Exit, task

REPODIR = 'repos'

# order is important
REPOLIST = [
    'ubermagutil',
    'discretisedfield',
    'ubermagtable',
    'micromagneticmodel',
    'micromagneticdata',
    'micromagnetictests',
    'mumax3c',
    'oommfc',
    'mag2exp',
    'ubermag',
]

EXTRA_REPOS = [
    'help',
    'tutorials',
    'ubermag.github.io',
    'workshop',
    'clustering_vector_fields',
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

    Examples
    --------

    1. Pull changes in all package repos

    ``per-repo "git pull"``

    2. Initialise pre-commit in all repos

    ``per-repo "pre-commit install"``
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


@task(
    help={
        'repo': 'List of repos to update; all are updated if not specified',
        'file': 'List of files to update; "all" updates all files',
        'branch': ('Name of the branch to work on. If the branch does not'
                   ' exist --create-branch must be passed.'),
        'create-branch': ('Create the specified branch. Overwrites existing'
                          ' branches [git option -B is used].'),
        'commit_message': 'Optionally pass a custom commit message.',
        'commit': 'Commit changes; defaults to true',
        'push': 'Push changes (requires creating a commit); defaults to true.'},
    iterable=['file', 'repo'])
def update_repometadata(c,
                        repo,
                        file,
                        branch,
                        create_branch=False,
                        commit_message='Update repository metadata',
                        commit=True,
                        push=True):
    """Update repo-metadata locally.

    The updates are done on the specified ``branch``. The branch is created if
    necessary. The task does NOT switch back to the previous branch.
    """
    from repometadata.repometadata import generate_files
    if len(file) == 0:
        raise Exit('No file specified; use "all" to update all files')
    if len(repo) == 0:
        repo = REPOLIST

    for r in repo:
        print(f'{Fore.BLUE}==> {r}')
        with c.cd(f'{REPODIR}/{r}'):
            cmd = '-B' if create_branch else ''
            c.run(f'git checkout {cmd} {branch}')
            if not create_branch:
                c.run('git pull')

        os.chdir('repometadata')
        print(os.getcwd())
        modified = generate_files(
            repository=r,
            files=file,
            pyproject_path=f'../{REPODIR}/{r}/pyproject.toml')
        os.chdir('..')

        shutil.copytree(src=f'repometadata/{r}',
                        dst=f'{REPODIR}/{r}',
                        dirs_exist_ok=True)

        shutil.rmtree(f'repometadata/{r}')
        if commit:
            with c.cd(f'{REPODIR}/{r}'):
                for f in modified:
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
