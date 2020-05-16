# Git Wrapper

The Simple Python Git Wrapper

This library is a simple git wrapper which let you perform many operations on any git repository in a powerful and simple way.

### Requirements

This library has been tested python >= 3.7, 3.8 and you need to have installed Git > 2.22.0

### Getting Started

The library is pretty simple, you only need to indicate where your repository is or create a new one.

```
from python_git_wrapper import Repository

repository = Repository('.') # Path of your git repository. It could be relative to your project or absolute
```

Or if the repository doesn't exist yet

```
repository = Repository('.', create=True)
```

Adding files:

```
repository.add_files('path to any file')
```

Committing changes:

```
repository.commit('commit message')
```

Finally, pushing them:

```
repository.push()
```

### Components

The library is divided in 3 main components.

- **Git Service**: Object which contains all the data to communicate with the git process properly.
    - NOTE: If you don't have configured the path of the git binary in your path. Execute the next command: `GitService.singleton('git path'')`

- **Repository**: It will be your entry point, which you will interact to provide an retrieve all the information. It is a reference to the repository you want to work on.

- **Git Elements**:

    - **Commit**: Containing all the relevant information about any commit

    - **Branch**: Contains the name of the branch

    - **Status**: Object which structure all the changes in your working directory

### API Overview

Small overview about the capabilities of this library. All this methods and attributes are accesible by the repository object.

| Method  | Description  | Return |
|---|---|---|
| build  | Create or init a new git repository | Repository |
| commit  | Commit the staged changes  | Status |
| status  | Retrieve the Status of the Working Directory | Status |
| push  | Push Changes to remote repository | Status |
| pull  | Pull changes to remote repository | Status |
| checkout  | Change HEAD reference | Status |
| create_branch | Create a new branch, go there if necessary  | Branch  |
| merge_branches  | Merge two branches. Support different merge modes  | Branch  |
| add_remote | Add a new remote repository | Status |
| remove_remote |  Remove a remote repository | Status  |
| execute  | execute any git command in the repository | str |
| revert_last_commit  | Generate a new commit reverting the previous one  | Commit |
| change_last_commit_message  | Rewrite the previous commit message  | Commit |
| get_commit_by_position  | Retrieve Commit by position in the current branch  |  Commit |
| get_branches_by_commit  | Retrieve all the branches which contain one specific commit | Commit  |


| Property  | Description  | Return |
|---|---|---|
| branches  | List of your local branches  | List[Branch] |
| current_branch  | The branch where it is currently the repository  | Branch |
| remote  | List of your remote repository names  | List[str] |
| last_commit  | The last commit in your repository  | Commit |

Detailed API Specification [Here](https://github.com/juanbenitopr/git-wrapper/blob/master/docs/API.md).