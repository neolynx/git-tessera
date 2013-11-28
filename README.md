# radish
> `radish` is a "Behavior-Driven Developement"-Tool written in python <br />
> Version: 0.01.27

***

**Author:** Timo Furrer <tuxtimo@gmail.com><br />
**License:** GPL<br />
**Version:** 0.01.27<br />

## <a name='TOC'></a>Table of contents

  1. [What is radish](#whatis)
  1. [Installation](#installation)
    1. [Missing dependencies](#missing_dependencies)
    1. [Simple installation with pip](#installation_pip)
    1. [Manual installation from source](#installation_source)
    1. [Update source installation](#installation_update)
    1. [Install on Windows](WINDOWS_INSTALLATION_GUIDE.md)
  1. [How to use?](#usage)
  1. [Writing tests](#write_tests)
  1. [Contribution](#contribution)
  1. [Infos](#infos)

## <a name='whatis'></a>What is `radish` ?
`radish` is a "Behavior-Driven Developement"-Tool written in python.<br />
It is inspired by other `BDD`-Tools like `cucumber` or `lettuce`.<br />

[[⬆]](#TOC)

## <a name='installation'></a>Installation
There are several ways to install `radish` on your computer:

[[⬆]](#TOC)

### <a name='missing_dependencies'></a>Missing dependencies
`radish` needs `libxml` to generated xunit files. So, if you haven't already installed it:

    apt-get install libxml2 lixbml2-dev libxslt1-dev

On some computers I've seen the problem that `zlib1g-dev` was not installed, which is used to compile lxml.
It result in the error:

    /usr/bin/ld: cannot find -lz

You can fix it with:

    apt-get install zlib1g-develop

[[⬆]](#TOC)

### <a name='installation_pip'></a>Simple installation with pip
This is probably the simplest way to install `radish`.<br />
Since the `radish` releases are hostet as well on [pip](https://pypi.python.org/pypi/pip) you can use the following command to install `radish`:

    pip install radish

*Note: On some systems you have to be root to install a package over pip.*

[[⬆]](#TOC)

### <a name='installation_source'></a>Manual installation from source
If you always want to be up to date with the newest commits you may want to install `radish` directly from [source code](https://github.com/timofurrer/radish).<br />
Use the following command sequence to clone the repository from github and install `radish` afterwards:

```bash
git clone https://github.com/timofurrer/radish.git ~/radish
cd ~/radish
git submodule init
git submodule update
python setup.py install
```

*Note: On some systems you have to be root to install a package over setuptools.*

[[⬆]](#TOC)

#### <a name='installation_update'></a>Update source installation
If you have once installation `radish` from source you might want to update it from time to time.<br />
Change into the directory where you have cloned `radish` into (default: `~/radish`) and pull the newest commit from github. When you've done this you need to re-install `radish` again.<br />
So, in summary:

```bash
cd ~/radish
git pull
python setup.py install
```

*Note: On some systems you have to be root to install a package over setuptools.*

[[⬆]](#TOC)

## <a name='usage'></a>How to use?

```bash
mkdir testprj
cd testprj
radish -c
```

```bash
creating radish/
creating radish/steps.py
creating radish/terrain.py
```

```bash
mkdir tests
cat > tests/001-howto.feature <<EOF
Feature: Provide a first test as example for using radish
  In order to be a good program, provide an example how to write a test.

  Scenario: Getting started using radish
    # Show the steps that need to be done to get testing with radish.

    Given I have radish version 0.01.15 installed

EOF
```

```bash
radish tests/001-howto.feature
```

```bash
tests/001-howto.feature:7: error: no step definition found for 'Given I have radish version 0.01.15 installed'
you might want to add the following to your steps.py:

@step(u'I have radish version 0.01.15 installed')
def I_have_radish_version_0_01_15_installed(step):
    assert False, "Not implemented yet"

```

add these 3 lines to radish/steps.py and run radish again:

```bash
radish tests/001-howto.feature
```

  1. Provide a first test as example for using radish                                  # 001-howto.feature
     In order to be a good program, provide an example how to write a test.

     1. Getting started using radish
        1. Given I have radish version 0.01.15 installed
           AssertionError: Not implemented yet

1 features (0 passed, 1 failed)
1 scenarios (0 passed, 1 failed)
1 steps (0 passed, 1 failed)
(finished within 0 minutes and 0.00 seconds)


[[⬆]](#TOC)

## <a name='write_tests'></a>Writing tests
Coming soon ...

[[⬆]](#TOC)

## <a name='contribution'></a>Contribution
### <a name='contribution_virtuelenv'></a> Use virtualenv
I recommend you to develop `radish` in a virtualenv, because than you can easily manage all the requirements.

```bash
virtualenv radish-env --no-site-packages
. radish-env/bin/activate
pip install -r requirements.txt
```

More coming soon ...

[[⬆]](#TOC)

## <a name='infos'></a>Infos
The files which are currently in the testfiles-folder are from lettuce - another TDD tool!

[[⬆]](#TOC)
