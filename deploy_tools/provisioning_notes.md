配置新网站
=========

* nginx
* python3
* Git
* pip
* virtualenv

以ubuntu为例，可以执行下面的命令安装：
	sudo apt-get install nignx git pyhon3 python3-pip
	sudo pip3 install virtual

## 配置nginx虚拟主机

* 参考nginx.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com

##systemd 任务，开机自动启动

* 参考gunicorn-systemd.template.conf
* 把SITENAME替换成所需的域名，例如staging-my-domain.com

## 文件夹结构

假有用户账户，家目录位/home/username

/home/username
sites
└── superlists-staging.ottg.eu
    ├── database
    ├── source
    ├── static
    └── virtualenv

