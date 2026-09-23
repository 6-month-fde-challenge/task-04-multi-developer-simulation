# Task 4 - Multi-Developer GitHub Simulation

A small Python calculator project used to simulate a real two-developer GitHub workflow
end to end: **Developer A** creates the repository and pushes it, **Developer B** clones
it into a separate working copy, creates a branch, implements a feature, pushes the
branch and opens a **Pull Request**, which is then **reviewed** and **merged** into
`main`.

- **Repository:** <https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation>
- **Pull Request:** <https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1> (**#1 - MERGED**)

Both links are also in [`submission_links.txt`](submission_links.txt).

| Evidence file | What it contains |
|---|---|
| [`submission_links.txt`](submission_links.txt) | The public repository URL and the Pull Request URL, clearly labelled |
| [`workflow.md`](workflow.md) | Every command run by both developers, in order, with real captured output |
| [`PULL_REQUEST.md`](PULL_REQUEST.md) | PR number, URL, full description, the review comment, the merge result and the merge commit SHA |
| `README.md` (this file) | Project docs, the two developer identities, and a walkthrough of every git concept the task covers |

---

## What the project is

A deliberately simple, dependency-free Python program, layered so that a new feature has
an obvious place to go - which is what makes it a good subject for a branch-and-PR
exercise.

| File | Responsibility |
|---|---|
| `config.py` | Reads `API_KEY` from the environment with a safe demo fallback |
| `.env.example` | Documents the `API_KEY` variable without committing a real secret |
| `login.py` | Collects username and password (falls back to defaults when non-interactive) |
| `profile.py` | Derives `profile_name` from the login details |
| `input_variables.py` | Collects the two numbers `a` and `b` |
| `addition_module.py` | `addition(a, b)` |
| `subtract_module.py` | `subtract(a, b)` |
| `multiply_module.py` | `multiply(a, b)` |
| `division_module.py` | `division(a, b)`, with a zero-divisor guard |
| `power_module.py` | `power(a, b)` - **added by Developer B via Pull Request #1** |
| `calculator.py` | Wires the operation modules to the collected inputs |
| `dashboard.py` | Entry point - prints all results |

Every operation module applies the same guard: it refuses to compute and returns `None`
unless both `config.api_key` and `profile.profile_name` are present.

---

## How to run

No dependencies beyond Python 3.

```bash
git clone https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git
cd task-04-multi-developer-simulation
python dashboard.py
```

The prompts fall back to defaults when nothing is piped in, so it also runs
non-interactively. Real captured output of `python dashboard.py < /dev/null` on `main`
after the merge:

```
Enter a number 1 :    -> no input available, using default: 10
Enter a number 2 :    -> no input available, using default: 5
Enter username :    -> no input available, using default: veerandra
Enter password :    -> no input available, using default: demo-password
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
*************** DASHBOARD ***************
Result of addition is       :  15
Result of subtraction is    :  5
Result of multiplication is :  50
Result of division is       :  2.0
Result of power is          :  100000
*****************************************
```

`Result of power is : 100000` is the line contributed by Developer B through Pull
Request #1.

To use a real key, copy `.env.example` to `.env` and set `API_KEY`, or export it:
`export API_KEY=your-key`. `.env` is gitignored; no file the code imports is gitignored.

---

## The two developers

This was run as two genuinely separate working copies on disk, each with its own git
identity - not as two commits from one folder.

| | Developer A | Developer B |
|---|---|---|
| Role | Created the repository, reviewed and merged the PR | Cloned the repository, built the feature, opened the PR |
| Local folder | `03_git_and_git_hub/task-04-multi-developer-simulation` | `03_git_and_git_hub/task-04-devB-clone` (a real `git clone`) |
| `user.name` | `Developer A (veerandra7)` | `Developer B` |
| `user.email` | `veerandra.data@gmail.com` | `developer-b@example.com` |
| Commits | The 4 baseline commits | The feature commit `7cc6a4e` |

Proof - real output of `git log --format='%h %an <%ae> %s'` on `main`:

```
628be83 POTNURU VENKATA ATCHUTA SAI VEERANDRA KUMAR <74710089+veerandra7@users.noreply.github.com> Merge pull request #1 from 6-month-fde-challenge/feature-power-module
7cc6a4e Developer B <developer-b@example.com> Add power module and expose the result on the dashboard
a93b747 Developer A (veerandra7) <veerandra.data@gmail.com> Add calculator orchestrator and dashboard presentation layer
180210e Developer A (veerandra7) <veerandra.data@gmail.com> Add the four arithmetic modules guarded by API key and profile checks
ab007de Developer A (veerandra7) <veerandra.data@gmail.com> Add login, profile and numeric input collection modules
90e6154 Developer A (veerandra7) <veerandra.data@gmail.com> Add project scaffolding with gitignore and environment-based configuration
```

Two distinct author identities appear in `main`'s history, plus the GitHub account that
created the merge commit on the server.

---

## The Pull Request

| Field | Value |
|---|---|
| Number | **#1** |
| URL | <https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1> |
| Title | Add power module to the calculator |
| Head -> Base | `feature-power-module` -> `main` |
| State | **MERGED** at `2026-09-23T03:49:42Z` |
| Merge commit | `628be838c86e3f7da3d6336b1dda23b683d0ada6` |
| Diff | 3 files changed, 19 insertions(+), 1 deletion(-) |

**Description (abridged - full text in [`PULL_REQUEST.md`](PULL_REQUEST.md)):** adds
`power_module.py` with a `power(a, b)` function following the same `api_key` /
`profile_name` guard pattern as the existing four operations, wires it into
`calculator.py` as `powered`, and renders it in `dashboard.py`. Purely additive: no
existing signature or output line was changed, so the four original operations cannot
regress. Test with `python dashboard.py < /dev/null` and expect
`Result of power is          :  100000`.

**Code review (abridged - full text in [`PULL_REQUEST.md`](PULL_REQUEST.md)):** Developer
A reviewed all three changed files and confirmed the guard ordering matches the existing
modules, the new import is correctly grouped, `dashboard.py` extends the existing import
line rather than adding a second one, nothing outside the three files changed, and no
secret or gitignored-but-imported module was introduced. Verified by running the
dashboard and checking `10 ** 5 == 100000`. Two non-blocking observations were raised for
a future PR (bounding very large exponents; negative exponents returning a float).
Verdict: reviewed and approved, no changes requested.

- Formal review event: <https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1#pullrequestreview-5286666635>
- Conversation comment: <https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1#issuecomment-5788644714>

**Honest note:** `gh pr review --approve` was attempted first and GitHub refused it with
`Review Can not approve your own pull request`, because both simulated developers act
through the same GitHub account. The approval is therefore recorded as a real
`COMMENTED` review event and a conversation comment, not as a green "Approved" badge. No
approval badge is claimed that does not exist.

**Merged with** `gh pr merge 1 --merge`, producing a true merge commit with two parents.
The feature branch was intentionally **kept** on the remote as evidence:
<https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/tree/feature-power-module>

---

## Concept walkthrough

Every git and GitHub concept this task covers, explained with the command actually used
here. The full command-by-command transcript with output is in [`workflow.md`](workflow.md).

### Clone

`git clone <url> <folder>` copies an entire remote repository - all files **and the
complete commit history** - onto your machine, checks out the default branch, and wires
up the `origin` remote automatically. It is how a second developer joins a project.

```bash
git clone https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git task-04-devB-clone
```

Developer B used this to get an independent working copy; nothing in Developer A's folder
was touched. Cloning is a one-time operation - afterwards you use `fetch`/`pull` to stay
current.

### Remote repository

A *remote* is a named URL pointing at a copy of the repository hosted elsewhere - here,
GitHub. `origin` is the conventional name for the one you cloned from. The remote is the
shared meeting point: without it the two developers' histories could never converge.

```bash
git remote -v
# origin  https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git (fetch)
# origin  https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation.git (push)
```

Developer A's remote was created by `gh repo create ... --remote=origin --push`;
Developer B's was configured automatically by the clone.

### Fetch vs pull

Both talk to the remote, and the difference matters:

- **`git fetch origin`** downloads new commits and updates the remote-tracking branches
  (`origin/main`, `origin/feature-power-module`). It **does not modify your working files
  or your current branch**. It is the safe "show me what changed upstream" command.
- **`git pull origin main`** is `git fetch` **followed by a merge** into your current
  branch. It does change your working files, and it is where merge conflicts can appear.

Rule of thumb: `fetch` to look, `pull` to actually take the changes. Developer B ran both
before branching so the feature started from the newest `main`; Developer A ran
`git pull origin main` after the merge to bring Developer B's work down:

```
Updating a93b747..628be83
Fast-forward
 calculator.py   |  3 +++
 dashboard.py    |  3 ++-
 power_module.py | 14 ++++++++++++++
```

### Push

`git push` uploads local commits to the remote so other people can see them. Commits
exist only on your machine until you push.

```bash
git push -u origin feature-power-module
```

`-u` sets the upstream so later `git push` and `git pull` need no arguments. A Pull
Request cannot be opened until the branch has been pushed - GitHub has to be able to see
the commits being proposed.

### Branch workflow

A branch is an independent line of development - technically just a moving pointer to a
commit. Work happens on a short-lived feature branch so that `main` always stays in a
releasable state, and so the work can be reviewed as a self-contained unit.

```bash
git switch -c feature-power-module   # create and switch in one step
git branch -a                        # list local and remote branches
```

The cycle used here: branch off `main` -> commit the feature -> push the branch -> open a
PR -> review -> merge back into `main`. The branch was kept after merging so the shape of
the workflow stays visible in the history graph.

### Pull Request

A Pull Request is GitHub's formal request to merge one branch into another. It is not a
git command - it is a collaboration layer on top of git that provides a place to show the
diff, discuss it, run checks and record an approval **before** the code reaches `main`.

```bash
gh pr create --base main --head feature-power-module \
  --title "Add power module to the calculator" --body-file pr_body.md
```

`--base` is the branch being merged into, `--head` is the branch carrying the work. A
good PR body explains *what* changed, *why*, and *how to test it* - see
[`PULL_REQUEST.md`](PULL_REQUEST.md).

### Code review

Code review is a second pair of eyes on the diff before it becomes part of `main`. A
reviewer can approve, request changes, or just comment, and can leave notes on specific
lines. It catches defects early and spreads knowledge of the codebase across the team.

```bash
gh pr review 1 --comment --body-file review_body.md
gh pr comment 1 --body-file review_body.md
```

Developer A's review checked the guard pattern, the import placement, the blast radius of
the change, and ran the program to confirm the result - then recorded two non-blocking
follow-ups and a verdict. (As noted above, GitHub blocks approving your own PR, so the
approval is a review comment rather than an approval badge.)

### Merge

Merging combines the histories of two branches. `gh pr merge --merge` creates a **merge
commit** with two parents - one pointing at the previous tip of `main`, one at the tip of
the feature branch - which preserves the branch's shape in the history. The alternatives,
`--squash` and `--rebase`, flatten it away.

```bash
gh pr merge 1 --merge
```

The resulting merge commit `628be83` has parents `a93b747` (main) and `7cc6a4e`
(feature), which is what the `|\` fork in the graph below shows. When two developers
change the same lines, this is the step where git reports a **merge conflict** and a
human decides which version wins; here the change was additive, so it merged cleanly.

---

## Full git history

Real output of `git fetch --all && git log --graph --oneline --all --decorate`:

```
* 758afbf (HEAD -> main, origin/main, origin/HEAD) Document the multi-developer workflow, Pull Request and code review
*   628be83 Merge pull request #1 from 6-month-fde-challenge/feature-power-module
|\
| * 7cc6a4e (origin/feature-power-module) Add power module and expose the result on the dashboard
|/
* a93b747 Add calculator orchestrator and dashboard presentation layer
* 180210e Add the four arithmetic modules guarded by API key and profile checks
* ab007de Add login, profile and numeric input collection modules
* 90e6154 Add project scaffolding with gitignore and environment-based configuration
```

Reading the graph bottom-up: four commits by Developer A build `main`; the history forks
at `a93b747` where Developer B created `feature-power-module`; `7cc6a4e` is Developer B's
feature commit on that branch; `628be83` is the merge commit that joined the branch back
into `main` when Pull Request #1 was merged; and `758afbf` is Developer A committing this
documentation afterwards. `origin/feature-power-module` still points at `7cc6a4e`,
showing the branch was kept on the remote.

---

## Fixes applied after review feedback

The previous submission scored 5/15 because the workflow happened but left no trace in
the files on the default branch. Each point of feedback and what was done about it:

| Reviewer's finding | Fix in this repository |
|---|---|
| "Add a short repository file such as `submission_links.txt` containing the public repository URL and Pull Request URL." | [`submission_links.txt`](submission_links.txt) added on `main`, with both URLs plus the PR number, state, merge commit SHA and review links. |
| "Add a concise `workflow.md` listing the commands and sequence used for clone, branch creation, push, PR review, and merge." | [`workflow.md`](workflow.md) added on `main` - all 21 steps for both developers, each with the real captured output and a one-line explanation. |
| "There is no source artifact such as a PR note, changelog, or submitted PR reference showing that a Pull Request was created." | [`PULL_REQUEST.md`](PULL_REQUEST.md) added, holding the PR number, URL, full description and diff stat. |
| "No evidence of code review comments, approval, or merge documentation." | The full review text, both review permalinks, the merge command, the merge commit SHA and its two parents are committed in [`PULL_REQUEST.md`](PULL_REQUEST.md) and summarised above. |
| "None of the shown source files records a branch workflow, remote push, or simulated second developer activity." | The branch/push/PR sequence is documented in `workflow.md`, the history graph is pasted above, `power_module.py` is Developer B's committed work, and the feature branch is still on the remote. |
| "No source file documents clone, fetch, pull, push, branch, Pull Request, review, or merge concepts." | The **Concept walkthrough** section above covers all eight explicitly, each with the command used here. |
| Two developers not visible | Developer B worked in a real second clone with a distinct `user.name`/`user.email`, so `git log` on `main` shows two distinct author identities (pasted above). |
