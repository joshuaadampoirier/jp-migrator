CREATE OR ALTER FUNCTION dbo._Check_Migration 
(
    @migration_name     NVARCHAR(MAX) 
)
RETURNS     BIT AS 

/* *****************************************************************************

Checks to see if a given migration exists.

Args
----

    @migration_name:    NVARCHAR(MAX)
                        Name of the migration script to check whether or not it
                        is found in the dbo._MigrationsRun table (i.e. whether 
                        or not the migration has been executed against this 
                        database).

Returns
-------

    @migration_exists:  BIT
                        1 if found (has been executed)
                        0 if not found (has not been executed)

***************************************************************************** */

BEGIN  


    DECLARE     @migration_exists    BIT 


    SELECT      @migration_exists = CASE 
                    WHEN    COUNT(1) > 0
                    THEN    1
                    ELSE    0
                    END     
    FROM        dbo._MigrationsRun 
    WHERE       Migration = @migration_name


    RETURN @migration_exists


END