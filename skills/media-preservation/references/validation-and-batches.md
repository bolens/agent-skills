# Validation and batch recovery

## Prove the intended equivalence

A source-file checksum establishes identity, not equivalence to a differently encoded file. A valid container does not establish complete media decoding. Use format-native integrity checks and a full decode where preservation warrants it, alongside stream and metadata comparisons.

For a lossless audio transcode, compare decoded samples using the same explicitly chosen representation, channel order, and alignment without resampling, downmixing, truncating precision, or applying gain. If normalization discards source information, equal hashes do not prove losslessness. Handle encoder padding and timing according to the source format, and report uncertainty for unsupported representations. For video, distinguish packet copy, decoded-frame equivalence, and perceptual similarity. A perceptual score cannot prove bit-exact preservation.

Check duration, sample/frame counts, seekability, start/end content, channel layout, language and default/forced flags as applicable. Compare meaningful tags, chapters, cover art, and attachments against the contract. Different containers may represent tags differently. Preserve unrepresentable data in a documented sidecar when that meets the user's intent. Do not silently strip metadata to obtain matching files.

For CUE splits, gapless albums, or chaptered audiobooks, verify ordering and boundaries as well as individual outputs. For HDR or variable-frame-rate video, check the retained color/timing semantics and target playback behavior rather than relying on dimensions alone. Use listening or visual samples to catch anomalies, without claiming they exhaustively validate the media.

## Resume without trusting stale output

Use the existing batch utility's manifest when available. Record source and output digests, selected transformation/options, tool versions, destination, and the result of each promised property check. Resume only when the manifest and current source/output agree. File existence or a nonzero size does not mean conversion completed.

Bound worker count for CPU, disk, and encoder capacity. On interruption, retain useful diagnostics and mark unfinished work. Avoid concurrent writers to the same destination. Validate temporary output before final promotion on the same filesystem when atomic rename is needed. Cross-filesystem moves require a different completion strategy. Never overwrite an unrelated destination as a resume shortcut.

Exercise a small representative batch including a corrupt input, unusual filename, collision, and interrupted run before launching a large conversion when changing batch logic. Use synthetic media fixtures where practical. Keep originals and failed inputs available for recovery. Do not add a second converter framework when the repository already owns these guarantees.
