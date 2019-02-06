from termcolor import colored
from menu import *
from server import *


if __name__ == "__main__":
    # init the global git_user variable
    git = On_Account()
    git.login()

    while True:

        while git.git_user is None:
            git.login()

        try:
            my_shell_input(git)
        except ConnectionError:
            print(colored("\n\t* Connection lost *", 'red'))
            my_press_enter()