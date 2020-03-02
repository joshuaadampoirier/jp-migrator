/*  Assumes >= PostgreSQL 9.1. Earlier versions do not support IF EXISTS.
***************************************************************************** */
CREATE TABLE IF NOT EXISTS public._MigrationsRun 
(
    Id              BIGINT          NOT NULL 
                    GENERATED       ALWAYS AS IDENTITY 
    ,Migration      TEXT            NOT NULL 
    ,DateRun        TIMESTAMP       NOT NULL 
)