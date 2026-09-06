#!/usr/bin/env bash
# Bisection script to find which test creates unwanted files/state
# Usage: ./find-polluter.sh <file_or_dir_to_check> <test_pattern>
# Example: ./find-polluter.sh '.git' 'src/**/*.test.ts'

set -e

if [ $# -ne 2 ]; then
  echo "Usage: $0 <file_to_check> <test_pattern>"
  echo "Example: $0 '.git' 'src/**/*.test.ts'"
  exit 1
fi

POLLUTION_CHECK="$1"
TEST_PATTERN="$2"
if [ -e "$POLLUTION_CHECK" ] || [ -L "$POLLUTION_CHECK" ]; then
  echo "Inconclusive: target already exists; preserve it and use an isolated fixture."
  exit 2
fi

echo "🔍 Searching for test that creates: $POLLUTION_CHECK"
echo "Test pattern: $TEST_PATTERN"
echo ""

# Get list of test files (find . emits ./-prefixed paths, so accept the
# pattern written with or without a leading ./)
TEST_PATTERN="${TEST_PATTERN#./}"
# find -path can't match '**/' against zero directory levels, so a pattern
# like src/**/*.test.ts would skip src/top.test.ts; also try the pattern
# with '**/' collapsed to cover files directly under the base directory.
TEST_FILES=()
discovered=$(mktemp)
trap 'rm -f -- "$discovered"' EXIT
if ! find . -type f \( -path "./$TEST_PATTERN" -o -path "./${TEST_PATTERN//\*\*\//}" \) -print0 >"$discovered"; then
  echo "Inconclusive: test discovery failed." >&2
  exit 2
fi
while IFS= read -r -d '' test_file; do
  TEST_FILES+=("$test_file")
done <"$discovered"
TOTAL=${#TEST_FILES[@]}
if [ "$TOTAL" -eq 0 ]; then
  echo "Inconclusive: no matching tests."
  exit 2
fi

echo "Found $TOTAL test files"
echo ""

COUNT=0
incomplete=0
for TEST_FILE in "${TEST_FILES[@]}"; do
  COUNT=$((COUNT + 1))

  # Skip if pollution already exists
  if [ -e "$POLLUTION_CHECK" ] || [ -L "$POLLUTION_CHECK" ]; then
    echo "⚠️  Pollution already exists before test $COUNT/$TOTAL"
    echo "   Skipping: $TEST_FILE"
    exit 2
  fi

  echo "[$COUNT/$TOTAL] Testing: $TEST_FILE"

  # Run the test
  npm test "$TEST_FILE" > /dev/null 2>&1 || incomplete=1

  # Check if pollution appeared
  if [ -e "$POLLUTION_CHECK" ] || [ -L "$POLLUTION_CHECK" ]; then
    echo ""
    echo "🎯 FOUND POLLUTER!"
    echo "   Test: $TEST_FILE"
    echo "   Created: $POLLUTION_CHECK"
    echo ""
    echo "Pollution details:"
    ls -la "$POLLUTION_CHECK"
    echo ""
    echo "To investigate:"
    echo "  npm test $TEST_FILE    # Run just this test"
    echo "  cat $TEST_FILE         # Review test code"
    exit 1
  fi
done

echo ""
if [ "$incomplete" -ne 0 ]; then
  echo "Inconclusive: a test failed; no creator of the requested target was observed."
  exit 2
fi
echo "No creator of the requested target was observed in the selected tests."
exit 0
