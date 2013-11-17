import os

from fabric.api import *
from fabric.operations import get, put
from fabric.operations import local as lrun
from fabric.contrib.project import rsync_project
from keys import SUDOPASS, PROJECT_DIR

env.use_ssh_config = True
env.password = SUDOPASS
local_dir = "/Users/ajames/Dropbox/VISD-Badges/"
deploy_dir = os.path.join(local_dir, 'deploy')
remote_deploy = os.path.join(PROJECT_DIR, 'deploy')


@task
def localhost():
    """
    Used to call local functions
    """
    env.run = lrun
    env.hosts = ['localhost']


@task
def webserver():
    """
    Used to call on the webserver(s)
    """
    env.run = run
    env.hosts = ['visd-badges']


@task
def rtouch():
    """
    A test function. Puts 'text.txt' in '/srv/www/test'
    """
    this_dir = '/srv/www/test'
    with cd(this_dir):
        sudo('touch test.txt', user='www-data')

@task
def sync_project():
    """
    Uses rsync to keep the local Django project synced with the remote.
    """
    with settings(warn_only=True):
        rsync_project(PROJECT_DIR, local_dir=local_dir, exclude='deploy/')
        with cd(PROJECT_DIR):
            sudo('chown -R www-data:www-data .')


@task
@hosts('visd-badges')
def pull_apache_files():
    """
    Gets apache2 configs and stuffs them into the apache dir on the local drive.
    """
    with lcd(deploy_dir):
        get('/etc/apache2/', '%(path)s')


@task
def push_apache_files():
    """
    rsync's apache files from the deploy folder to the server.
    """
    local_apache = os.path.join(deploy_dir, 'apache2/')
    with settings(warn_only=True):
        rsync_project('/etc/apache2', local_dir=local_apache,
                      extra_opts='--rsync-path="sudo rsync"')


@task
def restart_apache():
    """
    Restarts apache.
    """
    webserver()
    sudo('invoke-rc.d apache2 restart')


@task
def stop_apache():
    """
    Stops Apache.
    """
    sudo('invoke-rc.d apache2 stop')


@task
def tail_apache():
    """
    Puts a non-interactive tail on Apache's error log.
    """
    sudo('tail /var/log/apache2/error.log')


@task
def push_wsgi():
    """
    Updates the file mod_wsgi needs.
    """
    wsgi_path = os.path.join(remote_deploy, 'wsgi.py')
    put('wsgi.py', wsgi_path)
    sudo('chown www-data:www-data %s' % wsgi_path)


@task
def push_test_wsgi():
    """
    sends a test.wsgi to the /deploy directory.
    """
    wsgi_path = os.path.join(remote_deploy, 'test.wsgi')
    put('test.wsgi', wsgi_path)
    sudo('chown www-data:www-data %s' % wsgi_path)


@task
def new_apache():
    """
    Pushes new apache configs and restarts apache.
    """
    push_wsgi()
    push_apache_files()
    restart_apache()


@task
def git_push():
    """
    Pushes to the VISD repository.
    """
    with lcd(local_dir):
        local('git push git@github-visd:visd/VISD-Badges.git')


@task
@hosts('visd-badges')
def git_push_from_server():
    """
    Pushes from the server to the VISD repository. Make this rare.
    """
    with cd(PROJECT_DIR):
        run('git push git@github-visd:visd/VISD-Badges.git')


@task
def commit(message, sync=True):
    """
    Does a new git commit with the given message.
    """
    with lcd(local_dir):
        local('git add -A')
        local('git commit -m "%s"' % message)
        if sync:
            git_push()


@task
@hosts('visd-badges')
def commit_server(message, sync=True):
    """
    Makes a commit on the server branch. Be very careful.
    """
    with cd(PROJECT_DIR):
        local('git add -A')
        local('git commit -m "%s"' % message)
        if sync:
            git_push_from_server()


@task
def compare_dirs():
    """
    Checks the local directory and destination for a diff.
    """
    pass


@task
@hosts('visd-badges')
def git_fetch():
    """
    Configures a server to work with the VISD remote repository.
    """
    with cd(PROJECT_DIR):
        run('git fetch origin')


@task
@hosts('visd-badges')
def git_pull(branch='master'):
    """
    Pulls the master (or given) branch from origin and merges it.
    """
    with cd(PROJECT_DIR):
        run('git pull origin')


@task
def git_pull_locally():
    """
    Pulls the current version of the repo onto the local server.
    """
    with lcd(local_dir):
        local('git pull git@github-visd:visd/VISD-Badges.git')


@task
def git_status():
    """
    Asks for status.
    """
    with cd(PROJECT_DIR):
        run('git status')


@task
def sync_to_repo(message):
    """
    Makes a commit, pushes it to the repo, then tells the server to
    fetch the repo.
    """
    commit(message)
    git_fetch()


@task
def git_log():
    """
    Includes options to pretty up the log. On the local dir.
    """
    with lcd(local_dir):
        local('git log --graph --decorate --pretty=oneline --abbrev-commit master origin/master')


@task
@hosts('visd-badges')
def common_ancestor():
    """
    Returns the common ancestor of the most current commits on the server's repository and
    on the repo.
    """
    git_fetch()
    with cd(PROJECT_DIR):
        server_commit = run('git rev-parse HEAD')
        origin_commit = run('git rev-parse origin/master')
        return run('git merge-base %s %s' % (server_commit, origin_commit))


@task
@hosts('visd-badges')
def remote_branches():
    """
    Returns which branch we're on with all servers, along with the current commit.
    """
    with cd(PROJECT_DIR):
        remote_branch = run('git rev-parse --abbrev-ref HEAD')
        remote_commit = run('git rev-parse HEAD')
    return (remote_branch, remote_commit)


@task
def local_branches():
    """
    Looks at the branches we're on in local and web server and returns a comparison.
    """
    with lcd(local_dir):
        local_branch = local('git rev-parse --abbrev-ref HEAD')
        local_commit = local('git rev-parse HEAD')
    return (local_branch, local_commit)


@task
def compare_branches():
    remote_status = remote_branches()
    local_status = local_branches()
    return
