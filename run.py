#!/usr/bin/python3

import os
import sys
import subprocess
import re
from distutils.dir_util import copy_tree

def handle_envvars(pair):
    os.environ[pair[0]] = pair[1]
    return ""

def handle_extvars(pair):
    return "{0}={1} ".format(pair[0], pair[1])

def process(varname, handler, delim):
    varvalue = os.environ.get(varname)
    result = ""
    if (varvalue):
        pairs = varvalue.split("\n")
        for pair in pairs:
            kvpair = pair.split(delim,1)
            if (len(kvpair) == 2):
                result = result + handler(kvpair)
    return result

def env(name):
    value = os.environ.get(name)
    if value is not None and value:
        return True, value
    return False, None

def runshell(commandlist, capture=False, txt=None, sh=False):
    return subprocess.run(commandlist, capture_output=capture, text=txt, shell=sh, check=True)

def homedir():
    return os.path.expanduser("~")

def add_ssh_agent():
    output = runshell(["ssh-agent", "-s"], capture=True, txt=True, sh=True)
    auth_engine = re.compile("SSH_AUTH_SOCK=(.*?);")
    agent_engine = re.compile("SSH_AGENT_PID=(.*?);")
    sock = auth_engine.search(output.stdout)
    agentid = agent_engine.search(output.stdout)
    os.environ["SSH_AUTH_SOCK"] = sock.group(1)
    os.environ["SSH_AGENT_PID"] = agentid.group(1)


def setup_private_key():
    ssh_path = homedir() + "/.ssh/"
    if (not os.path.isdir(ssh_path)):
        os.mkdir(ssh_path, 0o755)
        pass
    has_key, key_value = env("SSH_PRIVATE_KEY")
    if (has_key):
        filepath = ssh_path + env("SSH_PRIVATE_KEY_FILE")[1]
        f = open(filepath, 'w')
        f.write(key_value)
        f.close()
        os.chmod(filepath, 0o600)
        add_ssh_agent()
        runshell(["ssh-add", filepath])
        pass

def export_envs():
    process("ANSIBLE_ENVVARS", handle_envvars, ":")

def execute_playbook():
    command = ["ansible-playbook"]
    command.append(env("ANSIBLE_PLAYBOOK")[1])
    extra_vars = process("ANSIBLE_EXTVARS", handle_extvars, "=")
    if (extra_vars):
        command.extend(["-e",extra_vars])
        pass
    runshell(command)
    pass

def main():
    copy_tree(env("ANSIBLE_DIRECTORY")[1], homedir())
    os.chdir(homedir())

    if (os.path.isfile("./requirements.yaml")):
        runshell(["ansible-galaxy", "collection", "install", "-r", "./requirements.yaml"])
        pass

    setup_private_key()
    export_envs()
    execute_playbook()

if __name__ == "__main__":
    main()

