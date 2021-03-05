class SqlQueries:   
    create_WHO_COVID19_data_table = ("""
        DROP TABLE IF EXISTS WHO_COVID19_data; 
        CREATE TABLE IF NOT EXISTS WHO_COVID19_data (
            date_reported timestamp NOT NULL,
            country_code varchar(64),
            country varchar(64),
            WHO_region varchar(64),
            new_cases int,
            cumulative_cases int,
            new_deaths int,
            cumulative_deaths int
        );
    """)

    create_staging_vaccinations_table = ("""
        DROP TABLE IF EXISTS staging_vaccinations; 
        CREATE TABLE IF NOT EXISTS staging_vaccinations (
            country varchar(64) NOT NULL,
            iso_code varchar(64),
            date timestamp NOT NULL,
            total_vaccinations int,
            people_vaccinated int,
            people_fully_vaccinated int,
            daily_vaccinations_raw int,
            daily_vaccinations int,
            total_vaccinations_per_hundred float(2),
            people_vaccinated_per_hundred float(2),
            people_fully_vaccinated_per_hundred float(2),
            daily_vaccinations_per_million float(2),
            vaccines varchar(64),
            source_name varchar(64),
            source_website varchar
        );
    """)

    create_staging_country_code_table = ("""
        DROP TABLE IF EXISTS staging_country_code; 
        CREATE TABLE IF NOT EXISTS staging_country_code (
            country_name varchar(64) NOT NULL,
            code_2digit varchar(64) NOT NULL,
            code_3digit varchar(64) NOT NULL
        );
    """)

    create_staging_useful_features_table = ("""
        DROP TABLE IF EXISTS staging_useful_features; 
        CREATE TABLE IF NOT EXISTS staging_useful_features (
            country_region varchar(64) NOT NULL,
            population_size int,
            tourism int,
            date_first_fatality timestamp,
            date_first_confirmed_case timestamp,
            latitude float,
            longtitude float,
            mean_age float(2),
            lockdown_date timestamp,
            lockdown_type varchar(64),
            country_code varchar(64)
        );
    """)
    
    # create_songplay_table = ("""
    #     DROP TABLE IF EXISTS songplays; 
    #     CREATE TABLE IF NOT EXISTS songplays (
    #         playid varchar(32) NOT NULL,
    #         start_time timestamp NOT NULL,
    #         userid int4 NOT NULL,
    #         "level" varchar(256),
    #         songid varchar(256),
    #         artistid varchar(256),
    #         sessionid int4,
    #         location varchar(256),
    #         user_agent varchar(256),
    #         CONSTRAINT songplays_pkey PRIMARY KEY (playid)
    #     );
    # """)

    # create_user_table = ("""
    #     DROP TABLE IF EXISTS users;   
    #     CREATE TABLE IF NOT EXISTS users (
    #         userid int4 NOT NULL,
    #         first_name varchar(256),
    #         last_name varchar(256),
    #         gender varchar(256),
    #         "level" varchar(256),
    #         CONSTRAINT users_pkey PRIMARY KEY (userid)
    #     );
    # """)

    # create_song_table = ("""
    #     DROP TABLE IF EXISTS songs;  
    #     CREATE TABLE IF NOT EXISTS songs (
    #         songid varchar(256) NOT NULL,
    #         title varchar(256),
    #         artistid varchar(256),
    #         "year" int4,
    #         duration numeric(18,0),
    #         CONSTRAINT songs_pkey PRIMARY KEY (songid)
    #     );
    # """)
    
    # create_artist_table = ("""
    #     DROP TABLE IF EXISTS artists; 
    #     CREATE TABLE IF NOT EXISTS artists (
    #         artistid varchar(256) NOT NULL,
    #         name varchar(256),
    #         location varchar(256),
    #         lattitude numeric(18,0),
    #         longitude numeric(18,0)
    #     );
    # """)   

    # create_time_table = ("""
    #     DROP TABLE IF EXISTS time; 
    #     CREATE TABLE IF NOT EXISTS time (
    #         start_time timestamp NOT NULL,
    #         "hour" int4,
    #         "day" int4,
    #         week int4,
    #         "month" varchar(256),
    #         "year" int4,
    #         weekday varchar(256),
    #         CONSTRAINT time_pkey PRIMARY KEY (start_time)
    #      );
    # """)

    # songplay_table_insert = ("""
    #     SELECT
    #             md5(events.sessionid || events.start_time) songplay_id,
    #             events.start_time, 
    #             events.userid, 
    #             events.level, 
    #             songs.song_id, 
    #             songs.artist_id, 
    #             events.sessionid, 
    #             events.location, 
    #             events.useragent
    #             FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
    #         FROM staging_events
    #         WHERE page='NextSong') events
    #         LEFT JOIN staging_songs songs
    #         ON events.song = songs.title
    #             AND events.artist = songs.artist_name
    #             AND events.length = songs.duration;
    # """)

    # user_table_insert = ("""
    #     SELECT distinct userid, firstname, lastname, gender, level
    #     FROM staging_events
    #     WHERE page='NextSong';
    # """)

    # song_table_insert = ("""
    #     SELECT distinct song_id, title, artist_id, year, duration
    #     FROM staging_songs;
    # """)

    # artist_table_insert = ("""
    #     SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    #     FROM staging_songs;
    # """)

    # time_table_insert = ("""
    #     SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
    #            extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
    #     FROM songplays;
    # """)