# Licensing

This collection has no single license covering all of its contents. Forking,
rewriting, or selectively importing upstream changes does not remove the
upstream license conditions. A provenance link is not a substitute for a
required license or copyright notice.

Repository-authored maintenance scripts and documentation are copyright the
repository owner. No separate license is granted for them at this time.

See `PROVENANCE.json` and each `skills/*/UPSTREAM.md` before redistribution.

## Audited skill sources

The 2026-09-05 audit checked the registered source subtrees and applicable
ancestor license files at their exact recorded revisions. Each imported skill
now contains the full upstream license. `UPSTREAMS.json` records its source path,
SPDX identifier, local path, and SHA-256. `make check-fast` rejects missing or
changed copies. These checks enforce notice retention, not every possible use
of the material.

| Source and copied scope | Terms and retained copies |
| --- | --- |
| [Caveman](https://github.com/JuliusBrussee/caveman/blob/3b74643f4d910f496babd4e634b1ba7168816f14/LICENSING.md), eight `skills/` subtrees | MIT, with a full `LICENSE` in each skill. The upstream scope note is preserved. The BSL engine, runtime modules, and binaries are not included in these forks. |
| [Omarchy](https://github.com/basecamp/omarchy/blob/d3d23fdddef846ebb98b52122a6ece66211c0daf/LICENSE), `omarchy` and `diagnose-crash` | MIT, with David Heinemeier Hansson's notice in each skill's `LICENSE`. |
| [Vercel Skills](https://github.com/vercel-labs/skills/blob/435076e78988e1e6ec40d00b0b1d76bdbbc5419a/LICENSE), `find-skills` | MIT, retained in `skills/find-skills/LICENSE`. The CLI and its dependency bundle are not copied, so its dependency notice list does not describe this fork. |
| [Web Quality Skills](https://github.com/addyosmani/web-quality-skills/blob/afa8da942115f2961fdbfa80807ea0b232ff6c00/LICENSE), four skill subtrees | MIT, with Addy Osmani's notice already retained in each skill's `LICENSE`. |
| [Archify](https://github.com/tt-a1i/archify/blob/06dd052602dd9a369e4d034e24faef0917b5a60c/archify/LICENSE), `archify/` | MIT for Archify code, retaining both tt-a1i and Cocoon AI copyright notices. Bundled material has separate terms in [its third-party notices](skills/archify/THIRD_PARTY_NOTICES.md). |
| [Anthropic frontend-design](https://github.com/anthropics/skills/tree/2235be7c60b551f5de82ade908fd3816455afcda/skills/frontend-design) | Apache-2.0, retained in `skills/frontend-design/LICENSE.txt`. `SKILL.md` identifies local modifications. No applicable upstream NOTICE file was present at that revision. |

The original frontend-design import at repository commit `32224e7` matches the
Anthropic revision above except for its local browser-verification paragraph.
Later local rewrites remain recorded as modifications. The old local-original
provenance was incorrect and has been replaced without importing newer behavior.

## Spec Kit integration

The generated `.specify/scripts/`, `.specify/templates/`, workflow integration,
and `.agents/skills/speckit-*` files come from
[GitHub Spec Kit v1.0.3](https://github.com/github/spec-kit/tree/6906bc582230bb752776e23287ee97990c1af743).
Its MIT license and GitHub copyright notice are retained in
[.specify/LICENSE](.specify/LICENSE). Include that license when copying or
redistributing these integration files. Project-authored memory is separate.

## Distribution and future imports

Keep the full relevant license and notices with each copied skill. MIT requires
retaining its copyright and permission notice. Apache-2.0 also requires notices
in modified files and preservation of applicable attribution and NOTICE text.
Neither license requires taking future updates or contributing modifications
back upstream. See the [MIT terms](https://opensource.org/license/mit) and
[Apache-2.0 section 4](https://www.apache.org/licenses/LICENSE-2.0).

Review terms at every candidate revision, including exceptions for files,
dependencies, images, and fonts. Do not copy an unlicensed subtree on the
assumption that public GitHub access permits unrestricted reuse. Do not apply a
new restrictive license retroactively to an older licensed copy, or assume that
the old terms automatically cover newly imported revisions.

Archify's icon catalogue includes attribution, share-alike, and non-commercial
terms as well as trademarks. Its MIT license does not clear every icon for every
use. Keep the applicable notices with generated artifacts and check the intended
use before selecting a mark. Source notice retention does not prove that an
arbitrary exported image or commercial use satisfies those separate terms.
