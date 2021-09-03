# Managing python versions

## The problem
I need python2.6 to run some specific security tool

## The solution
PyEnv manages multiple python versions on the system.
 - Automatically compiles Python
 - Manages the path and environment settings
 - https://github.com/pyenv/pyenv
 - https://github.com/pyenv/pyenv-installer
 - https://github.com/pyenv/pyenv/wiki/common-build-problems

---

```sh
# Installing a python version
pyenv install 3.8.5

# Listing all the python versions available
pyenv versions

# Switching python version
pyenv global 3.8.5
```

# Dependency Hell

## The problem
1. I installed tool-a from apt-get
2. I installed tool-b from pip
3. Everything is broken

## The solution
* Use one or the other
* Isolate each applications dependencies from another (virtualenvs)

## Creating a virtual enviroment
```sh
# create a project directory 
mkdir tool-c && cd tool-c
# create a hidden env folder to hold the virtualenv
python3 -m venv .env/
# Enter/active the virtualenv
source .env/bin/activate

(.env/) root@localhost:~$ pip install requests
```

# Pipx
Pipx is a tool that automates the installation of pip modules inside of isolated environments on your behalf.
* `pipx` is made specifically for install applications which expose command line tools 
* `pipx` should not be used for libraries, or development work

```sh
# Install pipx
python3 -m pip install pipx
# setup the path
pipx ensurepath
# install something with pipx in it's own env
pipx install pycowsay
# run it
pycowsay "I'm out of hell"
```

# Making Python Apps Semi-Portable
https://docs.python.org/3/library/zipapp.html

* They're the Jar files of the Python world!
* ZipApps by convention have the `.pyz` extension 
    * it's just a zip file
* Functionality has existed since 2.7
    * badly documentated and hidden
* Allows you to package a Python app in a zip format with all it's dependencies and run it in an isolated manner.

## Creating a ZipApp
https://docs.python.org/3/library/zipapp.html#creating-standalone-applications-with-zipapp

Run the following in your app folder
```sh
python -m pip install -r requirements.txt --target myapp
python -m zipapp -p "/usr/bin/env python3" myapp -m "myapp:main"
```

This will produce a standalone executable (zip) which can be run on any machine with the approriate interpreter

`python myapp.pyz`

Python ZipApps run completely in memory

This will not work with application that use C extensions

# Shiv
shiv modifies ZipApp to work with C Extensions
* spools all the files to disk under a shiv directory
* allows C Extensions to work
    * not guaranteed to be compatable with other architectures 
    * OSX vs Windows vs Nix

https://github.com/linkedin/shiv

# Docker
Stick with python 3 images based on Debian
 * `python:latest`
 * C extensions are available for debian
 * if you use Alpine, you will experience issues.

The bible of packaging Python apps in Docker
https://pythonspeed.com/docker/

## Docker in practice
```sh
git clone https://www.github.com/my-app
cd my-app
docker pull python
docker run -v $(pwd):/my-app -it $IMAGE_ID /bin/bash
```

# Wrapping a python binary
```sh
#!/usr/bin/env bash
source /opt/soc/app1/env/bin/activate
python3 /opt/soc/app1/main.py "$@"
deactivate
```
