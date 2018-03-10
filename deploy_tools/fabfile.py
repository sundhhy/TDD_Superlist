# -*- coding: utf-8 -*-
from fabric.contrib.files import append,exists,sed
from fabric.api import env, local, run
import random

REPO_URL = 'git@github.com:sundhhy/TDD_Superlist.git'

def deploy():
    site_folder = '/home/%s/sites/%s'%(env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run ('mkdir -p %s/%s',(site_folder, subfolder))

def _get_latest_source(source_floder):
    if exists(source_floder + '/.git'):
        run('cd %s && git fetch'%(source_floder,))
    else:
        run('git clone %s %s'%(REPO_URL, source_floder))
    # 5 获取本地仓库的当前提交的哈希值
    current_commit = local("git log -n 1 --format=%H", capture=True)
    # 6 将本地仓库恢复到指定的版本，即撤销服务器对代码的修改
    run('cd %s && git reset --hard %s'%(source_floder, current_commit))

#更新配置文件，设置ALLOWED_HOST DEBUG,还创建一个密钥
def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/setting.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]'%(site_name,)
        )
    secret_key_file = source_folder + 'superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'"%(key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s'%(virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt'%(virtualenv_folder, source_folder))

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manager.py collectstatic --noinput'%(source_folder,))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/pyhton3 manager.py migrate --noinput'%(source_folder,))

