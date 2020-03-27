import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cerberus-list-schema-firepubes",
    version="1.0",
    author="Amy Summers",
    author_email="amy@sakuradigital.co.uk",
    description="Cerburus based validation extended to support list schemas and "
                "list transposition to dictionary and python objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Firepubes/cerberus-list-schema",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
