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
import signal
import requests

"""
"""
SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) for n in dir(signal)
                                     if n.startswith('SIG') and '_' not in n)

def do_fake_request():
    url_get = "http://192.168.1.101:8123/get"
    r = requests.get(url_get)
    # r = requests.get('http://' + HOST_NAME + ':' + str(PORT_NUMBER) +'/get')

def signal_handler(asignal, frame):
    logging.info('Got signal: %s',
        SIGNALS_TO_NAMES_DICT.get(asignal, "Unnamed signal: %d" % asignal))
    global do_handle 
    do_handle = False
    #do_fake_request()

#signal.signal(signal.SIGINT, signal_handler)
#signal.signal(signal.SIGHUP, signal_handler)
#signal.signal(signal.SIGTERM, signal_handler)

def keep_running():
    global do_handle 
    logging.info("Inside keep_running do_handle=%s", do_handle)
    return do_handle 

# HOST_NAME = 'ct-apps01.arc.world' # !!!REMEMBER TO CHANGE THIS!!!
# HOST_NAME = '192.168.1.43' # !!!REMEMBER TO CHANGE THIS!!!
HOST_NAME = socket.gethostname()
PORT_NUMBER = 8123
do_handle = True

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
        self.log_message("post_data=%s", post_data)
        root = ET.fromstring(post_data)
        post_data=urllib.unquote_plus(post_data).replace("data=", "")
        self.log_message("post_data_unquoted=%s", post_data)
        self.log_message("tag=%s", root.tag)
        self.log_message("attrtib=%s", root.attrib)
 

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
                self.log_error("Exception on connect=%s", str(exc))
            else:
                cur = con.cursor()
                self.log_message("SQL to execute=%s", sql_str.encode('utf-8'))
                try:
                    cur.execute(sql_str)
                except BaseException, exc:
                    self.log_error("Exception on INSERT=%s", str(exc))
                con.commit()
                con.close()
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def log_message(self, format, *args):
        loc_str = format%args
        self.logfile.write("%s, %s - - [%s] %s\n"%
            (self.address_string(), 
            self.client_address[0],
            self.log_date_time_string(), 
            loc_str.decode('utf-8')))


if __name__ == '__main__':
    # logging.basicConfig(filename='http-server.log', format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    logging.basicConfig(filename=glob_logname, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), HttpProcessor)
    # Example SSL: httpd.socket = ssl.wrap_socket (httpd.socket, certfile='path/to/localhost.pem', server_side=True)
    logging.info("Server Starts - %s:%s", HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt as exc:
        logging.info("KeyboardInterrupt")
    except Exception as exc:
        #(exc_type, exc_value, exc_traceback) = sys.exc_info()
        #logging.info("Exception type=%s, value=%s, traceback=%\n", exc_type, exc_value, "") #exc_traceback)
        logging.info("Exception=%\n", str(exc))
    """
    while keep_running():
        httpd.handle_request()
    """

    httpd.server_close()
    logging.info("Server Stopped - %s:%s", HOST_NAME, PORT_NUMBER)
