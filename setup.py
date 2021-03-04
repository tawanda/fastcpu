import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastcpu",
    version="0.0.1",
    author="Tawanda Minya",
    author_email="tminya@gmail.com",
    description=" A queue service for quickly developing scripts that use all your CPUs efficiently",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tawanda/fastcpu",
    project_urls={
        "Bug Tracker": "https://github.com/tawanda/fastcpu/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.0",
)
