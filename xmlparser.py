#!/usr/bin/python

import argparse
import xml.etree.ElementTree as ET
import telnetlib
import time
from netaddr import *

PORT = 38751
xml_response = None
Header = None

def check_port_number(argv_port):
    if argv_port is None:
        return PORT
    else:
        return argv_port

def enable_debugging(argv_debug):
    if str(argv_debug).strip() == "enable":
        return True
    else:
        return False

def print_header():
    print "Mac Address                  Subscriber Interface                    Elapsed Time"
    print "================================================================================="
    print ""

def get_next_mac(mac, offset):
    return "{:012X}".format(int(mac, 16) + offset)

def convert_mac_address(mac):
    return ':'.join(s.encode('hex') for s in mac.decode('hex'))

parser = argparse.ArgumentParser()
parser.add_argument('-ip', '--ipaddress', help='Please provide the IP Address of the IOSXR router.',
                    required=True)
parser.add_argument('-p', '--port', help='Please provide the port number,\
                    if not then system will pick the DEFAULT port number.', type=int)
parser.add_argument('-u', '--user', help='Please provide user name.', required=True)
parser.add_argument('-pwd', '--password', help='Please provide password.', required=True)
parser.add_argument('-d', '--debug', help='Enable debugging.', choices=['enable'])


args = parser.parse_args()

ip_address = args.ipaddress
port_number = check_port_number(args.port)
user_name = args.user
password = args.password
is_debug = enable_debugging(args.debug)

query = ET.parse("xmlrequest.xml")
root = query.getroot()

xmlcount = 1

try:
    ios_xr_conn = telnetlib.Telnet(ip_address, PORT)
    if is_debug:
        ios_xr_conn.set_debuglevel(1)

    ios_xr_conn.read_until('Username: ')
    ios_xr_conn.write(user_name)
    ios_xr_conn.read_until('Password: ')
    ios_xr_conn.write(password)
    n, match, previous_text = ios_xr_conn.expect([r'User Access Verification', r'\$'], 1)
    if n == 0:
        print "Username and password is incorrect."
        ios_xr_conn.close()
    else:
        while xmlcount <= 500:
            xmlcount += 1
            try:
                xml_str = ET.tostring(root).strip()
                xmlrequest = "<?xml version='1.0' encoding='UTF-8'?>" + xml_str
                ios_xr_conn.write(xmlrequest + "\n")
                xml_response = ios_xr_conn.read_until("XML> ")
                try:
                    fxr = open("xmlresponse.xml", 'w')
                    fxr.write(xml_response.strip()[:-4])
                    fxr.close()
                except IOError:
                    print IOError.message
                query_response = ET.parse("xmlresponse.xml")
                response = query_response.getroot()
                for interface_id in response.iter('InterfaceName'):
                    subs_interface = interface_id.text
                second_query = ET.parse("xml_second_query.xml")
                sq_root = second_query.getroot()
                for interface_name in sq_root.iter("InterfaceName"):
                    interface_name.text = str(subs_interface)
                    second_query.write("xml_second_query.xml")
                second_xml_str = ET.tostring(sq_root).strip()
                sec_xmlrequest = "<?xml version='1.0' encoding='UTF-8'?>" + second_xml_str
                ios_xr_conn.write(sec_xmlrequest + "\n")
                xml_response = ios_xr_conn.read_until("XML> ")
            except IOError:
                print IOError.message
            start_time = time.time()
            for subs in root.iter('Username'):
                next_subscriber = str(get_next_mac(str(subs.text).replace(".", ""), 1))
                subs_mac_address = convert_mac_address(next_subscriber)
                mac_address = EUI(subs_mac_address, dialect=mac_cisco)
                subs.text = str(mac_address)
                query.write("xmlrequest.xml")
                end_time = time.time()
                if not is_debug:
                    if Header is None:
                        Header = True
                        print_header()
                    else:
                        elapsed_time = (end_time - start_time)
                        print str(mac_address) + "             " + str(subs_interface) + "             " + str(
                            elapsed_time)
except EOFError:
    print EOFError.message
ios_xr_conn.close()