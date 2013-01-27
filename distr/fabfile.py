from __future__ import with_statement
from fabric.api import put, run, env, cd, prefix, parallel
from fabric.contrib.files import exists
import os
#env.hosts = []
sys = "SUSE"

def init():
	run("zypper -qn install python-pip python-virtualenvwrapper")
	run("zypper -qn install python-devel libevent-devel blas-devel lapack-devel gcc-fortran")


def test():
	with cd("pepa"):
		with prefix("source /root/.virtualenvs/pepa/bin/activate"):
			out = run("supervisorctl -c worker_supervisord.conf status worker", quiet=True)
			if "RUNNING" in out:
				print("RUNNING")
			else:
				print("STOPPED")

def init_venv():
	if not exists("~/.virtualenvs/pepa/bin/activate"):
		with prefix("source  /usr/bin/virtualenvwrapper.sh"):
			run("mkvirtualenv -p /usr/bin/python2.7 --distribute pepa")

def install():
	with prefix("source /root/.virtualenvs/pepa/bin/activate"):
        	run("pip -q install pyparsing colorama gevent")
	        run("pip -q install numpy")
        	run("pip -q install scipy")
		run("pip -q install supervisor")
@parallel
def super():
	with prefix("source /root/.virtualenvs/pepa/bin/activate"):
		run("pip -q install supervisor")

def set_hosts():
	env.warn_only = True
	env.hosts = open('hosts', 'r').readlines()

def copy():
	if exists("~/pepa"):
		run("rm -rf ~/pepa")
	run("mkdir pepa")
	put("~/pepa/py.tar", "/root/pepa/py.tar")
	run("tar xvf /root/pepa/py.tar -C /root/pepa/")


def runs():
	with prefix("source /root/.virtualenvs/pepa/bin/activate"):
		with cd("pepa"):
			run("supervisord -c worker_supervisord.conf")


def restart():
	with prefix("source /root/.virtualenvs/pepa/bin/activate"):
		with cd("pepa"):
			run("supervisorctl -c worker_supervisord.conf restart all")

def stop():
	with prefix("source /root/.virtualenvs/pepa/bin/activate"):
		with cd("pepa"):
			run("supervisorctl -c worker_supervisord.conf stop all")


@parallel
def deploy():
	init()
	init_venv()
	install()
	copy()
	
	
