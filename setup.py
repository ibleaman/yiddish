from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='yiddish',
    version='0.0.26',
    author='Isaac L. Bleaman',
    author_email='bleaman@berkeley.edu',
    description='A Python library for processing Yiddish text',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ibleaman/yiddish',
    project_urls={
        'Source': 'https://github.com/ibleaman/yiddish',
        'Issues': 'https://github.com/ibleaman/yiddish/issues',
        'Loshn-koydesh data': 'https://github.com/ibleaman/loshn-koydesh-pronunciation',
    },
    keywords=['yiddish', 'transliteration', 'romanization', 'orthography', 'unicode', 'hebrew script', 'presentation forms', 'normalization', 'nlp', 'linguistics'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: Yiddish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Text Processing :: Linguistic',
    ],
    license='MIT',
    packages=['yiddish'],
    python_requires='>=3.9',
    package_data={
        'yiddish': [
            'submodules/hasidify_lexicon/*.csv',
            'submodules/loshn-koydesh-pronunciation/*.txt',
        ],
    },
)
