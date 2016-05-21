#!/usr/bin/env python
## To parse yaml file
import yaml

## To call command
from subprocess import call

## To know the platform
import platform

## To parse json
import json

## To split line in rc file
import re

##
import urllib2

##
import sys, os

################################################################################
def convert_plaform(p):
    if p == "Ubuntu":
        return "debian"
    else:
        return p
################################################################################

################################################################################
# Constantes
GITHUB_RAW = "https://raw.githubusercontent.com"
DEFAULT_EASY_FILE_IN_REPO = ".easy-install.yml"
DEFAULT_EASY_FILE_CONFIG = os.path.expanduser("~") + "/.easy-install.rc"
DEFAULT_BRANCH = "master"
INSTALL_CMD = "Install"

## Options
OPT_FILE = "file"
OPT_BRANCH = "branch"

## TODO
### Manage different host
OPT_HOST = "host"

## FIXME: check different platforms
OS_LOC = convert_plaform(platform.dist()[0])

## REGEX for splitting line
REGEX_SPLIT = "(" + INSTALL_CMD + ") +\"([^\"]+)[ \"',]+(\{[^}]+\})?"
REGEX_COMMENT = "^(\s*#|\s+)"

## For colors
COLOR_RED = "\033[1;31m"
COLOR_CYAN = "\033[1;36m"
COLOR_NRM = "\033[1;0m"
################################################################################

################################################################################
def print_error(s):
    print(COLOR_RED + s + COLOR_NRM)

def print_info(s):
    print(COLOR_CYAN + s + COLOR_NRM)
################################################################################

################################################################################
def install(list_cmd):
    os_found = False
    # If commands depend on platform, list_cmd is a list of dictionnary
    if type(list_cmd[0]) is dict:
        # we check each platform.
        for os_list_cmd in list_cmd:
            # If the current platform is the right platform
            if OS_LOC in os_list_cmd.keys():
                execute_cmd(os_list_cmd[OS_LOC])
                os_found = True
                break
        # If we never execute a command it means platform is not supported.
        if not os_found:
            print_error("YAML file doesn't support your OS")
            exit(1)
    # Else, list_cmd is a list of commands ie string list.
    else:
        execute_cmd(list_cmd)

# Execute a list of commands
def execute_cmd(list_cmd):
    for cmd in list_cmd:
        call(cmd, shell=True)

# Parse a YAML file
def atomic_easy_file(f):
    if type(f) is file:
        s = yaml.load(open(f))
    elif type(f) is str:
        s = yaml.load(f)
    if s.has_key("description"):
        print_info("-----> " + s["description"])
    else:
        print_error("No description for the YAML file. Please add one")
        exit(1)
    if s.has_key("depends-easy"):
        print_info("          Install dependencies with easy-install")
        parse_configuration_file(s["depends-easy"])
        print_info("          Install dependencies with easy-install... FINISHED")
    if s.has_key("depends"):
        print_info("          Install dependencies")
        install(s["depends"])
        print_info("          Install dependencies... FINISHED")
    if s.has_key("install"):
        print_info("          Install...")
        install(s["install"])
        print_info("          Install... FINISHED")
    else:
        print_error("No install commands")
        exit(1)
    if s.has_key("after_install"):
        print_info("          After install")
        execute_cmd(s["after_install"])
        print_info("          After install... FINISHED")
################################################################################

################################################################################
# Represents a line Install.
class easy_file():
    def __init__(self, user, repo, options = dict()):
        self.user = user
        self.repo = repo
        self.options = options

    def __str__(self):
        s = []
        s.append(self.get_host())
        s.append("/")
        s.append(self.user)
        s.append("/")
        s.append(self.repo)
        s.append("/")
        s.append(self.get_branch())
        s.append("/")
        s.append(self.get_file())
        return "".join(s)

    def get_host(self):
        if OPT_HOST in self.options.keys():
            pass
        else:
            return GITHUB_RAW

    def get_branch(self):
        if OPT_BRANCH in self.options.keys():
            return self.options[OPT_BRANCH]
        else:
            return DEFAULT_BRANCH

    def get_file(self):
        if OPT_FILE in self.options.keys():
            return self.options[OPT_FILE]
        else:
            return DEFAULT_EASY_FILE_IN_REPO

# Parse a line as 'Install "user/repo"' or 'Install "user/repo", {file: "file"}'
# and return an object
def parse_install_line(line):
    s = re.split(REGEX_SPLIT, line)
    repo = ""
    user = ""
    options = dict()
    if len(s) == 5:
        s = [s[1], s[2], s[3]]
        if s[0] == INSTALL_CMD:
            (user, repo) = s[1].split("/")
            if s[2] != None:
                options = json.loads(s[2])
            return (easy_file(user, repo, options))
        else:
            print_error("Error parsing rc file")
            exit(1)
    else:
        print_error("Error parsing rc file")
        exit(1)

def is_comment(line):
    return bool(re.search(REGEX_COMMENT, line))

# Execute a file or a list of line containing Install instructions.
def parse_configuration_file(f):
    contents = get_contents(f)
    for line in contents:
        if not is_comment(line) and len(line) != 0:
            print_info(80 * "#")
            content_line = urllib2.urlopen(str(parse_install_line(line)))
            atomic_easy_file(content_line.read())

# if f is a file, get_contents return the contents of this file. If f is a
# list, only returns f.
# Use in parse_configuration_file to be able to use this function when there is
# a depends-easy node in a YAML file.
def get_contents(f):
    if type(f) is str:
        return [x.strip() for x in open(f, "r")]
    elif type(f) is list:
        return f

argc = len(sys.argv)

if argc == 1:
    content = parse_configuration_file(DEFAULT_EASY_FILE_CONFIG)
elif argc == 2:
    content = parse_configuration_file(sys.argv[1])
else:
    print_error("./easy_install.py [config_file]")
    exit(1)
################################################################################
