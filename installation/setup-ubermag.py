"""Script to set up ubermag development."""
import argparse
import contextlib
import os
import pathlib
import re
import shutil
import subprocess as sp


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


def ensure_directory(base_dir_name):
    """Create (if not existing) and switch to `base_dir_name` directory."""
    # check if in empty subdirectory
    # or create if name is passed
    p = pathlib.Path(base_dir_name)
    if p.exists():
        if not p.is_dir():
            raise ValueError(
                f'Base directory {base_dir_name} is not a directory.'
            )
    else:
        p.mkdir(parents=True)
    os.chdir(p)
    print(os.getcwd())


def clone_repos(protocol):
    """Clone all repositories inside `base_dir_name`."""
    if protocol == 'ssh':
        base_url = 'git@github.com:ubermag/'
    elif protocol == 'https':
        base_url = 'https://github.com/ubermag/'
    else:
        raise ValueError(f'Unknown {protocol=}')
    for repo in REPOLIST:
        sp.run(['git', 'clone', f'{base_url}{repo}.git'])


def _execute_command(cmd):
    for repo in REPOLIST:
        with _change_directory(repo):
            sp.run(cmd)


@contextlib.contextmanager
def _change_directory(path):
    prev_path = pathlib.Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--base_dir', '-d',
        type=str,
        required=True,
        help='Name of the base directory that should contain all subpackages.'
    )
    parser.add_argument(
        '--conda_env', '-e',
        type=str,
        required=True,
        help=('Name of the conda environment that is meant to be used.'
              ' The environment must exist and be activated. It is only used'
              ' for very basic checks to avoiding installing packages to the'
              ' base environment.')
    )
    parser.add_argument(
        '--clone', '-c',
        type=str,
        default='',
        required=False,
        help=('If specified all subpackages will be cloned using the specified'
              ' protocol. Can be `ssh` or `https`.')
    )
    parser.add_argument(
        '--init_pre_commit', '-p',
        required=False,
        action='store_true',
        help='If specified pre-commit will be initialised for all subpackages.'
    )
    parser.add_argument(
        '--install', '-i',
        required=False,
        action='store_true',
        help=('Install all packages in development mode (using pip) with'
              ' additional development dependencies. WARNING Installs in the'
              ' current environment without any tests.')
    )

    args = parser.parse_args()

    # sanity checks
    assert shutil.which('conda'), 'Conda is missing'
    assert shutil.which('git'), 'git is missing'

    envs = sp.run(['conda', 'env', 'list'], stdout=sp.PIPE)
    assert re.findall(
        rf'^{args.conda_env}\s+\*\s+',
        envs.stdout.decode('utf-8', 'replace'),
        flags=re.MULTILINE
    ), f'missmatch between activated environment and passed {args.conda_env=}'

    # create directory and switch to it
    ensure_directory(args.base_dir)

    if not args.clone and not args.install and not args.init_pre_commit:
        print(f'No action specified. Run `python {__file__} -h` to get a list'
              ' of available actions.')

    if args.clone:
        clone_repos(args.clone)

    if args.install:
        _execute_command(['pip', 'install', '-e', '.[dev,test]'])

    if args.init_pre_commit:
        _execute_command(['pre-commit', 'install'])