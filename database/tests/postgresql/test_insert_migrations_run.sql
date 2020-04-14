/*  If _Insert_MigrationsRun procedure exists, it returns the name of the 
    procedure. If it does not exist, returns nothing.
***************************************************************************** */
SELECT      routine_name 
FROM        information_schema.routines
WHERE       routine_schema = 'public'
    AND     routine_name = '_insert_migrationsrun'
    AND     routine_type = 'PROCEDURE';