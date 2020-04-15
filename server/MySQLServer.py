import logging 
import pymysql 

from pymysql import OperationalError

from server.BaseServer import BaseServer 
# FUTURE DEVELOPMENT 
#from database.SQLServerDatabase import SQLServerDatabase 


logging.basicConfig(
    filename='MySQLServerDatabase.log',
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
                Connection to the SQL Server database.
    '''
    def __init__(
        self, 
        server,
        port,
        user, 
        password, 
        dbname=None,
    ):
        logging.info('Creating MySQL Server server object')

        self.server = server
        self.port = port 
        self.user = user  
        self.password = password 
        self.dbname = dbname 

        self.cnxn = self.__establish_connection()
        # FUTURE DEVELOPMENT 
        #self.database = MySQLServerDatabase(self.cnxn, dbname)

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
        
        try:
            cnxn = pymysql.connect(
                host=self.server,
                port=self.port,
                user=self.user, 
                password=self.password,
                database=self.dbname,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

        except OperationalError:
            logging.warning('Unable to connect, trying base connection ...')

            base_cnxn = pymysql.connect(
                server=self.server,
                port=self.port, 
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

            logging.info('Base connection established, creating database')
            
            # FUTURE DEVELOPMENT 
            # attempt to create database 
            #database = MySQLServerDatabase(base_cnxn, self.dbname)
            #base_cnxn.close()
            cnxn = base_cnxn

            # FUTURE DEVELOPMENT
            # second/final attempt to connect to database (now that db is there)
            #cnxn = pymysql.connect(
            #    host=self.server,
            #    port=self.port,
            #    user=self.user, 
            #    password=self.password,
            #    database=self.dbname,
            #    charset='utf8mb4',
            #    cursorclass=pymysql.cursors.DictCursor
            #)

        return cnxn 