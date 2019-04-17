import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='albert',
      version='1.3.1',
      description='Interact with hidden REST API of albertheijn.nl',
      long_description = long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/MHilhorst/albertheijn',
      author='M. Hilhorst',
      install_requires=[
          'requests'
      ],
      author_email='michaeljianghilhorst@gmail.com',
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent"
      ]
)
