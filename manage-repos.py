"""Script to set up ubermag for development."""
import argparse
import contextlib
import os
import re
import shutil
import subprocess as sp


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


def _execute_command(cmd):
    for repo in REPOLIST:
        with _change_directory(f'{REPODIR}/{repo}'):
            sp.run(cmd)


@contextlib.contextmanager
def _change_directory(path):
    prev_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_path)


def _check_conda_env(args):
    # simple check if the correct conda environment is activated
    envs = sp.run(['conda', 'env', 'list'], stdout=sp.PIPE)
    assert re.findall(
        rf'^{args.conda_env}\s+\*\s+',
        envs.stdout.decode('utf-8', 'replace'),
        flags=re.MULTILINE
    ), f'mismatch between activated environment and passed {args.conda_env=}'


def main(args):
    """Convenience-functionality to manage packages."""
    # sanity checks
    assert shutil.which('conda'), 'Conda is missing'
    assert shutil.which('git'), 'git is missing'

    no_action = True

    if args.clone:
        os.mkdir(REPODIR)
        if args.clone == 'ssh':
            base_url = 'git@github.com:ubermag/'
        elif args.clone == 'https':
            base_url = 'https://github.com/ubermag/'
        else:
            raise ValueError(f'Unknown protocol {args.clone}.')
        with _change_directory(REPODIR):
            for repo in REPOLIST:
                sp.run(['git', 'clone', f'{base_url}{repo}.git'])
            sp.run(['git', 'clone', f'{base_url}workshop.git'])
        no_action = False

    if args.pull:
        _execute_command(['git', 'pull'])
        no_action = False

    if args.install:
        _check_conda_env(args)
        _execute_command(['pip', 'install', '-e', '.[dev,test]'])
        no_action = False

    if args.uninstall:
        _check_conda_env(args)
        _execute_command(['pip', 'uninstall', '.'])
        no_action = False

    if args.init_pre_commit:
        _execute_command(['pre-commit', 'install'])
        no_action = False

    if no_action:
        print(f'No action specified. Run `python {__file__} -h` to get a list'
              ' of available actions.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
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
        '--init_pre_commit',
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
    parser.add_argument(
        '--uninstall', '-u',
        required=False,
        action='store_true',
        help='Uninstall all ubermag subpackages (using pip).'
    )
    parser.add_argument(
        '--pull', '-p',
        required=False,
        action='store_true',
        help='Pull changes for all repositories'
    )

    main(parser.parse_args())
