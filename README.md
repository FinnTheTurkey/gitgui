Git Gui
========
GitGui is meant for a single programmer, working on a project, who wants very simple version control and branches.
GitGui features:
1. Very simple. Big commit button, easy branching
2. Supports sending to servers: you can send your repo to your server from GitGui. You may have to set up username/password yourself.(see Setup with Github)


Important
----------
GitGui does **nothing** about conflicts. So, if you think you will have a conflict in your code, be warned
Note that a conflict only occurs if a line has been changed and committed in both branches, after they seperated.


Intended use
--------------
With GitGui, the intention is simple. Your hobbie is to create a little project. You want some form of version control.
GitGui is ideal for you. It's simple, fast, and will do most simple actions well.
You easily override one branch with another, without dealing with all the merge stuff. If you want to deal with all the merge stuff, you can!
GitGui works with Github, so you can share your project with the world! (see Setup with Github)

Setup with Github!
-----------------------
To setup GitGui with Github, you first have to setup your git repo with your account:
First, make sure you have a repository.
Then, clone it where you want it. (with ``git clone {GITHUB LINK}`` from a terminal of gitbash)
Then, in that folder, run this command: (with a terminal, or gitbash)
``
git config remote.origin.url https://{USERNAME}:{PASSWORD}@github.com/{USERNAME}/{REPONAME}.git
``
Now, you can send or get that repository from github with the "Get Branch From Server" and "Send Branch To Server" buttons.

Executables
------------
Right now, I have only compiled it for the Raspberry Pi. I have it's executable in the repo.
You can compile it for anything with pyinstaller. If you compile it for another platform, tell me, and I will intergrate it into my repo.


** Hope you like it!**