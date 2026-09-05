# Patches and build evidence

Record each local patch's source, affected upstream versions, purpose, and reproduction. Inspect the complete upstream change before deciding a patch is redundant. Successful patch application can still be semantically wrong after an upstream refactor. Resolve offsets, rejected hunks, or changed ownership using surrounding code, then rerun the original regression.

Build from a clean source tree and controlled dependency set. Record whether the environment represents stock Arch or an intentional derivative/custom toolchain. A stock clean-chroot result does not prove compatibility with a custom kernel, LLVM configuration, or installed DKMS stack. Check the target kernel/header pair and required build configuration separately when relevant.

Distinguish source integrity, build reproducibility, and functional correctness. Matching checksums authenticate only the relationship to the trusted checksum source. A reproducibility claim requires independent controlled builds and artifact comparison. Neither substitutes for the patch regression test.

For a pinned local package, establish why it is pinned and what upstream candidate would replace it. Verify that candidate fixes the original problem and preserves needed local behavior before proposing removal of the pin. Prepare a rollback package and relevant configuration recovery before an authorized live replacement. Do not clear all pins because one patch became obsolete.

Keep package revision changes, regenerated metadata, patches, and their tests coherent. Inspect final package contents for source-tree leftovers, build paths, unexpected executables, and accidental data before publication. Follow the repository's signing and release process rather than inventing a parallel uploader.
