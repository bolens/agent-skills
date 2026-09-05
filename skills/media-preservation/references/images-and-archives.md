# Images and archival packages

## Images

Inventory dimensions, bit depth, color space/profile, alpha, orientation, frame/page count, animation timing/loop/disposal, and relevant EXIF/IPTC/XMP metadata before transforming an image. Keep RAW originals and editing sidecars when they are the preservation master. A flattened preview does not preserve layers, edit history, or original sensor data.

Define whether equivalence means original bytes, decoded pixel values, or intended visual appearance. Orientation application, color conversion, alpha compositing, resizing, and bit-depth reduction change the comparison contract. Do not normalize both inputs to 8-bit RGB or remove alpha merely to obtain matching hashes. Assigning a color profile and converting between profiles are different operations. Preserve or explicitly transform the intended color interpretation. [ImageMagick color management](https://imagemagick.org/color-management/).

Validate every intended frame/page, not only the first image returned by a decoder. Check animation timing and transparency against the destination's capabilities. Inspect color-managed visual samples alongside full decode and metadata checks. A successful JPEG-to-PNG conversion does not restore lost detail. Separate archival originals from optimized delivery derivatives.

Metadata retention and privacy removal are different requested outcomes. If stripping location or identifying metadata is authorized, record those exclusions and inspect embedded thumbnails/sidecars too. Do not silently strip all metadata as a default optimization or promise privacy from one tag deletion.

## Archives and preservation packages

Distinguish compressing a file, packaging a tree, extracting a supplied archive, and creating an archival package with manifests, checksums, signatures, or recovery data. Discover the archive repo's supported formats and limits. Preserve the agreed member set, file bytes, names, hierarchy, empty directories, timestamps, permissions, links, and extended metadata where the format and destination support them. Record unavoidable losses.

List and validate archive members before extraction. Treat absolute paths, parent traversal, link targets, special files, duplicate members, and case/Unicode collisions as explicit policy decisions. Never follow a supplied link outside the disposable destination or overwrite unrelated files. Enforce limits on expanded bytes, members, nesting, and time for untrusted or unexpectedly large input. Do not execute extracted content as validation.

Use the format's integrity check, then a bounded disposable extraction and comparison when recoverability is promised. CRC success cannot establish provenance, authenticity, or that the intended files were included. Compare extracted contents and required metadata with the source manifest. Check extraction warnings and unsupported properties instead of calling them successful preservation. [GNU tar integrity guidance](https://www.gnu.org/software/tar/manual/html_node/Integrity.html).

A checksum manifest detects changes relative to that manifest; authenticity requires a trusted signature/key relationship when requested. Parity/recovery files are not a separate backup. For encrypted archives, test recovery with the intended credential path without logging secrets, and distinguish data encryption from exposed member names/metadata. Use `backup-restore-verification` for recovery from independent backup storage.
