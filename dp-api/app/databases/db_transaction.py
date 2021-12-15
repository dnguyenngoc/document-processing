import psycopg2
from psycopg2.extras import RealDictCursor
import time
from settings import config


ISOLEVEL = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
LIMIT_RETRIES = 2


class DB:
    def __init__(self, user, password, host, port, database, reconnect):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self._connection = None
        self._cursor = None
        self.reconnect = reconnect
        self.init()
        
    def connect(self,retry_counter=0):
        if not self._connection:
            try:
                self._connection = psycopg2.connect(user = self.user, password = self.password, host = self.host, 
                                                    port = self.port, database = self.database, connect_timeout=3,)
                retry_counter = 0
                self._connection.autocommit = False
                return self._connection
            except psycopg2.OperationalError as error:
                if not self.reconnect or retry_counter >= LIMIT_RETRIES:
                    raise error
                else:
                    retry_counter += 1
                    print("got error {}. reconnecting {}".format(str(error).strip(), retry_counter))
                    time.sleep(5)
                    self.connect(retry_counter)
            except (Exception, psycopg2.Error) as error:
                raise error

    def cursor(self):
        if not self._cursor or self._cursor.closed:
            if not self._connection:
                self.connect()
            self._cursor = self._connection.cursor(cursor_factory=RealDictCursor)
            return self._cursor
        
    def execute(self, query, is_retry_counter=False):
        retry_counter = 0
        try:
            self._cursor.execute(query)
        except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            if retry_counter >= LIMIT_RETRIES: raise error
            else:
                retry_counter += 1
                if is_retry_counter:
                    print("got error {}. retrying {}".format(str(error).strip(), retry_counter))
                    time.sleep(1)
                    self.reset()
                    self.execute(query, retry_counter)
        except (Exception, psycopg2.Error) as error:
            raise error
        return self._cursor.fetchone()

    # def execute_all(self, query, retry_counter=0):
    #     try:
    #         self._cursor.execute(query)
    #         retry_counter = 0
    #     except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
    #         if retry_counter >= LIMIT_RETRIES:
    #             raise error
    #         else:
    #             retry_counter += 1
    #             print("got error {}. retrying {}".format(str(error).strip(), retry_counter))
    #             time.sleep(1)
    #             self.reset()
    #             self.execute(query, retry_counter)
    #     except (Exception, psycopg2.Error) as error:
    #         raise error
    #     return self._cursor.fetchall()
    
    def close(self):
        if self._connection:
            if self._cursor:
                self._cursor.close()
            self._connection.close()
            print("PostgreSQL connection is closed")
        self._connection = None
        self._cursor = None

    def init(self):
        self.connect()
        self.cursor()
        
    def reset(self):
        self.close()
        self.connect()
        self.cursor()


conn = DB(user=config.DATABASE["user"], password=config.DATABASE["pass"],
          host=config.DATABASE["host"], port=config.DATABASE["port"], 
          database=config.DATABASE["database"], reconnect=True)