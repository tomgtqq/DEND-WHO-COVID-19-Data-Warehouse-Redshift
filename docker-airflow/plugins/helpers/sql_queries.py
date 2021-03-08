class SqlQueries:   
    create_WHO_COVID19_data_table = ("""
        DROP TABLE IF EXISTS WHO_COVID19_data; 
            CREATE TABLE IF NOT EXISTS WHO_COVID19_data (
            date_reported                        DATE NOT NULL,
            country_code                         VARCHAR NOT NULL,
            country                              VARCHAR NOT NULL,
            WHO_region                           VARCHAR NOT NULL,
            new_cases                            INTEGER,
            cumulative_cases                     INTEGER,
            new_deaths                           INTEGER,
            cumulative_deaths                    INTEGER,
            CONSTRAINT WHO_COVID19_data_pkey PRIMARY KEY (date_reported, country_code)
        )
        diststyle auto;
    """)

    create_staging_vaccinations_table = ("""
        DROP TABLE IF EXISTS staging_vaccinations; 
        CREATE TABLE IF NOT EXISTS staging_vaccinations (
            country                              VARCHAR(64) NOT NULL,
            iso_code                             VARCHAR(16),
            date                                 DATE NOT NULL,
            total_vaccinations                   INTEGER,
            people_vaccinated                    INTEGER,
            people_fully_vaccinated              INTEGER,
            daily_vaccinations_raw               INTEGER,
            daily_vaccinations                   INTEGER,
            total_vaccinations_per_hundred       FLOAT,
            people_vaccinated_per_hundred        FLOAT,
            people_fully_vaccinated_per_hundred  FLOAT,
            daily_vaccinations_per_million       FLOAT,
            vaccines                             VARCHAR,
            source_name                          VARCHAR,
            CONSTRAINT staging_vaccinations_pkey PRIMARY KEY (date, country)
        )
        diststyle auto;
    """)

    create_staging_country_code_table = ("""
        DROP TABLE IF EXISTS staging_country_code; 
        CREATE TABLE IF NOT EXISTS staging_country_code (
            country_name                        VARCHAR(64) NOT NULL,
            code_2digit                         VARCHAR(16) NOT NULL,
            code_3digit                         VARCHAR(16) NOT NULL
        )
        diststyle auto;
    """)

    create_staging_useful_features_table = ("""
        DROP TABLE IF EXISTS staging_useful_features; 
        CREATE TABLE IF NOT EXISTS staging_useful_features (
            country_region                      VARCHAR(64) PRIMARY KEY,
            population_size                     INTEGER,
            tourism                             INTEGER,
            date_first_fatality                 DATE,
            date_first_confirmed_case           DATE,
            latitude                            FLOAT,
            longtitude                          FLOAT,
            mean_age                            FLOAT,
            lockdown_date                       DATE,
            lockdown_type                       VARCHAR(64),
            country_code                        VARCHAR(64)
        )
        diststyle auto;
    """)

    create_staging_GDP_per_capita_table = ("""
        DROP TABLE IF EXISTS staging_GDP_per_capita; 
        CREATE TABLE IF NOT EXISTS staging_GDP_per_capita (
            country                             VARCHAR(64) NOT NULL,
            GDP_per_capita                      INTEGER NOT NULL,
            iso_code                            VARCHAR(16) NOT NULL
        )
        diststyle auto;
    """)

    create_staging_life_expectancy_table = ("""
        DROP TABLE IF EXISTS staging_life_expectancy; 
        CREATE TABLE IF NOT EXISTS staging_life_expectancy (
            country                             VARCHAR(64) NOT NULL,
            life_expectancy                     FLOAT NOT NULL,
            iso_code                            VARCHAR(16) NOT NULL
        )
        diststyle auto;
    """)


    create_staging_median_age_table = ("""
        DROP TABLE IF EXISTS staging_median_age; 
        CREATE TABLE IF NOT EXISTS staging_median_age (
            country                             VARCHAR(64) NOT NULL,
            median_age                          FLOAT NOT NULL,
            iso_code                            VARCHAR(16) NOT NULL
        )
        diststyle auto;
    """)

    create_staging_population_growth_table = ("""
        DROP TABLE IF EXISTS staging_population_growth; 
        CREATE TABLE IF NOT EXISTS staging_population_growth (
            country                             VARCHAR(64) NOT NULL,
            population_growth                   FLOAT NOT NULL,
            iso_code                            VARCHAR(16) NOT NULL
        )
        diststyle auto;
    """)

    create_staging_urbanization_rate_table = ("""
        DROP TABLE IF EXISTS staging_urbanization_rate; 
        CREATE TABLE IF NOT EXISTS staging_urbanization_rate (
            country                             VARCHAR(64) NOT NULL,
            urbanization_rate                   FLOAT NOT NULL,
            iso_code                            VARCHAR(16) NOT NULL
        )
        diststyle auto;
    """)
    
    create_vaccinations_fact_table = ("""
        DROP TABLE IF EXISTS vaccinations_fact; 
        CREATE TABLE IF NOT EXISTS vaccinations_fact (
            id                                      INTEGER IDENTITY(0,1) PRIMARY KEY,
            iso_code                                VARCHAR(16) DISTKEY,
            date                                    DATE SORTKEY,
            vaccines_id                             INTEGER NOT NULL,
            source_id                               INTEGER NOT NULL,
            new_cases                               INTEGER,
            cumulative_cases                        INTEGER,
            new_deaths                              INTEGER,
            cumulative_deaths                       INTEGER,
            total_vaccinations                      INTEGER,
            people_vaccinated                       INTEGER,
            people_fully_vaccinated                 INTEGER,
            daily_vaccinations_raw                  INTEGER,
            daily_vaccinations                      INTEGER,
            total_vaccinations_per_hundred          FLOAT,
            people_vaccinated_per_hundred           FLOAT,
            people_fully_vaccinated_per_hundred     FLOAT,
            daily_vaccinations_per_million          FLOAT  
        )
    """)

    create_country_region_dimension_table = ("""
        DROP TABLE IF EXISTS country_region_dim; 
        CREATE TABLE IF NOT EXISTS country_region_dim (
            iso_code                            VARCHAR(16) PRIMARY KEY,
            population                          BIGINT,
            first_fatality                      DATE,
            first_confirmed_case                DATE,
            lockdown_date                       DATE,
            lockdown_type                       VARCHAR(16),
            latitude                            FLOAT,
            longtitude                          FLOAT,
            GDP                                 INTEGER,
            life_expectancy                     FLOAT,
            population_growth                   FLOAT,
            urbanization_rate                   FLOAT
        )
        diststyle auto;
    """)

    create_time_dimension_table = ("""
        DROP TABLE IF EXISTS time_dim;  
        CREATE TABLE IF NOT EXISTS time_dim (
            date                               Date PRIMARY KEY,
            year                               INTEGER NOT NULL,
            month                              INTEGER NOT NULL,
            week_of_year                       INTEGER NOT NULL
        )
        diststyle auto;
    """)

    create_vaccines_dimension_table = ("""
        DROP TABLE IF EXISTS vaccines_dim;  
        CREATE TABLE IF NOT EXISTS vaccines_dim (
            id                                 INTEGER IDENTITY(0,1) PRIMARY KEY,
            name                               VARCHAR NOT NULL
        )
        diststyle auto;
    """)  
 
    create_source_dimension_table = ("""
        DROP TABLE IF EXISTS source_dim;  
        CREATE TABLE IF NOT EXISTS source_dim (
            id                                 INTEGER IDENTITY(0,1) PRIMARY KEY,
            name                               VARCHAR NOT NULL
        )
        diststyle auto;
    """)  

    vaccinations_fact_table_insert = ("""
        SELECT
            c.code_3digit                               AS iso_code,
            date_reported                               AS date,
            vaccines_dim.id                             AS vaccines_id,
            source_dim.id                               AS source_id,
            new_cases,
            cumulative_cases,
            new_deaths,
            cumulative_deaths,
            v.total_vaccinations                        AS total_vaccinations,
            v.people_vaccinated                         AS people_vaccinated,
            v.people_fully_vaccinated                   AS people_fully_vaccinated,
            v.daily_vaccinations_raw                    AS daily_vaccinations_raw,
            v.daily_vaccinations                        AS daily_vaccinations,
            v.total_vaccinations_per_hundred            AS total_vaccinations_per_hundred,
            v.people_vaccinated_per_hundred             AS people_vaccinated_per_hundred,
            v.people_fully_vaccinated_per_hundred       AS people_fully_vaccinated_per_hundred,
            v.daily_vaccinations_per_million            AS daily_vaccinations_per_million
        FROM WHO_COVID19_data  WHO
        JOIN staging_country_code  c ON (WHO.country_code=c.code_2digit)
        JOIN staging_vaccinations  v ON (WHO.country=v.country)
        JOIN vaccines_dim ON (vaccines_dim.name=v.vaccines)
        JOIN source_dim ON (source_dim.name=v.source_name);
    """)

    country_region_dimension_table_insert = ("""
        SELECT distinct
            F.country_code              AS iso_code,
            F.population_size           AS population,
            F.date_first_fatality       AS first_fatality,
            F.date_first_confirmed_case AS first_confirmed_case,
            F.lockdown_date             AS lockdown_date,
            F.lockdown_type             AS lockdown_type,
            F.latitude                  AS latitude,
            F.longtitude                AS longtitude,
            GDP.GDP_per_capita          AS GDP,
            exp.life_expectancy         AS life_expectancy,
            growth.population_growth    AS population_growth,
            rate.urbanization_rate      AS urbanization_rate
        FROM staging_useful_features F
        JOIN staging_GDP_per_capita GDP ON (F.country_code=GDP.iso_code)
        JOIN staging_life_expectancy exp ON (F.country_code=exp.iso_code)
        JOIN staging_population_growth growth ON (F.country_code=growth.iso_code)
        JOIN staging_urbanization_rate rate ON (F.country_code=rate.iso_code);
    """)

    time_dimension_table_insert = ("""
        SELECT distinct
            date_reported          AS date,
            DATE_PART(yr, date)    AS year,
            DATE_PART(mon, date)   AS month,
            DATE_PART(w, date)     AS week_of_year
        FROM WHO_COVID19_data;
    """)

    vaccines_dimension_table_insert = ("""
        SELECT distinct
            vaccines                   AS name
        FROM staging_vaccinations;
    """)

    source_dimension_table_insert = ("""
        SELECT distinct
            source_name                AS name
        FROM staging_vaccinations;
    """)