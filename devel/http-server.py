#!/usr/bin/env python
# -*- coding: utf-8 -

#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import BaseHTTPServer
import ssl
import urllib
import time
import xml.etree.ElementTree as ET
import psycopg2

# HOST_NAME = 'ct-apps01.arc.world' # !!!REMEMBER TO CHANGE THIS!!!
HOST_NAME = '192.168.1.43' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8123



class HttpProcessor(BaseHTTPServer.BaseHTTPRequestHandler):
    pg_srv = 'vm-pg'
    def do_GET(s):
        s.send_response(200)
        s.send_header('content-type','text/html')
        s.end_headers()
        s.wfile.write("hello !")
    def do_POST(s):
        """Respond to a POST request."""
        # Extract and print the contents of the POST
        length = int(s.headers['Content-Length'])
        #post_data = u''
        #post_data += s.rfile.read(length).decode('utf-8')
        post_data = s.rfile.read(length)
        post_data=urllib.unquote_plus(post_data).replace("data=", "")
        print "post_data="
        print post_data #.encode('utf-8')
        #root = ET.fromstring(post_data.encode('utf-8'))
        root = ET.fromstring(post_data)
        print u"tag=%s" % root.tag
        print u"attrib=%s" % root.attrib
 

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
            con_str = "host='" + s.pg_srv + "' dbname='arc_energo' user='arc_energo'" # password='XXXX' - .pgpass
            # print "con_str=%s" % con_str
            try:
                con = psycopg2.connect(con_str)
            except:
                print "I am unable to connect to the database"

            #TODO check return code
            cur = con.cursor()
            try:
                cur.execute(sql_str)
            except:
                print "ERROR while INSERT"
            con.commit()
        
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), HttpProcessor)
    # Example SSL: httpd.socket = ssl.wrap_socket (httpd.socket, certfile='path/to/localhost.pem', server_side=True)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
            httpd.serve_forever()
    except KeyboardInterrupt:
            pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
