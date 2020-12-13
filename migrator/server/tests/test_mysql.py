import logging 
import pymysql
import unittest 

from pymysql.connections import Connection
from pymysql import OperationalError

from migrator.server.MySQLServer import MySQLServer 


logging.basicConfig(
    filename='TestServer_MySQLServer.log',
    level=logging.INFO,
    format='|'
    '%(asctime)-18s|'
    '%(levelname)-4s|'
    '%(module)-18s|'
    '%(filename)-18s:%(lineno)-4s|'
    '%(funcName)-18s|'
    '%(message)-32s|',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class MySQLServerTestCase(unittest.TestCase):
    '''
    Test class for MySQL Server server class.
    '''

    def __build_server(self):
        '''
        Build MySQL server object to run unit tests against.

        Args:
            None 

        Returns:
            server:     MySQLServer object 
                        MySQLServer object representing a running MySQL server
        '''
        server = None 

        try:
            # create server object 
            server = MySQLServer(
                server='localhost',
                port=3306,
                user='root',
                password='badpassword123',
                dbname='testdatabase3'
            )

        except OperationalError:
            logging.warning('Verify MySQL server is running.')

        finally:
            return server 

    def test_server_type(self):
        '''
        Test to ensure creating a MySQL Server server object generates an object 
        of the expected type.
        '''
        # build server 
        server = self.__build_server()
        if server is None:
            self.skipTest('Verify MySQL server is running')

        self.assertIsInstance(server, MySQLServer)

    def test_connection_type(self):
        '''
        Test to ensure creating a MySQL Server server object generates a server 
        with a connection object of the expected type.
        '''
        # build server 
        server = self.__build_server()
        if server is None:
            self.skipTest('Verify MySQL server is running')
        
        # test connection type 
        cnxn = server.get_connection() 
        self.assertIsInstance(cnxn, Connection)