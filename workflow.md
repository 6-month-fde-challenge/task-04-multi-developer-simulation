# workflow.md - the exact command sequence used for this task

Every command below was really run, in this order, on Windows (Git Bash) against the
repository <https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation>.
The output blocks are the real captured output, not illustrations.

Two working copies exist on disk, which is the whole point of the exercise:

| Role | Folder | Git identity |
|---|---|---|
| Developer A (repo owner) | `03_git_and_git_hub/task-04-multi-developer-simulation` | `Developer A (veerandra7) <veerandra.data@gmail.com>` |
| Developer B (contributor) | `03_git_and_git_hub/task-04-devB-clone` | `Developer B <developer-b@example.com>` |

---

## Part 1 - Developer A creates the repository

### 1. Create the local repository

```bash
mkdir task-04-multi-developer-simulation
cd task-04-multi-developer-simulation
git init -b main
```

*Why:* `git init` turns a plain folder into a git repository. `-b main` names the first
branch `main` immediately, so the default branch never has to be renamed later.

```
Initialized empty Git repository in .../task-04-multi-developer-simulation/.git/
```

### 2. Set Developer A's identity

```bash
git config user.name "Developer A (veerandra7)"
git config user.email "veerandra.data@gmail.com"
```

*Why:* git stamps every commit with the name and email configured **in that working
copy**. Setting it per-repository is what makes the two simulated developers show up as
two distinct authors in `git log`.

```
Developer A (veerandra7)
veerandra.data@gmail.com
```

### 3. Commit the baseline in four logical commits

```bash
git add .gitignore .env.example config.py
git commit -m "Add project scaffolding with gitignore and environment-based configuration"

git add login.py profile.py input_variables.py
git commit -m "Add login, profile and numeric input collection modules"

git add addition_module.py subtract_module.py multiply_module.py division_module.py
git commit -m "Add the four arithmetic modules guarded by API key and profile checks"

git add calculator.py dashboard.py
git commit -m "Add calculator orchestrator and dashboard presentation layer"
```

*Why:* `git add` stages a chosen set of files and `git commit` records them as one
reviewable unit. Splitting the baseline into four commits by responsibility means the
history explains itself and any single layer can be reverted on its own.

```
a93b747 (HEAD -> main) Add calculator orchestrator and dashboard presentation layer
180210e Add the four arithmetic modules guarded by API key and profile checks
ab007de Add login, profile and numeric input collection modules
90e6154 Add project scaffolding with gitignore and environment-based configuration
```

### 4. Create the remote repository on GitHub and push

```bash
gh repo create 6-month-fde-challenge/task-04-multi-developer-simulation --public \
  -d "Task 4 - Multi-developer GitHub simulation: Developer A creates the repo, Developer B clones it, branches, pushes and opens a Pull Request that is reviewed and merged into main." \
  --source=. --remote=origin --push
```

*Why:* this one command creates the **remote repository** on GitHub, registers it
locally under the name `origin`, and **pushes** `main` to it. Without a remote there is
nothing for a second developer to clone.

```
https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation
To https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git
 * [new branch]      HEAD -> main
branch 'main' set up to track 'origin/main'.
```

### 5. Confirm the remote is registered and `main` is the default branch

```bash
git remote -v
gh repo view 6-month-fde-challenge/task-04-multi-developer-simulation --json defaultBranchRef,url,isPrivate
```

*Why:* `git remote -v` proves the local repository knows where to fetch from and push to.
The `gh repo view` check confirms GitHub itself treats `main` as the default branch, so a
clone lands on `main` and a Pull Request targets `main`.

```
origin  https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git (fetch)
origin  https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git (push)

{"defaultBranchRef":{"name":"main"},"isPrivate":false,"url":"https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation"}
```

---

## Part 2 - Developer B clones and builds a feature

### 6. Clone the remote repository into a separate folder

```bash
cd C:/Users/asus/Desktop/work/6-month-fde-challenge/03_git_and_git_hub
git clone https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git task-04-devB-clone
```

*Why:* `git clone` downloads the entire repository **including its full history**, checks
out the default branch, and automatically configures the `origin` remote. This is how a
second developer gets a copy to work in without touching Developer A's folder.

```
Cloning into 'task-04-devB-clone'...
remote: Enumerating objects: 20, done.
remote: Counting objects: 100% (20/20), done.
remote: Compressing objects: 100% (14/14), done.
remote: Total 20 (delta 6), reused 20 (delta 6), pack-reused 0 (from 0)
Receiving objects: 100% (20/20), done.
Resolving deltas: 100% (6/6), done.
```

### 7. Set Developer B's identity in the clone

```bash
cd task-04-devB-clone
git config user.name "Developer B"
git config user.email "developer-b@example.com"
```

*Why:* the clone inherits no author identity from Developer A's folder, so setting it
here makes every commit Developer B creates visibly authored by a different person.

```
Developer B
developer-b@example.com
```

### 8. Inspect the remote the clone was given

```bash
git remote -v
```

*Why:* the clone did not need `git remote add` - cloning wired `origin` up automatically.
This proves the link back to the shared repository exists.

```
origin  https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git (fetch)
origin  https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git (push)
```

### 9. Fetch, then pull, before starting work

```bash
git fetch origin --verbose
git pull origin main
```

*Why:* `git fetch` downloads new commits from the remote and updates the `origin/*`
tracking branches, but **does not touch your working files** - it is the safe
"what has changed?" command. `git pull` is `fetch` followed by a merge into the current
branch, so it actually moves your working copy forward. Running both before branching
guarantees the feature starts from the newest `main`.

```
POST git-upload-pack (224 bytes)
From https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation
 = [up to date]      main       -> origin/main

From https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation
 * branch            main       -> FETCH_HEAD
Already up to date.
```

(`Already up to date` is the correct result here: the clone was seconds old.)

### 10. List every branch, local and remote

```bash
git branch -a
```

*Why:* `-a` shows remote-tracking branches too, so you can see what exists on the server
before creating anything.

```
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```

### 11. Create the feature branch

```bash
git switch -c feature-power-module
```

*Why:* a branch is an isolated line of development. Building the feature here means
`main` stays releasable while the work is in progress, and it gives the Pull Request
something to compare against.

```
Switched to a new branch 'feature-power-module'
```

### 12. Implement the feature

Added `power_module.py` (a `power(a, b)` function using the same `api_key` /
`profile_name` guard pattern as the other four operations) and wired it into
`calculator.py` and `dashboard.py`.

```bash
git status --short
```

```
 M calculator.py
 M dashboard.py
?? power_module.py
```

Verified before committing:

```bash
python dashboard.py < /dev/null
```

```
*************** DASHBOARD ***************
Result of addition is       :  15
Result of subtraction is    :  5
Result of multiplication is :  50
Result of division is       :  2.0
Result of power is          :  100000
*****************************************
```

### 13. Commit the feature as Developer B

```bash
git add power_module.py calculator.py dashboard.py
git commit -m "Add power module and expose the result on the dashboard"
```

*Why:* the commit is the unit the reviewer will read. Naming the three files explicitly
(rather than `git add .`) keeps unrelated junk such as `__pycache__` out.

```
[feature-power-module 7cc6a4e] Add power module and expose the result on the dashboard
 3 files changed, 19 insertions(+), 1 deletion(-)
 create mode 100644 power_module.py
```

### 14. Push the feature branch to the remote

```bash
git push -u origin feature-power-module
```

*Why:* `git push` uploads the local branch to GitHub so other people can see it. `-u`
sets `origin/feature-power-module` as the upstream, so later `git push` / `git pull` need
no arguments. A Pull Request cannot be opened until the branch exists on the remote.

```
remote:
remote: Create a pull request for 'feature-power-module' on GitHub by visiting:
remote:      https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/new/feature-power-module
remote:
To https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git
 * [new branch]      feature-power-module -> feature-power-module
branch 'feature-power-module' set up to track 'origin/feature-power-module'.
```

### 15. Open the Pull Request

```bash
gh pr create --repo 6-month-fde-challenge/task-04-multi-developer-simulation \
  --base main --head feature-power-module \
  --title "Add power module to the calculator" \
  --body-file pr_body.md
```

*Why:* a Pull Request formally proposes merging `feature-power-module` into `main` and
opens a place to discuss the change before it lands. `--base` is the branch being merged
into, `--head` is the branch carrying the work. The full PR body is reproduced in
`PULL_REQUEST.md`.

```
https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1
```

---

## Part 3 - Developer A reviews and merges

### 16. Attempt a formal approval

```bash
gh pr review 1 --repo 6-month-fde-challenge/task-04-multi-developer-simulation \
  --approve --body "Reviewed by Developer A. ..."
```

*Why:* `--approve` is the normal way to record a green "Approved" review. It is reported
honestly here that **GitHub refused it**, because both simulated developers necessarily
act through the same GitHub account and GitHub does not allow approving your own Pull
Request:

```
failed to create review: GraphQL: Review Can not approve your own pull request (addPullRequestReview)
```

### 17. Record the review as a formal review comment instead

```bash
gh pr review 1 --repo 6-month-fde-challenge/task-04-multi-developer-simulation \
  --comment --body-file review_body.md

gh pr comment 1 --repo 6-month-fde-challenge/task-04-multi-developer-simulation \
  --body-file review_body.md
```

*Why:* GitHub does allow a `COMMENT`-type review on your own PR, so the review is a real
review event in the PR's Reviews section, and the same text is also posted in the
conversation thread. The full review text is in `PULL_REQUEST.md`.

```bash
gh api repos/6-month-fde-challenge/task-04-multi-developer-simulation/pulls/1/reviews \
  --jq '.[] | "state=\(.state) by=\(.user.login)"'
```

```
state=COMMENTED by=veerandra7
https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1#issuecomment-5760838331
```

### 18. Merge the Pull Request into `main`

```bash
gh pr merge 1 --repo 6-month-fde-challenge/task-04-multi-developer-simulation --merge \
  --subject "Merge pull request #1 from 6-month-fde-challenge/feature-power-module" \
  --body "Add power module to the calculator (reviewed by Developer A)"
```

*Why:* `--merge` creates a true **merge commit** with two parents, so the history keeps
the shape of the branch instead of flattening it (which `--squash` or `--rebase` would
do). The branch was deliberately **not** deleted, so it remains visible as evidence of
the branch workflow.

```bash
gh pr view 1 --repo 6-month-fde-challenge/task-04-multi-developer-simulation \
  --json number,title,state,mergedAt,mergeCommit,headRefName,baseRefName
```

```
{"baseRefName":"main","headRefName":"feature-power-module",
 "mergeCommit":{"oid":"239a281139910882b3bf30baea5f14c445fb9c17"},
 "mergedAt":"2026-09-21T12:56:59Z","number":1,"state":"MERGED",
 "title":"Add power module to the calculator"}
```

### 19. Developer A pulls the merged work back down

```bash
cd ../task-04-multi-developer-simulation
git pull origin main
```

*Why:* the merge happened on GitHub, so Developer A's local `main` was behind. `git pull`
brings Developer B's work into Developer A's working copy - this is the moment the two
developers' histories actually converge on one machine.

```
From https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation
 * branch            main       -> FETCH_HEAD
   a93b747..239a281  main       -> origin/main
Updating a93b747..239a281
Fast-forward
 calculator.py   |  3 +++
 dashboard.py    |  3 ++-
 power_module.py | 14 ++++++++++++++
 3 files changed, 19 insertions(+), 1 deletion(-)
 create mode 100644 power_module.py
```

### 20. Confirm two distinct authors are in the history

```bash
git log --format='%h %an <%ae> %s'
```

```
239a281 POTNURU VENKATA ATCHUTA SAI VEERANDRA KUMAR <74710089+veerandra7@users.noreply.github.com> Merge pull request #1 from 6-month-fde-challenge/feature-power-module
7cc6a4e Developer B <developer-b@example.com> Add power module and expose the result on the dashboard
a93b747 Developer A (veerandra7) <veerandra.data@gmail.com> Add calculator orchestrator and dashboard presentation layer
180210e Developer A (veerandra7) <veerandra.data@gmail.com> Add the four arithmetic modules guarded by API key and profile checks
ab007de Developer A (veerandra7) <veerandra.data@gmail.com> Add login, profile and numeric input collection modules
90e6154 Developer A (veerandra7) <veerandra.data@gmail.com> Add project scaffolding with gitignore and environment-based configuration
```

### 21. Fetch everything and print the final history graph

```bash
git fetch --all
git log --graph --oneline --all --decorate
```

*Why:* `--all` includes the feature branch, and `--graph` draws the branch-and-merge
shape, which is the clearest single proof that the branch workflow really happened.

```
*   239a281 (HEAD -> main, origin/main, origin/HEAD) Merge pull request #1 from 6-month-fde-challenge/feature-power-module
|\
| * 7cc6a4e (origin/feature-power-module) Add power module and expose the result on the dashboard
|/
* a93b747 Add calculator orchestrator and dashboard presentation layer
* 180210e Add the four arithmetic modules guarded by API key and profile checks
* ab007de Add login, profile and numeric input collection modules
* 90e6154 Add project scaffolding with gitignore and environment-based configuration
```

---

## Command index (quick reference)

| Concept | Command used here |
|---|---|
| Create repository | `git init -b main` |
| Set identity | `git config user.name` / `git config user.email` |
| Stage and commit | `git add <files>` / `git commit -m "..."` |
| Create remote + push | `gh repo create ... --source=. --remote=origin --push` |
| Inspect remote | `git remote -v` |
| **Clone** | `git clone <url> task-04-devB-clone` |
| **Fetch** | `git fetch origin --verbose` / `git fetch --all` |
| **Pull** | `git pull origin main` |
| List branches | `git branch -a` |
| **Branch** | `git switch -c feature-power-module` |
| **Push** | `git push -u origin feature-power-module` |
| **Pull Request** | `gh pr create --base main --head feature-power-module ...` |
| **Code review** | `gh pr review 1 --comment --body-file ...` / `gh pr comment 1 ...` |
| **Merge** | `gh pr merge 1 --merge` |
| Verify merge | `gh pr view 1 --json state,mergeCommit` / `gh pr list --state all` |
| History evidence | `git log --graph --oneline --all --decorate` |
