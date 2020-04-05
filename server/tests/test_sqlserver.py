import unittest 

from pymssql import Connection, OperationalError

from server.SQLServer import SQLServer 


class SQLServerTestCase(unittest.TestCase):
    '''
    Test class for SQL Server server class.
    '''

    def test_server_type(self):
        '''
        Test to ensure creating a SQL Server server object generates an object 
        of the expected type.
        '''
        try:
            # create server object 
            server = SQLServer(
                server='localhost',
                port='1401',
                user='SA',
                password='BadPassword123'
            )

            # test server object 
            self.assertIsInstance(server, SQLServer)

        except OperationalError:
            print('Warning: Unable to test, verify SQL Server is running.')

    def test_connection_type(self):
        '''
        Test to ensure creating a SQL Server server object generates a server 
        with a connection object of the expected type.
        '''
        try:
            # create server and connection 
            server = SQLServer(
                server='localhost',
                port='1401',
                user='SA',
                password='BadPassword123',
                dbname='josh'
            )
            cnxn = server.get_connection()

            # test connection type 
            self.assertIsInstance(cnxn, Connection)

        except OperationalError:
            print('Warning: Unable to test, verify SQL Server is running.')