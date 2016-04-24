#!/usr/bin/env python

from imaplib import IMAP4
import time
import re
import json
import daemon

# change these variable values
DEBUG = False
HOSTNAME = 'mail.server.dom'
USERNAME = 'account@server.dom'
PASSWORD = 'passsword'
MAILBOX = 'Inbox'
DATAFILE='/tmp/led.db'
NEWMAIL_OFFSET = 1   # my unread messages never goes to zero, yours might
MAIL_CHECK_FREQ = 30 # check mail every 60 seconds

#do not change bellow this lines

def checkmail():
  try:
    server = IMAP4(HOSTNAME)
    server.login(USERNAME, PASSWORD)
  except:
    print 'connection failed!'
    return

  if DEBUG:
    print('Logging in as ' + USERNAME)
    select_info = server.select(MAILBOX)
    total_email=re.findall(r'\d+(?:[.,]\d+)?', select_info[1][0])
    print('%d messages in %s' % (int(total_email[0]), MAILBOX))

  folder_status = server.status(MAILBOX, '(UNSEEN)')
  total_unseen = re.findall(r'\d+(?:[.,]\d+)?', folder_status[1][0])
  newmails = int(total_unseen[0])

  if DEBUG:
    print "You have", newmails, "new email(s)!"

  if newmails >= NEWMAIL_OFFSET:
    update_signal('new', 11)
  else:
    update_signal('normal', 11)

  time.sleep(MAIL_CHECK_FREQ)

def update_signal(mesg='new', port=12):
  data={'port': int(port), 'mesg': mesg}
  dataserial=json.dumps(data)
  try:
    dbfile=file(DATAFILE, 'w')
    dbfile.write(dataserial)
    dbfile.close()
  except:
    if DEBUG:
      print 'error update datafile.'

def run():
  with daemon.DaemonContext():
    while True:
      checkmail()

if __name__ == '__main__':
    run()
