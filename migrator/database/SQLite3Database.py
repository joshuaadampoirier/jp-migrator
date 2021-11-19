import logging
import pkg_resources

from sqlite3 import OperationalError

from migrator.database.BaseDatabase import BaseDatabase

logging.basicConfig(
    filename='SQLite3Database.log',
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


class SQLite3Database(BaseDatabase):
    """SQLite3 database class.

    Parameters
    ----------
    cnxn : database server connection
        Connection to the database.
    """
    def __init__(self, cnxn):
        logging.info('Creating database object')
        self.cnxn = cnxn
        self.__migrations_run()

    def __migrations_run(self):
        """If it does not exist, create a table to track the migrations executed
        against the database.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        logging.info('Creating _migrationsrun table')

        # open sql file
        path = 'sqlite3/_MigrationsRun.sql'
        filepath = pkg_resources.resource_filename(__name__, path)
        f = open(filepath, 'r')

        cursor = self.cnxn.cursor()

        # run sql command
        sql = f.read()
        cursor.execute(sql)
        self.cnxn.commit()

        # cleanup
        f.close()
        cursor.close()

    def check_migration(self, migration):
        """Checks if a given migration script name has already been executed
        against this database.

        Parameters
        ----------
        migration : str
            Path to the migration file being investigated.

        Returns
        -------
        exists : bool
            True if it has already been executed, otherwise False

        Notes
        -----
        We determine this by checking if the file exists in the _MigrationsRun
        table.

        SQLite3 does not support stored procedures, so we must dynamically build
        the SQL query here.
        """
        # create database cursor
        cursor = self.cnxn.cursor()

        # build sql query to determine if migration has been run
        sql = '''
            SELECT      COUNT(1)
            FROM        _MigrationsRun
            WHERE       Migration = '{m}'
        '''.format(m=migration)

        # run the sql query
        cursor.execute(sql)

        # if non-zero returned, migration exists; otherwise not
        if cursor.fetchone()[0] > 0:
            exists = True
        else:
            exists = False

        return exists

    def update_migrations_run(self, migration):
        """Insert the given migration into the _MigrationsRun table.

        Parameters
        ----------
        migration : str
            Pathname for the migration script.

        Returns
        -------
        None
        """
        # create database cursor
        cursor = self.cnxn.cursor()

        # build sql query to update _MigrationsRun
        sql = '''
            INSERT INTO _MigrationsRun
            (
                Migration
                ,DateRun
            )
            VALUES
            (
                '{m}'
                ,DATETIME('now')
            )
        '''.format(m=migration)

        try:
            # run the sql query
            cursor.execute(sql)
            self.cnxn.commit()

        except OperationalError:
            logging.error('Problem updating _MigrationsRun for {m}'.format(
                m=migration
            ))
            raise OperationalError
