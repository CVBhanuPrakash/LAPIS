import psycopg2 as pg
import pandas as pd 
from collections import OrderedDict


# hostname=str("139.59.61.252"),
# database_name= 'lb_dev',
# username='admin' ,
# pwd ='lb@1234',
# port_no=7777
cur=None
conn= None
data_frame=None
sch_code=None
cls=None
subj=None

def get_info(school_code,class_std,subject):
    global sch_code
    global cls
    global subj
    sch_code=school_code
    cls=class_std
    subj=subject
    return 

try:
    engine= conn=pg.connect(
        host="139.59.61.252",
        dbname='lb_stage',
        user='saran',
        password='}u3hMX{F',
        port=7777) 
    
    cur= conn.cursor()

    def section_percentage( ):
        sql_query="""SELECT lapis_roll_number,section_name, percentage FROM main.lapis_section_wise_percentage 
        where class={0} and school_code={1} and subject='{2}'""".format(cls,sch_code,subj)
        data_frame=pd.read_sql(sql_query,con=engine)
        return data_frame
    
    def section_name_count( ):
        sql_query="""SELECT DISTINCT section_name FROM main.lapis_section_wise_percentage 
        where class={0} and school_code={1} and subject='{2}'""".format(cls,sch_code,subj)
        data_frame=pd.read_sql(sql_query,con=engine)
        return data_frame ,data_frame.shape[0] 
    def indiv_percentage( ):
        sql_query="""SELECT lapis_roll_number , percentage FROM main.lapis_indiv_percentage 
        where class={0} and school_code={1} and subject='{2}'""".format(cls,sch_code,subj)
        data_frame=pd.read_sql(sql_query,con=engine)
        return data_frame
    def stu_details( ):
        sql_query="""SELECT school_code,lapis_roll_number,student_name, class , section FROM main.student_details
        where  school_code={0} """.format(sch_code)
        data_frame=pd.read_sql(sql_query,con=engine)
        return data_frame
    def roll_number( ):
        sql_query="""SELECT DISTINCT lapis_roll_number FROM main.lapis_indiv_percentage 
        where class={0} and school_code={1} and subject='{2}'""".format(cls,sch_code,subj)
        data_frame=pd.read_sql(sql_query,con=engine)
        return data_frame

    def get_worksheet_questions():
        sql_query="""SELECT question_id, question, hint FROM main.lapis_workbook_latex_questions"""
        data_frame=pd.read_sql(sql_query,con=engine)
        return data_frame
    
    def get_concept_id():
        sql_query="""SELECT concept_id, concept_name, topic_name, section_name, division_name FROM main.lapis_concept_id"""
        data_frame=pd.read_sql(sql_query,con=engine)
        return data_frame
        

    def get_qr( ):
        sql_query="""SELECT * FROM main.lapis_qr"""
        data_frame=pd.read_sql(sql_query,con=engine)
        return data_frame
    
    def get_test_response():
        sql_query="""SELECT * FROM main.lapis_omr_indiv_response"""
        data_frame=pd.read_sql(sql_query,con=engine)
        return data_frame

except Exception as error:
    print(error)
    
finally:
    if cur is not None:
        cur.close()





