#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import subprocess
import sys
import time
import unittest


class TestMCPyseriniServer(unittest.TestCase):
    
    def setUp(self):
        try:
            self.server_process = subprocess.Popen(
                [sys.executable, '-m', 'pyserini.server.mcp'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            time.sleep(1)
        except Exception as e:
            self.fail(f'Failed to start mcpyserini server: {e}')
    
    def tearDown(self):
        if hasattr(self, 'server_process') and self.server_process:
            if self.server_process.stdin:
                self.server_process.stdin.close()
            if self.server_process.stdout:
                self.server_process.stdout.close()
            if self.server_process.stderr:
                self.server_process.stderr.close()
            
            self.server_process.terminate()

            try:
                # Wait up to 5 seconds for graceful termination
                self.server_process.wait(timeout=5)
                print("Process terminated gracefully")
            except subprocess.TimeoutExpired:
                print("Process didn't terminate gracefully, forcing kill...")
                # Force kill the process
                self.server_process.kill()

                try:
                    # Wait a bit more for the kill to take effect
                    self.server_process.wait(timeout=2)
                    print("Process killed forcefully")
                except subprocess.TimeoutExpired:
                    print("Warning: Process still running after kill attempt")

    def send_mcp_request(self, method, params=None):
        # need to initialize the MCP connection first
        if not hasattr(self, '_initialized'):
            init_request = {
                'jsonrpc': '2.0',
                'id': 0,
                'method': 'initialize',
                'params': {
                    'protocolVersion': '2024-11-05',
                    'capabilities': {},
                    'clientInfo': {
                        'name': 'test-client',
                        'version': '1.0.0'
                    }
                }
            }
            
            try:
                init_json = json.dumps(init_request) + '\n'
                self.server_process.stdin.write(init_json)
                self.server_process.stdin.flush()
                
                init_response = self.server_process.stdout.readline()
                if init_response.startswith("Downloading index at "):
                    init_response = self.server_process.stdout.readline()
                if init_response:
                    json.loads(init_response.strip())
                
                initialized_request = {
                    'jsonrpc': '2.0',
                    'method': 'notifications/initialized'
                }
                initialized_json = json.dumps(initialized_request) + '\n'
                self.server_process.stdin.write(initialized_json)
                self.server_process.stdin.flush()
                
                self._initialized = True
            except Exception as e:
                self.fail(f'Failed to initialize MCP connection: {e}')
        
        request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params or {}
        }
        
        try:
            # Send request
            request_json = json.dumps(request) + '\n'
            self.server_process.stdin.write(request_json)
            self.server_process.stdin.flush()
            
            # Read response
            response_line = self.server_process.stdout.readline()
            if not response_line:
                stderr_output = self.server_process.stderr.read()
                self.fail(f'No response from server. stderr: {stderr_output}')
            
            return json.loads(response_line.strip())
        
        except Exception as e:
            stderr_output = self.server_process.stderr.read()
            self.fail(f'Error communicating with server: {e}. stderr: {stderr_output}')
    
    def test_server_starts(self):
        self.assertIsNotNone(self.server_process)
        self.assertIsNone(self.server_process.poll(), 'Server process should be running')
    
    def test_search_tool(self):
        response = self.send_mcp_request('tools/call', {
            'name': 'search',
            'arguments': {
                'query': 'what is a lobster roll',
                'index_name': 'msmarco-v1-passage',
                'k': 3
            }
        })

        self.assertTrue('result' in response and not response['result']['isError'])
    
    def test_get_index_status_tool(self):
        response = self.send_mcp_request('tools/call', {
            'name': 'get_index_status',
            'arguments': {
                'index_name': 'msmarco-v1-passage'
            }
        })      
        self.assertTrue('result' in response and not response['result']['isError'])

