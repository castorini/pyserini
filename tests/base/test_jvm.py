#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import importlib
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch


class TestJvmStartup(unittest.TestCase):
    def setUp(self):
        self.jnius_config = Mock()
        self.module_patcher = patch.dict(sys.modules, {'jnius_config': self.jnius_config})
        self.module_patcher.start()
        sys.modules.pop('pyserini._jvm', None)
        self.jvm = importlib.import_module('pyserini._jvm')

    def tearDown(self):
        sys.modules.pop('pyserini._jvm', None)
        self.module_patcher.stop()

    def test_configure_classpath_selects_latest_jar_and_sets_jvm_options(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            older_jar = os.path.join(tmpdir, 'anserini-1-fatjar.jar')
            newer_jar = os.path.join(tmpdir, 'anserini-2-fatjar.jar')
            with open(older_jar, 'w'):
                pass
            with open(newer_jar, 'w'):
                pass

            with patch.object(self.jvm.os.path, 'getctime', side_effect=lambda path: {
                older_jar: 1,
                newer_jar: 2,
            }[path]):
                self.jvm.configure_classpath(tmpdir)

        self.jnius_config.add_classpath.assert_called_once_with(newer_jar)
        self.jnius_config.add_options.assert_any_call('--add-modules=jdk.incubator.vector')
        self.jnius_config.add_options.assert_any_call('--enable-native-access=ALL-UNNAMED')
        self.jnius_config.add_options.assert_any_call('-Dslf4j.internal.verbosity=WARN')

    def test_configure_classpath_rejects_missing_fatjar(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(Exception, 'No matching jar file found'):
                self.jvm.configure_classpath(tmpdir)

    def test_detects_jvm_already_running_errors(self):
        self.assertTrue(self.jvm.is_jvm_already_running_error(Exception('JVM is already running')))
        self.assertTrue(self.jvm.is_jvm_already_running_error(Exception('Java virtual machine is already running')))
        self.assertFalse(self.jvm.is_jvm_already_running_error(Exception('No matching jar file found')))

    def test_suppress_jvm_startup_stderr_hides_native_stderr_writes(self):
        with tempfile.TemporaryFile() as stderr_capture:
            saved_stderr_fd = os.dup(2)
            try:
                os.dup2(stderr_capture.fileno(), 2)
                with self.jvm.suppress_jvm_startup_stderr():
                    os.write(2, b'hidden warning\n')
                os.write(2, b'visible warning\n')
            finally:
                os.dup2(saved_stderr_fd, 2)
                os.close(saved_stderr_fd)

            stderr_capture.seek(0)
            output = stderr_capture.read()

        self.assertNotIn(b'hidden warning', output)
        self.assertIn(b'visible warning', output)

    def test_verbose_jvm_env_keeps_stderr_visible(self):
        with tempfile.TemporaryFile() as stderr_capture:
            saved_stderr_fd = os.dup(2)
            try:
                os.dup2(stderr_capture.fileno(), 2)
                with patch.dict(self.jvm.os.environ, {'PYSERINI_VERBOSE_JVM': '1'}):
                    with self.jvm.suppress_jvm_startup_stderr():
                        os.write(2, b'visible startup warning\n')
            finally:
                os.dup2(saved_stderr_fd, 2)
                os.close(saved_stderr_fd)

            stderr_capture.seek(0)
            output = stderr_capture.read()

        self.assertIn(b'visible startup warning', output)


class TestJvmStartupIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        cls.jar_pattern = os.path.join(
            cls.repo_root, 'pyserini', 'resources', 'jars', 'anserini-*-fatjar.jar'
        )

    def setUp(self):
        if importlib.util.find_spec('jnius_config') is None:
            self.skipTest('jnius_config is not installed')
        if importlib.util.find_spec('jnius') is None:
            self.skipTest('jnius is not installed')
        if shutil.which('java') is None:
            self.skipTest('java is not available')
        if not glob.glob(self.jar_pattern):
            self.skipTest('Anserini fat jar is not available')

    def _run_pyclass_import(self, extra_env=None):
        env = os.environ.copy()
        env['PYTHONPATH'] = (
            self.repo_root if not env.get('PYTHONPATH')
            else self.repo_root + os.pathsep + env['PYTHONPATH']
        )
        if extra_env:
            env.update(extra_env)

        return subprocess.run(
            [
                sys.executable,
                '-c',
                'from pyserini.pyclass import JString; JString("started"); print("started")',
            ],
            cwd=self.repo_root,
            env=env,
            capture_output=True,
            text=True,
        )

    def test_pyclass_import_starts_jvm_without_startup_warnings(self):
        result = self._run_pyclass_import()

        self.assertEqual(
            result.returncode,
            0,
            msg=f'stdout:\n{result.stdout}\nstderr:\n{result.stderr}'
        )
        self.assertIn('started', result.stdout)
        self.assertNotIn('WARNING: Using incubator modules: jdk.incubator.vector', result.stderr)
        self.assertNotIn('SLF4J(I):', result.stderr)

    def test_verbose_jvm_env_still_allows_pyclass_import_to_start_jvm(self):
        result = self._run_pyclass_import({'PYSERINI_VERBOSE_JVM': '1'})

        self.assertEqual(
            result.returncode,
            0,
            msg=f'stdout:\n{result.stdout}\nstderr:\n{result.stderr}'
        )
        self.assertIn('started', result.stdout)


if __name__ == '__main__':
    unittest.main()
