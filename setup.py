# encoding: utf-8

from setuptools import setup

readme = open('README.rst').read()


setup(
    name="pytest-bpdb",
    packages=["pytestbpdb"],
    version="0.1.3.dev0",
    description="A py.test plug-in to enable drop to bpdb debugger on test failure.",
    long_description=readme,
    author="Sławek Ehlert",
    author_email="slafs.e@gmail.com",
    url="https://github.com/slafs/pytest-bpdb",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=[
        'pytest>=2.6.3',
        'bpython',
    ],
    # the following makes a plugin available to py.test
    entry_points = {
        "pytest11": [
            "pytestbpdb = pytestbpdb.ptbpdb",
        ]
    },
)
