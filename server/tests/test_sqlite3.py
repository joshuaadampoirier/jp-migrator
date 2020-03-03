import unittest 
from sqlite3 import Connection

from server.sqlite3 import SQLite3Server 


class SQLite3ServerTestCase(unittest.TestCase):
    '''
    Test class for SQLite3 server class.
    '''

    def test_server_type(self):
        '''
        Test to ensure creating a SQLite3 server object generates an object of
        the expected type.
        '''
        server = SQLite3Server('TestServer')
        self.assertIsInstance(server, SQLite3Server)

    def test_connection_type(self):
        '''
        Test to ensure creating a SQLite3 server object generates a server with 
        a connection object of the expected type.
        '''
        server = SQLite3Server('TestServer')
        cnxn = server.get_connection()
        self.assertIsInstance(cnxn, Connection)