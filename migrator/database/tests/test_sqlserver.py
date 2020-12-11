import logging 
import pkg_resources 
import unittest 

from pymssql import OperationalError 

from migrator.database.SQLServerDatabase import SQLServerDatabase 
from migrator.server.SQLServer import SQLServer


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


class SQLServerDatabaseTestCase(unittest.TestCase):
    '''
    Test class for SQL Server database class.
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

    def __get_result(self, path):
        '''
        Run the test query contained in the given test file.

        Args:
            path:       string
                        filename containing SQL test query

        Returns:
            result:     string
                        First record returned by query  
        '''
        # build server 
        server = self.__build_server() 
        if server is None:
            self.skipTest('Verify SQL Server is running')

        # load SQL query 
        filepath = pkg_resources.resource_filename(__name__, path)
        f = open(filepath, 'r')
        sql = f.read() 
        f.close()

        # execute query 
        cnxn = server.get_connection() 
        cursor = cnxn.cursor() 
        cursor.execute(sql)
        result = cursor.fetchone()[0]

        return result 

    def test_database_type(self):
        '''
        Test to ensure creating a SQL Server database object generates an object 
        of the expected type.
        '''
        # build server 
        server = self.__build_server() 
        if server is None:
            self.skipTest('Verify MySQL server is running')

        database = server.get_database()
        self.assertIsInstance(database, SQLServerDatabase)

    def test_migrations_run(self):
        '''
        Test to ensure the _MigrationsRun table was created in the database.
        '''
        # build SQL query and execute 
        path = 'sqlserver/test_migrations_run.sql'
        result = self.__get_result(path)

        # run the test 
        self.assertEqual(result, '_MigrationsRun')

    def test_insert_migrations_run(self):
        '''
        Test to ensure the _Insert_MigrationsRun procedure gets created in 
        SQL Server databases during server/database connection.
        '''
        # build SQL query and execute 
        path = 'sqlserver/test_insert_migrations_run.sql'
        result = self.__get_result(path)

        # run the test 
        self.assertEqual(result, '_Insert_MigrationsRun')

    def test_check_migration(self):
        '''
        Test to ensure the _Check_Migration function gets created in SQL Server 
        databases during server/database connection.
        ''' 
        # build SQL query and execute 
        path = 'sqlserver/test_check_migration.sql'
        result = self.__get_result(path)

        # run the test 
        self.assertEqual(result, '_Check_Migration')