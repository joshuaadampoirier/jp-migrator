/*  If _Insert_MigrationsRun procedure exists, it returns the name of the 
    procedure. If it does not exist, returns nothing.
***************************************************************************** */
SELECT      ROUTINE_NAME
FROM        INFORMATION_SCHEMA.ROUTINES 
WHERE       ROUTINE_SCHEMA = 'dbo'
    AND     ROUTINE_NAME = '_Insert_MigrationsRun'
    AND     ROUTINE_TYPE = 'PROCEDURE'