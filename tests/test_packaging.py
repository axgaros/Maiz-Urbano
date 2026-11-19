"""Regression tests for PyInstaller one-directory resource/data separation."""
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
import sys
import tempfile
import unittest

import main
from main import Store


class PackagingPathTests(unittest.TestCase):
    def test_source_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            data, resources = main.resolve_paths(frozen=False, source_file=str(Path(tmp) / 'main.py'))
            # Windows temp directories can be written using a DOS 8.3 alias
            # (e.g. RUNNER~1). resolve_paths canonicalizes those aliases.
            expected = Path(tmp).resolve()
            self.assertEqual(data, expected)
            self.assertEqual(resources, expected)

    def test_windows_onedir_resource_and_db_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe_dir = Path(tmp) / 'dist' / 'MaizUrbano'
            data, resources = main.resolve_paths(
                frozen=True, executable=exe_dir / 'MaizUrbano.exe',
                bundle_dir=exe_dir / '_internal',
            )
            expected_dir = exe_dir.resolve()
            self.assertEqual(data / 'data' / 'maiz_urbano.db', expected_dir / 'data' / 'maiz_urbano.db')
            self.assertEqual(resources / 'frontend' / 'index.html', expected_dir / '_internal' / 'frontend' / 'index.html')
            self.assertNotIn('_internal', str(data))

    def test_portable_data_survives_reopen(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe_dir = Path(tmp) / 'MaizUrbano'
            data, resources = main.resolve_paths(
                frozen=True, executable=exe_dir / 'MaizUrbano.exe',
                bundle_dir=exe_dir / '_internal',
            )
            path = data / 'data' / 'maiz_urbano.db'
            first = Store(path)
            first.sale([{'id': 'el-cre', 'quantity': 2}])
            reopened = Store(path)
            self.assertEqual(reopened.sales()[0]['total_cents'], 7000)
            self.assertTrue(path.exists())
            self.assertFalse((resources / 'data' / 'maiz_urbano.db').exists())

    def test_gui_entrypoint_calls_bridge(self):
        called = []
        webview_stub = SimpleNamespace(
            create_window=lambda title, url, **kw: called.append((title, url, kw)),
            start=lambda **kw: called.append(('start', kw)),
        )
        index = Path(main.__file__).parent / 'frontend' / 'index.html'
        with patch.dict(sys.modules, {'webview': webview_stub}), \
             patch.object(main, 'Api', return_value=object()), \
             patch.object(main, 'FRONTEND_PATH', index):
            main.run()
        self.assertEqual(called[0][1], str(index))
        self.assertIn('js_api', called[0][2])
        self.assertEqual(called[1][0], 'start')

    def test_missing_ui_fails_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(main, 'FRONTEND_PATH', Path(tmp) / 'missing.html'):
                with self.assertRaises(FileNotFoundError):
                    main.run()

    def test_self_check_does_not_leave_test_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frontend = root / 'frontend'
            frontend.mkdir()
            for name in ('index.html', 'styles.css', 'app.js'):
                (frontend / name).write_text('ok', encoding='utf-8')
            with patch.object(main, 'RESOURCE_ROOT', root), \
                 patch.object(main, 'DB_PATH', root / 'data' / 'maiz_urbano.db'):
                self.assertTrue(main.self_check())
            self.assertFalse(list((root / 'data').glob('*')))


if __name__ == '__main__':
    unittest.main()
