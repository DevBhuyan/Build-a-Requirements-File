#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 01:15:20 2025

@author: dev
"""


import os
import re
import pkg_resources


def extract_imports(file_path: str):
    '''


    Parameters
    ----------
    file_path : str
        DESCRIPTION.

    Returns
    -------
    imports : TYPE
        DESCRIPTION.

    '''

    imports = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Match `import module` or `from module import ...`
            # TODO: Need to add support for bracket multiline imports
            match = re.match(r'^(?:from|import)\s+([a-zA-Z0-9_\.]+)', line)
            if match:
                module = match.group(1).split('.')[0]
                imports.add(module)

    return imports


def get_library_versions(imports: set):
    '''


    Parameters
    ----------
    imports : set
        DESCRIPTION.

    Returns
    -------
    library_versions : TYPE
        DESCRIPTION.

    '''

    library_versions = {}
    for lib in imports:
        try:
            version = pkg_resources.get_distribution(lib).version
            library_versions[lib] = version
        except pkg_resources.DistributionNotFound:
            print(f"Warning: Library '{lib}' is not installed.")
            # TODO: Need to add mapping of lib-names. For example, it cannot detect sklearn, which is installed as scikit-learn in pip
        except Exception as e:
            print(f"Error while fetching version for '{lib}': {e}")

    return library_versions


def create_requirements_file(library_versions: dict,
                             output_path: str = 'requirements.txt'):
    '''


    Parameters
    ----------
    library_versions : dict
        DESCRIPTION.
    output_path : str, optional
        DESCRIPTION. The default is 'requirements.txt'.

    Returns
    -------
    None.

    '''

    with open(output_path, 'w') as req_file:
        for lib, version in library_versions.items():
            req_file.write(f"{lib}=={version}\n")
    print(f"requirements.txt created at {output_path}")


def main():
    '''


    Returns
    -------
    None.

    '''

    py_files = [f
                for f in os.listdir('.')
                if f.endswith('.py')]
    all_imports = set()

    for py_file in py_files:
        imports = extract_imports(py_file)
        all_imports.update(imports)

    library_versions = get_library_versions(all_imports)

    create_requirements_file(library_versions)


if __name__ == '__main__':
    main()
