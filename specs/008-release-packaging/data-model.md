# Packaging evidence model

This is an instruction contract, not a persisted database schema.

| Entity | Required fields | Relationships and rules |
| --- | --- | --- |
| Repository capability | language, build tools, application kind, runtime/native dependencies, OS/architecture support | One capability assessment selects many conditional targets |
| Target | ecosystem, destination, architecture/ABI, status, reason, required runner | Status is supported, conditional, or inapplicable; missing evidence is not support |
| Variant | logical source/bin/git identity, native name/channel/mode, tag/commit, version, conflict/coinstallation policy | Source and cached binary are not necessarily distinct recipes |
| Artifact | variant, build recipe revision, source hash, artifact digest, environment, payload | A built main snapshot has one resolved commit and immutable identity |
| Validation | artifact digest, check, result, environment, measurements, gaps | Executed, manual, skipped, and blocked evidence remain distinguishable |

Progression: assessed target -> prepared candidate -> locally validated candidate
-> published candidate only with authority -> destination verified. A failed check
keeps that target unresolved; it does not invalidate unrelated tested artifacts.
