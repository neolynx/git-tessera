# tessera

The most simple git based ticketing system.

If you want to
    - get rid of loosing your tickets because of changing the issue management system
    - have documented your tickets with your code
    - have a real unique and persistent ticket id
    - a shaXX save documented issue system

... you want to use tessera!

**License:** GPL
**Version:** 0.00.01

## Installation

TBD

## Usage

TBD

## Development
We recommend you to develop git-tessera inside a virtualenv, since the dependencies can be managed much easier and no unwanted packages installed somewhere on the system are involved.

```
virtualenv tessera-env --no-site-packages
```

*Note: the `--no-site-packages` option is only used for older versions of virtualenv. In newer versions it's default anyway but it is not a problem to use this option at all!*

Activate the virtualenv with:

```
. tessera-env/bin/activate
```

and deactivate it with:

```
deactivate
```

Now you can install all dependencies with the `requirements.txt` file:

```
pip install -r requirements.txt
```

After this command you can see the control with the `pip freeze` command

```
$ pip freeze
argparse==1.2.1
colorful==0.01.02
dulwich==0.9.4
funky==0.0.2
git-tessera==0.00.01
gittle==0.2.2
mimer==0.0.1
paramiko==1.10.0
pycrypto==2.6
web.py==0.37
wsgiref==0.1.2
```

Install `git-tessera` with the setup.py script inside the virtualenv:

```
python setup.py install
```

If you install `git-tessera` without installing the dependencies from the `requirements.txt` file the needed packages will be installed with the setup.py script!
