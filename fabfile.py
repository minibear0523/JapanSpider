# encoding=utf-8
from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm


env.hosts = ['192.168.1.4']
env.warn_only = True
env.user = 'minibear'


def prepare_deploy():
    local('git add --all && git commit')
    local('git push')


def deploy():
    code_dir = '/home/minibear/projects/JapanSpider'
    with cd(code_dir):
        run('git pull')


def d():
    prepare_deploy()
    deploy()
