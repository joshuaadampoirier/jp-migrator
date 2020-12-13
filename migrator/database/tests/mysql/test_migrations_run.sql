/*  If _MigrationsRun table exists, it returns the name of the table. If it does
    not exist, returns nothing.
***************************************************************************** */
SELECT      TABLE_NAME
FROM        INFORMATION_SCHEMA.TABLES 
WHERE       TABLE_NAME = '_MigrationsRun';