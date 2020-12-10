import logging
import pkg_resources

from database.BaseDatabase import BaseDatabase

logging.basicConfig(
    filename='MySQLServerDatabase.log',
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


class MySQLDatabase(BaseDatabase):
    '''
    MySQL database class.

    Parameters
    ----------
    cnxn:       database server connection
                Connection to the database.

    dbname:     string
                Name of the database to be created.
    '''
    def __init__(self, cnxn, dbname):
        logging.info('Creating MySQL database object')
        self.cnxn = cnxn
        self.dbname = dbname

        self.__create_database()
        self.__migrations_run()
        self.__check_migration()
        self.__insert_migrations_run()

    def __create_database(self):
        '''
        Create the database if it does not already exist.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        # build query and open cursor
        logging.info('Creating MySQL database if it does not exist')
        sql = f'CREATE DATABASE IF NOT EXISTS {self.dbname};'

        # create the database
        cursor = self.cnxn.cursor()
        cursor._defer_warnings = True
        cursor.execute(sql)
        self.cnxn.select_db(self.dbname)

        # cleanup
        cursor.close()
        self.cnxn.commit()

    def __migrations_run(self):
        '''
        If it does not exist, create a table to track the migrations executed
        against the database.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        logging.info('Create _MigrationsRun table')

        # open sql file
        path = 'mysql/_MigrationsRun.sql'
        filepath = pkg_resources.resource_filename(__name__, path)
        f = open(filepath, 'r')

        cursor = self.cnxn.cursor()
        cursor._defer_warnings = True

        # run sql command
        sql = f.read()
        cursor.execute(sql)
        self.cnxn.commit()

        # cleanup
        f.close()
        cursor.close()

    def __check_migration(self):
        '''
        Create the check migration function in the database. This function
        (being created in this function) checks to see if a given migration has
        been executed against the database.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        logging.info('Create _CheckMigration function')

        # open sql file
        path = 'mysql/_CheckMigration.sql'
        filepath = pkg_resources.resource_filename(__name__, path)
        f = open(filepath, 'r')

        cursor = self.cnxn.cursor()
        cursor._defer_warnings = True

        # run sql command
        sql = f.read()
        cursor.execute('DROP FUNCTION IF EXISTS _Check_Migration;')
        cursor.execute(sql)
        self.cnxn.commit()

        # cleanup
        f.close()
        cursor.close()

    def __insert_migrations_run(self):
        '''
        Create the stored procedure which inserts a given migration into the
        _MigrationsRun table.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        logging.info('Create _Insert_MigrationsRun stored procedure')

        # open sql file
        path = 'mysql/_InsertMigrationsRun.sql'
        filepath = pkg_resources.resource_filename(__name__, path)
        f = open(filepath, 'r')

        cursor = self.cnxn.cursor()
        cursor._defer_warnings = True

        # run sql command
        sql = f.read()
        cursor.execute('DROP PROCEDURE IF EXISTS _Insert_MigrationsRun;')
        cursor.execute(sql)
        self.cnxn.commit()

        # cleanup
        f.close()
        cursor.close()

    def check_migration(self, migration):
        '''
        Checks if a given migration script name has already been executed
        against this database.

        Parameters
        ----------
        migration:      str
                        Path to the migration file being investigated.

        Returns
        -------
        exists:         bool
                        True if it has already been executed, otherwise False
        '''
        # create database cursor
        cursor = self.cnxn.cursor()
        cursor._defer_warnings = True

        # build sql query to determine if migration has been run
        sql = f"SELECT dbo._Check_Migration('{migration}');"

        # run the sql query
        cursor.execute(sql)
        exists = cursor.fetchone()[0]

        # cleanup
        cursor.close()

        return exists

    def update_migrations_run(self, migration):
        '''
        Insert the given migration into the _MigrationsRun table.

        Parameters
        ----------
        migration:      str
                        Pathname for the migration script.

        Returns
        -------
        None
        '''
        # create database cursor
        cursor = self.cnxn.cursor()
        cursor._defer_warnings = True

        # build sql query to update _MigrationsRun
        sql = f"CALL dbo._Insert_MigrationsRun('{migration}');"

        # run the sql query
        cursor.execute(sql)
        self.cnxn.commit()

        # cleanup
        cursor.close()
