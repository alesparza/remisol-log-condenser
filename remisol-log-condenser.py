import getopt
import os
import sys

from openpyxl import Workbook

import logMessage

DEBUG: bool = False
USAGE: str = """usage: remisol-log-condenser.py -i <inputfile> -o <outputfile> 
alt-usage: remisol-log-condenser.py -d <directory>
optional flag: -f <ALL|ASTM>"""


def parseDir(dirSource):
  """
  Parses an entire directory
  """
  masterLines: list[logMessage] = []
  files: list = os.listdir(dirSource)
  for f in files:
    print('Next file: {}'.format(f))
    inputFile: str = dirSource + '\\' + f
    newLines: list[logMessage] = parseLog(inputFile)
    for line in newLines:
      masterLines.append(line)


  # get all the files in the directory
  # parse the viewer, append to master list
  # return master list
  return masterLines


def writeFile(data,outputFile, save):
  print('Writing file {}...'.format(outputFile))
  # write to excel
  nb: Workbook = Workbook(write_only=True)
  ns = nb.create_sheet()
  # write header
  ns.append(['Timestamp', 'Server', 'Process ID', 'Contents'])
  # write lines

  for line in data:
    if save == 'ALL':
      ns.append([line.getTimestamp(), line.getServer(), line.getPID(), line.getContents()])
    elif save == 'ASTM' and line.isASTM:
      ns.append([line.getTimestamp(), line.getServer(), line.getPID(), line.getContents()])
  nb.save(outputFile)
  nb.close()
  print('Wrote to file!')


def parseLog(inputFile):
  """
  Parses an input file
  """
  print('Parsing {}'.format(inputFile))
  f = open(inputFile, 'r')
  lines: list[logMessage] = []
  # convert the lines to Message objects
  for line in f:
    message: logMessage = logMessage.Message(line)
    lines.append(message)

  # print an example line for debugging
  if DEBUG and len(lines) > 16:
    message: logMessage = lines[17]
    print('test line: {}'.format(message.toString()))
    message.getSplit()
    print('Version: {}'.format(message.getVersion()))
    print('Server: {}'.format(message.getServer()))
    print('ASTM: {}'.format(message.isASTM))
    print('Incoming: {}'.format(message.isIncoming))
    print('ASTM string: {}'.format(message.getASTMString()))
    print('Timestamp: {}'.format(message.getTimestamp()))
    print('PID: {}'.format(message.getPID()))
    print('Contents: {}'.format(message.getContents()))

  return lines

# main method
def main(argv):
  """
  This program will read in an .xlsx or .csv and parse out the Order or
  Manufacturer messages.  It also adds some headers for easier pivot tableing.
  Do note the dependencies.
  """
  print('Remisol Log Condenser')
  if DEBUG:
    print('Argument count: ' + str(len(argv)))
    print('Arguments: ' + str(argv))

  # set up some defaults
  inputFile: str = ''
  outputFile: str = 'output.xlsx'
  dirSource: str = ''
  save: str = 'ALL'

  # get the arguments for input and output file
  try:
    opts, args = getopt.getopt(argv, 'hi:o:s:d:f:', ['input=', 'output=', 'dir=', 'format='])

  except getopt.GetoptError:
    print(USAGE)
    sys.exit(2)

  for opt, arg in opts:
    if DEBUG:
      print('Parsing option {} and argument {}'.format(opt, arg))
    if opt == '-h':
      print(USAGE)
      sys.exit(2)
    elif opt in ('-d', '--dir'):
      dirSource = arg
    elif opt in ('-i', '--input'):
      inputFile = arg
    elif opt in ('-o', '--output'):
      outputFile = arg
    elif opt in ('-f', '--format'):
      save = arg

  if DEBUG:
    print('Input file: ' + inputFile)
    print('Output file: ' + outputFile)
    print('Directory source: ' + dirSource)
    print('Format: ' + save)

  # quit if there is no input file or directory source
  if inputFile == '' and dirSource == '':
    print(USAGE)
    sys.exit(2)

  if save not in ['ALL', 'ASTM', '']:
    print('Format must be ALL or ASTM')
    print(USAGE)
    sys.exit(5)

  # handle directory files first
  if dirSource != '':
    if DEBUG:
      print('Processing files in directory {}'.format(dirSource))
    mergedLines: list[logMessage] = parseDir(dirSource)
    writeFile(mergedLines, outputFile, save)
    print('Bye bye')
    sys.exit(0)

  if '.txt' not in inputFile:
    print('Only works with .txt input files')
    print(USAGE)
    sys.exit(3)



  # otherwise handle the single input file
  else:
    logLines: list[logMessage] = parseLog(inputFile)
    writeFile(logLines, outputFile, save)
    print('Bye bye')
    sys.exit(0)


# runs main
if __name__ == '__main__':
  main(sys.argv[1:])
