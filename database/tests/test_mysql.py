import logging 
import pkg_resources 
import unittest 

from pymysql import OperationalError

from database.MySQLDatabase import MySQLDatabase 
from server.MySQLServer import MySQLServer


logging.basicConfig(
    filename='TestDatabase_MySQLDatabase.log',
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


class MySQLDatabaseTestCase(unittest.TestCase):
    '''
    Test class for MySQL database class.
    '''

    def test_database_type(self):
        '''
        Test to ensure creating a MySQL database object generates an object 
        of the expected type.
        '''
        try:
            # create server object 
            server = MySQLServer(
                server='localhost',
                port=3306,
                user='root',
                password='badpassword123',
                dbname='TestDatabaseName'
            )

            database = server.get_database()
            self.assertIsInstance(database, MySQLDatabase)

        except OperationalError:
            logging.warning('Unable to test db type, verify MySQL server is running.')

    def test_migrations_run(self):
        '''
        Test to ensure the _MigrationsRun table was created in the database.
        '''
        try:
            # build SQL query and execute 
            path = 'mysql/test_migrations_run.sql'
            filepath = pkg_resources.resource_filename(__name__, path)            
            f = open(filepath, 'r')
            sql = f.read()

            # create server object 
            server = MySQLServer(
                server='localhost',
                port=3306,
                user='root',
                password='badpassword123',
                dbname='TestDatabaseName'
            )

            # get connection and run query
            cnxn = server.get_connection()
            cursor = cnxn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            cursor.close()

            # run the test 
            self.assertEqual(result, '_MigrationsRun')

        except OperationalError:
            logging.warning('Unable to test _MigrationsRun, verify MySQL server is running.')

        finally:
            # cleanup 
            f.close() 

    def test_insert_migrations_run(self):
        '''
        Test to ensure the _Insert_MigrationsRun procedure gets created in 
        SQL Server databases during server/database connection.
        '''
        try:
            # build SQL query and execute 
            path = 'mysql/test_insert_migrations_run.sql'
            filepath = pkg_resources.resource_filename(__name__, path)
            f = open(filepath, 'r')
            sql = f.read() 

            # create server object 
            server = MySQLServer(
                server='localhost',
                port=3306,
                user='root',
                password='BadPassword123',
                dbname='TestDatabaseName'
            )

            # get connection and run query 
            cnxn = server.get_connection() 
            cursor = cnxn.cursor() 
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            cursor.close() 

            # run the test 
            self.assertEqual(result, '_Insert_MigrationsRun')

        except OperationalError:
            logging.warning('Unable to test _Insert_MigrationsRun, verify MySQL Server is running.')

        finally: 
            # cleanup 
            f.close() 

    def test_check_migration(self):
        '''
        Test to ensure the _Check_Migration function gets created in MySQL  
        databases during server/database connection.
        ''' 
        try: 
            # build SQL query and execute 
            path = 'mysql/test_check_migration.sql'
            filepath = pkg_resources.resource_filename(__name__, path)
            f = open(filepath, 'r') 
            sql = f.read() 

            # create server object 
            server = MySQLServer(
                server='localhost',
                port=3306,
                user='root',
                password='badpassword123',
                dbname='TestDatabaseName'
            )

            # get connection and run query 
            cnxn = server.get_connection() 
            cursor = cnxn.cursor() 
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            cursor.close() 

            # run the test 
            self.assertEqual(result, '_Check_Migration')

        except OperationalError:
            logging.warning('Unable to test _Check_Migration, verify MySQL is running.')

        finally:
            # cleanup 
            f.close() 