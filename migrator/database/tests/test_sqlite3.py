import pkg_resources 
import unittest 

from migrator.database.SQLite3Database import SQLite3Database 
from migrator.server.SQLite3Server import SQLite3Server


class SQLite3DatabaseTestCase(unittest.TestCase):
    '''
    Test class for SQLite3 database class.
    '''

    def test_database_type(self):
        '''
        Test to ensure creating a SQLite3 database object generates an object of
        the expected type.
        '''
        server = SQLite3Server('TestServer')
        database = server.get_database()
        self.assertIsInstance(database, SQLite3Database)

    def test_migrations_run(self):
        '''
        Test to ensure the _MigrationsRun table was created in the database.
        '''
        # build objects to test
        server = SQLite3Server('TestServer')
        cnxn = server.get_connection()
        cursor = cnxn.cursor()

        # build SQL query and execute 
        path = 'sqlite3/test_migrations_run.sql'
        filepath = pkg_resources.resource_filename(__name__, path)            
        f = open(filepath, 'r')        
        sql = f.read()
        cursor.execute(sql)

        # run the test 
        self.assertEqual(cursor.fetchone()[0], '_MigrationsRun')

        # cleanup 
        f.close()
        cursor.close()