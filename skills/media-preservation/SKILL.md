---
name: media-preservation
description: Convert, remux, organize, and verify audio or video collections while preserving intended streams, metadata, chapters, artwork, and source integrity. Use for archival media workflows and resumable conversion batches, not generic image generation or browser recordings.
---

# Media preservation

Establish what must survive the transformation before choosing an encoder or converter. Prefer the repository's verified media utilities and format contracts over a new shell pipeline.

## Define the preservation contract

Identify source formats, destination use, playback requirements, intended losslessness, selected tracks, language/default dispositions, channel layout, sample rate/depth, frame timing, color/HDR metadata, chapters, tags, artwork, subtitles, attachments, and sidecars where applicable. Do not assume a preferred archival format is universal. Read the local utility's platform and dependency requirements before running it.

Inspect representative sources with installed tools such as `ffprobe` and format-native validators. Inventory actual streams rather than selecting the first audio/video track blindly. Decide separately whether to copy compressed streams, decode/re-encode losslessly, or produce a lossy derivative. Converting a lossy source to a lossless container cannot recover discarded information. [FFmpeg stream selection and processing](https://ffmpeg.org/ffmpeg.html#Stream-selection).

Read [validation and batch recovery](references/validation-and-batches.md) for lossless claims, metadata migration, or multi-file work. Resolve ambiguous track selection or intentional quality loss before the dependent conversion. Preserve originals unless their removal is explicitly requested and validated output satisfies the agreed contract.

## Transform and verify

Use existing converters first. Quote paths, preserve unusual filenames, and handle output collisions explicitly. Build an explicit stream/metadata mapping compatible with the target container. An indiscriminate `-map 0` may include unsupported attachments or streams. Record intentional omissions and format limitations instead of silently dropping content.

Write to a distinct temporary output with an explicit format or suitable extension. Treat the process exit code as only one check. Validate decodeability and the promised properties before promoting output to its final path. Keep source checksums, tool versions, conversion options, and validation results in a compact manifest when the batch needs reproducibility.

For archival packages, verify both file integrity and the media contract. Use [backup-restore-verification](../backup-restore-verification/SKILL.md) when the question concerns backup recoverability. Use [cli-web-evidence](../cli-web-evidence/SKILL.md) for browser recordings, not as the archival validation workflow.

Report completed, failed, skipped, and intentionally lossy items. State exactly which streams and properties were compared. Do not describe an unverified batch or a checksum-only check as preservation proof.
