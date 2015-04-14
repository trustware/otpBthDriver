import os
import signal
import subprocess
import time


def main():
  # Run Bluetooth LE scan tool and write output to file
  print 'Scanning BTLE...'
  shellCmdToFile('hcitool lescan', 1.5, '.scanOutput', '.scanErr')

  # Read output and remove temp files
  with open('.scanOutput', 'r') as fileOut:
    linesOut = fileOut.readlines()
  with open('.scanErr', 'r') as fileErr:
    linesErr = fileErr.readlines()
  os.remove('.scanOutput')
  os.remove('.scanErr')

  # Try to catch common problems
  if len(linesErr) > 0:
    if linesErr[0] == 'Set scan parameters failed: Operation not permitted\n':
      print 'BTLE scanning failed; did you run this script as root?'
      return
    if linesErr[0] == 'Set scan parameters failed: Input/output error\n':
      print 'BTLE scanning failed; trying restarting the local hardware device'
      return
    if len(linesOut) == 0:
      print 'BTLE scanning failed for an unknown reason. Error log:'
      for line in linesErr:
        print line
      return

  # Parse scan output. Each device is a tuple (hardware address, name)
  devices = []
  for line in linesOut[1:]:
    parts = line.split(' ')
    if len(parts) != 2 or len(parts[1]) < 14:
      continue
    devices.append((parts[0], parts[1][:-1]))

  # Identify valid Trustware devices. Valid device data consists of three
  # concatenated strings: TOTP (6 chars), UID (8 chars), company URL (12 chars).
  # Result is a list of tuples (UID, TOTP, company URL)
  trustWareDevices = []
  for device in devices:
    totp = device[1][:6]
    uid = device[1][6:14]
    url = device[1][14:]
    if not totp.isdigit() or not totp.isdigit():
      continue
    trustWareDevices.append((uid, totp, url))
  
  print trustWareDevices


def shellCmdToFile(command, duration, nameOut, nameErr):
  # Run shell command with output piped to file
  fileOut = open(nameOut, 'w')
  fileErr = open(nameErr, 'w')
  process = subprocess.Popen(command.split(), stdout=fileOut, stderr=fileErr)

  # Terminate process after x seconds and wait a moment to write output files
  time.sleep(duration)
  try:
    process.send_signal(signal.SIGINT)
  except OSError as e:
    pass
  time.sleep(0.5)
  fileOut.close()
  fileErr.close()


if __name__ == "__main__":
  main()
