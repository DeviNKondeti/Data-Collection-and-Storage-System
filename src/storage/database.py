from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import DB_CONFIG
import pandas as pd

class DatabaseHandler:
    def __init__(self, db_type='postgres'):
        self.config = DB_CONFIG[db_type]
        self.engine = self._create_engine()
        
    def _create_engine(self):
        """Create SQLAlchemy engine"""
        if self.config['type'] == 'postgres':
            conn_string = f"postgresql+psycopg2://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
        elif self.config['type'] == 'mysql':
            conn_string = f"mysql+mysqlconnector://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
        else:
            raise ValueError("Unsupported database type")
            
        return create_engine(conn_string)
        
    def store_dataframe(self, df, table_name, if_exists='append'):
        """Store pandas DataFrame in database"""
        try:
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=if_exists,
                index=False
            )
            return True
        except Exception as e:
            print(f"Error storing data: {e}")
            return False
            
    def execute_query(self, query):
        """Execute raw SQL query"""
        with self.engine.connect() as connection:
            return connection.execute(query)