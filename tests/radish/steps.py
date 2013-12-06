
# -*- coding: utf-8 -*-

import os

from radish import step

@step(u'I initialize a git repository under "(.*)"')
def I_initialize_a_git_repository_under(step, repo_dir):
    assert not os.path.exists(repo_dir)
    os.makedirs(repo_dir)

@step(u'I use the repository under "(.*)"')
def I_use_the_repository_under(step):
        assert False, "Not implemented yet"

@step(u'I initialise tessera')
def I_initialise_tessera(step):
        assert False, "Not implemented yet"

@step(u'I create a Tessera')
def I_create_a_Tessera(step):
    assert False, "Not implemented yet"

