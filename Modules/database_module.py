import psycopg2

'''Class: To connect to the database.
        Function-1: connect_db:: Returns TRUE if connected or FALSE if not connected.
        Function-2: disconnect_db:: If connected, when called db will be disconnected.
        '''
        
#database calss to connect database
class Database():
        conn=None
        cursor=None

        def connect_db(self):
                try:
                        Database.conn=psycopg2.connect(host='139.59.61.252',database='lb_dev', port='7777',user='nagaraj',password='#Tj42Xf8')
                        Database.cursor=Database.conn.cursor()
                        return True
                except Exception as e:
                        return False

        def disconnect_db(self):
                Database.cursor.close()
                Database.conn.close()


