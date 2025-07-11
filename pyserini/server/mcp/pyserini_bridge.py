#!/usr/bin/env python3
import sys
import json
import requests

class PyseriniToolsBridge:
    def __init__(self):
        self.session = requests.Session()
        self.session_id = None
        print("Pyserini tools bridge started", file=sys.stderr)
        sys.stderr.flush()
        
    def setup_pyserini_session(self):
        """Initialize connection to pyserini server"""
        if self.session_id:
            return True
            
        print("Setting up pyserini session", file=sys.stderr)
        sys.stderr.flush()
        
        try:
            init_data = {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "claude-bridge", "version": "1.0.0"}
                }
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/event-stream'
            }
            response = self.session.post('http://localhost:8000/mcp/', 
                                       json=init_data, 
                                       headers=headers, 
                                       timeout=10)
            
            self.session_id = response.headers.get('mcp-session-id')
            print(f"Got session ID: {self.session_id}", file=sys.stderr)
            sys.stderr.flush()
            
            if self.session_id:
                # Send initialized notification
                headers['mcp-session-id'] = self.session_id
                init_notify = {
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                    "params": {}
                }
                self.session.post('http://localhost:8000/mcp/', 
                                json=init_notify, 
                                headers=headers, 
                                timeout=5)
                return True
                
        except Exception as e:
            print(f"Pyserini setup failed: {e}", file=sys.stderr)
            sys.stderr.flush()
            
        return False
        
    def handle_message(self, data):
        """Handle individual JSON-RPC messages"""
        method = data.get("method", "")
        
        if method == "initialize":
            print("Handling initialize", file=sys.stderr)
            sys.stderr.flush()
            
            return {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": False}
                    },
                    "serverInfo": {
                        "name": "pyserini-tools-bridge",
                        "version": "1.0.0"
                    }
                }
            }
            
        elif method == "tools/list":
            print("Handling tools/list", file=sys.stderr)
            sys.stderr.flush()
            
            # Get tools from pyserini server
            if not self.setup_pyserini_session():
                return {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {"tools": []}
                }
            
            try:
                tools_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list",
                    "params": {}
                }
                
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json, text/event-stream',
                    'mcp-session-id': self.session_id
                }
                
                response = self.session.post('http://localhost:8000/mcp/',
                                           json=tools_request,
                                           headers=headers,
                                           timeout=10)
                
                # Parse streaming response
                for line in response.text.split('\n'):
                    if line.startswith('data: '):
                        try:
                            result = json.loads(line[6:])
                            if "result" in result and "tools" in result["result"]:
                                tools = result["result"]["tools"]
                                print(f"Got {len(tools)} tools from pyserini", file=sys.stderr)
                                sys.stderr.flush()
                                
                                return {
                                    "jsonrpc": "2.0",
                                    "id": data.get("id"),
                                    "result": {"tools": tools}
                                }
                        except json.JSONDecodeError:
                            continue
                            
            except Exception as e:
                print(f"Failed to get tools: {e}", file=sys.stderr)
                sys.stderr.flush()
            
            return {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": {"tools": []}
            }
            
        elif method == "tools/call":
            print("Handling tools/call", file=sys.stderr)
            sys.stderr.flush()
            
            params = data.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            print(f"Calling pyserini tool: {name} with args: {arguments}", file=sys.stderr)
            sys.stderr.flush()
            
            # Forward the tool call directly to pyserini
            if not self.setup_pyserini_session():
                return {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "error": {"code": -32603, "message": "Failed to connect to pyserini"}
                }
            
            try:
                tool_request = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": name,
                        "arguments": arguments
                    }
                }
                
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json, text/event-stream',
                    'mcp-session-id': self.session_id
                }
                
                response = self.session.post('http://localhost:8000/mcp/',
                                           json=tool_request,
                                           headers=headers,
                                           timeout=30)
                
                # Parse streaming response
                for line in response.text.split('\n'):
                    if line.startswith('data: '):
                        try:
                            result = json.loads(line[6:])
                            if "result" in result:
                                print(f"Got result from pyserini", file=sys.stderr)
                                sys.stderr.flush()
                                return {
                                    "jsonrpc": "2.0",
                                    "id": data.get("id"),
                                    "result": result["result"]
                                }
                            elif "error" in result:
                                print(f"Got error from pyserini: {result['error']}", file=sys.stderr)
                                sys.stderr.flush()
                                return {
                                    "jsonrpc": "2.0",
                                    "id": data.get("id"),
                                    "error": result["error"]
                                }
                        except json.JSONDecodeError:
                            continue
                            
            except Exception as e:
                print(f"Tool call failed: {e}", file=sys.stderr)
                sys.stderr.flush()
                
            return {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "error": {"code": -32603, "message": "Tool call failed"}
            }
            
        elif method.startswith("notifications/"):
            print(f"Received notification: {method}", file=sys.stderr)
            sys.stderr.flush()
            return None
            
        else:
            print(f"Unknown method: {method}", file=sys.stderr)
            sys.stderr.flush()
            return {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
    
    def run(self):
        """Main loop to handle JSON-RPC messages"""
        print("Starting message loop", file=sys.stderr)
        sys.stderr.flush()
        
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    print("No more input, exiting", file=sys.stderr)
                    break
                    
                line = line.strip()
                if not line:
                    continue
                    
                print(f"Received: {line[:100]}...", file=sys.stderr)
                sys.stderr.flush()
                
                try:
                    data = json.loads(line)
                    response = self.handle_message(data)
                    
                    if response:
                        output = json.dumps(response)
                        print(output)
                        sys.stdout.flush()
                        print(f"Sent response for {data.get('method')}", file=sys.stderr)
                        sys.stderr.flush()
                        
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}", file=sys.stderr)
                    sys.stderr.flush()
                    
        except Exception as e:
            print(f"Main loop error: {e}", file=sys.stderr)
            sys.stderr.flush()

if __name__ == "__main__":
    bridge = PyseriniToolsBridge()
    bridge.run()