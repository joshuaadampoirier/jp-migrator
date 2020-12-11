import logging 
import unittest 

from pymssql import Connection, OperationalError

from server.SQLServer import SQLServer 


logging.basicConfig(
    filename='TestServer_SQLServer.log',
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


class SQLServerTestCase(unittest.TestCase):
    '''
    Test class for SQL Server server class.
    '''

    def __build_server(self):
        '''
        Build SQL Server object to run unit tests against.

        Args:
            None 

        Returns:
            server:     SQL Server object 
                        SQL Server object representing a running SQL Server
        '''
        server = None 

        try:
            # create server object 
            server = SQLServer(
                server='localhost',
                port='1401',
                user='SA',
                password='BadPassword123',
                dbname='TestDatabaseName'
            )

        except OperationalError:
            logging.warning('Verify SQL Server is running.')

        finally:
            return server 

    def test_server_type(self):
        '''
        Test to ensure creating a SQL Server server object generates an object 
        of the expected type.
        '''
        server = self.__build_server()
        if server is None:
            self.skipTest('Verify SQL Server is running')
            
        # test server object 
        self.assertIsInstance(server, SQLServer)

    def test_connection_type(self):
        '''
        Test to ensure creating a SQL Server server object generates a server 
        with a connection object of the expected type.
        '''
        server = self.__build_server() 
        if server is None:
            self.skipTest('Verify SQL Server is running')

        cnxn = server.get_connection()

        # test connection type 
        self.assertIsInstance(cnxn, Connection)