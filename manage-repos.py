"""Script to set up ubermag for development."""
import argparse
import contextlib
import os
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

EXTRA_REPOS = [
    'help',
    'mumax3c',
    'ubermag.github.io',
    'workshop',
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


def clone(protocol, repo_list):
    """Clone all repositories."""
    os.makedirs(REPODIR, exist_ok=True)
    if protocol == 'ssh':
        base_url = 'git@github.com:ubermag/'
    elif protocol == 'https':
        base_url = 'https://github.com/ubermag/'
    else:
        raise ValueError(f'Unknown protocol {args.clone}.')
    with _change_directory(REPODIR):
        for repo in repo_list:
            sp.run(['git', 'clone', f'{base_url}{repo}.git'])


def main(args):
    """Convenience-functionality to manage packages."""
    # sanity checks
    assert shutil.which('conda'), 'Conda is missing'
    assert shutil.which('git'), 'git is missing'

    no_action = True

    if args.clone:
        clone(args.clone, REPOLIST)
        no_action = False

    if args.clone_extras:
        clone(args.clone, EXTRA_REPOS)
        no_action = False

    if args.pull:
        _execute_command(['git', 'pull'])
        no_action = False

    if args.install:
        _execute_command(['pip', 'install', '-e', '.[dev,test]'])
        no_action = False

    if args.uninstall:
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
        '--clone', '-c',
        type=str,
        default='',
        required=False,
        help=('If specified all subpackages will be cloned using the specified'
              ' protocol. Can be `ssh` or `https`.')
    )
    parser.add_argument(
        '--clone_extras',
        type=str,
        default='',
        required=False,
        help=('If specified the additional repositories will be cloned using'
              ' the specified protocol. Can be `ssh` or `https`. Currently,'
              ' these are the `website-repository`, the `workshop`, `help`,'
              ' and `mumax3c`')
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
