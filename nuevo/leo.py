from sqlalchemy import create_engine, MetaData, Table, select

# Definir la URI de la base de datos
DATABASE_URI = 'sqlite:///usuarios.db'

# Crear el engine (motor de conexión)
engine = create_engine(DATABASE_URI)

# Conectar a la base de datos
connection = engine.connect()

# Crear un objeto MetaData para reflejar la estructura de la base de datos
metadata = MetaData()

# Reflejar la tabla que deseas consultar (supongamos que la tabla se llama 'usuarios')
usuarios_table = Table('usuarios', metadata, autoload_with=engine)

# Crear una consulta SELECT
query = select(usuarios_table)

# Ejecutar la consulta
result = connection.execute(query)

# Iterar sobre los resultados
for row in result:
    print(row)