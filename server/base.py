class BaseServer:
    '''
    Base server object for all database server types.
    '''

    @classmethod
    def _get_param_names(cls):
        '''
        Get parameter names for the server
        
        Parameters
        ----------
        None 
        Returns
        -------
        params:     list 
                    List of the class parameters.
        '''
        # fetch the constructor 
        init = getattr(cls.__init__, 'Server Class', cls.__init__)

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
                        'Server objects should always specify their '
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
        Get parameters for this server.

        Parameters
        ----------
        None
        Returns
        -------
        params:     dictionary
                    Dictionary of parameters for this server and each of their
                    set values.
        '''
        # initialize dictionary
        params = dict()

        # loop through parameters, adding to parameter dictionary
        for key in self._get_param_names():
            params[key] = getattr(self, key)

        return params

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


        Notes
        -----
        All servers should overload this function with their own instance.
        '''
        pass

    def get_connection(self):
        '''
        Retrieve connection to database server.

        Parameters
        ----------
        None 

        Returns
        -------
        cnxn:       connection object 
                    Open connection to the SQLite3 database server.
        '''
        return self.cnxn 