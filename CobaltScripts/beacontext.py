#!/usr/bin/env python

import argparse
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

parser = argparse.ArgumentParser(description='beacon info')
parser.add_argument('--computer')
parser.add_argument('--ip')
args = parser.parse_args()

fromaddr = "<gmaile-mailaccounthere>"
toaddr = ["7777777777@txt.att.net", "8888888888@vtext.com"]
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ", ".join(toaddr)
msg['Subject'] = "INCOMING BEACON"

hostname = args.computer
internal_ip = args.ip

body = "Check your teamserver! \nHostname - " + hostname + "\nInternal IP - " + internal_ip
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "<gmailpasswordhere>")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
