from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='yiddish',
    version='0.0.4',
    author='Isaac L. Bleaman',
    author_email='bleaman@berkeley.edu',
    description='A Python library for processing Yiddish text',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ibleaman/yiddish',
    license='MIT',
    packages=['yiddish'],
    test_suite='tests',
)
