#!/usr/bin/python3

import os
import sys

def handle_envvars(pair):
    return "export {0}={1};".format(pair[0], pair[1])

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

def main(args):
    if (len(args) != 2):
        print("Usage: 'exp envs' to process environment variables. 'exp vars' to process extra variables")
    else:
        if (args[1] == "envs"):
            return process("ANSIBLE_ENVVARS", handle_envvars, ":")
        elif (args[1] == "vars"):
            return process("ANSIBLE_EXTVARS", handle_extvars, "=")
    return ""


if __name__ == "__main__":
    print(main(sys.argv[:]))

