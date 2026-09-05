# Validate public stack examples

Choose the repository's existing validator after inspecting its implementation and transitive helpers. Do not run a live preparation or deployment merely to make example validation pass.

## Bound the inputs and output

Use tracked public examples in a fresh temporary tree when the checkout also contains runtime configuration. Preserve relative layout, include files, and supporting templates. Confirm every referenced file remains within that allowed tree or an explicitly approved public source. Do not dereference symlinks into live paths. Do not load ignored files because Compose discovers them automatically.

Separate Compose model interpolation from service-level `env_file` values delivered to containers. Passing `--env-file` selects an interpolation source but does not replace every service env-file path. Shell values can override example interpolation inputs. Use a controlled child-process environment with only required non-sensitive tool settings and explicit fixture values. Do not print the parent environment to debug precedence. See [Docker interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/).

Select the intended Compose files, profiles, and project directory explicitly. Use `docker compose config --quiet` for a validation result when supported by the installed CLI. Full `config` output and `config --environment` can disclose values. Quiet mode suppresses the rendered model, but errors may still contain sensitive text. Review diagnostics before sharing them. See [Docker config](https://docs.docker.com/reference/cli/docker/compose/config/).

A repository renderer may replace several service env-file paths with one example file or make a shared file optional. That proves only the normalized fixture. Check the original paths, required/optional flags, override order, and referenced example coverage separately. Report missing generated bundles and optional tools as skipped coverage. Do not pull or generate upstream bundles without the relevant authorization and version review.

## Classify helpers by their actual effects

| Helper behavior | Handling for a repository-only task |
|---|---|
| Parse public YAML or audit tracked metadata | Run after checking input scope and output |
| Render examples in temporary directories | Check inherited environment, references, normalization, and diagnostic handling |
| Copy config, synchronize env files, create directories/networks/volumes | Test an isolated fixture or inspect source; do not run against live paths |
| Use `docker run` as a validator | It creates a container and may pull an image or mount private config. Prefer an installed validator or report an unavailable check unless that runtime action is authorized |
| Reload monitoring, restart services, or combine validation with reload/smoke checks | Split the read-only subset from operational actions |
| Scan files including ignored content | Exclude when private runtime reads are prohibited; scan only the intended publication boundary |
| Regenerate catalog, topology, diagram, or site | Use the corresponding source and inspect the generated diff |

A readonly mount protects writes to that mount, not confidentiality or outbound access. A helper's `--check` or dry-run option must be verified from its implementation. Preserve the repository's validation contract by recording a blocked check rather than silently substituting weaker proof.

## Report the proof precisely

Record the source revision or changed-file scope, examples used, checks performed, normalized inputs, skipped profiles/bundles, and unavailable tools. Do not include private endpoints, host paths, credentials, raw environment values, or unsanitized logs. A successful example render says nothing about the deployed image, remote storage availability, runtime authentication, or exposure from another client.
