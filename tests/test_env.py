import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from providers import load_env


class LoadEnvTests(unittest.TestCase):
    def test_reads_exported_and_quoted_values(self):
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / '.env'
            env_file.write_text(
                'export PROVIDER=gemini\nMODEL="model with spaces"\nAPI_KEY=\'secret-value\'\n',
                encoding='utf-8',
            )
            with patch.dict(os.environ, {}, clear=True):
                load_env(env_file)
                self.assertEqual(os.environ['PROVIDER'], 'gemini')
                self.assertEqual(os.environ['MODEL'], 'model with spaces')
                self.assertEqual(os.environ['API_KEY'], 'secret-value')

    def test_existing_environment_values_take_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / '.env'
            env_file.write_text('MODEL=file-model\n', encoding='utf-8')
            with patch.dict(os.environ, {'MODEL': 'terminal-model'}, clear=True):
                load_env(env_file)
                self.assertEqual(os.environ['MODEL'], 'terminal-model')

    def test_reports_malformed_assignment(self):
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / '.env'
            env_file.write_text('not-an-assignment\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Dòng 1'):
                load_env(env_file)


if __name__ == '__main__':
    unittest.main()
