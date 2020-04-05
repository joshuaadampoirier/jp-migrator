import logging 
import unittest 
from sqlite3 import Connection

from server.SQLite3Server import SQLite3Server 


logging.basicConfig(
    filename='TestServer_SQLite3.log',
    level=logging.INFO,
    format='|' \
    '%(asctime)-18s|' \
    '%(levelname)-4s|' \
    '%(module)-18s|' \
    '%(filename)-18s:%(lineno)-4s|' \
    '%(funcName)-18s|' \
    '%(message)-32s|',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class SQLite3ServerTestCase(unittest.TestCase):
    '''
    Test class for SQLite3 server class.
    '''

    def test_server_type(self):
        '''
        Test to ensure creating a SQLite3 server object generates an object of
        the expected type.
        '''
        logging.info('Test Server SQLite3: Server type')

        server = SQLite3Server('TestServer')
        self.assertIsInstance(server, SQLite3Server)

    def test_connection_type(self):
        '''
        Test to ensure creating a SQLite3 server object generates a server with 
        a connection object of the expected type.
        '''
        logging.info('Test Server SQLite3: Connection type')

        server = SQLite3Server('TestServer')
        cnxn = server.get_connection()
        self.assertIsInstance(cnxn, Connection)