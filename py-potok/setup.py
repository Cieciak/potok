from setuptools import setup, find_packages

setup(
    name='py-potok',
    version='0.4',
    packages=find_packages("src"),
    package_dir={"": "src"},
)