from fabric.api import env, cd, run
from invoke import Responder
from _credentials import github_username, github_password
'''这里采用的是fabric3 1.14.post1,在最新版的fabric中不知为什么使用默认用户root登录不成功，原因未知。
   
   在fabric3中的run函数并无watchers传参。'''
env.hosts = ['112.124.6.127', ]
env.user = 'huang'
env.port = 22
env.password = 'a2251029'


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


def deploy():
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'Djangoblog'

    project_root_path = '~/apps/Djangoblog/Djangoblog'

    # 先停止应用
    with cd(supervisor_conf_path):
        cmd = 'supervisorctl stop {}'.format(supervisor_program_name)
        run(cmd)

    # 进入项目根目录，从 Git 拉取最新代码
    with cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        run(cmd)

    # 安装依赖，迁移数据库，收集静态文件
    with cd(project_root_path):
        run('pipenv install --deploy --ignore-pipfile')
        run('pipenv run python manage.py migrate')
        run('pipenv run python manage.py collectstatic --noinput')

    # 重新启动应用
    with cd(supervisor_conf_path):
        cmd = 'supervisorctl start {}'.format(supervisor_program_name)
        run(cmd)
