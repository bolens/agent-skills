# Reproduce validation

From the root with Python, Bash, Git, and native check tools:

```sh
python3 -m unittest discover -s tests -p test_speckit.py -v
python3 -m unittest discover -s tests -p test_devcontainer_setup.py -v
make check-fast
make check
```

Fixtures use temporary checkouts and controlled tools. Permission checks require a non-root POSIX user. Installed client links can fail independently of source validation.

Build `.devcontainer/Dockerfile` with `.devcontainer` as context. Mount a disposable Git checkout at `/workspace`, run as vscode, run `bash .devcontainer/post-create.sh` twice, then `make check-fast test portability`. Do not mount credentials or the Docker socket. The [verification record](verification.md) identifies the actual commands and image.
