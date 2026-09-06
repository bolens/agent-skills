# Packaging receipt contract

A packaging handoff must include:

1. Repository language/build/application evidence and the conditional target matrix.
2. Native mapping for tagged source, tagged upstream binary, and main-tip variants,
   including unsupported variants, destination rules, and coinstallation limits.
3. Tag and resolved commit, recipe/toolchain/dependency inputs, version, architecture,
   libc/OS baseline, source hashes, artifact hashes, and signing state.
4. Measured compressed, installed, and closure costs as applicable, with the baseline,
   feature profile, excluded build files, and reasons for required bundled runtimes.
5. Exact tested artifact, clean-environment checks, install/upgrade/switch/removal
   outcomes, and unavailable platform evidence.
6. Update automation and remaining coverage gaps, publication authority and state,
   and the destination-specific next action.

The receipt is proportional to the task. An audit reports gaps without building or
publishing. Existing release coordination retains ownership of delivery.
