# Bounded polluter search

Run `find-polluter.sh TARGET PATTERN` from an isolated test checkout when a test
creates an unexpected file or directory. The wrapper needs Bash and Python 3.9+.
The runner uses POSIX process groups on Linux/macOS and invokes the available
`npm test -- FILE`. Use the repository's own runner when npm is not its test
contract. This is a sequential search, not bisection.

The target must be absent and inspectable before running tests. The helper never
deletes an existing target or an observed artifact. Tests can modify other files,
so use disposable fixtures or an isolated checkout and review their side effects.

Discovery stays under the current directory, does not follow symlinks, and skips
`.git`, `node_modules`, `.venv`, `.devenv`, `.direnv`, and `__pycache__` directories.
Matching paths are sorted before execution. A discovery error or limit prevents
all test execution, rather than testing an incomplete selection.

Defaults are 60 seconds per test, 600 seconds for discovery and tests together,
1,000 matching tests, and 100,000 inspected entries. Use `--timeout`,
`--total-timeout`, `--max-tests`, and `--max-entries` for a bounded adjustment after
narrowing the pattern. Progress output shares the total deadline, including pipe
backpressure. Error reporting gets a separate best-effort 0.1-second window. A stalled filesystem operation in the kernel cannot be
interrupted by the discovery deadline check.

Each test starts in an owned process group with stdin closed and output discarded.
Normal exit, timeout, and cancellation all clean up remaining group members.
Cleanup allows 0.1 seconds for TERM, then sends KILL and waits up to one second
for the direct child. Descendants that deliberately create a separate session
are outside this cleanup boundary. No discovery scratch files are created.

Exit 1 identifies the first observed creator, including a test that exits with an
error after creating the target. Exit 2 means discovery, execution, or attribution
was inconclusive. Timeouts stop the search without running later tests. Signal
cancellation returns 130 or 143. Exit 0 means no creator was observed among the
selected successful tests, not that every project test or background behavior is
clean. Rerun a reported test directly to inspect its logs.
