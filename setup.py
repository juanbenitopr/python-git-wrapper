import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gyt",
    version="0.1.0",
    author="Juan Benito Pacheco Rubio",
    author_email="juanbenito.pr@gmail.com",
    description="Simple git wrapper for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juanbenitopr/git-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires='>=3.6',
)
