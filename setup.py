from setuptools import setup

setup(
  name = "make_indices",
  version = "1.0.0",
  author = "John Baber-Lucero",
  author_email = "pypi@frundle.com",
  description = ("Brittle way to create a collection of static gallery html pages"),
  license = "GPLv3",
  url = "https://github.com/jbaber/make_indices",
  packages = ['make_indices'],
  install_requires = ['docopt', 'python-magic',],
  entry_points = {
    'console_scripts': ['make-indices=make_indices.make_indices:main'],
  }
)

