# Comparing audit runs

Use existing audit reports and task records when the request asks what changed
or returns to a previously inspected fleet. Load only records relevant to the
current scope. A one-off inventory does not need a new history store or schedule.

## Establish comparable evidence

Bind each prior finding to the repository's verified remote identity, worktree,
revision, inspected surface, and check result. Record when evidence was observed
separately from when the underlying change occurred. Local remote-tracking refs
need their own freshness qualification. A path rename alone does not identify
a new repository; matching directory basenames do not prove the same repository.

Check whether the earlier command, scan depth, exclusions, runtime, and selected
repositories match the new run. If they differ, state which comparisons remain
valid. A missing nested repository can reflect a shallower scan, and a missing
failure can reflect a skipped test. Neither proves repair or removal.

## Update findings without erasing their basis

Use a short disposition for each material prior finding: newly observed,
changed, rechecked, resolved, disputed, or not rechecked. The label is less
important than the evidence behind it. Resolve only when a relevant current
check demonstrates the original issue is gone. Expired evidence needs a recheck;
it does not establish either continued failure or recovery.

Retain the previous evidence link when replacing a conclusion. For conflicting
results, compare revisions, environments, and check coverage before choosing
between them. Keep an unresolved conflict visible with the next discriminating
check. Several reports derived from one CI run are one observation, not
independent confirmation. An upstream fix announcement does not prove a local
consumer has adopted it.

Prioritize changes that affect the requested maintenance decision. Carry forward
unresolved high-impact findings even when unchanged. Separate observed facts,
their practical impact, and a proposed action. A recommendation does not authorize
that action or replace the repository's controlling policy.

## Correct the repeatable cause

If a user correction exposes a wrong repository mapping, missed scan boundary,
stale reference, or irrelevant prioritization rule, correct that cause in the
existing authorized task record or workflow. Preserve the correction's scope
and supporting evidence so it does not become a blanket rule for other repos.
Do not merely rewrite the final summary and repeat the same faulty comparison.

Report the baseline, comparable coverage, material changes, unresolved prior
findings, and gaps. Persistent workflow edits require implementation scope;
read-only audits can propose them. Keep records in the repository's established
location and retain source history without collecting unrelated private data.
