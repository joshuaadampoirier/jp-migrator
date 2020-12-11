import logging 
import unittest 

from psycopg2 import OperationalError 
from psycopg2.extensions import connection 

from server.PostgreSQLServer import PostgreSQLServer 


logging.basicConfig(
    filename='TestServer_PostgreSQL.log',
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


class PostgreSQLServerTestCase(unittest.TestCase):
    '''
    Test class for PostgreSQL server class.
    '''

    def __build_server(self):
        '''
        Build PostgreSQL server object to run unit tests against.

        Args:
            None 

        Returns:
            server:     PostgreSQLServer object 
                        PostgreSQLServer object representing a running PG server
        '''
        server = None 

        try:
            # create server object 
            server = PostgreSQLServer(
                user='joshuapoirier',
                password='badpassword123',
                host='localhost',
                port='5432',
                dbname='testserver'
            )

        except OperationalError:
            logging.warning('Verify PostgreSQL server is running.')

        finally:
            return server 

    def test_server_type(self):
        '''
        Test to ensure creating a PostgreSQL server object generates an object 
        of the expected type.
        '''
        server = self.__build_server()
        if server is None:
            self.skipTest('Verify PostgreSQL server is running')

        # test server object 
        self.assertIsInstance(server, PostgreSQLServer)

    def test_connection_type(self):
        '''
        Test to ensure creating a PostgreSQL server object generates a server 
        with a connection object of the expected type.
        '''
        server = self.__build_server() 
        if server is None:
            self.skipTest('Verify PostgreSQL server is running')

        cnxn = server.get_connection()

        # test connection type 
        self.assertIsInstance(cnxn, connection)