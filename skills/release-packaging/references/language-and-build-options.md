# Select packages from language and build capabilities

Read actual manifests and build recipes before selecting targets. Treat these as starting points, not a language-to-platform guarantee. Native libraries, GUI frameworks, kernel APIs, plugins, licensing, and runtime deployment can rule out a format that the language toolchain otherwise supports. Verify current tool documentation and build an artifact before declaring a new target supported.

## Capability assessment

For each release unit, identify:

- product: library, CLI, desktop application, service, plugin, or static web assets
- source language and build system, minimum supported toolchain, release profiles, install/staging support, and generated/vendored inputs
- output: source archive, registry package, executable, shared library, application bundle, or container
- target OS, CPU baseline/architecture, libc/ABI, runtime dependencies, native bindings, and available cross/native build tools
- existing packaging backends, license/distribution restrictions, signing needs, target runners, and destination eligibility

Select supported formats from that evidence. Mark a plausible format conditional with the exact missing port, backend, runner, or verification. Mark an unsuitable format inapplicable with a reason. Prioritize current stable/rolling targets and current supported runtimes. Do not introduce an obsolete dependency pin merely to enable an old platform.

## Language-specific decisions

| Repository capability | Appropriate output candidates | Checks before claiming lean cross-platform support |
| --- | --- | --- |
| Rust executable | Per-target release binaries and source recipes; native packages and supported app formats; crates.io for a deliberately publishable crate | Inspect target support and native dependencies. Use release profiles and deliberate feature selection. Measure LTO/size options and split debug symbols where appropriate; do not silently change panic behavior or disable required features. [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html) |
| Go executable | Per-target binaries, native packages, source recipes; versioned Go modules for consumers | Verify GOOS/GOARCH and CPU level. cgo requires compatible native libraries and a target C toolchain when cross-compiling. Disabling cgo changes available implementations and may change behavior; test before calling the result portable. [cgo](https://pkg.go.dev/cmd/cgo) |
| C/C++ or other native compiler | Native packages, libraries/development packages, executable archives, and supported app bundlers | Require target sysroot/toolchain, ABI/loader evidence, explicit CPU floor, install staging, shared-library metadata, and native tests. Use distro hardening and measured release optimization. Never use `-march=native` for a generic distributed artifact |
| Python distribution | sdist and wheel under the same project/version; native packages or isolated CLI installation; standalone app bundling only with a supported backend | Verify build backend, entrypoints, dependencies, interpreter tags, and native-extension OS/libc/architecture tags. A wheel does not bundle Python by definition. Test the built sdist and wheel in clean environments. [Packaging flow](https://packaging.python.org/en/latest/flow/) |
| JS/TS library or CLI | npm tarball with exports/bin metadata; native wrappers only where runtime provisioning is defined | Inspect packed files and use an allowlist. Keep build tools out of runtime dependencies; preserve dynamic imports/assets and required optional-platform dependencies. Native addons need target builds. An Electron or other desktop backend adds its own platform/runtime matrix. [package.json](https://docs.npmjs.com/files/package.json/) |
| .NET component or application | NuGet for packable components/tools; framework-dependent or self-contained app output; native installers with an available backend | Decide who supplies the runtime. Single-file and Native AOT artifacts are target-specific. Enable trimming/AOT only when reflection, dynamic loading, and real app behavior pass. [Deployment](https://learn.microsoft.com/en-us/dotnet/core/deploying/), [Native AOT](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/) |
| JVM component or application | Maven-compatible artifacts for libraries; JAR/runtime image and native packages via an appropriate backend for applications | Separate sources/Javadoc publication artifacts from runtime payload. `jpackage` builds native formats on their target platform. Minimize runtime modules only after dynamic/service loading tests; stage its input directory carefully. [Central requirements](https://central.sonatype.org/publish/requirements/), [jpackage](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jpackage.html) |
| Other language ecosystem | Native registry format when a publishable product and metadata exist, such as a Ruby gem or PHP Composer package; native wrappers only with a working runtime plan | Inspect the repository's actual pack/publish contract and current official documentation. Do not manufacture a registry target based on file extensions |
| Static web frontend | Built web assets; optional server/OCI deployment when part of the product | A frontend build alone does not justify desktop installers or nine OS packages. A configured desktop wrapper is a separate application product |

For Swift, Zig, cross-language projects, or another toolchain, follow the same assessment using its supported target list and actual installable outputs. Do not silently exclude an otherwise supported target because its language is absent from this table.

## Native registry variants

Use the ecosystem's version grammar and source/binary relationship. Examples include Python sdist plus wheels, JVM source/Javadoc companions, and a source-built package served from a binary cache. These are not necessarily separate `-bin` identities.

Use immutable prerelease or development versions for main snapshots where the registry permits, with opt-in discovery such as npm `next` instead of `latest`. Map the commit to the native version; never replace already published bytes. If snapshot publication or an alternate binary identity is unsupported, document the repository/archive route. Verify native rules before promising a package-git equivalent. See [npm publishing](https://docs.npmjs.com/cli/commands/npm-publish/).

Reuse an existing verified artifact across suitable package-manager wrappers when architecture, ABI, installation layout, runtime, and signature contracts match. Do not cross-convert DEB/RPM/APK archives as a substitute for native metadata and target testing. Do not rewrite the application or add a heavyweight bundler solely to fill every row of the target matrix.
