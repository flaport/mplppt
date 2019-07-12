import mplppt
import setuptools

description = """ Convert a matplotlib figure to a powerpoint slide """

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="mplppt",
    version=mplppt.__version__,
    author=mplppt.__author__,
    author_email="floris.laporte@gmail.com",
    description=description.replace("\n", " "),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/flaport/mplppt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
