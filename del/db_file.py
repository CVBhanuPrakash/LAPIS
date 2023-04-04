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
                        Database.conn=psycopg2.connect(host='139.59.61.252',port=7777, database='lb_dev',user='nagaraj',password='#Tj42Xf8')
                        Database.cursor=Database.conn.cursor()
                        return True
                except:
                        return False

        def disconnect_db(self):
                Database.cursor.close()
                Database.conn.close()


class School(Database):
        
   
        def insert_school_details(self,school_details):
                table_columns=school_details.keys()
                table_values=school_details.values()
                try:
                        #dynamic query making
                        q1="INSERT INTO main.school_detail("
                        q2=''
                        for i in table_columns:
                                q2=q2+i+','
                        q2=q2[:len(q2)-1]
                        q3=") VALUES("
                        q4=''
                        for i in table_values:
                                q4=q4+"'"+str(i)+"'"+','
                        q4=q4[:len(q4)-1]
                        q5=');'

                        query=q1+q2+q3+q4+q5

                        Database.cursor.execute(query)
                        Database.conn.commit()
                        return True
                except:
                        Database.conn.rollback()
                        return False