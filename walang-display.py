#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import daemon
import json
import os

DATAFILE='/tmp/led.db'

def Blink(mesg="normal", pin=11):
  '''
  Blink led on pin 11 or 12 GPIO
  mesg normal,new,alarm
  '''

  PIN = pin
  GPIO.setmode(GPIO.BOARD)

  signal = {'normal': "", 'new':".", 'alarm':"...---"}
  dot = 0.05
  dash = 0.5
  speed=0
  kode = signal[mesg]
  t=0

  while True:
    t,conf=modification_date(DATAFILE, t)
    if conf:
      PIN=conf['port']
      kode = signal[conf['mesg']]
      print "sending %s on %d port" % (conf['mesg'], conf['port'])
    GPIO.setup(PIN, GPIO.OUT)
    for x in kode:
      if x==".":
        speed=dot
      elif x=="-":
        speed=dash
      elif x==" ":
        continue
      GPIO.output(PIN,True)
      time.sleep(speed)
      GPIO.output(PIN,False)
      time.sleep(dash)
    time.sleep(2*dash)
  GPIO.cleanup()

def run():
  with daemon.DaemonContext():
    Blink()

def modification_date(filename, waktu):
  try:
    t = os.path.getmtime(filename)
  except OSError:
    print "file %s tidak ada. create." % filename
    create_file(filename)
    t=0

  if waktu != t:
    dbfile=file(filename, 'r')
    try:
      jsondata=json.load(dbfile)
      dbfile.close()
      return t,jsondata
    except ValueError:
      print 'data format error'
  return t,False

def create_file(filename):
  dbfile=file(filename, 'w')
  data={'port': 11, 'mesg': 'normal'}
  dataserial=json.dumps(data)
  dbfile.write(dataserial)
  dbfile.close()
  return

if __name__ == '__main__':
  run()
