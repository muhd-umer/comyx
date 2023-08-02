import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simcomm",
    author="Muhammad Umer",
    author_email="thisismumer@gmail.com",
    description="SimComm is an optimized library for simulating wireless communication systems. It is purely written in Python and used NumPy and SciPy for numerical computation. It is designed to be easy to use and flexible to extend.",
    keywords=[
        "python",
        "communication",
        "simulator",
        "wireless communication",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muhd-umer/simcomm",
    project_urls={
        "Documentation": "https://simcomm.readthedocs.io",
        "Bug Reports": "https://github.com/muhd-umer/simcomm/issues",
        "Source Code": "https://github.com/muhd-umer/simcomm",
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={"": "./"},  # "": "src
    packages=setuptools.find_packages(where="./"),
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    # install_requires=['Pillow'],
)
