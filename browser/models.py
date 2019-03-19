import pyodbc
import pandas as pd

DATABASES_CONNECTORS = {'Microsoft Access': 'pyodbc', 'MySQL': 'pyodbc', 'Oracle': 'pyodbc',
						'Microsoft SQL Server': 'pyodbc', 'Microsoft Visual FoxPro': 'pyodbc', 'IBM DB2': 'pyodbc'}
SELECT_QUERIES = {
	'database': {'Microsoft SQL Server': "SELECT [name] as Database_Name FROM sys.databases"},
	'schemas': {'Microsoft SQL Server': '''SELECT [name] as [Schema_Name] FROM sys.schemas WHERE [schema_id] IN (
		SELECT DISTINCT [schema_id] FROM sys.tables WHERE [type] = 'U' AND [is_ms_shipped] = 0)'''},
	'tables': {
		'Microsoft SQL Server': '''SELECT [name] as Table_Name, [type_desc] as Table_Type,
		schema_name(schema_id) as [Schema_Name], [create_date] as 
		Create_Date, [modify_date] as Modify_Date, [max_column_id_used] as Number_of_Columns FROM sys.tables'''},
	'records': {
		'Microsoft SQL Server': '''SELECT TOP 100 * FROM [{DB_NAME}].[{Schema_Name}].[{Table_Name}]'''
	}
}
CONNECTION_STRING = {'Microsoft SQL Server': "DRIVER={{SQL Server}};SERVER={0}; database={1};UID={2};PWD={3}"}
MASTER_DB = {'Microsoft SQL Server': 'master'}


def get_connectors():
	return list(DATABASES_CONNECTORS.keys())


def get_databases(server_type, server_name, user_name, password):
	con_str = CONNECTION_STRING.get(server_type).format(server_name, MASTER_DB.get(server_type), user_name, password)
	if DATABASES_CONNECTORS.get(server_type) == 'pyodbc':
		conn = pyodbc.connect(con_str)
		query = SELECT_QUERIES.get('database').get(server_type)
		df = pd.read_sql_query(query, conn)
		conn.close()
		return df

def get_schemas(server_type, server_name, db_name, user_name, password):
	con_str = CONNECTION_STRING.get(server_type).format(server_name, db_name, user_name, password)
	if DATABASES_CONNECTORS.get(server_type) == 'pyodbc':
		conn = pyodbc.connect(con_str)
		query = SELECT_QUERIES.get('schemas').get(server_type)
		df = pd.read_sql_query(query, conn)
		conn.close()
		return df


def get_table(server_type, server_name, db_name, user_name, password):
	con_str = CONNECTION_STRING.get(server_type).format(server_name, db_name, user_name, password)
	if DATABASES_CONNECTORS.get(server_type) == 'pyodbc':
		conn = pyodbc.connect(con_str)
		query = SELECT_QUERIES.get('tables').get(server_type)
		df = pd.read_sql_query(query, conn)
		conn.close()
		return df


def get_top_records(server_type, server_name, db_name, schema_name, table_name, user_name, password):
	con_str = CONNECTION_STRING.get(server_type).format(server_name, db_name, user_name, password)
	if DATABASES_CONNECTORS.get(server_type) == 'pyodbc':
		conn = pyodbc.connect(con_str)
		query = SELECT_QUERIES.get('records').get(server_type).format(DB_NAME=db_name, Schema_Name=schema_name,
																	  Table_Name=table_name)
		df = pd.read_sql_query(query, conn)
		conn.close()
		return df
