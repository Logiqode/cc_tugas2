import http.server
import socketserver
import json
import mysql.connector
import time

PORT = 8008
DB_HOST = "db"
DB_USER = "root"
DB_PASS = "secretpassword"
DB_NAME = "currency_db"

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
            )
            return conn
        except:
            print("Waiting for Database...")
            time.sleep(5)
            retries -= 1
    return None

conn = get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (id INT AUTO_INCREMENT PRIMARY KEY, conversion TEXT)")
    conn.close()

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/save':
            length = int(self.headers['Content-Length'])
            
            data = json.loads(self.rfile.read(length))
            
            entry = f"{data['amount']} USD = {data['result']} IDR"
            
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO history (conversion) VALUES (%s)", (entry,))
                conn.commit()
                conn.close()
                print(f"Saved to DB: {entry}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Saved")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()