CREATE OR ALTER PROCEDURE dbo._Insert_MigrationsRun 
(
    @migration_name  NVARCHAR(MAX)
)
AS


/*  ****************************************************************************

Inserts the filenames of successfully executed migration scripts into the 
dbo._MigrationsRun table.


Args
----

    @migration_name     NVARCHAR(MAX)
                        Filename of the migration script to be inserted into the 
                        dbo._MigrationsRun table. 


***************************************************************************** */


BEGIN TRY  


    INSERT INTO dbo._MigrationsRun 
    (
        Migration 
        ,DateRun 
    )
    VALUES 
    (
        @migration_name 
        ,SYSUTCDATETIME()
    )
    

END TRY 
BEGIN CATCH 


    IF (@@TRANCOUNT > 0)
    BEGIN 
        ROLLBACK TRANSACTION 
    END 


    PRINT('Error: Could not insert into dbo._MigrationsRun.')
    ;THROW 


END CATCH 