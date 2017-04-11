from setuptools import setup, find_packages

VERSION = '0.0.4'

REQUIREMENTS = [
    'lxml',
    'python-amazon-mws',
    'python-dateutil',
    'requests'
]

PACKAGES = find_packages()

setup(
    name='python-amazon-mws-tools',
    packages=PACKAGES,
    url='https://github.com/ziplokk1/python-amazon-mws-tools',
    license='LICENSE.txt',
    author='Mark Sanders',
    author_email='sdscdeveloper@gmail.com',
    install_requires=REQUIREMENTS,
    description='Wrapper modules to request and parse responses for python-amazon-mws.',
    include_package_data=True,
    version=VERSION
)
