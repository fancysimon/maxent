
def ReadFileByLine(name):
    '''
    Example usage:

      for line in ReadFileByLine('filename')
          print line
    '''
    f = open(name)
    for line in f:
        line = line.rstrip('\n')
        yield line
    f.close()