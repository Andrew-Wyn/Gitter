from github import *
import os
import platform
import sys
from termcolor import colored
import socket
import menu

user = None
psw = None

class On_Account():
    def __init__(self):
        self.functions = {"repositories" : "return all repository of this account", "logout": "logout this account and return to the log menu", "quit": "exit and close the program", "repbylang": "repbylang lang, return all repositories whit a determinate language", "work": "work repo, to work on some repo move to a new menu"}
        self.git_user = None
        self.repositories = []
    # LOG
    def logout(self):
        self.git_user = None
        print("\nLogged out")


    def login(self):
        global user
        global psw

        menu.print_from_file("titolo.txt")
        print("\t* Legend *\n\n" + colored("color", 'yellow') + " -> nome account\n" + colored("color", 'blue') + " -> nome repository\n")
        print("\t- LOGIN -\n")
        user = input("Inserisci User-Name: ")
        psw = input("Inserisci Password: ")

        self.git_user = Github(user, psw)
        
        try:
            self.git_user.get_user().get_repos()[0].name    
        except GithubException:
            self.git_user = None
            print(colored("\n\t* error to log *", 'red'))
            menu.my_press_enter()
        except socket.error:
            self.git_user = None
            print(colored("\n\t* error to log *", 'red'))
            menu.my_press_enter()

    def get_repo_lang(self, lang): # fetch all repositories -> to fix only user repos
        print("\n\t- Repositories with '{}' language -".format(lang))
        repositories = self.git_user.search_repositories(query='language:{}'.format(lang))
        _void = True
        for repo in repositories:
            _void = False
            print(repo)
        if _void:
            print("\nNessuna repository contenente il linguaggio '{}'".format(lang))

    # REPOSITORIES
    def restore_repositories(self):
        self.repositories.clear()
        for repo in self.git_user.get_user().get_repos():
            self.repositories.append(repo.name)

    def print_repositories(self):
        self.repositories.clear()
        print("\n* Repositories *\n")
        # fetchs all repositories on the account:
        for repo in self.git_user.get_user().get_repos():
            self.repositories.append(repo.name)
            print("\t- " + repo.name)


class On_Repo():
    def __init__(self, working_repo):
        self.work_on_repo_functions = {"referres" : "Get the top 10 referrers over the last 14 days", "dir": "Return all the files in the repository", "create": "create [path-file-to-up] [name-file-in-server] [commit] [branch], create a file on the server, autocommitted", "branch": "list all branches", "commit": "get date of the last commit","back": "return to main menu"}
        self.working_repo = working_repo
        self.repo_brach = []

    # WORK ON REPOS 
    def content_dir(self): # issue with no file repos
        try:
            contents = self.working_repo.get_contents("")
            print("\n* Content of the repo *")
            while len(contents) >= 1:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(self.working_repo.get_contents(file_content.path))
                else:
                    print("\t- " + file_content.path)
        except GithubException:
            print(colored("\n\t* Error occurred during reading contents *", 'red'))

    def get_referres(self):
        contents = self.working_repo.get_top_referrers()
        _void = True
        print("\n* Referres *")
        for ref in contents:
            _void = False
            print("\t- " + str(ref))
        if _void:
            print("\nNessun refer nella repo corrente")

    def create_file(self, file_to_up, path_to_up, commit, branch):
        try:
            file_to_up = open(file_to_up, "rb") # opening for [r]eading as [b]inary
            data = file_to_up.read(-1) # if you only wanted to read 512 bytes, do .read(512)
            file_to_up.close()
        except OSError:
            print(colored("\n\t* Error occurred during Open '{}' file *".format(file_to_up), 'red'))

        try:
            self.working_repo.create_file(path_to_up, commit, data, branch)
            print(colored("\n\t* success *", 'green'))
        except GithubException:
            print(colored("\n\t* Error occurred during send file *", 'red'))

    # BRANCH
    def init_branch(self):
        self.repo_brach.clear()
        print(self.repo_brach)   
        for branch in self.working_repo.get_branches():
            self.repo_brach.append(branch.name)

    def check_brach(self, to_check):
        if len(self.repo_brach) == 0:
            self.init_branch()     
        return to_check in self.repo_brach

    def print_branches(self):
        print("\n* Branches *\n")
        for branch in self.repo_brach:
            print("\t- " + branch)

    # COMMIT
    def get_last_commit(self):
        commit = self.working_repo.get_commit(sha = 'sha')
        print("\n* Last Commit *\n")
        print("\t- " + commit.commit.author.date)
        