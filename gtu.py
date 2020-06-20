banner="""  ___  _ _____ _   _           _              _____   __  
  / _ \/ /__   \ |_| |__   __ _| |_ /\ /\  ___|___ /  /__\ 
 / /_\/| | / /\/ __| '_ \ / _` | __/ / \ \/ __| |_ \ / \// 
/ /_\\ | |/ /  | |_| | | | (_| | |_\ \_/ /\__ \___) / _  \ 
\____/ |_|\/    \__|_| |_|\__,_|\__|\___/ |___/____/\/ \_/ 
"""
print(banner)
import argparse
import getpass
import os
import subprocess
import sys

from github import *

def main(args):
    if not args.password:
        args.password = getpass.getpass("Password for {}: ".format(args.username))

    g = Github(args.username, args.password)
    check_login(g)

    if not os.path.exists(args.dest):
        os.makedirs(args.dest)

    os.chdir(args.dest)

    for user in g.search_users(args.target):
        for repo in user.get_repos():
            clone_repo(repo)


def check_login(github):
    try:
        github.get_user().login
        return
    except RateLimitExceededException as exception:
        print('Rate limit exceeded: {}'.format(exception))
    except BadCredentialsException as exception:
        print('Bad credentials: {}'.format(exception))
    except TwoFactorException as exception:
        print('Your account is configured with two factor auth: {}'.format(exception))

    exit()


def clone_repo(repo):
    if not os.path.exists(repo.name):
        subprocess.run(['git', 'clone', repo.clone_url], check=True)


def parse_args():
    parser = argparse.ArgumentParser(description='Download all of a user\'s '
                                                 'github repositories')
    parser.add_argument('-u', '--username', type=str, help='Your username')
    parser.add_argument('-p', '--password', type=str, help='Your password - '
                                        'if omitted, you will be prompted')
    parser.add_argument('-d', '--dest', type=str, help='Where to download the '
                                        'repositories to')
    parser.add_argument('-t', '--target', type=str, help='The user to download '
                                        'all repositories from. If ommitted, '
                                        'your username is used.')

    if len(sys.argv) <= 1:
        parser.print_help()
        exit()

    args = parser.parse_args()

    if not args.username:
        print("You must provide a username")
        exit()

    if not args.dest:
        args.dest = args.username if not args.target else args.target

    if not args.target:
        args.target = args.username

    return args

if __name__ == '__main__':
    main(parse_args())
