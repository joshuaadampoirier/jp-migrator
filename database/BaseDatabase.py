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