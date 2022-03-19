import pkg_resources

from setuptools import setup, find_packages

pkg_resources.require('setuptools>=39.2')

reqs = [line.strip() for line in open('requirements.txt')]
dev_reqs = [line.strip() for line in open('requirements_dev.txt')]

setup(
    name='pygeoserv',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    extras_require={
        "dev": dev_reqs,  # pip install ".[dev]"
    },
    url='',
    license='MIT',
    author='Francis Pelletier',
    author_email='pelletier.f@gmail.com',
    description=''
)
