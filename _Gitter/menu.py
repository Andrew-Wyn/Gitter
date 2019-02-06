import os
import platform
import sys
from termcolor import colored
import server

_os = str(platform.platform())

def clear_shell():
    sys.stdout.flush()
    # to use only on mingw shell
    os.system('clear')

    if "Windows" in _os :
        os.system('cls')
    else: 
        os.system('clear')

def my_press_enter():
    input("\nPress Enter ...")
    
def print_from_file(file_name):
    clear_shell()
    file = open(file_name, "r+")

    for line in file:
        print(colored(line, 'magenta'), end='')
    
    print("\n")
    sys.stdout.flush()

def call_help(functions):
    print("\n\t- commands -\n")
    for id in functions:
        if len(id)>6:
            print("{}\t\t\t{}".format(id, functions[id]))
        else:
            print("{}\t\t\t\t{}".format(id, functions[id]))

def my_shell_input(git):
    print_from_file("titolo.txt")
    commands = str(input("[" + colored(git.git_user.get_user().name, "yellow") + "] Gitter > "))
    if commands.split(" ")[0] in git.functions:
        # switch for the functions
        if commands == "repositories":
            git.print_repositories()
        elif commands.split(" ")[0] == "repbylang":
            try:
                git.get_repo_lang(commands.split(" ")[1])
            except IndexError:
                print("\nerror, the correct usage is: repbylang [name-lang]")
        elif commands.split(" ")[0] == "work":
            try:
                git.restore_repositories()
                if commands.split(" ")[1] in git.repositories:
                    work_on_repo(server.On_Repo(git.git_user.get_repo("{}/{}".format(server.user, commands.split(" ")[1]))))
                else:
                    print(colored("\n\t* la repository '{}' non esiste *".format(commands.split(" ")[1]), 'red'))
            except IndexError:
                print("\nerror, the correct usage is: work [name-repo]")
        elif commands == "logout":
            git.logout()
        elif commands == "quit":
            sys.exit()
        else:
            print("'{}' is not a command, use 'help' to more informations".format(commands))
    else:
        if commands == "help":
            call_help(git.functions)
        else:
            print("'{}' is not a command, use 'help' to more informations".format(commands))
    
    my_press_enter()

def work_on_repo(git_on_work):
    git_on_work.init_branch()
    while True:
        print_from_file("titolo.txt")
        commands = str(input("[" + colored(git_on_work.working_repo.full_name, "blue") + "] Gitter > "))
        if commands.split(" ")[0] in git_on_work.work_on_repo_functions:
            # switch for the functions
            if commands == "referres":
                git_on_work.get_referres()
            elif commands == "dir":
                git_on_work.content_dir()
            elif commands == "branch":
                git_on_work.print_branches()
            elif commands == "commit":
                git_on_work.get_last_commit()
            elif commands.split(" ")[0] == "create":
                try:
                    branch = commands.split(" ")[4]
                    if git_on_work.check_brach(branch):
                        git_on_work.create_file(commands.split(" ")[1], commands.split(" ")[2], commands.split(" ")[3], branch)
                    else:
                        print("\nerror, il branch '{}' inserito non esiste -> usa branches per vedere quelli della repo".format(branch))
                except IndexError:
                    print("\nerror, the correct usage is: create [path-file-to-up] [name-file-in-server] [commit] [branch]")
            elif commands == "back":
                return
            else:
                print("'{}' is not a command, use 'help' to more informations".format(commands))
        else:
            if commands == "help":
                call_help(git_on_work.work_on_repo_functions)
            else:
                print("'{}' is not a command, use 'help' to more informations".format(commands))
        
        my_press_enter()