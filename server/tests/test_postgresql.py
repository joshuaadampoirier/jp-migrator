import unittest 

from psycopg2 import OperationalError 
from psycopg2.extensions import connection 

from server.postgresql import PostgreSQLServer 


class PostgreSQLServerTestCase(unittest.TestCase):
    '''
    Test class for PostgreSQL server class.
    '''

    def test_server_type(self):
        '''
        Test to ensure creating a PostgreSQL server object generates an object 
        of the expected type.
        '''
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
            print('Warning: Unable to test, verify server is running.')

    def test_connection_type(self):
        '''
        Test to ensure creating a SQLite3 server object generates a server with 
        a connection object of the expected type.
        '''
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
            print('Warning: Unable to test, verify server is running.')