"""Template-based generation of common files in all Ubermag repositories."""
import argparse
import datetime
import os
import jinja2
import requests
import tomli

all_repos = [
    'discretisedfield',
    'mag2exp',
    'micromagneticdata',
    'micromagneticmodel',
    'micromagnetictests',
    'oommfc',
    'ubermag',
    'ubermagtable',
    'ubermagutil',
]


def authors_to_dict(authors_in):
    """Match authors and affiliations."""
    with open('./authors.toml', 'rb') as fin:
        authors_toml = tomli.load(fin)

    affiliation_numbers = {}
    authors = []
    affiliation_counter = 0

    for author in authors_in:
        details = authors_toml['authors'][author]

        for affiliation in details['affiliations']:
            if affiliation not in affiliation_numbers:
                affiliation_counter += 1
                affiliation_numbers[affiliation] = affiliation_counter

        authors.append({
            'name': author,
            'github': details['github'][1:],  # strip @ symbol
            'affiliations': ','.join([str(affiliation_numbers[a])
                                      for a in details['affiliations']]),
        })

    return {'authors': authors,
            'affiliations': [{'details': authors_toml['affiliations'][a],
                              'number': index}
                             for a, index in affiliation_numbers.items()]}


def generate_files(*, repository, files=None, pyproject_path=''):
    """Generate files from jinja2 templates.

    Parameters
    ----------
    repository : str

        Name of the repository to update.

    files : List(str), optional

        Names of the files to be updated. If not specified all files will be
        updated.

    repopath : str, optional

        Local path to the repository. Output will be written to the local
        repository. If not specified download pyproject.toml from GitHub.
    """
    if 'all' in files:
        files = [
            '.github/workflows/conda.yml',
            '.github/workflows/workflow.yml',
            '.gitignore',
            '.pre-commit-config.yaml',
            'binder/environment.yml',
            'LICENSE',
            'Makefile',
            'README.md',
            'nbval.cfg',
            'pyproject.toml',
            'setup.cfg',
            'setup.py',
        ]

    if pyproject_path:
        with open(pyproject_path, 'rb') as f:
            pyproject = tomli.load(f)
    else:
        req = requests.get(
            f'https://raw.github.com/ubermag/{repository}/master/pyproject.toml',
            headers={'Cache-Control': 'no-cache'})
        pyproject = tomli.loads(req.text)

    authors = [author['name'] for author in pyproject['project']['authors']]
    data = {
        'about': pyproject['tool']['ubermag']['about'],
        'authors': authors_to_dict(authors)['authors'],
        'affiliations': authors_to_dict(authors)['affiliations'],
        'classifiers': pyproject['project']['classifiers'],
        'contributors': authors_to_dict(
            pyproject['tool']['ubermag']['contributors'])['authors'],
        'copyright_holder': pyproject['tool']['ubermag']['copyright_holder'],
        'dependencies': pyproject['project']['dependencies'],
        'description': pyproject['project']['description'],
        'doi': pyproject['tool']['ubermag']['doi'],
        'omit': pyproject['tool']['coverage']['run']['omit'],
        'optional_dependencies': pyproject['project']['optional-dependencies'],
        'package': repository,
        'url': pyproject['project']['urls']['homepage'],
        'version': pyproject['project']['version'],
        'year': datetime.datetime.now().year,
    }
    if 'scripts' in pyproject['project']:
        data['console_scripts'] = [
            {'name': key, 'entrypoint': val}
            for key, val in pyproject['project']['scripts'].items()]

    os.makedirs(f'{repository}/.github/workflows', exist_ok=True)
    env = jinja2.Environment(keep_trailing_newline=True,
                             loader=jinja2.FileSystemLoader('./templates/'))

    for t_name in env.list_templates():
        name = t_name[: -len('.jinja') - 1]
        if name in files:
            template = env.get_template(name=t_name)
            template.stream(**data).dump(f'{repository}/{name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Update repository\'s metadata')
    parser.add_argument('--repo', '-r',
                        type=str,
                        nargs='+',
                        required=True,
                        help='Repository name.')
    parser.add_argument('--file', '-f',
                        type=str,
                        nargs='+',
                        required=True,
                        help='Metadata file.')
    args = parser.parse_args()

    repos = all_repos if 'all' in args.repo else args.repo

    for repo in repos:
        generate_files(repository=repo, files=args.file)
