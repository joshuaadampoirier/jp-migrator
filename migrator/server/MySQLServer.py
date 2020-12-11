import logging
import pymysql

from migrator.server.BaseServer import BaseServer
from migrator.database.MySQLDatabase import MySQLDatabase


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


class MySQLServer(BaseServer):
    '''
    MySQLServer server object.

    Parameters
    ----------
    server:     string
                Server address to connect to.

    port:       int
                Port to connect to server through

    user:       string
                Database server login name.

    password:   string
                Database server login password.

    dbname:     string
                Name of the database to connect to.
                Defaults to master, the system database.

    cnxn:       Database connection object
                Connection to the MySQL database.
    '''
    def __init__(
        self,
        server,
        port,
        user,
        password,
        dbname=None
    ):
        logging.info('Creating MySQL server object')

        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname

        self.cnxn = self.__establish_connection()
        self.database = MySQLDatabase(self.cnxn, dbname)

    def __del__(self):
        try:
            logging.info('Closing database connection')
            self.cnxn.close()
        except AttributeError:
            logging.warning('Unable to close connection')

    def __establish_connection(self):
        '''
        Retrieve connection to the MySQL Server database server.

        Parameters
        ----------
        None

        Returns
        -------
        cnxn:       connection object
                    Open connection to the MySQL Server database server.
        '''
        logging.info('Establishing server connection')

        # connect to the server, without a database in mind
        cnxn = pymysql.connect(
            host=self.server,
            port=self.port,
            user=self.user,
            password=self.password,
            charset='utf8mb4'
        )

        return cnxn
