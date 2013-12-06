
# -*- coding: utf-8 -*-

from radish import world, before, after


@before.all
def before_all():
    pass

@after.all
def after_all(result):
    pass

@before.each_step
def before_each_step(step):
    pass

@after.each_step
def after_each_step(step):
    pass