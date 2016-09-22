from setuptools import setup, find_packages
import xiblint

setup(
    name='xiblint',
    version=xiblint.__version__,
    description='Checks .xib and .storyboard files for compliance with best practices',
    url='https://github.com/lyft/xiblint',
    author='Ilya Konstantinov',
    author_email='ikonstantinov@lyft.com',
    install_requires=[],
    packages=find_packages(),
    scripts=['bin/xiblint'],
)
