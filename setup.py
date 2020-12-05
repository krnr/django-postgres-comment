from pathlib import Path
from setuptools import find_packages, setup

setup(
    name="django-postgres-comment",
    version="0.1.0",
    url="https://gitlab.usetech.ru/pub/django-postgres-comment",
    author="ylobanov",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires="Django>=2.0",
)
