import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-git-wrapper",
    version="0.9.0.post1",
    author="Juan Benito Pacheco Rubio",
    author_email="juanbenito.pr@gmail.com",
    description="Simple git wrapper for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juanbenitopr/git-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities"
    ],
    python_requires='>=3.7',
)
