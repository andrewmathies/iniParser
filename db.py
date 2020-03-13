import psycopg2 as pp
import logging

from config import dbConfig
from datatype import DataType

logger = logging.getLogger('ini_converter')

class db():
    def __init__(self):
        logger.info('creating db connection')
        
        with open('pwd_db', 'r') as pwFile:
            pw = pwFile.read().strip()
            dbConfig['password'] = pw

        self.conn = pp.connect(**dbConfig)
        self.cur = self.conn.cursor()

    def cleanup(self):
        logger.info('cleaning up db connection')

        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def buildTables(self):
        commands = (
            """
            create table if not exists appliance (
                id serial primary key,
                type varchar(20) not null
            )
            """,
            """
            create table if not exists ui_type (
                id serial primary key,
                type varchar(20) not null
            )
            """,
            """
            create table if not exists cooktop_type (
                id serial primary key,
                type varchar(20) not null
            )
            """,
            """
            create table if not exists model (
                id serial primary key,
                modelname varchar(30) not null,
                appliancetype integer
                    references appliance (id),
                ovenui integer
                    references ui_type (id),
                cooktoppresent boolean,
                cooktoptype integer
                    references cooktop_type (id),
                double boolean,
                mccount integer,
                uppererd integer,
                lowererd integer
            )
            """,
            """
            create table if not exists address (
                modelid integer
                    references model (id),
                mc1address integer,
                mc2address integer,
                uiladdress integer,
                uiraddress integer,
                uicaddress integer,
                stuiaddress integer
            )
            """,
            """
            create table if not exists relay (
                modelid integer
                    references model (id),
                pk902 varchar(20),
                pk903 varchar(20),
                pk905 varchar(20),
                pk906 varchar(20),
                pk909 varchar(20),
                pk910 varchar(20),
                pk915 varchar(20),
                pk916 varchar(20),
                pq701 varchar(20),
                sk902 varchar(20),
                sk903 varchar(20),
                sk905 varchar(20),
                sk906 varchar(20),
                sk909 varchar(20),
                sk910 varchar(20),
                sk915 varchar(20),
                sk916 varchar(20),
                sq701 varchar(20)
            )
            """)

        try:
            for command in commands:
                logger.info('executing command ' + command[:20])
                self.cur.execute(command)
                self.conn.commit()

        except (Exception, pp.DatabaseError) as err:
            logger.error(err)
            self.conn.rollback()
            self.cur = self.conn.cursor()

    def insert(self, dataType, map):
        logger.info('creating entry in ' + dataType.value)
        
        for key, val in map:
            if key == 'ApplianceType':
                self.cur.execute('select id from appliance where id=%s', (val))
                applianceID = self.cur.fetchone()
                if len(applianceID) == 0:
                    self.cur.execute('insert into appliance (type) values (%s)', (val))




        keys = map.keys()
        cols = '(' + ', '.join(keys) + ')'
        types = '(' + '%s, ' * (len(keys) - 1) + '%s)'

        data = tuple(map.values())
        logger.info('inserting ' + str(map))

        self.cur.execute('insert into ' + dataType.value + ' ' + cols + ' values ' + types, data)
        self.conn.commit()

if __name__ == '__main__':
    test = db()
    test.buildTables()

    map1 = {
        'ApplianceType': 'Range',
        'OvenUI': 'VFD',
        'CooktopPresent': 'TRUE',
        'CooktopType': 'Gas',
        'Double': 'FALSE',
        'McCount': '1',
        'UpperERD': '1',
        'LowerERD': '2'
    }

    map2 = {
        'Mc1Address': '80',
        'Mc2Address': '-1',
        'UilAddress': '-1',
        'UirAddress': '-1',
        'UicAddress': '83',
        'StuiAddress': '-1'
    }
    
    map3 = {
        '1K906': 'OvenLight',
        '1K915': 'DLB',
        '1K916': 'ConvBake',
        '1Q701': 'CoolFanEn',
        '1K909': 'Broil',
        '1K910': 'Bake',
        '1K905': 'DoorLock',
        '1K902': 'ConvFanEn',
        '1K903': 'ConvFanDir'
    }

    #test.insert(DataType.MODEL, map1)
    #test.insert(DataType.ADDRESS, map2)
    #test.insert(DataType.RELAY, map3)

    test.cleanup()
