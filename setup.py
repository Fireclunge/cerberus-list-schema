import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cerberus-list-schema",
    version="1.0.1",
    author="Amy Summers",
    author_email="amy@sakuradigital.co.uk",
    description="Cerburus based validation extended to support list schemas and "
    "list transposition to dictionary and python objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Firepubes/cerberus-list-schema",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["cerberus", "munch",],
    keywords=[
        "validation",
        "schema",
        "dictionaries",
        "normalization",
        "list",
        "array",
        "cerberus",
        "object",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.4",
)
