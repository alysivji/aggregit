from setuptools import setup, find_packages

setup(
    name='aggregit',
    version='0.0.1',
    description='This project will aggregate statistics from git services.',
    url='https://github.com/alysivji/aggregit',
    author='Aly Sivji',
    author_email='alysivji@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['tests', ]),
    install_requires=[''],
    download_url='https://github.com/alysivji/aggregit',
)
