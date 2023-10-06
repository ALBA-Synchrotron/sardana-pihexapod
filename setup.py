"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['sardana', 'pipython']

setup(
    author="Alberto López Sánchez",
    author_email='ctbeamlines@cells.es',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="ALBA Python hexapod library",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='sardana_pihexapod',
    name='sardana_pihexapod',
    packages=find_packages(include=['sardana_pihexapod', 'sardana_pihexapod.*']),

    url='https://github.com/ALBA-Synchrotron/sardana-pihexapod',
    version='1.1.3',
    zip_safe=False,
)
