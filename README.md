# Lab


## Cloning on new Machine
```bash
git clone
cd lab
git submodule update --init --recursive
```


## Editing an Existing Project
```bash
cd <project>
git pull

# make changes
git add .
git commit
git push

# update pointer in lab
cd lab
git add language/project
git commit
git push
```

## Adding a new Project
```bash
cd lab
git submodule add <repo> <language/repo-name>
git add .gitmodules language/repo-name
git commit 
git push
```

OR

```bash
# Create new Repo on GH
cd lab
git submodule add -b main <new_repo> <language/repo-name>

# add stuff to new submodule and push

# update super project pointer
cd lab
git add <language/repo>
git commit
git push
```
