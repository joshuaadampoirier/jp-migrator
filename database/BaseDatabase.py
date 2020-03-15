import logging 

logging.basicConfig(
    filename='BaseDatabase.log',
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

class BaseDatabase:
    '''
    Base database class for all database types.
    '''

    @classmethod
    def _get_param_names(cls):
        '''
        Get parameter names for the database
        
        Parameters
        ----------
        None 
        Returns
        -------
        params:     list 
                    List of the class parameters.
        '''
        # fetch the constructor 
        init = getattr(cls.__init__, 'Database Class', cls.__init__)

        if init is object.__init__:
            # no constructor to inspect
            params = []
        else:
            # inspect constructor
            sig = inspect.signature(init)
            parameters = [p for p in sig.parameters.values() 
                          if p.name != 'self' and 
                          p.kind != p.VAR_KEYWORD]

            for p in parameters:
                if p.kind == p.VAR_POSITIONAL:
                    raise RuntimeError(
                        'Database objects should always specify their '
                        'parameters in the signature of their __init__. '
                        '{class_} with constructor {signature} does not follow '
                        'this convention.'.format(
                            class_=cls, 
                            signature=sig
                        )
                    )

            # Extract and sort argument names excluding 'self'
            params = sorted([p.name for p in parameters])

        return params

    def get_params(self):
        '''
        Get parameters for this database.

        Parameters
        ----------
        None
        Returns
        -------
        params:     dictionary
                    Dictionary of parameters for this database and each of their
                    set values.
        '''
        # initialize dictionary
        params = dict()

        # loop through parameters, adding to parameter dictionary
        for key in self._get_param_names():
            params[key] = getattr(self, key)

        return params   

    def get_name(self):
        '''
        Retrieve the name of the database.

        Parameters
        ----------
        None 

        Returns 
        -------
        dbname:     str 
                    Name of the database.
        '''
        return self.dbname 

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

        Notes
        -----
        We determine this by checking if the file exists in the _MigrationsRun
        table.

        All databases should overload this function with their own instance.
        '''
        pass  

    def run_migration(self, migration):
        '''
        Run migration against database.

        Parameters
        ----------
        migration:      str 
                        Path to the migration script.

        Returns
        -------
        None 
        '''
        # read the migration script 
        f = open(migration, 'r')
        sql = f.read()

        try:
            # run the migration script 
            cursor = self.cnxn.cursor() 
            cursor.execute(sql)
            self.cnxn.commit()
        except:
            logging.error('Problem deploying {m}'.format(m=migration))
            raise

        # update the _MigrationsRun table
        self.update_migrations_run(migration)

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

        Notes 
        -----
        All databases should overload this function with their own instance.
        '''
        pass 