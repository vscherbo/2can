#!/usr/bin/env python2.7
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
from daemon import runner
import datetime

# HOST_NAME = 'ct-apps01.arc.world' # !!!REMEMBER TO CHANGE THIS!!!
# HOST_NAME = '192.168.1.43' # !!!REMEMBER TO CHANGE THIS!!!
HOST_NAME = socket.gethostname()
PORT_NUMBER = 8123


if HOST_NAME.find('ct-apps') >= 0:
    db_host = 'vm-pg'
    cfg_wrk_dir = '/opt/2can'
else:   
    db_host = 'vm-pg-devel'
    cfg_wrk_dir = '/smb/system/Scripts/2can/devel'

glob_logname = cfg_wrk_dir + '/httpd-2can.log'

class HttpProcessor(BaseHTTPServer.BaseHTTPRequestHandler):
    pg_srv = db_host
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
        # self.log_message("post_data_unquoted=%s", post_data)
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
    def log_date_time_string(self):
        return datetime.datetime.now()
    """
    def log_message(self, format, *args):
        loc_str = format%args
        self.server.logfile = daemon_runner.daemon_context.stderr
        self.server.logfile.write("%s, %s - - %s %s\n"%
            (self.log_date_time_string(), 
            self.address_string(), 
            self.client_address[0],
            loc_str.decode('utf-8')))
    """

class httpd2can():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path =  cfg_wrk_dir + '/httpd-2can.pid'
        self.pidfile_timeout = 5
            
    def run(self):
        server_class = BaseHTTPServer.HTTPServer
        self.httpd = server_class((HOST_NAME, PORT_NUMBER), HttpProcessor)
        # Example SSL: httpd.socket = ssl.wrap_socket (httpd.socket, certfile='path/to/localhost.pem', server_side=True)
        logger.info("Server Starts - %s:%s", HOST_NAME, PORT_NUMBER)

        try:
            self.httpd.serve_forever()
        except Exception as exc:
            (exc_type, exc_value, exc_traceback) = sys.exc_info()
            logger.info("Exception type=%s, value=%s, traceback=%s", exc_type, exc_value, exc_traceback)
        finally:
            self.httpd.server_close()
            logger.info("Server Stopped - %s:%s", HOST_NAME, PORT_NUMBER)
            

if __name__ == '__main__':

    logger = logging.getLogger("httpd-2can")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler(glob_logname)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    app = httpd2can()

    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.daemon_context.stdout = handler.stream
    daemon_runner.daemon_context.stderr = handler.stream
    #This ensures that the logger file handle does not get closed during daemonization
    daemon_runner.daemon_context.files_preserve = [handler.stream]
    daemon_runner.daemon_context.working_directory = cfg_wrk_dir
    daemon_runner.daemon_context.umask = 0o002
    daemon_runner.do_action()

