from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in interiofloors_customizations/__init__.py
from interiofloors_customizations import __version__ as version

setup(
	name="interiofloors_customizations",
	version=version,
	description="this interior floor",
	author="portaltech",
	author_email="safdar211@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
