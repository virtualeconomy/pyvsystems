from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyvsystems",
    version="0.2.1",
    description="A python wrapper for vsys api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["api wrapper", "blockchain", "vsystems", "smart contract", "supernode", "defi"],
    url="https://github.com/virtualeconomy/pyvsystems",
    author="V SYSTEMS",
    author_email="info@v.systems",
    license="MIT",
    packages=["pyvsystems"],
    install_requires=["requests", "python-axolotl-curve25519", "pyblake2", "base58"],
    python_requires='>=3.4'
)
