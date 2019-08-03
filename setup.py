import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpinfo",
    version="0.2.1",
    author="Timothy Brown",
    author_email="sysop@timb.us",
    description="Gathers platform information of the currently running Raspberry Pi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timothybrown/rpinfo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
)