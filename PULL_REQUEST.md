# Pull Request evidence

This file records the Pull Request in the repository itself, so the whole review and
merge cycle is visible from a plain file snapshot of `main` without needing to open
GitHub.

## Summary

| Field | Value |
|---|---|
| PR number | **#1** |
| PR URL | <https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1> |
| Title | **Add power module to the calculator** |
| Opened by | Developer B (from the clone `task-04-devB-clone`) |
| Source branch (`--head`) | `feature-power-module` |
| Target branch (`--base`) | `main` |
| State | **MERGED** |
| Merged at | `2026-09-21T12:56:59Z` |
| Merged by | `veerandra7` |
| Merge method | merge commit (`gh pr merge 1 --merge`) |
| **Merge commit SHA** | **`8cb881749c70b0795e22e527bc42ab1b34178b40`** |
| Commits in PR | 1 (`b3ab4862bf2cded7ea5caa20393fb747b8171c9a`) |
| Diff | 3 files changed, 19 insertions(+), 1 deletion(-) |
| Branch after merge | kept on the remote, deliberately not deleted |

Command used to open it:

```bash
gh pr create --repo 6-month-fde-challenge/task-04-multi-developer-simulation \
  --base main --head feature-power-module \
  --title "Add power module to the calculator" \
  --body-file pr_body.md
```

Output:

```
https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1
```

---

## Files changed by this Pull Request

```
 calculator.py   |  3 +++
 dashboard.py    |  3 ++-
 power_module.py | 14 ++++++++++++++
 3 files changed, 19 insertions(+), 1 deletion(-)
 create mode 100644 power_module.py
```

---

## Full Pull Request description (as submitted)

> ## What changed
>
> Adds a fifth arithmetic operation to the calculator.
>
> - **`power_module.py` (new)** - `power(a, b)` returns `a ** b`. It follows exactly the
>   same guard pattern as `addition_module.py`, `subtract_module.py`,
>   `multiply_module.py` and `division_module.py`: it returns `None` and prints an
>   explanatory message when `config.api_key` is missing or when `profile.profile_name`
>   is empty, so an unauthenticated caller never gets a silent result.
> - **`calculator.py`** - imports `power_module.power` and publishes the result as
>   `powered`, next to `total`, `subtraction`, `multiplication` and `div`.
> - **`dashboard.py`** - imports `powered` and renders `Result of power is` in the
>   dashboard block.
>
> ## Why
>
> The dashboard advertised itself as the project's integration point but only covered
> four operations. Exponentiation is the natural next operation and it lets us prove
> that the module pattern established by Developer A extends cleanly: a new operation
> needs one new module plus two one-line wiring changes, with no edits to `config.py`,
> `login.py`, `profile.py` or `input_variables.py`.
>
> ## How to test
>
> ```bash
> git fetch origin
> git switch feature-power-module
> python dashboard.py < /dev/null
> ```
>
> Expected output with the non-interactive defaults (`a = 10`, `b = 5`):
>
> ```
> *************** DASHBOARD ***************
> Result of addition is       :  15
> Result of subtraction is    :  5
> Result of multiplication is :  50
> Result of division is       :  2.0
> Result of power is          :  100000
> *****************************************
> ```
>
> To check the guard path, temporarily clear the profile (`profile_name = ""`) and
> confirm `power` prints `No logged-in profile - cannot run exponentiation` and returns
> `None` rather than raising.
>
> ## Risk / scope
>
> Additive only. No existing function signature, output line or module import was
> changed or removed, so the four original operations are untouched.
>
> ---
> Submitted by **Developer B** from the clone at `task-04-devB-clone`, branch
> `feature-power-module`.

---

## Code review

Posted twice so it is visible both as a formal review event and in the conversation
thread:

- Formal review (`state = COMMENTED`):
  <https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1#pullrequestreview-5266839970>
- Conversation comment:
  <https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1#issuecomment-5760838331>

Commands:

```bash
gh pr review 1 --repo 6-month-fde-challenge/task-04-multi-developer-simulation \
  --comment --body-file review_body.md
gh pr comment 1 --repo 6-month-fde-challenge/task-04-multi-developer-simulation \
  --body-file review_body.md
```

### Full review text

> ### Code review by Developer A
>
> I reviewed the three changed files against `main`.
>
> **What I checked and what I found**
>
> 1. `power_module.py` - the API key guard and the `profile_name` guard are both present
>    and they are ordered the same way as in `addition_module.py` and the other three
>    operations, so the failure messages stay consistent across the codebase. Returning
>    `None` instead of raising matches the established contract. Good.
> 2. `calculator.py` - `powered = power(a, b)` sits with the other four assignments and
>    the new import is grouped with the other module imports. The `__main__` print line
>    is aligned with the existing column layout. Good.
> 3. `dashboard.py` - `powered` is added to the existing `from calculator import ...`
>    line rather than a second import statement, which is what I would have asked for.
>    Good.
> 4. No changes to `config.py`, `login.py`, `profile.py` or `input_variables.py`, so the
>    change is genuinely additive and cannot regress the four existing operations.
> 5. No secret material and no new gitignored-but-imported module was introduced -
>    `power_module.py` is committed and tracked.
>
> **Verification I ran**
>
> ```
> python dashboard.py < /dev/null
> ```
>
> produced `Result of power is          :  100000` for the default inputs `a = 10`,
> `b = 5`, which is correct (10 ** 5).
>
> **Non-blocking observations for a future PR**
>
> - `power(a, b)` with a large `b` can be slow or memory-hungry for big integers; a
>   sanity bound on the exponent would be worth adding later. Not a blocker for this
>   change, since the inputs are read as small integers.
> - A negative exponent returns a float while the other integer operations return ints.
>   Acceptable, and it mirrors how `division` already returns a float.
>
> **Verdict: reviewed and approved.** No changes requested. Merging into `main`.

### Honest note about the approval badge

A formal GitHub **approval** (`gh pr review --approve`) was attempted first and was
**rejected by GitHub**:

```
failed to create review: GraphQL: Review Can not approve your own pull request (addPullRequestReview)
```

Both simulated developers necessarily operate through the same GitHub account
(`veerandra7`), and GitHub does not permit approving your own Pull Request. The approval
is therefore recorded as the review text above (a real `COMMENTED` review event plus a
conversation comment) rather than as a green "Approved" badge. This document does not
claim an approval badge that does not exist.

---

## Merge

```bash
gh pr merge 1 --repo 6-month-fde-challenge/task-04-multi-developer-simulation --merge \
  --subject "Merge pull request #1 from 6-month-fde-challenge/feature-power-module" \
  --body "Add power module to the calculator (reviewed by Developer A)"
```

Verified state after merging:

```
{"author":{"login":"veerandra7"},"baseRefName":"main","headRefName":"feature-power-module",
 "mergeCommit":{"oid":"8cb881749c70b0795e22e527bc42ab1b34178b40"},
 "mergedAt":"2026-09-21T12:56:59Z","number":1,"state":"MERGED",
 "title":"Add power module to the calculator",
 "url":"https://github.com/6-month-fde-challenge/task-04-multi-developer-simulation/pull/1"}
```

```
$ gh pr list --state all
1   Add power module to the calculator   feature-power-module   MERGED   2026-09-21T12:56:06Z
```

The merge commit itself, showing **two parents** (proof of a real merge rather than a
squash or a fast-forward):

```
commit 8cb881749c70b0795e22e527bc42ab1b34178b40
Author: POTNURU VENKATA ATCHUTA SAI VEERANDRA KUMAR <74710089+veerandra7@users.noreply.github.com>
Date:   Mon Sep 21 18:26:59 2026 +0530
Parents: ca6835b2e01c9fad8a86f5fb01aeab10edaafcd7 b3ab4862bf2cded7ea5caa20393fb747b8171c9a

    Merge pull request #1 from 6-month-fde-challenge/feature-power-module
    Add power module to the calculator (reviewed by Developer A)

 calculator.py   |  3 +++
 dashboard.py    |  3 ++-
 power_module.py | 14 ++++++++++++++
 3 files changed, 19 insertions(+), 1 deletion(-)
```

The feature branch still exists on the remote after the merge:

```
$ gh api repos/6-month-fde-challenge/task-04-multi-developer-simulation/branches --jq '.[].name'
feature-power-module
main
```
