import re
from datatype import DataType

def insert(map, dataType, tokens):
    # validate no path in tokens
    if '\\' in tokens[2]:
        return

    if dataType == DataType.MODEL or dataType == DataType.ADDRESS:
        map[tokens[0]] = tokens[2]
    elif dataType == DataType.RELAY:
        cavity = int(tokens[0][5:6])
        cavityString = ''

        if cavity == 1:
            cavityString = 'p'
        else:
            cavityString = 's'

        relay = tokens[0][7:]
        map[cavityString + relay] = tokens[2]
    else:
        raise Exception('unknown data type:', dataType)

def sectionHeader(dataType):
    section = ''

    if dataType == DataType.MODEL:
        section = '\[PhysicalProperties\]'
    elif dataType == DataType.ADDRESS:
        section = '\[Communication\]'
    elif dataType == DataType.RELAY:
        section = '\[RelayMap\]'
    else:
        raise Exception('unknown datatype:', dataType)

    return section

def parseData(lines, dataType):
    reading = False
    data = {}
    section = sectionHeader(dataType)

    for line in lines:
        if re.match(section, line):
            reading = True
        elif reading:
            if not line:
                break
            
            if line[0] == ';':
                continue

            tokens = line.split(' ', 3)
            
            if len(tokens) < 3:
                raise Exception('didnt find 3 tokens', dataType, tokens)
            
            insert(data, dataType, tokens)
    
    return data

def parse(path):
    ini = open(path, 'r')
    lines = [l.strip() for l in ini.readlines()]
    
    modelData = parseData(lines, DataType.MODEL)
    addresses = parseData(lines, DataType.ADDRESS)
    relays = parseData(lines, DataType.RELAY)

    return modelData, addresses, relays

if __name__ == '__main__':
    print(parse('test.ini'))
