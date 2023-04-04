from flask import Flask,render_template,request,send_file,jsonify,redirect,url_for
from werkzeug.utils import secure_filename
import os
import pathlib
import sys
sys.path.append('C:/Users/RISHU/Desktop/Lapis/Functions')   #change
from Functions.functions import *
from flask_cors import CORS
from email.mime import message
from workbook_complete_v2 import generate_worksheet


app=Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'input_files'
DOWNLOAD_FOLDER = 'sample_files'
ALLOWED_EXTENSIONS = {'.csv','.xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER']=DOWNLOAD_FOLDER
school_code=''
school_tag=''
student_data=''

@app.route('/',methods=['GET','POST'])
def welcome():
    return redirect(url_for('school_data'))


@app.route('/lapis',methods=['GET','POST'])
def home():
    return redirect(url_for('school_data'))



####################### SCHOOL DATA INSERTION ##########################
#   School Data Insertion
@app.route('/lapis/school-data',methods=['GET','POST'])
def school_data():

    if request.method == 'POST':
        school_details_temp=dict(zip(request.form.keys(),request.form.values()))
        school_details_final={k: v for k, v in school_details_temp.items() if v}    # this dict will only stores the key-value pair of only filled  detials in the HTML FORM provided
    
     #if  hits/pressed Preview button 
        if('submit_target' in school_details_final):    
            if(school_details_final['submit_target']=='preview'):        #if  hits/pressed Preview button
                del school_details_final['submit_target']   #deleting submit_taget value(becoz school_details dictionary should contain only keys as same as the school table column names) 
                return render_template('/school/school_data_preview.html',school_data=school_details_final)
                
                #if user pressed on  upload button
            else:
                del school_details_final['submit_target']    #deleting submit_taget value(becoz school_details dictionary should contain only keys as same as the school table column names) 
                status=send_school_data_to_db(school_details_final) #calling function module function to insert school data
                return render_template('/school/school_data_index.html',insertion_status=status)
      #if  hits/pressed Back Button in Preview page
        else:
            return render_template('/school/school_data_index.html',insertion_status=None)
   
    return render_template('/school/school_data_index.html',insertion_status=None)



####################### ADD STUDENT DATA (or) STUDENT DATA INSERTION ##########################
#Student Data Insertion
@app.route('/lapis/student-data-insertion',methods=['GET','POST'])
def student_data_insertion():

    if request.method == 'POST':
        global school_code
        global school_tag
        global student_data

        #checking the POST  field present in the form 
        if 'submit_target' in request.form:
            if request.form['submit_target']=='upload':
                insert_status=send_student_data_to_db(school_code,school_tag,student_data)
                student_data=''
                school_code=''
                school_tag=''
                return render_template('/student/student_data_index.html',school_details=get_school_names(),message=insert_status)  

            elif request.form['submit_target']=='preview':
                f = request.files['input_file']
                school_code=request.form['school_code']
                school_tag_status=get_school_tag(school_code)

                if(not school_tag_status):
                    return render_template('/student/student_data_index.html',school_details=get_school_names(),message=[False,school_tag_status[1]])
                else:
                    school_tag=school_tag_status[1]
                    
                #if file not selected
                if f.filename=='':
                    return  render_template('/student/student_data_index.html',school_details=get_school_names(),message=[False,"No File Selected"])

                #if file selected and if it was allowed file
                if f and pathlib.Path(f.filename).suffix in ALLOWED_EXTENSIONS:
                    filename=secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    extract_status=extractAndFormatFileData(school_code,UPLOAD_FOLDER+'/'+filename)
                    if(extract_status[0]):
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
                        student_data=extract_status[1]               
                        return render_template('/student/student_data_preview.html',student_data=student_data)
                    else:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))                
                        return render_template('/student/student_data_index.html',school_details=get_school_names(),message=extract_status)

                #if it was not a allowed file
                else:
                    return render_template('/student/student_data_index.html',school_details=get_school_names(),message=[False,"This File Is Not Allowed, Upload Only '.csv' or '.xlsx' Files"])
    
    return render_template('/student/student_data_index.html',school_details=get_school_names(),message=None)



#download sample student file
@app.route('/lapis/download-student-data-sample-file')
def download_student_data_sample_file():
    filename="student_data_sample_file.csv"
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename),as_attachment=True)





####################### ADDING LAPIS EXAM INFORMATION  ##########################
#lapis exam information
@app.route('/lapis/lapis-exam-info',methods=['GET','POST'])
def lapis_exam_info():
    if request.method=='POST':
        exam_info={}
        exam_info['school_code']=request.form['school_code']
        exam_info['std']=request.form['std']
        exam_info['science_exam_date']=request.form['science_exam_date']
        exam_info['science_qp_code']=request.form['science_qp_code']
        exam_info['maths_exam_date']=request.form['maths_exam_date']
        exam_info['maths_qp_code']=request.form['maths_qp_code']
        status=send_lapis_exam_info_to_db(exam_info)
        return render_template('/lapis_exam/lapis_exam_info.html',school_details=get_school_names(),message=status)
    return render_template('/lapis_exam/lapis_exam_info.html',school_details=get_school_names(),message=None)




####################### LAPIS OMR RESPONSE ##########################
#lapis OMR Response
@app.route('/lapis/lapis-omr-response',methods=['GET','POST'])
def lapis_omr_response():

    if request.method == 'POST':
        #checking the POST  field present in the form 
        if 'submit_target' in request.form:
            if request.form['submit_target']=='preview':
                pass
                return render_template('/lapis_exam/lapis_omr_response_index.html',school_details=get_school_names(),message=None)

            elif request.form['submit_target']=='upload':
                f = request.files['input_file']
                if f.filename=='':
                    return  render_template('/lapis_exam/lapis_omr_response_index.html',school_details=get_school_names(),message=[False,"No File Selected"])

                #if file selected and if it was allowed file
                if f and pathlib.Path(f.filename).suffix in ALLOWED_EXTENSIONS:
                    filename=secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    extract_status=extract_and_insert_omr_response(UPLOAD_FOLDER+'/'+filename)
                    if(extract_status[0]):
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
                      
                        return render_template('/lapis_exam/lapis_omr_response_index.html',school_details=get_school_names(),message=extract_status)

                    else:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))                
                        return render_template('/lapis_exam/lapis_omr_response_index.html',school_details=get_school_names(),message=extract_status)

                #if it was not a allowed file
                else:
                    return render_template('/lapis_exam/lapis_omr_response_index.html',school_details=get_school_names(),message=[False,"This File Is Not Allowed, Upload Only '.csv' or '.xlsx' Files"])

    return render_template('/lapis_exam/lapis_omr_response_index.html',school_details=get_school_names(),message=None)


#download sample omr response file
@app.route('/lapis/download-omr-response-sample-file')
def download_omr_response_sample_file():
    filename="omr_response_sample_file.csv"
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename),as_attachment=True)





####################### LAPIS ANSWERKEY UPLOAD ##########################
@app.route('/lapis/lapis-answerkey',methods=['GET','POST'])
def lapis_answer_key():
    if request.method == 'POST':
        #checking the POST  field present in the form 
        if 'submit_target' in request.form:
            if request.form['submit_target']=='preview':
                pass
                return render_template('/lapis_exam/lapis_answerkey_index.html',message=None)

            elif request.form['submit_target']=='upload':
                f = request.files['input_file']
                if f.filename=='':
                    return  render_template('/lapis_exam/lapis_answerkey_index.html',message=[False,"No File Selected"])

                #if file selected and if it was allowed file
                if f and pathlib.Path(f.filename).suffix in ALLOWED_EXTENSIONS:
                    filename=secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    qp_code=request.form['qp_code']
                    subject=(request.form['subject'].strip()).lower()
                    extract_status=extract_and_insert_answerkey(qp_code,subject,UPLOAD_FOLDER+'/'+filename)
                    if(extract_status[0]):
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
                        return render_template('/lapis_exam/lapis_answerkey_index.html',message=extract_status)

                    else:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))                
                        return render_template('/lapis_exam/lapis_answerkey_index.html',message=extract_status)

                #if it was not a allowed file
                else:
                    return render_template('/lapis_exam/lapis_answerkey_index.html',message=[False,"This File Is Not Allowed, Upload Only '.csv' or '.xlsx' Files"])

    return render_template('/lapis_exam/lapis_answerkey_index.html',message=None)



#download sample omr response file
@app.route('/lapis/download-answerkey-sample-file')
def download_answerkey_sample_file():
    filename="answerkey_sample_file.csv"
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename),as_attachment=True)






####################### CONCEPT ID UPLOAD ##########################
@app.route('/lapis/concept-id-upload',methods=['GET','POST'])
def lapis_concept_id_upload():
    if request.method == 'POST':
        #checking the POST  field present in the form 
        if 'submit_target' in request.form:
            if request.form['submit_target']=='preview':
                pass
                return render_template('/lapis_exam/lapis_concept_id_index.html',message=None)

            elif request.form['submit_target']=='upload':
                f = request.files['input_file']
                if f.filename=='':
                    return  render_template('/lapis_exam/lapis_concept_id_index.html',message=[False,"No File Selected"])

                #if file selected and if it was allowed file
                if f and pathlib.Path(f.filename).suffix in ALLOWED_EXTENSIONS:
                    filename=secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    # qp_code=request.form['qp_code']
                    extract_status=extract_and_insert_conceptid(UPLOAD_FOLDER+'/'+filename)
                    if(extract_status[0]):
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
                        return render_template('/lapis_exam/lapis_concept_id_index.html',message=extract_status)

                    else:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))                
                        return render_template('/lapis_exam/lapis_concept_id_index.html',message=extract_status)

                #if it was not a allowed file
                else:
                    return render_template('/lapis_exam/lapis_concept_id_index.html',message=[False,"This File Is Not Allowed, Upload Only '.csv' or '.xlsx' Files"])

    return render_template('/lapis_exam/lapis_concept_id_index.html',message=None)


#download sample omr response file
@app.route('/lapis/download-concept-id-sample-file')
def download_conceptId_sample_file():
    filename="concept_id_sample_file.xlsx"
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename),as_attachment=True)






####################### LAPIS REPORT GENERATION ##########################

@app.route('/lapis/student-data/json')
def json_student_data():
    # print(type(jsonify(get_student_details())))
    return jsonify(get_student_details()) 

@app.route('/lapis/report-generation')
def report_generation():
    return render_template('/report/report_index.html')

@app.route('/lapis/student-report',methods=['GET','POST'])
def student_report():
    if request.method=='POST':
        school=request.form['school-names']
        print(request.form)
        # print(request.form['section'])
        # print(request.forms[''])print(request.forms[''])
        # print(school)
        return "render_template('/report/teacher_report.html')"
    return render_template('/report/student_report.html')

@app.route('/lapis/teacher-report')
def teacher_report():
    return render_template('/report/teacher_report.html')

@app.route('/lapis/pricipal-report')
def principal_report():
    return render_template('/report/principal_report.html')



####################### LAPIS QR ##########################
@app.route('/lapis/qr-upload',methods=['GET','POST'])
def lapis_qr():
    if request.method == 'POST':
        #checking the POST  field present in the form 
        if 'submit_target' in request.form:
            if request.form['submit_target']=='preview':
                pass
                return render_template('lapis_qrcode.html',message=None)

            elif request.form['submit_target']=='upload':
                f = request.files['input_file']
                if f.filename=='':
                    return  render_template('lapis_qrcode.html',message=[False,"No File Selected"])

                #if file selected and if it was allowed file
                if f and pathlib.Path(f.filename).suffix in ALLOWED_EXTENSIONS:
                    filename=secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    # qp_code=request.form['qp_code']
                    extract_status=extract_and_insert_lapisqr(UPLOAD_FOLDER+'/'+filename)
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return render_template('lapis_qrcode.html',message=extract_status) 

                #if it was not a allowed file
                else:
                    return render_template('lapis_qrcode.html',message=[False,"This File Is Not Allowed, Upload Only '.csv' or '.xlsx' Files"])
    
    return render_template('lapis_qrcode.html',message=None)


#download sample omr response file
@app.route('/lapis/download-lapis-qr-sample-file')
def download_lapis_qr_sample_file():
    filename="lapis-qr_sample_file.csv"
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename),as_attachment=True)


####################### WORSKSHEET GENERATION ##########################
@app.route('/lapis/worksheet-generation',methods=['GET','POST'])
def worksheet_generation():

    if request.method == 'POST':
        school_code=request.form['school_name']
        std=request.form['std']
        section=request.form['section']
        subject=request.form['subject']
        if 'generate' in request.form:
            if request.form['generate']=='Generate Worksheet':
                genetation_status=generate_worksheet(12,6,'math')
                return render_template('/worksheet/worksheet.html',message=genetation_status)
            else:
                return render_template('/worksheet/worksheet.html',message=(True,'Preview clicked. Will be available in future'))

        else:
            return render_template('/worksheet/worksheet.html',message=(True,'Preview clicked.This feature will be available in future'))
    
    return render_template('/worksheet/worksheet.html',message=None)




# ########################### SUPPORTING FUNCTIONS #################################
# def Is_correct_file_extension():



if __name__=='__main__':
    app.run(debug=True)
