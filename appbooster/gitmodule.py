#!/usr/bin/python

import sys

from git import *
from gitdb import *


def createRepo(repoAddress):
    repo = Repo.init(repoAddress, bare=True)
    return repo


def cloneRepo(fromUrl, toDir):
    Repo.clone_from(fromUrl, toDir)


def getRepo(repoAddress):
    repo = Repo(repoAddress)
    return repo


def repoCommit(repoAddress, message):
    repo = Repo(repoAddress)
    repo.git.status()
    repo.git.add('.')
    repo.git.commit(m=message)


def repoPull(repoAddress):
    repo = Repo(repoAddress)
    repo.git.fetch()
    repo.git.reset('--hard')


def repoPush(repoAddress):
    repo = Repo(repoAddress)
    repo.git.push()


def main(argv):
    import getopt

    repoAddress = ''
    repoCommit("/Users/chesthair/gitModule/git@github.com:abccb1/AlgoLib.git", "aaaa")
    try:
        opts, args = getopt.getopt(argv, "hc:i:o:", ["iRepo=", "ofile=", "cloneFrom=", "getRepo=", "cloneTo="])
    except getopt.GetoptError:
        print 'gitModle.py -h for help'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'gitModle.py -c <repoAddress>'
            print 'gitModle.py --clone <addressCloneTo>'
            sys.exit()
        elif opt in ("-i", "--iRepo"):
            repoAddress = arg
            repo = createRepo(repoAddress)
        elif opt in ("--cloneFrom"):
            fromUrl = arg
        elif opt in ("--cloneTo"):
            toUrl = arg
            Repo.clone_from(toUrl, fromUrl)
        elif opt in ("--getRepo"):
            repo = Repo(arg)
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            print 'Input file is "', repoAddress
            print 'Output file is "', outputfile
            repo = Repo(repo)
            assert not repo.bare


if __name__ == "__main__":
    main(sys.argv[1:])
