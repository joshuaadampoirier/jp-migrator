/*  ****************************************************************************

Table definition for the _MigrationsRun table, keeping track of which migration 
scripts have been executed against the database.

***************************************************************************** */

IF NOT EXISTS 
(
    SELECT      1
    FROM        SYS.TABLES 
    WHERE       NAME = '_MigrationsRun'
)
    CREATE TABLE dbo._MigrationsRun 
    (
        Id              BIGINT          NOT NULL 
                                        IDENTITY(1, 1)
        ,Migration      NVARCHAR(MAX)   NOT NULL 
        ,DateRun        DATETIME        NOT NULL 
    )