#!/usr/bin/env python
# -*- coding: utf-8 -

#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import BaseHTTPServer
import ssl
import urllib
import time
import xml.etree.ElementTree as ET
import psycopg2
import socket
import logging
import sys
import codecs

# HOST_NAME = 'ct-apps01.arc.world' # !!!REMEMBER TO CHANGE THIS!!!
# HOST_NAME = '192.168.1.43' # !!!REMEMBER TO CHANGE THIS!!!
HOST_NAME = socket.gethostname()
PORT_NUMBER = 8123

if HOST_NAME.find('ct-apps') > 0:
   db_host = 'vm-pg'
else:   
   db_host = 'vm-pg-devel'

glob_logname = '2can-httpd.log'
glob_logfile = codecs.open(glob_logname, 'a', 'utf-8', buffering=0)

class HttpProcessor(BaseHTTPServer.BaseHTTPRequestHandler):
    pg_srv = db_host
    logfile = glob_logfile
    # logfile = open('2can-httpd.log', 'a', 0)
    # def __init__(self, logfilename):
    #    self.logfile = open(logfilename, 'a', 0)
    def do_GET(self):
        self.send_response(404)
        self.send_header('content-type','text/html')
        self.end_headers()
        self.wfile.write("page not found")
    def do_POST(self):
        """Respond to a POST request."""
        # Extract and print the contents of the POST
        length = int(self.headers['Content-Length'])
        #post_data = u''
        #post_data += self.rfile.read(length).decode('utf-8')
        post_data = self.rfile.read(length)
        post_data=urllib.unquote_plus(post_data).replace("data=", "")
        self.log_message("post_data={}".format(post_data))
        #root = ET.fromstring(post_data.encode('utf-8'))
        root = ET.fromstring(post_data)
        self.log_message("tag={}".format(root.tag))
        self.log_message("attrtib={}".format(root.attrib))
 

        for child in root:
            ins_dic = root.attrib.keys()
            val_dic = root.attrib.values()
            ins_str = u"INSERT INTO operations2can(tag," 
            val_str = u' VALUES(' + u"'" + root.tag + u"',"
            if 'Device' == child.tag:
                dev_keys = []
                for k in child.attrib.iterkeys():
                    # add tag_name as a prefix to the key to make unique field_name
                    dev_keys.append(child.tag+'_'+k)

                ins_dic += dev_keys
                val_dic += child.attrib.values()

            ins_dic = ['description' if ('Reason' ==  fld) else fld for fld in ins_dic]
            ins_str += u','.join(ins_dic)
            val_dic = [u'NULL' if ( '' ==  v ) else u"'" + v + u"'" for v in val_dic]
            val_str += ','.join(val_dic)

            ins_str += u')'
            val_str += u');'
            sql_str = ins_str + val_str
            # print "sql_str=%s" % sql_str
            con_str = "host='" + self.pg_srv + "' dbname='arc_energo' user='arc_energo'" # password='XXXX' - .pgpass
            # print "con_str=%s" % con_str
            try:
                con = psycopg2.connect(con_str)
            except BaseException, exc:
                self.log_error(" Exception on connect={}".format(str(exc)))
                self.log_message(" SQL to execute=R{}".format(sql_str))

            #TODO check return code
            cur = con.cursor()
            try:
                cur.execute(sql_str)
            except BaseException, exc:
                self.log_error(" Exception on INSERT={}".format(str(exc)))
                self.log_message(" SQL to execute={}".format(sql_str))
            con.commit()
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def log_message(self, a_str):
        #t_args = tuple([a.decode('UTF-8') for a in args])
        #t_args = repr(args).decode('utf-8')
        #print "a_str=", a_str
        # self.logfile.write("%s, %s - - [%s] %s\n" % 
        self.logfile.write("{}, {} - - [{}] {}\n".format(self.address_string(), 
            self.client_address[0],
            self.log_date_time_string(), 
            a_str )) 
            #a_str.encode('utf-8') )) 

if __name__ == '__main__':
    # logging.basicConfig(filename='http-server.log', format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    logging.basicConfig(filename=glob_logname, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), HttpProcessor)
    # Example SSL: httpd.socket = ssl.wrap_socket (httpd.socket, certfile='path/to/localhost.pem', server_side=True)
    logging.info("Server Starts - %s:%s", HOST_NAME, PORT_NUMBER)
    try:
            httpd.serve_forever()
    except KeyboardInterrupt:
            pass
    httpd.server_close()
    logging.info("Server Stops - %s:%s", HOST_NAME, PORT_NUMBER)
