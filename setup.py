#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install as _install


class install(_install):
    """Override setup tools install class to allow NLTK data download."""

    def run(self):
        """Run install."""
        _install.do_egg_install(self)
        import nltk
        nltk.download("punkt")


extras_require = {
    'linter': [
        "flake8"
    ],
    'docs': [
        "sphinx"
    ],
    'dev': [
        "pytest>=3.4.0,<4",
        "setuptools>=38.5.0",
        "tox>=2.9.0",
    ]
}

extras_require['dev'] = (
    extras_require['linter'] +
    extras_require['docs'] +
    extras_require['dev']
)

setup(
    name='auto-complete-server',
    version='0.0.1',
    description="""Auto-completion server.""",
    author='Yacine Nouri',
    author_email='yacine@nouri.io',
    url='https://github.com/ynouri/auto-complete-server',
    include_package_data=True,
    cmdclass={'install': install},
    install_requires=[
        "pandas>=0.22.0",
        "numpy>=1.14.0",
        "nltk>=3.2.0",
        "datrie>=0.7.1"
    ],
    setup_requires=[
        "nltk"
    ],
    python_requires='>=3.6,<4',
    extras_require=extras_require,
    py_modules=['auto_complete_server'],
    zip_safe=False,
    keywords='auto complete, most popular completion',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
