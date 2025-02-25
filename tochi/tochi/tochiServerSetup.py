from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from .aiEngine import natural_to_sql 
from dotenv import load_dotenv
import os

from .utility import extract_values
from .pgdbConnector import execute_sql_query

class RequestHandeler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path  ==  "/query":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
        
            try:
                data = json.loads(post_data)

                if "query" not in data:
                    self.send_error(400, "Bad Request: 'query' is required")
                    return
                
                natural_quary = data["query"]
                
                load_dotenv("./.env")
                api_key = os.getenv("API_KEY")
                
                sql_query = natural_to_sql(natural_quary, api_key)
                values = extract_values(natural_quary)
                
                
                print(execute_sql_query(sql_query, values))

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"sql_query": sql_query}).encode("utf-8"))    
            except Exception as e:
                print(F'Error form tochiServerSetup File: {e}')


    def do_get(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Tochi server is running...")
        else:
            self.send_error(404, "Not Found: This endpoint does not exist.")


    