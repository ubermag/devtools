import re
import ast
import json
import string
import datetime
import requests
import argparse

all_repos = ['discretisedfield']
all_files = ['LICENSE', 'README.md']


def authors_readme(authors):
    with open(f'./authors.json', 'rt') as fin:
        data = json.load(fin)

    authors_line_list = []
    affiliations_list = []
    superscripts = {}
    for author in authors:
        github, *affiliations = data['authors'][author]
        
        for affiliation in affiliations:
            if affiliation not in affiliations_list:
                affiliations_list.append(affiliation)

        superscripts[author] = [affiliations_list.index(affiliation) + 1
                                for affiliation in affiliations]

        authors_line_list.append(f'[{author}](https://github.com/{github[1:]})<sup>{",".join(map(str, superscripts[author]))}</sup>')
        
    header = ', '.join(authors_line_list)
    header += '\n\n'
    header += '  \n'.join([fr'<sup>{i+1}</sup>{data["affiliations"][a]}' for i, a in enumerate(affiliations_list)])
    
    return header


def contributors_readme(contributors):
    with open(f'./authors.json', 'rt') as fin:
        data = json.load(fin)

    contributors_list = []
    for contributor in contributors:
        github, *_ = data['authors'][contributor]
        contributors_list.append((contributor, github))
        
    return '\n'.join([f'- [{c}](https://github.com/{g[1:]})'
                      for c, g in contributors_list])


def placeholders(template):
    return re.findall('\$(\w+)', template)


def generate_files(*, repository, files):
    # Get metadata.json from repo's URL, extract data, and set defaults.
    repository_url = f'https://raw.github.com/ubermag/{repository}/master/metadata.json'
    data = ast.literal_eval(requests.get(repository_url,
                                         headers={'Cache-Control': 'no-cache'}).text)
    data.setdefault('year', datetime.datetime.now().year)
    data.setdefault('package', repository)
    data.setdefault('authors_readme', authors_readme(data['authors']))
    data.setdefault('contributors_readme', contributors_readme(data['contributors']))
    
    for file in files:
        # Read template file.
        with open(f'./templates/{file}', 'rt') as fin:
            template = string.Template(fin.read())
    
        # Create content.
        content = template.substitute({key: data[key]
                                       for key in placeholders(template.template)})
        
        # Write file.
        with open(f'./{file}', 'wt') as fout:
            print(content, file=fout)
            
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update repository\'s metadata')
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