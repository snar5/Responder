from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import sqlite3
import settings
import urlparse
from os import curdir, sep

from www.header import * 
from www.body import * 
from www.scripts import * 
from www.footer import * 

enabled = "<font color='green'>[ON]</font>"
disabled = "<font color='red'>[OFF]</font>"

class Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def log_message(self, format, *args):
        return 

    def do_GET(self):
	option = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('option', None)
	urlParams = urlparse.urlparse(self.path)
	if self.path.endswith(".js"):
		mimetype = 'application/javascript'
		path = 'servers' + self.path
		f = open (path)
		data = f.read()
		f.close()
		self.send_response(200) 
		self.send_header('Content-type', mimetype) 
		self.end_headers() 
		self.wfile.write(data)
		return 

	if self.path.endswith(".gif"):
		mimetype = 'image/gif'
		path = curdir + sep + self.path
		f = open (path)
		self.send_response(200)
		self.send_header('Content-type', mimetype)
		self.end_headers()
		self.wfile.write(f.read())
		f.close()
		return 

	if self.path.endswith(".css"):
                mimetype = 'text/css'
                path = "servers" + self.path
                f = open (path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
		return 
	if self.path.endswith(".png"):
                mimetype = 'image/png'
                path = 'servers' + self.path
		f = open (path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

	if option is None: 
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		#self.wfile.write(page_alt)
		self._build_page()

	# -- Ajax Calls 

	elif option[0] == "clear_poison": # Clear Poison Table
		self._conn = self._connect_to_database()
		self._reset_poisoned(self._conn)
		self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

	elif option[0] == "dump_hashes": #Dump Database Hashes
		self._conn = self._connect_to_database() 
		rst_hash_dump = self._cred_dump(self._conn)
		self.send_response(200) 
		self.send_header('Content-type','text/html')
		self.end_headers() 
		for rst in rst_hash_dump:
			self.wfile.write("{0}<br>n".format(rst[0])); 
		
	elif option[0] == "captured_creds": # List Captured Creds 
		self._conn = self._connect_to_database() 
		rst_captured_creds = self._get_creds_list(self._conn)
		self.send_response(200) 
		self.send_header('Content-type','text/html') 
		self.end_headers() 
		self.wfile.write("<table><tr><th>User</th><th>Type</th><th>Client</th><th>Date</th></tr>")
        	for rst in rst_captured_creds:
                	self.wfile.write("<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(rst[0],rst[1],rst[2],rst[3]))
		self.wfile.write("</table>")

	elif option[0] == "poison_details":
		self._conn = self._connect_to_database() 
		rst_poison_details = self._get_poisoner_details(self._conn)
		self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
		self.wfile.write("<table><tr><th>Victim IP</th><th>Number of Poisons</th></tr>")
		for rst in rst_poison_details:
			self.wfile.write("<tr><td>{0}</td><td>{1}</td></tr>".format(rst[0],rst[1]))
		self.wfile.write("</table>")

	elif option[0] == "poison_count":
		self._conn = self._connect_to_database()	
		rst_poison = self._get_poison_stats(self._conn)
		self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
		title = ''
		for rst in rst_poison:
			title = title + "{0} {1}\n".format(rst[0],rst[1])
		self.wfile.write("<a href='#' title='" + title + "'> Poisoned </a>")
	
	elif option[0] == "cred_count":
		self._conn = self._connect_to_database() 
		rst_creds = self._get_cred_stats(self._conn)
		self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
		title = ''
                for rst in rst_creds:
                        title = title + "{0} {1} {2}\n".format(rst[0],rst[1],rst[2])
                self.wfile.write("<a href='#' title='" + title + "'> Card Type Captured</a>")

	elif option[0] == "request_names":
		self._conn = self._connect_to_database()
		rst_names_list = self._get_request_names(self._conn) 
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write("<table><tr><th>Requested Names</th><th>Number of Requests</th></tr>")
		for rst in rst_names_list:
                	self.wfile.write("<tr><td>{0}</td><td>{1}</td></tr>".format(rst[0],rst[1]))
		self.wfile.write("</table>")

	# -- End Ajax Calls 
	# -- First CALL TO BE MADE IS GET info 

	elif option[0] == "getIP":
		self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
		self.wfile.write("You are using interface: <b><u>{1}</u></b> | You are listening on:  <b><u>{0}</u></b>".format(settings.Config.Bind_To,settings.Config.Interface))

    def _build_page(self):

# --- Base Page Creation before all AJAX calls to fill in tabs etc. 

	self.wfile.write(page_header)
	self.wfile.write(page_body)
	
	# Menu of Buttons on Side 

	self.wfile.write("<nav>")
	self.wfile.write("<button id='btnHash' class='ui-button ui-corner-all ui-widget'>")
	self.wfile.write("<span class='ui-icon ui-icon-newwin'></span> Display Hashes</button>")
	self.wfile.write("<button id='btnClearCounters' class='ui-button ui-corner-all ui-widget'>")
        self.wfile.write("<span class='ui-icon ui-icon-info'></span> Clear Counters</button>")
	self.wfile.write("</nav>\n")
	
	# Main Area of Page holding tabs 

	self.wfile.write("<article>") 
	self.wfile.write("<div id='tabs'>")
	self.wfile.write("<ul>")
	self.wfile.write("<li><span id='bubble_cap_cred' class='r-badge'></span><a href='#tabs-1'>Captured Credentials Details</a></li>")
	self.wfile.write("<li><span id='bubble_poison' class='r-badge'></span><a href='#tabs-2'>Poisoner Details</a></li>") 
	self.wfile.write("<li><span id='bubble_names'  class='r-badge'></span><a href='#tabs-3'>Requested Names</a></li>")
	self.wfile.write("<li><a href='#tabs-4'>Running Servers</a></li>")  
	self.wfile.write("</ul>") 

	self.wfile.write("<div id='tabs-1'></div>")
	self.wfile.write("<div id='tabs-2'></div>")
	self.wfile.write("<div id='tabs-3'></div>")
	self.wfile.write("<div id='tabs-4'>")
	self.wfile.write("<table>")
        self.wfile.write("<tr><td>HTTP:</td><td>{0}</td></tr>".format(enabled if settings.Config.HTTP_On_Off else disabled))
        self.wfile.write("<tr><td>HTTPS:</td><td>{0}</td></tr>".format(enabled if settings.Config.SSL_On_Off else disabled))
        self.wfile.write("<tr><td>WPAD:</td><td>{0}</td></tr>".format(enabled if settings.Config.WPAD_On_Off else disabled))
        self.wfile.write("<tr><td>AUTH Proxy:</td><td>{0}</td></tr>".format(enabled if settings.Config.ProxyAuth_On_Off else disabled))
        self.wfile.write("<tr><td>SMB  Server:</td><td>{0}</td></tr>".format(enabled if settings.Config.SMB_On_Off else disabled))
        self.wfile.write("<tr><td>Kerberos Server:</td><td>{0}</td></tr>".format(enabled if settings.Config.Krb_On_Off else disabled))
        self.wfile.write("<tr><td>SQL Server:</td><td>{0}</td></tr>".format(enabled if settings.Config.SQL_On_Off else disabled))
        self.wfile.write("<tr><td>FTP Server:</td><td>{0}</td></tr>".format(enabled if settings.Config.FTP_On_Off else disabled))
        self.wfile.write("<tr><td>IMAP Server:</td><td>{0}</td></tr>".format(enabled if settings.Config.IMAP_On_Off else disabled))
        self.wfile.write("<tr><td>POP3 Server:</td><td>{0}</td></tr>".format(enabled if settings.Config.POP_On_Off else disabled))
        self.wfile.write("<tr><td>SMTP Server:</td><td>{0}</td></tr>".format(enabled if settings.Config.SMTP_On_Off else disabled))
        self.wfile.write("<tr><td>DNS Server:</td><td>{0}</td></tr>".format(enabled if settings.Config.DNS_On_Off else disabled))
        self.wfile.write("<tr><td>LDAP Server:</td><td>{0}</td></tr>".format(enabled if settings.Config.LDAP_On_Off else dsiabled))	
	self.wfile.write("</table>")
	self.wfile.write("</div>")

	self.wfile.write("</div></article>") 

	self.wfile.write(page_footer) 
    
# --  Database Connection Methods 

    def _connect_to_database(self):
	conn = sqlite3.connect("./Responder.db")
	return conn
    def _get_db_stats(self,conn):
	results = conn.execute("Select DISTINCT user from Responder;")
	return results.fetchall()
    def _get_cred_stats(self,conn):
	results = conn.execute("SELECT DISTINCT type,module, COUNT(type) as countof from responder group by type;")
	return results.fetchall()
    def _get_poison_stats(self,conn):
	results = conn.execute("select DISTINCT Poisoner, COUNT(Poisoner) as countof from Poisoned group by Poisoner;")
	return results.fetchall()
    def _get_creds_list(self,conn):
	results = conn.execute("select user,type,client,timestamp from responder;")
        return results.fetchall()
    def _get_details(self,conn):
	results = conn.execute("select user,type,client,timestamp from responder;")
	return results.fetchall()
    def _get_poisoner_details(self,conn):
	results = conn.execute("SELECT DISTINCT SentToIp, COUNT(SentToIp) As Countof FROM Poisoned group by SentToIp;")
	return results.fetchall()
    def _get_request_names(self,conn):
	results = conn.execute("SELECT DISTINCT ForName, COUNT(ForName) as CountOf FROM Poisoned group by ForName;")
	return results.fetchall()
    def _cred_dump(self,conn):
	results = conn.execute("SELECT fullhash FROM Responder WHERE UPPER(user) in (SELECT DISTINCT UPPER(user) FROM Responder) order by type")
	return results.fetchall()
    def _reset_poisoned(self,conn):
	print "Clearing Database"
	conn.execute("Delete from Poisoned;")
	conn.commit()
	return


def run(server_class=HTTPServer, handler_class=Server, port=880):
   server_address = ('', port)
   httpd = server_class(server_address, handler_class)
   httpd.serve_forever()
