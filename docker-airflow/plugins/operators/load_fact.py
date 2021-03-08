from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_create="",
                 sql_insert="",
                 mode="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.table=table
        self.sql_create=sql_create
        self.sql_insert=sql_insert
        self.mode=mode

    def execute(self, context):
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info(f"Create {self.table} fact tables")
        redshift_hook.run(f"{self.sql_create}")
        
        columns = "(iso_code,date,vaccines_id,source_id,new_cases,cumulative_cases,new_deaths,cumulative_deaths,total_vaccinations,\
                    people_vaccinated,people_fully_vaccinated,daily_vaccinations_raw,daily_vaccinations,total_vaccinations_per_hundred,\
                    people_vaccinated_per_hundred,people_fully_vaccinated_per_hundred,daily_vaccinations_per_million)"
        
        if self.mode == "delete-load":
            self.log.info(f"DELETE {self.table} fact tables")
            redshift_hook.run(f"DELETE FROM {self.table};")
            
        self.log.info(f"INSERT DATA INTO {self.table}")
        redshift_hook.run(f"INSERT INTO {self.table} {columns} {self.sql_insert}")
