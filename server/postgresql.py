import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from server.base import BaseServer 
from database.postgresql import PostgreSQLDatabase 


class PostgreSQLServer(BaseServer):
    '''
    PostgreSQL server object.

    Parameters 
    ----------
    user:       string 
                Database server login name.

    password:   string 
                Database server login password.

    host:       string 
                Host server address.

    port:       string 
                Port host server is serving through.

    dbname:     string 
                Name of the database to connect to. 
                Defaults to postgres, the system database.

    cnxn:       Database connection object
                Connection to the PostgreSQL database.
    '''
    def __init__(
        self, 
        user, 
        password, 
        host='localhost', 
        port='5432', 
        dbname='postgres'
    ):
        self.user = user 
        self.password = password 
        self.host = host 
        self.port = port 
        self.dbname = dbname 
        self.cnxn = self.__establish_connection()
        self.database = PostgreSQLDatabase(self.cnxn)

    def __del__(self):
        self.cnxn.close()

    def __establish_connection(self):
        '''
        Retrieve connection to the SQLite3 database server.

        Parameters 
        ----------
        None 

        Returns
        -------
        cnxn:       connection object 
                    Open connection to the SQLite3 database server.
        '''
        cnxn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.dbname
        )
    
        cnxn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
        return cnxn 


def main():
    """
    Build a PostgreSQL server object; connected to a PostgreSQL database server.

    Parameters
    ----------
        None
    Returns
    -------
        0
    """
    server = PostgreSQLServer(
        'joshuapoirier',
        'badpassword123',
        'localhost',
        '5432'
    )

    print(server.dbname)


    return 0


if __name__ == '__main__':
    main()