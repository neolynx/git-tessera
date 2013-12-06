
# -*- coding: utf-8 -*-

import os
import tempfile
import subprocess

from radish import step, world

@step(u'I use a new temporary directory')
def I_use_a_new_temporary_directory(step):
    world.tmp = tempfile.mkdtemp(suffix="tesseratest")

@step(u'I initialize a git repository under the temporary directory')
def I_initialize_a_git_repository_under(step):
    assert subprocess.call(["git", "init", world.tmp]) == 0

@step(u'I use the repository under the temporary directory')
def I_use_the_repository_under(step):
    world.repository = world.tmp

@step(u'I initialise tessera')
def I_initialise_tessera(step):
    assert subprocess.call(["git", "tessera", "init"], cwd=world.repository)

@step(u'I create a Tessera')
def I_create_a_Tessera(step):
    assert False, "Not implemented yet"

