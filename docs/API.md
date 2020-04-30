
API
-----

Detailed specification of the methods available from the repository object.

`def __init__(self, path: str):`

**path**: str
    Relative or absolute path to your repository. **Mandatory**

----
```
@classmethod
 def build(cls, path: str = '.', create_repository: bool = False, create_project: bool = False): -> Repository
```
Class-method to create a new repository from zero, it helps when you need to init a new repository or create a new whole git project

**path**: str
    Relative or absolute path to your repository. **Mandatory**

**create_repository**: boolean
    This argument will init a git repository in the path. **Optional** Default to Fals

**create_project**: boolean
    In case you need a git project from zero, it will create a new folder with the git repository inside. **Optional** Default to False

**Returns** -> Repository

----
`def commit(self, message: str, add_files: bool = False) -> Status`
Commit the files staged in your staging area. You can optionaly add all the files tracked in your repository

**message**: str
    Message used to describe the commit changes. **Mandatory**
**add_files**: boolean
    It indicate if you want to add all the files modified and tracked in your repository. **Optional** Default to False

**Returns** -> Status

`def status(self) -> Status`
Retrieve the current status of your repository.

**Returns** -> Status

---
`def push(self, remote_name: str = 'origin', force: bool = False, remote_branch: str = None, local_branch: str = None) -> Status`
Push the changes to your remote repository.


**remote_name**: str
    Name of the remote repository where you want to push the changes. **Mandatory**

**force**: boolean
    Forcing pushing the changes. **Optional** Default to False

**remote_branch**: str
    Remote branch destination of the changes. **Optional** Default to upstream branch
    
**local_branch**: str
    Local branch source of your changes. If you don't specify it will use your current branch. **Optional** Default Current Branch

**Returns** -> Status

---
`def pull(self, remote_name: str = 'origin', force: bool = False, remote_branch: str = None, local_branch: str = None) -> Status`

Pull the changes to your remote repository.

**remote_name**: str
    Name of the remote repository where you want to push the changes. **Mandatory**

**force**: boolean
    Forcing pulling the changes. **Optional** Default to False

**remote_branch**: str
    Remote branch source of the changes. **Optional** Default to upstream branch

**local_branch**: str
    Local branch destination of your changes. If you don't specify it will use your current branch. **Optional** Default current branch

**Returns** -> Status

---
`def checkout(self, destination: str) -> Status`

Change your HEAD reference to another pointer. The pointer must exist

 **destination**: str
    Name of the destionation pointer, it could be branch name, commit hash, and so on. **Mandatory**

**Returns** -> Status

---
`def create_branch(self, name: str, move_to: bool = False) -> Branch`

Create a new branch


**name**: str
    Name of your new branch. **Mandatory**

**move_to**: boolean
    Flag to specify if you want to go to the new branch. **Optional** Default False

**Returns** -> Status

---
`def merge_branches((self, branch_origin: Branch, branch: Branch, squash=False, new_commit=False) -> Branch`

Merge one branch into another one. **TAKE CARE** This library doesn't support confflict resolution. the status structure would provide troubles in that situation, if your project is prune to conflicts don't use it.

**branch_origin**: str
    Base branch to the merge. **Mandatory**

**branch**: boolean
    Branch conbined to the base branch. **Mandatory**

**squash**: boolean
    Flag to indicate you want to merge using squash mode. **Optional** Default to False

**new_commit**: boolean
    Flag to indicate you want to create a new commit with the merge. **Optional** Default to False

**Returns** -> Branch

---
`def add_remote(self, url: str, name: str = 'origin') -> Status`

Add a new remote repository reference


**url**: str
    Url where the remote repository is located. **Mandatory**

**name**: str
    Name to your remote repository. **Optional** Default to origin

**Returns** -> Status

---
`def remove_remote(self, name: str = 'origin') -> Status`

Remove a remote repository referente


**name**: str
    Name of your remote repository. **Mandatory**

**Returns** -> Status

---
`def revert_last_commit(self) -> Commit`

Create a new commit reverting the last one

**Returns** -> Commit

---
`def change_last_commit_message(self, message: str) -> Commit`

Rewrite the previous commit with the new message specified.


**message**: str
    Message used to describe better the previous commit changes. **Mandatory**

**Returns** -> Commit

---
`* def get_commit_by_position(self, position: int) -> Commit`

Retrieve a commit by its position in the branch.

**position**: int
    Position of the commit you want to retrieve. **Mandatory**

**Returns** -> Commit

---
`* def get_branches_by_commit(self, commit: Commit) -> List[Branch]`

Retrieve all the branches which contain a specific commit

**commit**: Commit
    commit used to look the branches. **Mandatory**

**Returns** -> List[Branch]

---
`def execute(self, command: str, *args) -> str`

This method will execute any git command. In case the previous methods don't satisfy your current necesities.

**command**: str
    Git command to execute. **Mandatory**
**args**: boolean
    Additional parameters the git command will need. **Optional**

**Returns** -> str

---