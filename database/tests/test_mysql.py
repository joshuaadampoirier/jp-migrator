import logging 
import pkg_resources 
import unittest 

from pymysql import OperationalError

from database.MySQLDatabase import MySQLDatabase 
from server.MySQLServer import MySQLServer


logging.basicConfig(
    filename='TestDatabase_MySQLDatabase.log',
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


class MySQLDatabaseTestCase(unittest.TestCase):
    '''
    Test class for MySQL database class.
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
                dbname='TestDatabaseName'
            )

        except OperationalError:
            logging.warning('Verify MySQL server is running.')

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
            self.skipTest('Verify MySQL server is running')

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
        Test to ensure creating a MySQL database object generates an object 
        of the expected type.
        '''
        # build server 
        server = self.__build_server() 
        if server is None:
            self.skipTest('Verify MySQL server is running')

        database = server.get_database()
        self.assertIsInstance(database, MySQLDatabase)

    def test_migrations_run(self):
        '''
        Test to ensure the _MigrationsRun table was created in the database.
        '''
        # build SQL query and execute 
        path = 'mysql/test_migrations_run.sql'
        result = self.__get_result(path)

        # run the test 
        self.assertEqual(result, '_MigrationsRun')

    def test_insert_migrations_run(self):
        '''
        Test to ensure the _Insert_MigrationsRun procedure gets created in 
        SQL Server databases during server/database connection.
        '''
        # build SQL query and execute 
        path = 'mysql/test_insert_migrations_run.sql'
        result = self.__get_result(path)

        # run the test 
        self.assertEqual(result, '_Insert_MigrationsRun')

    def test_check_migration(self):
        '''
        Test to ensure the _Check_Migration function gets created in MySQL  
        databases during server/database connection.
        ''' 
        # build SQL query and execute 
        path = 'mysql/test_check_migration.sql'
        result = self.__get_result(path) 

        # run the test 
        self.assertEqual(result, '_Check_Migration')