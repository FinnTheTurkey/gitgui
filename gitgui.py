#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
from git import Repo
import git, os, time, copy
import socket

def getall(diree):
                el = []
                l = os.listdir(diree)
                for i in l:
                    if os.path.isdir(os.path.join(diree,i)):
                        el.extend(getall(os.path.join(diree,i)))
                    else:
                        el.append(os.path.join(diree,i))
                return el;
class RevisionRecovery(object):
    def __init__(self,repo,main):
        self.repo = repo
        if not self.repo:
            messagebox.showerror("No Repository selected!","No Repository Selected! Click the button below the status button to select one!")

        else:
            self.main = main
            self.root = tk.Toplevel()
            self.selection = None
            s = ttk.Style(self.root)
            s.theme_use('clam')
            self.root.title("View Revisions")
            self.revs = tk.Listbox(self.root,width=25,height=25)
            self.revs.grid(row=0,column=0,rowspan=1)
            self.message = tk.Text(self.root,width=30,height=25)
            self.message.grid(row=0,column=1,columnspan=1)
            tk.Button(self.root,text="Restore!", command=self.restore).grid(row=1,column=0,columnspan=2)
            head = self.repo.head            # the head points to the active branch/ref
            master = head.reference     # retrieve the reference the head points to
            index = self.repo.index

            self.rev = master.log()
            l = []
            for i in self.rev:
                self.revs.insert(0,time.asctime(time.localtime(i.time[0])))

            self.revs.bind("<Double-Button-1>", self.onselect)

    def onselect(self,event):
        i = self.revs.curselection()[0]
        self.message.delete(0.0,'end')
        r = copy.deepcopy(self.rev)
        r.reverse()
        self.selection = r[i]
        self.message.insert('end',str(self.selection.message).replace(';;;','\n'))

    def restore(self):
        if (self.selection == None):
            messagebox.showerror("No Revisionn Selected","You have to select a revision to restore from")
            return
        if (messagebox.askokcancel("Resstore Revision?","Are you shure you want to restore this revision? It will wipe any non-committed revisions!")):
            
            #self.repo.git.checkout(self.selection.newhexsha) ## Worry about later
            a = simpledialog.askstring("Name of branch","Enter the name of the new branch")
            if a:
                a = a.replace(" ","_")
                self.repo.git.checkout(self.selection.newhexsha,b=a)
                self.main.abranch = a
                self.main.updateButton()
                
                
            self.root.destroy()
            
            
            

        

            
        

        
class BranchUi(object):
    def __init__(self,repo,main):
       
        self.repo = repo
        if not self.repo:
            messagebox.showerror("No Repository selected!","No Repository Selected! Click the button below the status button to select one!")
        else:    
        
            self.main = main
            self.root = tk.Toplevel()
            self.bran = tk.Listbox(self.root)
            self.bran.grid(row=0,column=0,columnspan = 4
                           )
            tk.Button(self.root,text="New Branch", command=self.new).grid(row=1,column=0)
            tk.Button(self.root,text="Remove Branch", command=self.removeBranch).grid(row=1,column=1)
            
            tk.Button(self.root,text="Set Active Branch", command=self.setbranch).grid(row=2,column=0,columnspan=2)
            tk.Button(self.root,text="Replace Branch", command=self.merge).grid(row=3,column=0)
            tk.Button(self.root,text="Merge Branch", command=self.realmerge).grid(row=3,column=1)
            
            self.updateBranch()

    def new(self):
        a = simpledialog.askstring("Name of branch","Enter the name of the new branch")
        if a:
            a = a.replace(" ","_")
            self.repo.git.branch(a)
            self.updateBranch()

    def setbranch(self):
        sel = self.branches[self.bran.curselection()[0]]
        if not sel.startswith("* "):
            sel = sel[2:len(sel)]
            try:
                self.repo.git.checkout(sel)
            except:
                messagebox.showerror("Error","You MUST commit before switching branches.")
            self.updateBranch()

    def removeBranch(self):
        sel = self.branches[self.bran.curselection()[0]]
        if not sel.startswith("* "):
            if messagebox.askokcancel("Are you sure?","Once a branch is deleted, you cannot get it back"):
                
                sel = sel[2:len(sel)]
                self.repo.git.branch("-D",sel)
                self.repo.git.fetch("--all","--prune")
                self.updateBranch()
        else:
            messagebox.showerror("Cannot","You can't delete the active branch!")

    def merge(self):
        sel = self.branches[self.bran.curselection()[0]]
        if not sel.startswith("* "):
            if messagebox.askokcancel("Are you sure?","Are you sure you want to merge this branch with the active branch? (this branch will NOT be removed)"):
                sel = sel[2:len(sel)]
                old = self.main.abranch
                self.repo.git.checkout(sel)
                self.repo.git.merge(old,s="ours")
                self.repo.git.checkout(old)
                self.repo.git.merge(sel)
                self.repo.git.fetch("--all","--prune")
                self.updateBranch()
        else:
            messagebox.showerror("Cannot","You can't merge the active branch with the active branch!")

    def realmerge(self):
        sel = self.branches[self.bran.curselection()[0]]
        if not sel.startswith("* "):
            if messagebox.askokcancel("Are you sure?","Are you sure you want to merge this branch with the active branch? (this branch will NOT be removed)"):
                sel = sel[2:len(sel)]
                old = self.main.abranch
                
                self.repo.git.merge(sel)
                self.repo.git.fetch("--all","--prune")
                
                
                self.updateBranch()
                
        else:
            messagebox.showerror("Cannot","You can't merge the active branch with the active branch!")

            

    def updateBranch(self):
        self.bran.delete(0,'end')
        b = self.repo.git.branch()
        branches = b.split('\n')
        self.branches = branches
        for e, i in enumerate(branches):
            
            self.bran.insert('end',i)
            if (i.startswith('* ')):
                self.bran.select_set(e)
                self.main.abranch = i.replace("* ",'')
                self.main.updateButton()
                

        
        

        
        


    
class GitGui(object):
    def __init__(self):

        if not os.path.exists(os.path.join(os.path.expanduser("~"),".gitgui")):
            os.mkdir(os.path.join(os.path.expanduser("~"),".gitgui"))
            f = open(os.path.join(os.path.expanduser("~"),".gitgui","lastused.txt"),'w')
            f.write("")
            f.flush()
            f.close()
            f = open(os.path.join(os.path.expanduser("~"),".gitgui","verformat.txt"),'w')
            f.write("Revision {!}")
            f.flush()
            f.close()

        f = open(os.path.join(os.path.expanduser("~"),".gitgui","lastused.txt"),'r')
        r= f.read()
        f.close()

        f = open(os.path.join(os.path.expanduser("~"),".gitgui","verformat.txt"),'r')
        self.verinfo= f.read()
        f.close()
        
        
        self.gitdir = None
        self.gitrepo = None
        self.repo = None
        
        self.root = tk.Tk()
        self.root.title("GitGui")
        s = ttk.Style()
        s.theme_use('clam')
        ttk.Button(self.root,text="Commit", command=self.commit).grid(row=0,column=0)
        
        ttk.Button(self.root,text="Display Modified Files", command=self.status).grid(row=0,column=2)
        self.dir = ttk.Button(self.root,text="[No Repository Selected] Click here to select one!",command=self.selectPath)
        self.dir.grid(row=1,column=0,columnspan=3)
        self.message = tk.Text()
        
        self.message.grid(row=2,column=0,columnspan=3)
        
        ttk.Button(self.root,text="See past revisions",command=lambda:RevisionRecovery(self.repo,self)).grid(row=3,column=0,columnspan=1)
        ttk.Button(self.root,text="Connect Remote", command=self.remotecon).grid(row=3,column=2,columnspan=1)

        ttk.Button(self.root,text="Branches",command=lambda:BranchUi(self.repo,self)).grid(row=3,column=1)

        ttk.Button(self.root,text="Send Branch To Server",command=self.push).grid(row=4,column=2)
        ttk.Button(self.root,text="Get Branch From Server",command=self.pull).grid(row=4,column=0)
        ttk.Button(self.root,text="Set Version Format",command=self.setVersionFormat).grid(row=4,column=1)

        self.abranch = None

        if (os.path.exists(r)):
            self.setPath(r)
            

                                                         
        else:
            self.ft = True
                        


        
        self.root.mainloop()

    def genorateVerFormat(self):
        
        v = copy.deepcopy(self.verinfo)
        allbranches = []
        b = self.repo.git.branch()
        branches = b.split('\n')
        d = {}
        heads = self.repo.heads
        for e, i in enumerate(branches):
            
            
            if (i.startswith('* ')):
                allbranches.append(i.replace("* ",'')
                                   )
                a = i.replace("* ",'')
            else:
                allbranches.append(i.replace(" ",'')
                                   )
                a = i.replace(" ",'')

            h = heads[a]
            d[a] = len(h.log())

        head = self.repo.head            # the head points to the active branch/ref
        master = head.reference     # retrieve the reference the head points to
        index = self.repo.index
        d['!'] = len(master.log())
        d['!!'] = master.name
        v = time.strftime(v)
        for i in d:
            v = v.replace('{'+i+'}',str(d[i]))

        return v
        

            

    def remotecon(self):
        if not self.repo:
            messagebox.showerror("No Repository selected!","No Repository Selected! Click the button below the status button to select one!")
            return
        pl = simpledialog.askstring("Connect","Enter URL to connect to this git repo")
        if pl:
            self.repo.git.remote("add","origin",pl)
    def push(self):
        if not self.repo:           
            messagebox.showerror("No Repository selected!","No Repository Selected! Click the button below the status button to select one!")
            return
        self.repo.git.push("-u","origin",self.abranch)

    def pull(self):
        if not self.repo:
            messagebox.showerror("No Repository selected!","No Repository Selected! Click the button below the status button to select one!")
            return
        
        self.repo.git.pull("origin",self.abranch)
        
    def updateButton(self):
        head = self.repo.head            # the head points to the active branch/ref
        master = head.reference     # retrieve the reference the head points to
        index = self.repo.index
        self.dir.config(text="["+self.gitdir+":Branch %s] Revision #%i" % (self.abranch,len(master.log())))
        self.message.delete(0.0,'end')
        self.message.insert('end',self.genorateVerFormat())

    def commit(self):
        if not self.repo:
            messagebox.showerror("No Repository selected!","No Repository Selected! Click the button below the status button to select one!")
            return
        head = self.repo.head            # the head points to the active branch/ref
        master = head.reference     # retrieve the reference the head points to
        index = self.repo.index

        
        
        if not self.repo.untracked_files and not self.repo.index.diff(None):
            messagebox.showerror("No files edited","No files have been changed or added in this repository since the last commit")
            return
        txt = '\nNew Files: \n-----------------\n'
        
        txt += ' \n '.join(self.repo.untracked_files)
        txt += "\nModified Files: \n-----------------\n"
        l = []
        for i in self.repo.index.diff(None):
            
            l.append(i.a_path)
        txt += ' \n '.join(l)

        
        
        f = open(os.path.join(self.gitdir,"VERSION.txt"),'w')
        f.write(self.genorateVerFormat())
        f.flush()
        f.close()

        
        
        for i in self.repo.untracked_files:
            
            index.add([i])

        for i in self.repo.index.diff(None):
            if (os.path.exists(os.path.join(self.gitdir,i.a_path))):
                index.add([i.a_path])
            else:
                self.repo.git.rm(i.a_path)
        a = self.message.get(0.0,'end')+txt

        a = a.replace('\n',';;;')
        index.commit(a)
        self.updateButton()
        self.message.delete(0.0,'end')
        self.message.insert('end',self.genorateVerFormat())

    def status(self):
        if not self.repo:
            messagebox.showerror("No Repository selected!","No Repository Selected! Click the button below the status button to select one!")
            return
        txt = 'New Files: \n-----------------\n'
        head = self.repo.head            # the head points to the active branch/ref
        master = head.reference     # retrieve the reference the head points to
        index = self.repo.index
        txt += ' \n '.join(self.repo.untracked_files)
        txt += "\nModified Files: \n-----------------\n"
        l = []
        for i in self.repo.index.diff(None):
            
            l.append(i.a_path)
        txt += ' \n '.join(l)
        messagebox.showinfo("Status:",txt)
        
        

    def selectPath(self):
        dire = filedialog.askdirectory(initialdir=os.path.expanduser("~"))
        if dire:
            
            self.setPath(dire)
            user = simpledialog.askstring("Config info","What is your username?")
            email = simpledialog.askstring("Config info","What is your email address?")
            self.repo.git.config("--global","user.name",user)
            self.repo.git.config("--global","user.email",email)

    def setPath(self,dire):
            
            self.gitdir = dire
            if os.path.exists(os.path.join(dire,'.git')):
                 
                

                # rorepo is a Repo instance pointing to the git-python repository.
                # For all you know, the first argument to Repo is a path to the repository
                # you want to work with
                repo = Repo(self.gitdir)
                
                
                assert not repo.bare
            else:
                repo = Repo.init(dire)
                filename = os.path.join(dire,'README.md')
                open(filename, 'wb').close()
                repo.index.add([filename])
                repo.index.commit("Adding "+filename+ "to repo")
                repo.create_head('master')

            self.repo = repo
            index = self.repo.index
            head = self.repo.head            # the head points to the active branch/ref
            master = head.reference     # retrieve the reference the head points to
            
                

            self.dir.config(text="["+dire+"] Revision #%i" % len(master.log()))
            self.message.delete(0.0,'end')
            self.message.insert('end',self.genorateVerFormat())

            f = open(os.path.join(os.path.expanduser("~"),".gitgui","lastused.txt"),'w')
            f.write(dire)
            f.flush()
            f.close()

            b = self.repo.git.branch()
            branches = b.split('\n')
            self.branches = branches
            for e, i in enumerate(branches):
                
                if (i.startswith('* ')):
                    
                    self.abranch = i.replace("* ",'')
                    self.updateButton()


    def setVersionFormat(self):
        r = simpledialog.askstring("Enter format to show version","""You can use {branchname} to add the branch revision number, or {!} to add current branch revision number,or {!!} to add the current branch name, and date and time (%Y, %m, etc...)""")
        if r:
            self.verinfo = r
            f = open(os.path.join(os.path.expanduser("~"),".gitgui","verformat.txt"),'w')
            f.write(self.verinfo)
            f.flush()
            f.close()
            self.message.delete(0.0,'end')
            self.message.insert('end',self.genorateVerFormat())

            
            
            
            

                    
        
        
        

if __name__ == '__main__':
   
    GitGui()
