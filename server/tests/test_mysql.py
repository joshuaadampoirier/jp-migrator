import logging 
import pymysql
import unittest 

from pymysql.connections import Connection
from pymysql import OperationalError

from server.MySQLServer import MySQLServer 


logging.basicConfig(
    filename='TestServer_MySQLServer.log',
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


class MySQLServerTestCase(unittest.TestCase):
    '''
    Test class for MySQL Server server class.
    '''

    def test_server_type(self):
        '''
        Test to ensure creating a MySQL Server server object generates an object 
        of the expected type.
        '''
        try:
            # create server object 
            server = MySQLServer(
                server='localhost',
                port=3306,
                user='root',
                password='badpassword123'
            )
            
            # test server object 
            self.assertIsInstance(server, MySQLServer)

        except OperationalError:
            logging.warning('Unable to test, verify MySQL Server is running.')

    def test_connection_type(self):
        '''
        Test to ensure creating a MySQL Server server object generates a server 
        with a connection object of the expected type.
        '''
        try:
            # create server and connection 
            server = MySQLServer(
                server='localhost',
                port=3306,
                user='root',
                password='badpassword123'
            )
            cnxn = server.get_connection()

            # test connection type 
            self.assertIsInstance(cnxn, Connection)

        except OperationalError:
            logging.warning('Unable to test, verify MySQL Server is running.')