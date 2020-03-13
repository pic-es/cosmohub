# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="cosmohub",
    description="CosmoHub API",
    packages=["cosmohub"],
    author="Pau Tallada Crespí",
    author_email="pau.tallada@gmail.com",
    setup_requires=["setuptools>=42", "wheel", "setuptools_scm[toml]>=3.4"],
    include_package_data=True,
    zip_safe=False,
    entry_points={},
)
