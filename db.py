import psycopg2 as pp
from datatype import DataType

class db():
    def __init__(self):
        self.db = 'test'
        self.uname = 'andrew'
        dbFile = open('pwd_db')
        self.pw = dbFile.readLine().strip()

    def setup(self):
        self.conn = pp.connect('dbname=' + self.db + ' user=' + self.uname)
        self.cur = self.conn.cursor()

    def cleanup(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def buildTables(self):
        pass

    def insert(self, dataType, map):
        keys = map.keys()
        cols = '(' + ', '.join(keys) + ')'
        types = '(' + '%s, ' * (len(keys) - 1) + '%s)'

        if dataType == DataType.MODEL:
            table = 'model'
        elif dataType == DataType.ADDRESS:
            table = 'address'
        elif dataType == DataType.RELAY:
            table = 'relay'
        else:
            raise Exception('unkown data type:', dataType)

        self.cur.execute('insert into ' + table + ' ' + cols + ' VALUES ' + types, map.values)

if __name__ == '__main__':
    test = db()
    test.setup()
    map = {'ApplianceType': 'Range', 'OvenUI': 'VFD', 'CooktopPresent': 'TRUE'}
    test.insert(DataType.MODEL, map)
    test.cleanup()
