import pkg_resources 
import unittest 

from psycopg2 import OperationalError 

from database.PostgreSQLDatabase import PostgreSQLDatabase 
from server.PostgreSQLServer import PostgreSQLServer


class PostgreSQLDatabaseTestCase(unittest.TestCase):
    '''
    Test class for PostgreSQL database class.
    '''

    def test_database_type(self):
        '''
        Test to ensure creating a PostgreSQL database object generates an object 
        of the expected type.
        '''
        try:
            # create server object 
            server = PostgreSQLServer(
                'joshuapoirier',
                'badpassword123',
                'localhost',
                '5432'
                ,'testserver2'
            )

            database = server.get_database()
            self.assertIsInstance(database, PostgreSQLDatabase)

        except OperationalError:
            print('Warning: Unable to test db type, verify server is running.')

    def test_migrations_run(self):
        '''
        Test to ensure the _MigrationsRun table was created in the database.
        '''
        try:
            # build SQL query and execute 
            path = 'postgresql/test_migrations_run.sql'
            filepath = pkg_resources.resource_filename(__name__, path)            
            f = open(filepath, 'r')
            sql = f.read()

            # create server object 
            server = PostgreSQLServer(
                'joshuapoirier',
                'badpassword123',
                'localhost',
                '5432'
                ,'testserver3'
            )

            # get connection and run query
            cnxn = server.get_connection()
            cursor = cnxn.cursor()
            cursor.execute(sql)
            cursor.close()

            # run the test 
            self.assertEqual(cursor.fetchone()[0], '_migrationsrun')

        except OperationalError:
            print('Warning: Unable to test _MigrationsRun, verify server is running.')

        finally:
            # cleanup 
            f.close() 