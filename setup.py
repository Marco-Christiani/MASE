import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mase",
    version="0.0.4",
    author="Marco Christiani",
    author_email="mchristiani2017@gmail.com",
    description="A data simulation engine for multivariate time series data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marco-Christiani/MASE",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'pyplot-themes',
        'seaborn',
    ]
)