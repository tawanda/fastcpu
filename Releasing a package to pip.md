# Releasing a package to pip

### Install the required packages:

> Setuptools: Setuptools is a package development process library designed for creating and distributing Python packages.
> 
> Wheel: The Wheel package provides a bdist_wheel command for setuptools. It creates .whl file which is directly installable through the pip install command. We'll then upload the same file to pypi.org.
> 
> Twine: The Twine package provides a secure, authenticated, and verified connection between your system and PyPi over HTTPS.
> 
> Tqdm: This is a smart progress meter used internally by Twine.

1. python -m pip install --upgrade pip setuptools wheel
2. python -m pip install tqdm
3. python -m pip install --upgrade twine


Then follow this guide:

https://packaging.python.org/tutorials/packaging-projects/

### releasing

Run

```
python -m build
```

Then


* you don’t need to specify --repository; the package will upload to https://pypi.org/ by default.

```
python -m twine upload dist/*
```

