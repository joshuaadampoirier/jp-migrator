import argparse 


from server.SQLite3Server import SQLite3Server 
from server.PostgreSQLServer import PostgreSQLServer


def _parse_args():
    '''
    Parses and validates command-line arguments. Generates help and usage 
    messageds.

    Parameters
    ----------
    None 

    Returns 
    -------
    args:       Namespace
                Populated with values
    '''
    parser = argparse.ArgumentParser(description='Parameters for jp-migrator')

    # optional host argument
    parser.add_argument(
        '--host', 
        type=str, 
        help='Name or address of host server'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        help='Port data is being served through'
    )
    
    parser.add_argument(
        '--user', 
        type=str, 
        help='Server login username'
    )
    
    parser.add_argument(
        '--password', 
        type=str, 
        help='Server login password'
    )

    args = parser.parse_args()
    return args


def main():
    '''
    Primary orchestration of database migration.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    args = _parse_args()

    dbname = 'w3resourceModel'
    server = SQLite3Server(dbname)

if __name__ == '__main__':
    main()