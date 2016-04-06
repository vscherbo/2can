#!/usr/bin/env python
# -*- coding: utf-8 -

import requests

payment_xml=u"""<Payment Id="18" Amount="1200.00" CreatedAt="2013-09-30T13:34:42.5+04:00" RRN="111111111110" CardType="Visa" TID="" MID="" Card="424242** **** **** 4242" Description="" AuthCode="8e2a73" Status="Completed"><Device Id="66" Name="" Model="Galaxy Gio" /></Payment>"""

void_xml=u"""<Payment Id="19" Amount="1200.00" CreatedAt="2013-09-30T13:36:35.6+04:00" RRN="111111111110" CardType="Visa" TID="" MID="" Card="424242** **** **** 4242" Description="" AuthCode="21eabd" Status="Voided"><Device Id="70" Name="" Model="Galaxy Gio" /></Payment>"""

refund_xml=u"""<Refund Id="23" Amount="500.00" CreatedAt="2013-10-01T13:57:14.9+04:00" RRN="" CardType="Visa" TID="" MID="" Card="424242** **** **** 4242" Payment="22" Reason="Расторжение договора"><Device Id="84" Name="" Model="Galaxy Gio" /></Refund>"""


real_2can="""data=%ef%bb%bf%3cPayment+Id%3d%221672518%22+Amount%3d%2220.00%22+CreatedAt%3d%222016-02-04T12%3a23%3a55.000%2b03%3a00%22+RRN%3d%22603512672518%22+CardType%3d%22Visa%22+TID%3d%2276004196%22+MID%3d%2276004196%22+Card%3d%22427685**+****+****+4779%22+Description%3d%22%d0%a2%d0%b5%d1%81%d1%82%22+AuthCode%3d%22116209%22+Status%3d%22Completed%22%3e%3cDevice+Id%3d%2259157%22+Name%3d%22%22+Model%3d%22Quest+410%22+%2f%3e%3c%2fPayment%3e"""

#url_post = "http://paragpaph.ru:8123/post"
#url_post = "http://217.150.43.11:8123/post"
#url_post = "http://217.150.43.9:8123"

#url_post = "http://2can.kipspb.ru:8123/post"
url_get = "http://ct-apps01.arc.world:8123/get"
url_post = "http://ct-apps01.arc.world:8123/post"

#r = requests.post(url_post, data = payment_xml)
#r = requests.post(url_post, data = void_xml)
r = requests.post(url_post, data = refund_xml.encode('utf-8'))
#r = requests.get(url_get)

print(r.status_code)

                                                                                                                                                     
