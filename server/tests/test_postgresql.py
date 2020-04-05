import logging 
import unittest 

from psycopg2 import OperationalError 
from psycopg2.extensions import connection 

from server.PostgreSQLServer import PostgreSQLServer 


logging.basicConfig(
    filename='TestServer_PostgreSQL.log',
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


class PostgreSQLServerTestCase(unittest.TestCase):
    '''
    Test class for PostgreSQL server class.
    '''

    def test_server_type(self):
        '''
        Test to ensure creating a PostgreSQL server object generates an object 
        of the expected type.
        '''
        logging.info('Test Server SQLite3: Server type')

        try:
            # create server object 
            server = PostgreSQLServer(
                user='joshuapoirier'
                ,password='badpassword123'
                ,host='localhost'
                ,port='5432'
                ,dbname='testserver'
            )

            # test server object 
            self.assertIsInstance(server, PostgreSQLServer)

        except OperationalError:
            logging.warning('Unable to test, verify PostgreSQL server is running.')

    def test_connection_type(self):
        '''
        Test to ensure creating a PostgreSQL server object generates a server 
        with a connection object of the expected type.
        '''
        logging.info('Test Server SQLite3: Server type')

        try:
            # create server and connection 
            server = PostgreSQLServer(
                user='joshuapoirier'
                ,password='badpassword123'
                ,host='localhost'
                ,port='5432'
                ,dbname='testserver'
            )
            cnxn = server.get_connection()

            # test connection type 
            self.assertIsInstance(cnxn, connection)

        except OperationalError:
            logging.warning('Unable to test, verify PostgreSQL server is running.')