/*  If _Insert_MigrationsRun procedure exists, it returns the name of the 
    procedure. If it does not exist, returns nothing.
***************************************************************************** */
SELECT      ROUTINE_NAME
FROM        INFORMATION_SCHEMA.ROUTINES 
WHERE       ROUTINE_SCHEMA = 'dbo'
    AND     ROUTINE_NAME = '_Check_Migration'
    AND     ROUTINE_TYPE = 'FUNCTION'