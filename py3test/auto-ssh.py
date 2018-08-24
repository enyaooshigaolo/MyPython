"""
File:               LinuxBashShellScriptForOps:pyLinuxHostsSSHKeyInitialization.py
User:               jinke
Create Date:        2018/2/2
Create Time:        11:24
 """
import time
import os
import logging
import logging.handlers
import sys
from fabric.api import *
from fabric.colors import red, green, yellow, blue, magenta, cyan, white
from fabric.context_managers import *
from fabric.contrib.console import confirm
 
env.roledefs = {
    'all': ['192.168.12.89', '192.168.12.95', '192.168.12.19',],
	'slaves': ['192.168.12.95', '192.168.12.19',],
}
 
env.passwords = {
    'root@192.168.12.89:22':'jk',
    'root@192.168.12.95:22':'jk',
    'root@192.168.12.19:22':'jk',
}
 
env.port = '22'
env.user = "root"
env.sudo_user = "root"  # fixed setting, it must be 'root'
env.disable_known_hosts = True
env.warn_only = False
#env.command_timeout = 25
env.connection_attempts = 2
 
def initLoggerWithRotate(logPath="/var/log", logName=None, singleLogFile=True):
    current_time = time.strftime("%Y%m%d%H")
    if logName is not None and not singleLogFile:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + "_" + current_time + ".log"
    elif logName is not None and singleLogFile:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + ".log"
    else:
        logName = "default"
        logFilename = logName + ".log"
    if not os.path.exists(logPath):
        os.makedirs(logPath)
        logFilename = os.path.join(logPath, logFilename)
    else:
        logFilename = os.path.join(logPath, logFilename)
    logger = logging.getLogger(logName)
    log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")
    file_handler = logging.handlers.RotatingFileHandler(logFilename, maxBytes=104857600, backupCount=5)
    file_handler.setFormatter(log_formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger
 
mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")
 
def _win_or_linux():
    # os.name ->(sames to) sys.builtin_module_names
    if 'posix' in sys.builtin_module_names:
        os_type = 'Linux'
    elif 'nt' in sys.builtin_module_names:
        os_type = 'Windows'
    return os_type
 
def is_windows():
    if "windows" in _win_or_linux().lower():
        return True
    else:
        return False
 
def is_linux():
    if "linux" in _win_or_linux().lower():
        return True
    else:
        return False
 
def is_debian_family():
    import platform
    # http://stackoverflow.com/questions/2988017/string-comparison-in-python-is-vs
    # http://stackoverflow.com/questions/1504717/why-does-comparing-strings-in-python-using-either-or-is-sometimes-produce
    if platform.system() == "Linux":
        distname = platform.linux_distribution()
        if "Ubuntu" in distname or "Debian" in distname:
            return True
        else:
            return False
    else:
        return False
 
def is_rhel_family():
    import platform
    if platform.system() == "Linux":
        distname = platform.linux_distribution()
        if "CentOS" in distname or "Debian" in distname:
            return True
        else:
            return False
    else:
        return False
 
# log_path = "/var/log" if os.path.exists("/var/log") or os.makedirs("/var/log") else "/var/log"
log_path = "/var/log"
log_name = "." + os.path.splitext(os.path.basename(__file__))[0]
 
log = initLoggerWithRotate(logPath="/var/log", logName=log_name, singleLogFile=True)
log.setLevel(logging.INFO)
 
def is_valid_ipv4(ip, version=4):
    from IPy import IP
    try:
        result = IP(ip, ipversion=version)
    except ValueError:
        return False
    if result is not None and result != "":
        return True
 
@roles('all')
def reset_ssh_public_host_key():
    with settings(warn_only=False):
        if confirm("Are you really want to reset ssh public key on this host? "):
            print blue("Reconfigure openssh-server")
            sudo("rm /etc/ssh/ssh_host_* && systemctl restart sshd")
        else:
            print green("user canceled this operation.")
        
			
@roles('all')
def inject_admin_ssh_public_key():
    with settings(warn_only=False):
	sudo('rm -rf /root/.ssh/')
        sudo('yes | ssh-keygen -N "" -f /root/.ssh/id_rsa')
 
@roles('slaves')
def scan_host_ssh_public_key():
    with settings(warn_only=False):
        get('/root/.ssh/id_rsa.pub', '/root/.ssh/id_rsa.temp', use_sudo=True)
        local('cat /root/.ssh/id_rsa.temp >>  /root/.ssh/authorized_keys && rm -f  /root/.ssh/id_rsa.temp')
 
def put_authorized_keys():
    sudo('rm -f /root/.ssh/authorized_keys')
    #这里必须复制一次，否则不生效
    put('/root/.ssh/authorized_keys', '/root/.ssh/authorized_keys.temp', use_sudo=True)
    run('cat /root/.ssh/authorized_keys.temp > /root/.ssh/authorized_keys && rm -  f /root/.ssh/authorized_keys.temp')
 
def config_ssh_connection():
    #execute(reset_ssh_public_host_key)
    execute(inject_admin_ssh_public_key)
    local('rm -f /root/.ssh/authorized_keys && cat /root/.ssh/id_rsa.pub > /root/.ssh/authorized_keys')
    execute(scan_host_ssh_public_key)
    execute(put_authorized_keys)
 
def terminal_debug_win32(func):
    command = "fab -f %s %s" % (__file__, func)
    os.system(command)
 
def terminal_debug_posix(func):
    command = "fab -f %s %s" % (__file__, func)
    os.system(command)
 
if __name__ == '__main__':
    import re
    if len(sys.argv) == 1:
        if is_windows():
            terminal_debug_win32("config_ssh_connection")
            sys.exit(0)
        if is_linux():
            terminal_debug_posix("config_ssh_connection")
            sys.exit(0)
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print red("Please use 'fab -f %s'" % " ".join(str(x) for x in sys.argv[0:]))
    sys.exit(1)
