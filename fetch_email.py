import imaplib
import base64
import os
import email
import getpass
# from OpenSSL.crypto import load_certificate, FILETYPE_PEM

# https://stackoverflow.com/questions/2230037/how-to-fetch-an-email-body-using-imaplib-in-python

username = "crashlytics@svenmeyer.com"
password = input("Password :")
host = "imap.1und1.de"
port = 993
'''
# def getMsgs(servername=host):
if True:
  usernm = email_user # getpass.getuser()
  passwd = email_pass = "crashlytics" # getpass.getpass()
  # subject = 'Your SSL Certificate'
  imap = imaplib.IMAP4_SSL(host)
'''
from imaplib import IMAP4_SSL

email_message_list = []

with IMAP4_SSL(host) as imap:
  imap.login(username, password)
  imap.list()   # not sure if we need this
  imap.select('Inbox')
  typ, data = imap.search(None, 'ALL')
# typ, data = imap.search(None,'(UNSEEN SUBJECT "%s")' % subject)
  print("typ =", typ)
  if typ == 'OK':
    id_list = data[0].split()
    latest_email_id = id_list[-1] # remember the latest
    if len(id_list) > 0:
      for num in id_list:
        print("num=", num)
        typ, data = imap.fetch(num,'(RFC822)')
        email_raw = data[0][1]# converts byte literal to string removing b''
        email_bytes = email.message_from_bytes(email_raw)
        email_raw_string = email_raw.decode('utf-8')
        email_message = email.message_from_string(email_raw_string)
        
        email_message_list.append(email_message)
        
        # get.body does not work ... so we try to find some html
        # email_body = email_bytes.get_body(preferencelist=('plain', 'html'))
        
        print("email_message.get_content_type() =", email_message.get_content_type())
        email_body_html = ''
        email_body_text = ''
        maintype = email_message.get_content_maintype()
        # if email_message.get_content_type() == 'multipart/alternative':
        # if maintype == 'multipart':
        if True:
            multi_part = email_message
            for part in email_message.walk():
                print(">>>", part.get_content_type() )
                if part.get_content_type() == 'text/html':
                    email_body_html = part.get_payload()
                    # print(email_body_html)
                    continue
# We do not need this as this will be covered by the walk loop
'''                    
        elif email_message.get_content_type() == 'text/html':
            email_body_html = email_message.get_payload()
            
        elif email_message.get_content_type() == 'text/plain':
            email_body_text = email_message.get_payload()
'''         
#       we can mark the message 'seen' if we want
#        typ, data = imap.store(num,'-FLAGS','\\Seen')
#        yield email_message

'''
def getAttachment(msg,check):
  for part in msg.walk():
    if part.get_content_type() == 'application/octet-stream':
      if check(part.get_filename()):
        return part.get_payload(decode=1)

if __name__ == '__main__':
  for msg in getMsgs():
    print("len=", len(msg))


    payload = getAttachment(msg,lambda x: x.endswith('.pem'))
    if not payload:
      continue
    try:
      cert = load_certificate(FILETYPE_PEM,payload)
    except:
      cert = None
    if cert:
      cn = cert.get_subject().commonName
      filename = "%s.pem" % cn
      if not os.path.exists(filename):
        open(filename,'w').write(payload)
        print("Writing to %s" % filename)
      else:
        print("%s already exists" % filename)
'''