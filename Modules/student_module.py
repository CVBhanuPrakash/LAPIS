from database_module import Database
from school_module import School        #.get_all_school_names
import random
import string

'''Class: Main aim is to insert the data of each student one by one
        It needs 3 arguments, school_code,school_tag and the student details
        
        Function-1:generate_student_login_id:: Generates the login ID by combining school_tag and lapis_roll_number
        Function-2:generate_password:: Generates password of 8 character length
        Function-3:Insert_Student_Data_To_DB::Inserts the student details into the database if succesfuly inserted returns TRUE else FALSE
                        to the function file(or from where the function was called)
        '''

class Student(Database):
         
        def Insert_Student_Data(self,school_code,school_tag,student_data):
                lapis_roll_number=student_data['lapis_roll_number']
                school_code=school_code
                school_tag=school_tag
                student_name=student_data['student_name']
                app_login_id=self.generate_student_login_id(school_tag,lapis_roll_number)
                app_password=self.generate_password()
                clasS=student_data['std']
                section=student_data['section']

                query="INSERT INTO main.student_details(lapis_roll_number, school_code, student_name, app_login_id, app_password, class, section) VALUES ({},{},'{}','{}','{}',{},'{}');".format(lapis_roll_number,school_code,student_name,app_login_id,app_password,clasS,section)
                try:
                        Database.cursor.execute(query)
                        Database.conn.commit()
                        return True
                except:
                        Database.conn.rollback()
                        return False

        def generate_student_login_id(self,school_tag,lapis_roll_number):
                app_login_id=str(school_tag)+str(lapis_roll_number)
                return app_login_id

        def generate_password(self):
                #combination
                lower=string.ascii_lowercase
                upper=string.ascii_uppercase
                numbers=string.digits
                special_chars='!@#$?'    
                combination=lower+upper+numbers+special_chars
                #creating random 8 chars password
                temp=random.sample(combination, 8)
                        #joining list elements into string
                password="".join(temp)

                return password

        def get_student_data(self,school_data):
                query="SELECT school_code, class,section,student_name,app_login_id FROM main.student_details order by school_code;"
                
                Database.cursor.execute(query)
                temp = Database.cursor.fetchall()       #all student data from student database
                # school_data=get_all_school_names()       #all school_code and school_name from school_database
                '''     School_code is key and school_name is value
                        ex:{12:'Lotus Public School'}
                '''
                student_data=[]         #will contains list of dict ( Student details )
                # print(temp)
                # print(school_data[102])
                for each_student in temp:
                        student={}             #each student data will be stored
                        student['school_code']=each_student[0]
                        student['School_name']=school_data[each_student[0]]     #school_name from school_data key. Also 'each_student[0]' is the school_code from student database
                        student['Class']=each_student[1]
                        student['Section']=each_student[2]
                        student['Name']=each_student[3]
                        student['Id']=each_student[4]
                        student_data.append(student)

                return student_data
                # except:
                #         return False