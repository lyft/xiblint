from setuptools import setup, find_packages
import xiblint

setup(
    name='xiblint',
    version=xiblint.__version__,
    description='Checks .xib and .storyboard files for compliance with best practices',
    license='apache2',
    url='https://github.com/lyft/xiblint',
    author='Ilya Konstantinov',
    author_email='ikonstantinov@lyft.com',
    install_requires=[
        'defusedxml>=0.5.0',
    ],
    packages=find_packages(),
    entry_points={'console_scripts': ['xiblint=xiblint.__main__:main']},
)
