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
            create table appliance (
                id serial primary key,
                type varchar(20) not null
            )
            """,
            """
            create table ui_type (
                id serial primary key,
                type varchar(20) not null
            )
            """,
            """
            create table cooktop_type (
                id serial primary key,
                type varchar(20) not null
            )
            """,
            """
            create table model (
                id serial primary key,
                modelname varchar(30) not null,
                foreign key (appliancetype)
                    references appliance (id),
                foreign key (ovenui)
                    references ui_type (id),
                cooktoppresent boolean,
                foreign key (cooktoptype)
                    references cooktop_type (id),
                double boolean,
                mccount integer,
                uppererd integer,
                lowererd integer
            )
            """,
            """
            create table model_addresses (
                foreign key (modelid)
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
            create table model_relays (
                foreign key (modelid)
                    references model (id)
                1k902 varchar(20),
                1k903 varchar(20),
                1k905 varchar(20),
                1k906 varchar(20),
                1k909 varchar(20),
                1k910 varchar(20),
                1k915 varchar(20),
                1k916 varchar(20),
                1q701 varchar(20),
                2k902 varchar(20),
                2k903 varchar(20),
                2k905 varchar(20),
                2k906 varchar(20),
                2k909 varchar(20),
                2k910 varchar(20),
                2k915 varchar(20),
                2k916 varchar(20),
                2q701 varchar(20)
            )
            """)

        try:
            i = 0

            for command in commands:
                logger.info('executing command ' + i)
                i += 1
                self.cur.execute(command)
        
        except (Exception, pp.DatabaseError) as err:
            logger.error(err)
            self.conn.rollback()
            self.cur = self.conn.cursor()
        else:
            self.conn.commit()

    def insert(self, dataType, map):
        logger.info('creating entry in ' + dataType.value)
        
        keys = map.keys()
        cols = '(' + ', '.join(keys) + ')'
        types = '(' + '%s, ' * (len(keys) - 1) + '%s)' 
        self.cur.execute('insert into ' + dataType.value + ' ' + cols + ' VALUES ' + types, map.values)

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
