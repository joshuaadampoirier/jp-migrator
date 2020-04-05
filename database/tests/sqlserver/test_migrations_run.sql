/*  If _MigrationsRun table exists, it returns the name of the table. If it does
    not exist, returns nothing.
***************************************************************************** */
SELECT      t.NAME
FROM        SYS.TABLES t 
JOIN        SYS.SCHEMAS s 
ON          s.SCHEMA_ID = t.SCHEMA_ID 
WHERE       s.NAME = 'dbo'
    AND     t.NAME = '_MigrationsRun'