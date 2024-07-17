import psycopg2


class Connection:
    connection = any

    def __init__(self, connection_config):
        self.connection = psycopg2.connect(database=connection_config['database'], user=connection_config['user'],
                                           password=connection_config['password'], host=connection_config['host'],
                                           port=connection_config['port'])
