#!/usr/local/bin/python2.7
# -*- coding: utf-8 -

# import requests
import codecs
from requests import Request, Session

# https://2can.ru/operations/payments?_nocache=1455096934802&_nocache=1455096934802
# https://2can.ru/operations/payments?_nocache=1455103380856&_nocache=1455103380856
# PrevSortBy=id&PrevSortOrder=Desc&PaymentID=&AuthCode=&FromDate=01.02.2016&ToDate=10.02.2016&DeviceIDs=59157&ReconciliationStatus=Any&ShowCompleted=true&ShowCompleted=false&ShowDeclined=true&ShowDeclined=false&ShowVoided=true&ShowVoided=false'

url='https://2can.ru/signin'


sess = Session()
sess.verify=False
req = Request('GET', 
            url,
            auth=('2can@kipspb.ru', 'M0bile-card'),
)


# _nocache=1455096934802&_nocache=1455096934802
req.params={
'FromDate':'01.02.2016',
'ToDate':'10.02.2016',
'DeviceIDs':'59157',
'ReconciliationStatus':'Any',
'ShowCompleted':'true',
'ShowDeclined':'true',
'ShowVoided':'true',
}

url='https://2can.ru/operations/payments'

prepped = sess.prepare_request(req)
resp = sess.send(prepped)
print resp.status_code

respf=codecs.open('resp.txt', 'w', 'utf-8')
respf.write(resp.text)
respf.close()

print resp.text
"""
print resp.text
print "="
print auth_result
print cookie_file
print cookie_value
print sessid
"""




