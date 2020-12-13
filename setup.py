# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in biox/__init__.py
from biox import __version__ as version

setup(
	name='biox',
	version=version,
	description='Stores the customizations created for Biox Green Tech. Pvt Ltd, by Charioteer Software Private Limited',
	author='Charioteer Software Private Limited',
	author_email='superadmin@charioteersoftware.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
