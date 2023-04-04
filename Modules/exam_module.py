from database_module import Database

class Exam(Database):
       
        def insert_omr_response(self,omr_response):
                try:
                        for response in omr_response:
                                query="INSERT INTO main.lapis_omr_response(lapis_roll_number, question_paper_code, question_number_in_question_paper, response) VALUES ({}, {}, {}, '{}');".format(response['lapis_roll_number'],response['question_paper_code'],response['question_number_in_question_paper'],response['response'])
                                Database.cursor.execute(query)
                        Database.conn.commit()
                        return (True,"OMR Response inserted successfuly")
                except Exception as e:
                        Database.conn.rollback()
                        return (False, e)


                        
       
        def insert_lapis_exam_info(self,exam_info):
                try:
                        #this code is avoid duplication of data:
                        query1='SELECT school_code, math_exam_date, science_exam_date, math_qp_code, science_qp_code, class FROM main.lapis_exam_info;'
                        Database.cursor.execute(query1)
                        temp = Database.cursor.fetchall()
                        for row in temp:
                                if(int(exam_info['school_code'])==int(row[0]) 
                                        and int(exam_info['maths_qp_code'])==int(row[3])
                                        and int(exam_info['science_qp_code'])==int(row[4])
                                        and int(exam_info['std'])==int(row[5])
                                        ):
                                        return (False,'Data already exists')

                        #if data is unique
                        query="INSERT INTO main.lapis_exam_info(school_code, math_exam_date, science_exam_date, math_qp_code, science_qp_code, class) VALUES ({}, '{}', '{}', {}, {}, {});".format(exam_info['school_code'],exam_info['maths_exam_date'],exam_info['science_exam_date'],exam_info['maths_qp_code'],exam_info['science_qp_code'],exam_info['std'])
                        Database.cursor.execute(query)
                        Database.conn.commit()
                        return (True,'Exam Information Inserted Successfuly')
                except Exception as e:
                        Database.conn.rollback()
                        return (False,e)




        def insert_answerkey(self,key_answer_data):
                try:
                        for answerkey in key_answer_data:
                                query="INSERT INTO main.lapis_correct_options_details(base_question_paper_code, base_question_number, question_id, correct_option, subject) VALUES ({}, {}, '{}','{}','{}');".format(answerkey['qp_code'],answerkey['question_number'],answerkey['question_id'],answerkey['correct_option'],answerkey['subject'])
                                Database.cursor.execute(query)
                        Database.conn.commit()
                        return (True,"AnswerKeys inserted successfuly")

                except Exception as e:
                        Database.conn.rollback()
                        return (False, e)

