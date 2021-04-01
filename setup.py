from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('dclist/__init__.py') as f:
  version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

extras_require = {'dev': ['python-dotenv']}
readme = ''
with open('README.md') as f:
  readme = f.read()

setup(
  name = 'dclist.py',
  packages = ['dclist', 'dclist.helpers'],
  version = version,
  license = 'MIT',
  description = 'GQL-API wrapper for dclist.net',
  author = 'ilkergzlkkr',
  author_email = 'guzelkokarilker@gmail.com',
  url = 'https://github.com/dclist/python-sdk',
  download_url = 'https://github.com/dclist/python-sdk.git',
  install_requires = requirements,
  long_description = readme,
  extras_require = extras_require,
  long_description_content_type = "text/markdown",
  classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
  ],
)