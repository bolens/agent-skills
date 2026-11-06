import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/configure-browser-package-mirror.py'
SPEC = importlib.util.spec_from_file_location('browser_mirror', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BrowserPackageMirror(unittest.TestCase):
    def test_preserves_signed_suites_components_other_sources_and_comments(self):
        source = '# http://azure.archive.ubuntu.com/ubuntu is an example\nTypes: deb\nURIs: http://azure.archive.ubuntu.com/ubuntu/\nSuites: noble noble-updates noble-backports\nComponents: main universe restricted multiverse\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n\nTypes: deb\nURIs: http://security.ubuntu.com/ubuntu\nSuites: noble-security\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n'
        expected = source.replace('URIs: http://azure.archive.ubuntu.com/ubuntu/', 'URIs: https://archive.ubuntu.com/ubuntu/')
        self.assertEqual(MODULE.configure_sources(source), expected)
        self.assertEqual(MODULE.configure_sources(expected), expected)

    def test_exact_hosted_image_mirror_file_representation(self):
        # Primary provider fixture: actions/runner-images tag ubuntu24/20261101.360,
        # images/ubuntu/scripts/build/configure-apt-sources.sh replaces Azure with
        # this exact local mirror token (Azure priority 1, HTTPS archive priority 2).
        source = 'Types: deb\nURIs: mirror+file:/etc/apt/apt-mirrors.txt\nSuites: noble noble-updates noble-backports\nComponents: main universe\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n\nURIs: http://security.ubuntu.com/ubuntu\nSuites: noble-security\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n'
        expected = source.replace('mirror+file:/etc/apt/apt-mirrors.txt', 'https://archive.ubuntu.com/ubuntu')
        self.assertEqual(MODULE.configure_sources(source), expected)
        self.assertEqual(MODULE.configure_sources(expected), expected)

    def test_handles_https_origin_and_preserves_other_uri_tokens(self):
        source = 'URIs: https://azure.archive.ubuntu.com/ubuntu https://security.ubuntu.com/ubuntu\n'
        self.assertEqual(MODULE.configure_sources(source), 'URIs: https://archive.ubuntu.com/ubuntu https://security.ubuntu.com/ubuntu\n')

    def test_rejects_unknown_or_lookalike_hosts_without_writing(self):
        for source in ['URIs: https://azure.archive.ubuntu.com.evil/ubuntu\n', 'URIs: https://mirror.invalid/ubuntu\n', 'URIs: mirror+file:/tmp/apt-mirrors.txt\n', 'URIs: mirror+file:/etc/apt/apt-mirrors.txt.evil\n', 'URIs: mirror+file:/etc/apt/apt-mirrors.txt/\n', '# URIs: http://azure.archive.ubuntu.com/ubuntu\n']:
            with self.assertRaisesRegex(ValueError, 'no files changed'):
                MODULE.configure_sources(source)


if __name__ == '__main__':
    unittest.main()
