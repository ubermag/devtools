"""Template-based generation of common files in all Ubermag repositories."""
import argparse
import datetime
import os
import re
import string

import requests
import tomli

all_repos = [
    'discretisedfield', 'mag2exp', 'micromagneticdata', 'micromagneticmodel',
    'micromagnetictests', 'oommfc', 'ubermag', 'ubermagtable', 'ubermagutil'
]
all_files = [
    '.gitignore', '.github/workflows/conda.yml',
    '.github/workflows/workflow.yml', 'LICENSE', 'Makefile', 'pyproject.toml',
    'README.md', 'setup.cfg', 'setup.py'
]


def authors_readme(authors):
    """Extract authors and affiliations for README."""
    with open('./authors.toml', 'rb') as fin:
        data = tomli.load(fin)

    affiliations = {}
    author_details = {}
    affiliation_counter = 0
    for author in authors:
        details = data['authors'][author]

        for affiliation in details['affiliations']:
            if affiliation not in affiliations:
                affiliation_counter += 1
                affiliations[affiliation] = affiliation_counter

        author_details[author] = {
            'superscripts': ','.join(
                [str(affiliations[a]) for a in details['affiliations']]),
            'github': details['github'][1:]  # no "@"
        }

    header = ', '.join([(fr'[{author}](https://github.com/{details["github"]})'
                         fr'<sup>{details["superscripts"]}</sup>')
                        for author, details in author_details.items()])
    header += '\n\n'
    header += '  \n'.join([(fr'<sup>{index}</sup> '
                            fr'*{data["affiliations"][affiliation]}*')
                           for affiliation, index in affiliations.items()])
    return header


def contributors_readme(contributors):
    """Extract contributors for README."""
    with open('./authors.toml', 'rb') as fin:
        data = tomli.load(fin)

    return '\n'.join([(f'- [{contributor}](https://github.com/'
                       f'{data["authors"][contributor]["github"][1:]})')
                      for contributor in contributors])


def list2mlstring(inp, quote='', indentation='  ', sep='\n'):
    """Convert a list into a multi-line string, one line per element."""
    return sep.join(f'{indentation}{quote}{elem}{quote}' for elem in inp)


def placeholders(template):
    return re.findall(r'\$(\w+)', template)


def generate_files(*, repository, files):
    req = requests.get(
        f'https://raw.github.com/ubermag/{repository}/master/pyproject.toml',
        headers={'Cache-Control': 'no-cache'})
    pyproject = tomli.loads(req.text)

    authors = [author['name'] for author in pyproject['project']['authors']]
    data = {
        'about': pyproject['tool']['ubermag']['about'],
        'authors': ', '.join(authors),
        'authors_readme': authors_readme(authors),
        'classifiers': list2mlstring(pyproject['project']['classifiers']),
        'contributors_readme': contributors_readme(
            pyproject['tool']['ubermag']['contributors']),
        'copyright_holder': pyproject['tool']['ubermag']['copyright_holder'],
        'dependencies': list2mlstring(pyproject['project']['dependencies']),
        'description': pyproject['project']['description'],
        'doi': pyproject['tool']['ubermag']['doi'],
        'package': repository,
        'tomlauthors': list2mlstring(
            [f'{{name = "{author}"}}' for author in authors], sep=',\n'),
        'tomldependencies': list2mlstring(
            pyproject['project']['dependencies'], quote='"', sep=',\n'),
        'tomlcontributors': list2mlstring(
            pyproject['tool']['ubermag']['contributors'],
            quote='"', sep=',\n'),
        'url': pyproject['project']['urls']['homepage'],
        'version': pyproject['project']['version'],
        'year': datetime.datetime.now().year,
    }

    if 'scripts' in pyproject['project']:
        data['console_scripts'] = 'console_scripts =\n'
        data['console_scripts'] += '\n'.join(
            f'  {s} = {n}' for s, n in pyproject['project']['scripts'].items())
        data['tomlentrypoints'] = '\n[project.scripts]\n'
        data['tomlentrypoints'] += list2mlstring(
            [f'{s} = "{n}"' for s, n in
             pyproject['project']['scripts'].items()],
            indentation='', sep=',\n') + '\n'
    else:
        data['console_scripts'] = ''
        data['tomlentrypoints'] = ''

    # Might be obsolete if we clone the repos first.
    os.makedirs(f'./{repository}/.github/workflows', exist_ok=True)

    for file in files:
        # Read template file.
        with open(f'./templates/{file}', 'rt') as fin:
            template = string.Template(fin.read())

        # Create content.
        content = template.safe_substitute(
            {key: data[key]
             for key in placeholders(template.template)})

        # Write file.
        with open(f'./{repository}/{file}', 'wt') as fout:
            print(content, file=fout)


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
    files = all_files if 'all' in args.file else args.file

    for repo in repos:
        generate_files(repository=repo, files=files)
