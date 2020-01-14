# coding: utf-8

import os.path
from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import html
import socketserver
from urllib.parse import parse_qs
from io import BytesIO
import sys
from datetime import datetime
from uuid import uuid1


MESSAGE_INTERVAL = 4    # E eilenn
LOG_SIZE = 50           # Niver a c'hemennadenn dre fichennaoueg


KEMENNADENN = """
  <message>
    <id>{}</id>
    <type>{}</type>
    <time>{}</time>
    <host>{}</host>
    <div class="message-container" style="background-color:hsl({}, 60%, 96%);">
      <div class="pseudo-container">
        <div class="pseudo" style="color:hsl({}, 68%, 60%);background-color:hsl({}, 60%, 88%);">{}</div>
      </div>
      <div class="message-body">
        <div class="message-plain">{}</div>
      </div>
    </div>
  </message>"""


XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n'
XML_ROOT_START = "<messages>"
XML_ROOT_END = "\n</messages>"

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.client_address[0] + ':' + str(self.client_address[1])
    
        # Read cookies
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if cookies:
            print(cookies)
        if "last_id" in cookies:
            last_id = cookies["last_id"].value
        else:
            last_id = ""
        
        # Parse query string
        query_dict = {}
        if self.path.find('?') > 0:
            path, query = self.path.split("?")
            query_dict = parse_qs(query)
            print(query_dict)
            if "p" in query_dict and "k" in query_dict:
                # New message received
                pseudo = query_dict["p"][0][:32]   # 32 chars max
                pseudo_lower = pseudo.lower()
                message = query_dict["k"][0]
                if host not in users or users[host]["pseudo"] != pseudo:
                    # User unknown, store new user
                    b = hash(pseudo_lower).to_bytes(8, byteorder='big', signed='signed')
                    s = sum(b)
                    hue = s%360
                    users[host] = {
                                    "pseudo": pseudo,
                                    "hue": hue,
                                    "last_message": datetime.min,
                                    #"num_messages": 0,
                                  }
                    
                # Check the client activity interval,
                # refuse client if too short
                now = datetime.now()
                if (now-users[host]["last_message"]).total_seconds() > MESSAGE_INTERVAL:
                    # Accept and store message
                    users[host]["last_message"] = now
                    #users[host]["num_messages"] += 1
                    print("Message:", message)
                    # ID, "IP:port", deiziat, type, pseudo, kemennadenn
                    content_type = "text"
                    if ('<' in message) and ('>' in message):
                        content_type = "html"
                    messages.insert(0,
                        (str(uuid1()), host, now.isoformat(), content_type, pseudo, message))
        
        else:
            path = self.path
        
        self.send_response(200)
        self.end_headers()
        
        if path == "/clear":
            messages.clear()
            self.wfile.write(pajenn_degemer)
        
        elif path == '/' or path == "/index.html":
            self.wfile.write(pajenn_degemer)
        
        elif path == "/kemennadennou":
            # Goulenn AJAX eus ar c'hliant
            # Adkas ar c'hemennadennoù d'ar c'hliant
            xmldoc = ""
            for m in messages:
                id = m[0]
                if id == last_id:
                    # Don't send older messages than last_id
                    break
                
                hostname = m[1]
                isotime = m[2]
                content_type = m[3]
                pseudo = m[4]
                message = m[5]
                hue = users[hostname]["hue"]   
                xmldoc += KEMENNADENN.format(
                    id,
                    content_type,
                    isotime,
                    hostname,
                    hue,
                    hue,
                    (hue+180)%360,
                    pseudo,
                    message)
            
            if xmldoc:
                response = ""
                response += XML_HEADER
                response += XML_ROOT_START
                response += xmldoc
                response += XML_ROOT_END
                #print("response:", response)
                self.wfile.write(response.encode("utf-8")) ### Kollet eurvezhioù debugiñ evit ur gudenn a indentation amañ :(
            
        else:
            filename = os.path.abspath(os.path.curdir) + path
            try:
                with open(filename, 'rb') as f:
                    self.wfile.write(f.read())
                    
            except FileNotFoundError:
                self.send_error(404, "File not found")


if __name__ == "__main__":
    port = int(sys.argv[1])
    Handler = MyHTTPRequestHandler
    messages = []
    users = {}
    
    with open("kaoz.html", 'rb') as f:
        pajenn_degemer = f.read()
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()
        
