# hardcoded values
SERVERS_1_10: list = ['UPHAPPNDC638']  # there are others
SERVERS_2_1: list = ['UPHHEMERAPP001']  # there are others
VERSION_2_1: str = '2.1'
VERSION_1_10: str = '1.10'
INCOMING: str = '-><'
OUTGOING: str = '<-<'


def __init__():
  pass


class Message:
  """logMessage class"""

  def __init__(self, line):
    self.isASTM: bool = False
    self.isIncoming: bool = False
    self.version: str = ''
    self.ASTMLine: str = ''
    self.timestamp: str = ''
    self.pid: str = ''
    self.server: str = ''
    self.contents: str = ''
    self.originalLine = line
    self.splitLine = line.split('|')

    # get the metadata

    # determine the version
    if len(self.splitLine) > 2 and self.splitLine[2] in SERVERS_2_1:
      self.version = '2.1'
    elif len(self.splitLine) > 3 and self.splitLine[3] in SERVERS_1_10:
      self.version = '1.10'

    # save timestamp and PID
    if self.version == VERSION_2_1:
      self.timestamp = self.splitLine[1]
      self.pid = self.splitLine[3]
      self.server = self.splitLine[2]

      for lines in range(4, len(self.splitLine)):
        self.contents = self.contents + self.splitLine[lines] + '|'
      self.contents = self.contents[:len(self.contents) - 2]

    elif self.version == VERSION_1_10:
      self.timestamp = self.splitLine[1] + '.' + self.splitLine[2]
      self.pid = self.splitLine[4]
      self.server = self.splitLine[3]

      for lines in range(5, len(self.splitLine)):
        self.contents = self.contents + self.splitLine[lines] + '|'
      self.contents = self.contents[:len(self.contents) - 2]

    # find the ASTM delimiter INCOMING or OUTGOING
    incomingIndex = self.originalLine.find(INCOMING)
    outgoingIndex = self.originalLine.find(OUTGOING)
    if incomingIndex != -1 or outgoingIndex != -1:
      self.isASTM = True

    fullLength: int = len(self.originalLine)
    if incomingIndex != -1:
      self.isASTM = True
      self.isIncoming = True
      self.ASTMLine = self.originalLine[incomingIndex + 2:fullLength - 1]

    if outgoingIndex != -1:
      self.isASTM = True
      self.ASTMLine = self.originalLine[outgoingIndex + 2:fullLength - 1]

  def toString(self):
    return self.originalLine

  def getSplit(self):
    print(self.splitLine)

  def getVersion(self):
    return self.version

  def getASTMString(self):
    return self.ASTMLine

  def getTimestamp(self):
    return self.timestamp

  def getPID(self):
    return self.pid

  def getContents(self):
    return self.contents

  def getServer(self):
    return self.server
