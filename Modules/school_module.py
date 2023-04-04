from database_module import Database

class School(Database):

        # ======= SCHOOL DATA INSERTION ======
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
                        return (True, 'School data inserted sucessfuly')
                except Exception as e:
                        Database.conn.rollback()
                        return (False,e)


                        

        def get_school_names(self):
                query="SELECT school_code, school_name FROM main.school_detail;"
                try:
                        Database.cursor.execute(query)
                        temp = Database.cursor.fetchall()
                        school_details=[]
                        for each in temp:
                                school_details.append({'code':each[0],'name':each[1]})
                        # print(school_details)
                        return school_details

                except Exception as e: 
                        return e

        
        def get_all_school_names(self):
                query="SELECT school_code, school_name FROM main.school_detail;"
                try:
                        Database.cursor.execute(query)
                        temp = Database.cursor.fetchall()
                        school_details={}
                        for each in temp:
                                school_details.update({each[0]:each[1]})
                        return school_details

                except: 
                        return {'0':None}
        
        def get_school_tag(self,school_code):
                try:
                        query="SELECT  school_tag FROM main.school_detail where school_code={};".format(school_code)
                        Database.cursor.execute(query)
                        temp = Database.cursor.fetchone()
                        return temp[0]
                except Exception as e:
                        return False
        
        