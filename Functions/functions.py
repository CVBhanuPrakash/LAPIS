import sys
import pandas as pd
import json
import xlrd
import pathlib
sys.path.append('C:/Users/RISHU/Desktop/Lapis/Modules') #will change for each system
from school_module import School
from student_module import Student 
from exam_module import Exam
from lapis_module import Lapis




# -------------------------------------------------------------------------------
#school 
def send_school_data_to_db(school_details):
    try:
        school=School()
        if( not school.connect_db()):
            return [False,"Problem Occured While Connecting Database"]
        insertion_status=school.insert_school_details(school_details)
        school.disconnect_db()
        return insertion_status
    except Exception as e:
        return [False,e]


def get_school_names():
    # print("came")
    try:
        school=School()
        school.connect_db()
        school_details=school.get_school_names()
        school.disconnect_db()
        # print(school_details)
        return school_details
    except:
        return False

def get_school_tag(school_code):
    try:
        school=School()
        school.connect_db()
        school_tag=school.get_school_tag(school_code)
        school.disconnect_db()
        return (True,school_tag)
    except Exception as e:
        return (False,e) 

# -------------------------------------------------------------------------------



# -------------------------------------------------------------------------------
#student
def extractAndFormatFileData(school_code,filepath):
    df=read_file(filepath)
    try:
        df.columns=['lapis_roll_number','school_code','student_name','std','section']
        dfJSON=df.to_json(orient='records')     #str type
        dfParsed=json.loads(dfJSON)     # <class 'list'>
        student_data=json.dumps(dfParsed,indent=4)  #<class 'str'>
        student_data=json.loads(student_data)
        #data validation
        for index,i in enumerate(student_data):
            if not str(i['lapis_roll_number']).isnumeric():
                return (False,f"[ Column: 'Lapis ROll Number', Index: {index+1} ], Found invalid data '{i['lapis_roll_number']}'. Roll number should be numeric.")
            if(int(i['school_code'])!=int(school_code)):
                return (False,f"[ Column: 'School code', Index: {index+1} ],selected school code is '{school_code}', but found '{i['school_code']}' as school code.")
            if not (str(i['std']).strip().isnumeric() and len(str(i['std']))==1):
                return (False,f"[ Column: 'Standard', Index: {index+1} ], Found invalid data '{i['std']}'.")
            if not len((str(i['section']).strip()))==1:
                return (False,f"[ Column: 'Section', Index: {index+1} ],  Found invalid data '{i['section']}'.")
        return (True,student_data)

    except Exception as e:
        return (False,'Invalid Data: '+str(e))


def send_student_data_to_db(school_code,school_tag,student_data):
    try:
        st=Student()
        if(not st.connect_db()):
            return (False, "Problem Occured While Connecting Database")
        for student in student_data:
            if(not st.Insert_Student_Data(school_code,school_tag,student)):
                st.disconnect_db()
                return (False, 'Problem Occured While Inserting Data, Lapis roll number may already exists')
        st.disconnect_db()
        return (True, 'Student Data Inserted Successfuly')
    except Exception as e:
        return (False,e)

# -------------------------------------------------------------------------------




# -------------------------------------------------------------------------------
#lapis exam info
def send_lapis_exam_info_to_db(exam_info):
    try:
        exam=Exam()
        if (not exam.connect_db()):
            return (False, 'Problem Occured While Communicating With Database')
        status=exam.insert_lapis_exam_info(exam_info)
        exam.disconnect_db()
        return status
    except Exception as e:
        return (False,e)


#lapis OMR Response:
def extract_and_insert_omr_response(filepath):
    df=read_file(filepath)
    try:
        df.columns=['lapis_roll_number','question_paper_code','question_number_in_question_paper','response']
        dfJSON=df.to_json(orient='records')     #str type
        dfParsed=json.loads(dfJSON)     # <class 'list'>
        omr_response=json.dumps(dfParsed,indent=4)  #<class 'str'>
        omr_response=json.loads(omr_response)
        #data validation
        for index,i in enumerate(omr_response):
            if not str(i['lapis_roll_number']).isnumeric():
                return (False,f"[ Column: 'Lapis Roll Number', Index: {index+1} ],Found invalid data '{i['lapis_roll_number']}'. Roll number should be numeric.")
            if not str(i['question_paper_code']).isnumeric():
                return (False,f" [ Column: 'Question Paper Code', Index: {index+1} ], Found invalid data '{i['question_paper_code']}'.Question paper code should be numeric.")
            if not str(i['question_number_in_question_paper']).isnumeric():
                return (False,f"[ Column: 'Question number', Index: {index+1} ], Found invalid data '{i['question_number_in_question_paper']}'. Question number should be numeric.")
            # print(len((str(i['response']).strip())))
            if not len((str(i['response']).strip()))==1:
                return (False,f"[ Column: 'Response', Index: {index+1} ], Found invalid data '{i['response']}'.")
        #OMR Response Data Insertion
        try:
            exam=Exam()
            if not exam.connect_db():
                return (False, 'Problem Occured While Communicating With Database')
            status=exam.insert_omr_response(omr_response)
            exam.disconnect_db()
            return status
        except Exception as e:
            return (False,e)
    except Exception as e:
        return (False,e)



#ANSWER KEY
def extract_and_insert_answerkey(qp_code,subject,filepath):
    df=read_file(filepath)
    try:
        df.columns=['qp_code','question_number','question_id','correct_option','subject']
        dfJSON=df.to_json(orient='records')     #str type
        dfParsed=json.loads(dfJSON)     # <class 'list'>
        key_answer_data=json.dumps(dfParsed,indent=4)  #<class 'str'>
        key_answer_data=json.loads(key_answer_data)
        
        #data validation
        for index,i in enumerate(key_answer_data):
            if(int(i['qp_code'])!=int(qp_code)):
                return (False,f"[ Column: 'qp code', Index: {index+1} ],selected Qp code is '{qp_code}', but found '{i['qp_code']}' as Qp code.")
            if not str(i['question_number']).isnumeric():
                return (False,f"[ Column: 'Question number', Index: {index+1} ], Found invalid data '{i['question_number']}'. Question number should be numeric.")
            if not len((str(i['correct_option']).strip()))==1:
                return (False,f"[ Column: 'Correct Option', Index: {index+1} ], Found invalid data '{i['correct_option']}'. Option should be a single letter.")
            if not (str(i['subject']).strip().lower())==subject:
                return (False,f"[ Column: 'Subject', Index: {index+1} ], Found invalid data '{i['subject']}'. selected Subject is '{subject}', but found '{i['subject']}'.")
      
        #Answer key  Insertion
        try:
            exam=Exam()
            if not exam.connect_db():
                return (False, 'Problem Occured While Communicating With Database')
            status=exam.insert_answerkey(key_answer_data)
            exam.disconnect_db()
            return status

        except Exception as e:
            return (False,e)

    except Exception as e:
        return (False,e)




#CONCEPT ID UPLOAD
def extract_and_insert_conceptid(filepath):
    df=read_file(filepath)
    try:
        df.columns=['concept_id','concept_name','topic_name','section_name','chapter_tag']
        dfJSON=df.to_json(orient='records')     #str type
        dfParsed=json.loads(dfJSON)     # <class 'list'>
        conceptId_data=json.dumps(dfParsed,indent=4)  #<class 'str'>
        conceptId_data=json.loads(conceptId_data)
        
        # data validation
        for index,i in enumerate(conceptId_data):
            # print(len(str(i['section_name']).strip()))
            if(len(str(i['section_name']).strip())<=2 or len(str(i['chapter_tag']))<=2):
                return (False,f'Invalid Data: found miscellaneous values in the columns at the {index+1}th index.')
            if not str(i['concept_id']).isnumeric():
                return (False,f"[ Column: 'Concept ID', Index: {index+1} ], Found invalid data '{i['concept_id']}'. Concept ID should be numeric.")
        # #Answer key  Insertion
        try:
            lapis=Lapis()
            if not lapis.connect_db():
                return (False, 'Problem Occured While Communicating With Database')
            status=lapis.insert_conceptId(conceptId_data)
            lapis.disconnect_db()
            return status
        except Exception as e:
            return (False,e)
    except Exception as e:
        return (False,e)

# -------------------------------------------------------------------------------






# -------------------------------------------------------------------------------
#REPORT GENERATION
def get_student_details():
        s=Student()
        school=School()
        if(not s.connect_db()):
            return False
        school_data=school.get_all_school_names()
        # print(school_data)
        student_data=s.get_student_data(school_data)
        if(not student_data):
            s.disconnect_db()
            return False
        else:
            s.disconnect_db()
            student_data=json.dumps(student_data,indent=4) 
            return student_data
#----------------------------------------------------





#LAPIS QR
def extract_and_insert_lapisqr(filepath):
    df=read_file(filepath)
    try:
        df.columns=['question_id','video_link','description']
        dfJSON=df.to_json(orient='records')     #str type
        dfParsed=json.loads(dfJSON)     # <class 'list'>
        qr_data=json.dumps(dfParsed,indent=4)  #<class 'str'>
        qr_data=json.loads(qr_data)
        try:
            lapis=Lapis()
            if not lapis.connect_db():
                return (False, 'Problem Occured While Communicating With Database')
            status=lapis.insert_lapisQr(qr_data)
            lapis.disconnect_db()
            return status
        except Exception as e:
            return (False,e)

    except Exception as e:
        return (False,e)




#fuction to read input files 
def read_file(filepath):
    df=''
    file_extention=pathlib.Path(filepath).suffix
    if(file_extention=='.csv'):
        df=pd.read_csv(filepath) 
    elif(file_extention=='.xlsx'):
        df=pd.read_excel(filepath)
    return df   