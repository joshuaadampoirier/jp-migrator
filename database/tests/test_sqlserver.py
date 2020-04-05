import logging 
import pkg_resources 
import unittest 

from pymssql import OperationalError 

from database.SQLServerDatabase import SQLServerDatabase 
from server.SQLServer import SQLServer


logging.basicConfig(
    filename='TestDatabase_SQLServer.log',
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


class SQLServerDatabaseTestCase(unittest.TestCase):
    '''
    Test class for SQL Server database class.
    '''

    def test_database_type(self):
        '''
        Test to ensure creating a SQL Server database object generates an object 
        of the expected type.
        '''
        try:
            # create server object 
            server = SQLServer(
                server='localhost',
                port='1401',
                user='SA',
                password='BadPassword123',
                dbname='TestDatabaseName'
            )

            database = server.get_database()
            self.assertIsInstance(database, SQLServerDatabase)

        except OperationalError:
            logging.warning('Unable to test db type, verify SQL Server server is running.')

    def test_migrations_run(self):
        '''
        Test to ensure the _MigrationsRun table was created in the database.
        '''
        try:
            # build SQL query and execute 
            path = 'sqlserver/test_migrations_run.sql'
            filepath = pkg_resources.resource_filename(__name__, path)            
            f = open(filepath, 'r')
            sql = f.read()

            # create server object 
            server = SQLServer(
                server='localhost',
                port='1401',
                user='SA',
                password='BadPassword123',
                dbname='TestDatabaseName'
            )

            # get connection and run query
            cnxn = server.get_connection()
            cursor = cnxn.cursor()
            cursor.execute(sql)
            cursor.close()

            # run the test 
            self.assertEqual(cursor.fetchone()[0], '_MigrationsRun')

        except OperationalError:
            logging.warning('Unable to test _MigrationsRun, verify SQL Server server is running.')

        finally:
            # cleanup 
            f.close() 