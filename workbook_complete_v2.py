from asyncio.windows_events import NULL
from lib2to3.pgen2.token import NEWLINE
from pydoc import doc
from venv import create
import pandas as pd

from pylatex import Document, MiniPage,LargeText,LineBreak,LongTable, MultiColumn
from pylatex.utils import bold,NoEscape
import pylatex as pl
from pylatex.package import Package

from pylatex import PageStyle, Head, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number


import db_retrive as db
import pyqrcode
from pylatex.base_classes import Environment, CommandBase, Arguments
from pylatex import Section, UnsafeCommand, Command

import numpy
from matplotlib import pyplot as plt





#temporary initialization (values Will change according to the input  in generate_worksheet() )
folder_name = "C6M - LaPIS Workbook/"

school_code = 12
current_standard = 6
subject_name = 'math'


q_list = []
q_len=0
append_char='A'
tag_name='A'
roll_numb=[]
section_percent=0
section_names='A' 
section_count=2
student_overall_percentage=10
student_details=[]
test_response=[]
section_names_list=[]
worksheet_questions=[]
qr_db=[]
lapis_qr_question_ids=[]
geometry_options={}
doc=[]
file_name='a'




class insert_img(CommandBase):
    _latex_name = 'img'


class insert_question(CommandBase):
    _latex_name = 'question'
    

class insert_hint(CommandBase):
    _latex_name = 'hints'

class insert_question(CommandBase):
    _latex_name = 'qrdes'
    

class insert_hint(CommandBase):
    _latex_name = 'qr'

class insert_hint(CommandBase):
    _latex_name = 'questionID'

class insert_hint(CommandBase):
    _latex_name = 'mcqfourfour'

class insert_hint(CommandBase):
    _latex_name = 'mcqfourtwo'








"""
mistake_list = []
for i in range(1, (q_len+1)):
    temp = tag_name+str(i)
    mistake_list.append(temp)
"""


"""
Latex custom commands
"""
# Create a new document
def get_lib():
    
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('ragged2e'))
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('xcolor'))
    doc.packages.append(Package('geometry'))
    doc.packages.append(Package('caption'))
    doc.packages.append(Package('subcaption'))
    doc.packages.append(Package('enumitem'))
    doc.packages.append(Package('amssymb'))
    doc.packages.append(Package('multirow'))
    doc.packages.append(Package('tcolorbox'))
    doc.packages.append(Package('xparse'))
    doc.packages.append(Package('tikz'))
    doc.packages.append(Package('array'))
    doc.packages.append(Package('wasysym'))
    doc.packages.append(Package('float'))
    doc.packages.append(Package('lipsum'))
    # doc.packages.append(Package('babel'))
    doc.packages.append(Package('babel', options=['english']))
    doc.packages.append(Package('wrapfig'))
    doc.packages.append(Package('tabularx'))
    doc.packages.append(Package('array'))
    doc.packages.append(Package('physics'))
    doc.packages.append(Package('mathdots'))
    doc.packages.append(Package('yhmath'))
    doc.packages.append(Package('cancel'))
    doc.packages.append(Package('color'))
    doc.packages.append(Package('gensymb'))
    doc.packages.append(Package('extarrows'))
    doc.packages.append(Package('booktabs'))
    doc.packages.append(Package('fancyhdr'))
    doc.packages.append(Package('lastpage'))
    doc.packages.append(Package('tfrupee'))
    doc.append(pl.Command('renewcommand', arguments=[pl.NoEscape(r'\footrulewidth'),'0.5pt']))

def add_custom_commands():
    
    new_comm = UnsafeCommand('newcommand', '\img', options=3,
                                extra_arguments=r'\begin{figure}[H] \centering \includegraphics[ width = #1, height = #2]{#3} \end{figure}')
    doc.append(new_comm)

    
    new_comm = UnsafeCommand('newcommand', '\question', options=1,
                                extra_arguments=r'\vspace{2.5mm} \begin{raggedright} {#1}  \leavevmode \\ \end{raggedright}')

    doc.append(new_comm)

    new_comm = UnsafeCommand('newcommand', '\hints', options=1,
                                # extra_arguments= r'\vspace{2.5mm} \begin{raggedright} {\textbf{\underline{{Answer:}}}}\medskip\\ \begin{minipage}{\textwidth}{#1}\end{minipage}\\ \leavevmode \medskip \end{raggedright} \rule{\textwidth}{2pt}')                                

                                extra_arguments=r'\vspace{2.5mm} \begin{raggedright} {\textit{\textbf{{\underline{Answer:}}}}} \\ \medskip {#1}  \leavevmode \\ \medskip \end{raggedright} \rule{\textwidth}{0.10pt} ')
    doc.append(new_comm)

    new_comm = UnsafeCommand('newcommand', '\questionID', options=1,
                                extra_arguments=r'\vspace{2.5mm} \begin{raggedright} {\textit{\textbf{\underline{{Question: #1}}}}}   \\ \end{raggedright}')
    doc.append(new_comm)


    new_comm = UnsafeCommand('newcommand', '\qrdes', options=2,
                                extra_arguments=r'\begin{minipage}{0.75\textwidth} \hrule \renewcommand{\arraystretch}{2.5} \begin{tabular}{ p{1\textwidth} }\large Hi, here in this video you will learn \textbf{#1} \end{tabular} \hrule \end{minipage} \hfill \begin{minipage}{0.15\textwidth} \includegraphics[width=2cm]{#2} \end{minipage}')
    doc.append(new_comm)

    new_comm = UnsafeCommand('newcommand', '\qr', options=1,
                                 extra_arguments=r'\begin{minipage}{3cm} \includegraphics[width=2cm]{#1} \end{minipage} \rule{\textwidth}{0.15pt}')
    doc.append(new_comm)

    new_comm = UnsafeCommand('newcommand', '\mcqfourfour', options=9,
                              extra_arguments=r'\vspace{2.5mm} \begin{raggedright} \textbf{#1} #2 \hfill \textit{#7} \textit{#8}\\ #9 \begin{multicols}{4}{} (a) #3\\ \columnbreak (b) #4\\ \columnbreak (c) #5\\ \columnbreak (d) #6\\ \end{multicols} \end{raggedright}')
    doc.append(new_comm)

    new_comm = UnsafeCommand('newcommand', '\mcqfourtwo', options=9,
                              extra_arguments=r'\vspace{2.5mm} \begin{raggedright} \textbf{#1} #2 \hfill \textit{#7} \textit{#8}\\ #9 \begin{multicols}{2}{} (a) #3\\ (c) #5\\ \columnbreak (b) #4\\ (d) #6\\ \end{multicols} \end{raggedright}')
    doc.append(new_comm)

       
# Gets all the question details from the database based in the question id
def append_questions(sheet_id, relative_qno):
    
    qs = worksheet_questions[worksheet_questions['question_id']==sheet_id]
    question = qs['question'].values[0]
    hints = qs['hint'].values[0]
    doc.append(NoEscape(r"""\questionID {"""+str(relative_qno)+"""}""")) #question number
    doc.append(NoEscape(r"""\question"""+question)) 
    # doc.append(NoEscape(question))
    if hints != "{}":
        doc.append(NoEscape(r'\hints'+hints))
        # doc.append(NoEscape(hints))
    else:
        doc.append(NoEscape(r'\rule{\textwidth}{0.15pt}'))

# Gets the tag and the qr of the question type
def append_qr(id):
    
    if id in lapis_qr_question_ids:
        descrip = qr_db[qr_db['question_id'] == id]['video_description'].values[0]
        # doc.append(NoEscape(r'\qrdes'))
        doc.append(NoEscape(r"""\qrdes {"""+descrip+"""}{"""+id+""".png}"""))
        # doc.append(NoEscape(r'\qr'))



def generate_qr():
    for id in lapis_qr_question_ids:
        qr = ''
        qr = qr+id
        qr = folder_name+ qr+".png"
        link = qr_db[qr_db['question_id'] == id]['video_link'].values[0]  #getting the qr link for a question_id
        url = pyqrcode.create(link)
        url.png(f'{qr}', scale=6)

def generate_woksheet_question_tag(id):
    q_list = []
    for j in range(len(append_char)):
        dr = ''
        dr = dr+id+append_char[j]
        q_list.append(dr)
    
    return q_list


def create_graphs(sections,percentage,name,rollnumber,clas,subject):
    
    ##bar graph
    # fig = plt.figure()
    xpos_val = 1
    xpos_list = []
    xtickslist = []
    fig, ax= plt.subplots()
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side =ax.spines["top"]
    top_side.set_visible(False)

    for xposlen in range(0,len(sections)):
        xpos_list.append(xpos_val)
        xpos_val = xpos_val+3.2 #xpos_val+2.6

    
        
    
    # lst = [ "\\\\" , "+++" , "||", ".", "*","//", "o", "O" ]
    # patterns=[]

    # for l in range(0,len(sections)):
    #     patterns.append(lst[l])

    plt.bar(xpos_list,percentage,hatch='\\\\\\\\\\\\\\\\\\',width = 1.8,color='white', edgecolor='black') #width = 1.6,
    plt.xlabel("Topic wise Performance")
    plt.ylabel("Percentage of fluency")
    plt.xticks(xtickslist)
    plt.yticks(xtickslist)
    
    for x, p,q in zip(xpos_list, percentage,sections):
        plt.text(x, p+2.5, p,ha='center')
        plt.text(x+1.44,3,q,rotation='vertical',ha='center') #x-1.2


    # # labels = patterns
    # handles = [plt.Rectangle((0,0),0.2,0.6,edgecolor='black',fill=None,hatch=label) for label in patterns]
    # plt.gca()
    # a=fig.legend(handles,sections,bbox_to_anchor=(1.4, 0.98)) #bbox_to_anchor=[0.5, 1]
    

    plt.savefig(folder_name+"png_files/"+name+"_"+subject+"_Class" +clas +"_bargraph"+".png",dpi=720,bbox_inches='tight',pad_inches=0.4)
    plt.clf()


def get_mistake_list(roll):
    sorted_list = []
    for section_name in section_names_list:
        temp = test_response[(test_response['lapis_roll_number'] == roll)&(test_response['response_output'] !='Correct') & (test_response['section_name'] == section_name)]['question_id'].values.tolist()
        sorted_list.append(temp)
        
    mistake_list = dict(zip(section_names_list, sorted_list))
    return mistake_list


def cover_page(subject,stu_name,clas,sect,schol):
    ##Footer info
    header = PageStyle("header")
    header.append(pl.Command('renewcommand', arguments=[pl.NoEscape(r'\footrulewidth'),'1pt']))
    with header.create(Foot("L")):
        header.append(NoEscape(r"""\vspace{0.5cm}"""))
        header.append("www.learnbasics.fun")
        # header.append(NoEscape(r"""\hspace{3cm}"""))
    with header.create(Foot("C")):
        header.append(NoEscape(r"""\vspace{0.5cm}"""))
        header.append(" Workbook of "+ stu_name)
        # header.append(NoEscape("""\linebreak"""))
        # header.append("Class "+ clas + " "+ sect+","+schol)
    with header.create(Foot("R")):
        # header.append("www.learnbasics.fun")
        # header.append(NoEscape("""\linebreak"""))
        # page_no = simple_page_number()
        header.append(NoEscape(r"""\vspace{0.5cm}"""))
        header.append(NoEscape(r"Page \thepage"))
    doc.preamble.append(header)
    doc.change_document_style("header")
    ## Top portion of the page 1
    with doc.create(MiniPage(align='c')):
        doc.append(LargeText(bold("Learn Basics Workbook - "+ subject)))
        doc.append(NoEscape(r'\vspace{1cm}'))
    doc.append(LineBreak())
    doc.append(NoEscape(r"\noindent\rule{\textwidth}{1pt}\\"))
    # doc.append(NoEscape("""\\vspace{1cm}\\"""))
    doc.append(LineBreak())
    with doc.create(MiniPage(align='c')):
        doc.append(NoEscape("""\\underline{"""))
        doc.append(LargeText(bold("LaPIS Diagnostic Test Report - "+ subject)))
        doc.append(NoEscape("""}"""))
        # doc.append(NoEscape("""\\vspace{0.3cm}\\"""))
        doc.append(LineBreak())
        doc.append(LineBreak())
        # doc.append(NoEscape(r'\begin{tabular}{ | p{2cm} p{1cm} p{10cm}| }'))
        # doc.append(NoEscape(r'\rowcolors{1}{gray!10}{gray!10}'))
        # doc.append(NoEscape("""\hline"""))
        # doc.append(NoEscape(r'\hfil Name & \hfil: &\hfil '+stu_name+ r' \\'))
        # doc.append(NoEscape(r'\hfil Class & \hfil : &\hfil '+clas+ r' \\'))
        # doc.append(NoEscape(r'\hfil Section &\hfil : &\hfil '+sect+ r' \\'))
        # doc.append(NoEscape(r'\hfil School &\hfil : &\hfil '+schol+ r' \\'))
        # doc.append(NoEscape(r'\end{tabular}'))
        doc.append(NoEscape(r'{\renewcommand{\arraystretch}{4}'))
        # doc.append(NoEscape(r'\rowcolors{1}{gray!10}{gray!10}'))
        doc.append(NoEscape(r'\begin{tabular}{ | p{2cm} p{1cm} p{10cm}| }'))
        doc.append(NoEscape("""\hline"""))
        doc.append(NoEscape(r'\textbf{\LARGE Name } & \textbf{\large :} & \textbf{\large ' + stu_name +'}'+ r'\\' ))
        doc.append(NoEscape(r'\textbf{\LARGE Class } & \textbf{\large :} & \textbf{\large ' +clas +'}'r'\\'))
        doc.append(NoEscape(r'\textbf{\LARGE Section } & \textbf{\large :} &\textbf{\large ' +sect +'}'r'\\'))
        doc.append(NoEscape(r'\textbf{\LARGE School} & \textbf{\large :} & \textbf{\large ' +schol +'}'r'\\'))
        doc.append(NoEscape("""\hline"""))
        doc.append(NoEscape(r'\end{tabular}}'))
        doc.append(NoEscape("""\\vspace{1.5cm}"""))
        doc.append(LineBreak())
        doc.append(NoEscape(r"\noindent\rule{\textwidth}{1pt}"))
        doc.append(NoEscape("""\\vspace{1cm}"""))
        ## Adding bar graph
        doc.append(LineBreak())
        doc.append(NoEscape("""\\underline{"""))
        doc.append(LargeText(bold(stu_name+"'s Performance Report")))
        doc.append(NoEscape("""}"""))
        doc.append(LineBreak())
        doc.append(LineBreak())
        doc.append(NoEscape(r"""\includegraphics[ width = 10cm, keepaspectratio]{png_files/"""+stu_name+"""_"""+subject+"""_Class""" +clas +"""_bargraph.png}"""))
        doc.append(LineBreak())
        doc.append(LineBreak())
    doc.append(LineBreak())
    doc.append(pl.Command('newpage'))

## Planner Page
def page_2(subject,stu_name,clas,sect,schol):
    doc.append(pl.Command('centering'))
    doc.append(LargeText(bold(stu_name+"'s Study Planner")))
    doc.append(LineBreak())
    doc.append(NoEscape(r"\noindent\rule{\textwidth}{2pt}"))
    with doc.create(LongTable("| l | l| l | l | l | l |")) as data_table:
            data_table.add_hline()
            data_table.add_row(["Date", "Topic Planned","Q Number", "Teacher Remark","Teacher Sign","Parent Sign"])
            data_table.add_hline()
            data_table.end_table_header()
            data_table.add_hline()
            row = [" ", " ", " "," "," "," "]
            for i in range(15):
                data_table.add_row(row)
                data_table.append(NoEscape(r'[1.5ex]'))
                data_table.add_hline()
    doc.append(NoEscape(r'\bigskip')) 
    doc.append("Teacher's Feedback to Student")
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    doc.append(NoEscape(r"""\framebox(15cm,1.6cm){}"""))
    # doc.append(NoEscape(r'\item[] \framebox[\linewidth]{\rule{0pt}{2cm} {\vspace{10cm} }'))
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    with doc.create(MiniPage(width=NoEscape(r"0.45\textwidth"),pos='l', align='l')):
            doc.append(pl.Command('centering'))
            doc.append(NoEscape(r"\par\noindent\rule{40mm}{0.4pt} \linebreak Class Teacher Signature"))
    with doc.create(MiniPage(width=NoEscape(r"0.45\textwidth"),pos='l', align='l')):
            doc.append(pl.Command('centering'))
            doc.append(NoEscape(r"\par\noindent\rule{40mm}{0.4pt} \linebreak Principal Signature"))
            doc.append(LineBreak())
    doc.append(pl.Command('newpage'))  


def page_3(subject,stu_name,clas,sect,schol):
    doc.append(pl.Command('centering'))
    doc.append(LargeText(bold(stu_name+"'s Study Planner")))
    doc.append(LineBreak())
    doc.append(NoEscape(r"\noindent\rule{\textwidth}{2pt}"))
    doc.append(NoEscape(r'\begin{table}[H]'))
    doc.append(NoEscape(r'\centering'))
    doc.append(NoEscape(r'\renewcommand{\arraystretch}{2}'))
    doc.append(NoEscape(r'\begin{tabular}{|p{1.5cm}|p{2.5cm}|p{2cm}|p{2cm}|p{1.5cm}|p{1.5cm}|}'))
    doc.append(NoEscape(r'\hline'))
    doc.append(NoEscape(r'\multicolumn{1}{|c|}{\textbf{Date}} & \multicolumn{1}{c|}{\textbf{Topics Planned}} & \multicolumn{1}{c|}{\textbf{Q. Numbers}} & \multicolumn{1}{c|}{\textbf{Teacher Remark}} & \multicolumn{1}{c|}{\textbf{Teacher Sign}} & \multicolumn{1}{c|}{\textbf{Parent Sign}} \\'))
    doc.append(NoEscape(r'\hline'))
    for i in range(15):
        doc.append(NoEscape(r'          &       &       &       &       &  \\'))
        doc.append(NoEscape(r'\hline'))
    doc.append(NoEscape(r'\end{tabular}'))
    doc.append(NoEscape(r'\end{table}'))
    doc.append(NoEscape(r'\bigskip')) 
    doc.append("Teacher's Feedback to Student")
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    doc.append(NoEscape(r"""\framebox(15cm,1.6cm){}"""))
    # doc.append(NoEscape(r'\item[] \framebox[\linewidth]{\rule{0pt}{2cm} {\vspace{10cm} }'))
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    doc.append(LineBreak())    
    with doc.create(MiniPage(width=NoEscape(r"0.45\textwidth"),pos='l', align='l')):
            doc.append(pl.Command('centering'))
            doc.append(NoEscape(r"\par\noindent\rule{40mm}{0.4pt} \linebreak Class Teacher Signature"))
    with doc.create(MiniPage(width=NoEscape(r"0.45\textwidth"),pos='l', align='l')):
            doc.append(pl.Command('centering'))
            doc.append(NoEscape(r"\par\noindent\rule{40mm}{0.4pt} \linebreak Principal Signature"))
            doc.append(LineBreak())
    doc.append(pl.Command('newpage'))  






def sections_tables(roll, section_name):
    print(roll, section_name)
    weak_concepts_list = []
    topics_list = test_response[(test_response['lapis_roll_number'] == roll)&(test_response['response_output'] !='Correct') & (test_response['section_name'] == section_name)]['topic_name'].values.tolist()
    topics_list = list(dict.fromkeys(topics_list)) ## removes duplicates
    if len(topics_list) == 0:
        return


    for topic in topics_list:
        temp_concept_list = test_response[(test_response['lapis_roll_number'] == roll)&(test_response['response_output'] !='Correct')& (test_response['topic_name'] == topic) & (test_response['section_name'] == section_name)]['concept_name'].values.tolist()
        temp_concept_list = list(dict.fromkeys(temp_concept_list))
        if len(temp_concept_list) == 0:
            topics_list.remove(topic)
            continue
        weak_concepts_list.append(temp_concept_list)
    no_of_topics = len(topics_list)

    ##Cleaning the list from trailing spaces
    for i in range(len(topics_list)):
        topics_list[i] = str(topics_list[i]).strip()
        for j in range(len(weak_concepts_list[i])):
            weak_concepts_list[i][j] = str(weak_concepts_list[i][j]).strip()



    doc.append(NoEscape(r"""\begin{center}"""))
    # doc.append(NoEscape(r"""\begin{longtable}
        # \huge\textbf{"""+Section_name+"""}"""))
    # doc.append(NoEscape(r"""\Large{\textbf{"""+section_name+"""}}"""))
    # doc.append(LineBreak())
    doc.append(NoEscape(r'\medskip'))
    doc.append(NoEscape(r"""\begin{tikzpicture}"""))
    doc.append(NoEscape(r"""\node (table) [inner sep=0pt] {"""))
    doc.append(NoEscape(r'{\renewcommand{\arraystretch}{1.4}'))
    doc.append(NoEscape(r"""\begin{tabular}{  m{5.2cm} | m{12.2cm}  } """))
    doc.append(NoEscape(r"""\textbf{Topics} & \textbf{To be Improved}
        \\
        \hline"""))
    if no_of_topics != 1:
        for x in range(0,no_of_topics-1):
            concepts = ', '.join(weak_concepts_list[x])
            doc.append(NoEscape(r"""\normalsize{ \textbf{"""+ str(topics_list[x]) +"""}} & """+ str(concepts)))
            doc.append(NoEscape(r"""\\
            \hline"""))
    concepts = ', '.join(weak_concepts_list[no_of_topics-1])
    doc.append(NoEscape(r"""\normalsize{\textbf{"""+ str(topics_list[no_of_topics-1]) +"""}} & """+ str(concepts)))
    doc.append(NoEscape(r"""\end{tabular}}};"""))
    doc.append(NoEscape(r"""\draw [rounded corners=.5em] (table.north west) rectangle (table.south east);"""))
    doc.append(NoEscape(r"""\end{tikzpicture}"""))
    # doc.append(NoEscape(r"""\end{longtable}"""))
    doc.append(NoEscape(r"""\end{center}"""))
    ## Question Insert


    ## Question Insert
def add_content(roll):
    mistake_list_sorted = get_mistake_list(roll)
    relative_qno = 1
    for section_title, mistaken_qid in mistake_list_sorted.items():
        
        doc.append(NoEscape(r"\noindent\rule{\textwidth}{2pt}"))
        doc.append(NoEscape("""\\vspace{0.2cm}"""))
        doc.append(LineBreak())
        doc.append(pl.Command('centering'))
        doc.append(LargeText(bold(section_title)))
        doc.append(LineBreak())
        doc.append(NoEscape(r"\noindent\rule{\textwidth}{2pt}"))
        sections_tables(roll, section_title)
        for id in mistaken_qid:
            append_qr(id)
            questions = generate_woksheet_question_tag(id)
            for question_no in questions:
                append_questions(question_no, relative_qno)
                relative_qno = relative_qno + 1





def print_worksheet(roll):    
    ## Pylatex information
    

    section_response = section_percent[section_percent['lapis_roll_number'] == roll]
    percentage_overall = student_overall_percentage[student_overall_percentage['lapis_roll_number'] == roll]['percentage'].values[0]
    
    student_info = student_details[student_details['lapis_roll_number'] == roll]
    name = str(student_info['student_name'].values[0])
    class_studying = str(student_info['class'].values[0])
    section_studying = str(student_info['section'].values[0])
    
    sections = section_response['section_name'].values.tolist()
    percentage = section_response['percentage'].values.tolist()
    create_graphs(sections, percentage, name, roll, class_studying, subject_name)
    cover_page(subject_name, name, class_studying, section_studying,"Lotus Public School")
    page_3(subject_name, name, class_studying, section_studying,"Lotus Public School")

    add_content(roll)
    # append_qr('C6MDT2')
    # append_qr('C6MDT3')
    
    file_name = folder_name+name+"_"+class_studying+"custom"
    # print("Done : "+name)
    return file_name


def generate_worksheet(sc_code,std,s_name):
    global folder_name
    global school_code
    global current_standard
    global subject_name
    global q_list
    global q_len
    global append_char
    global tag_name
    global roll_numb
    global section_percent
    global section_names
    global section_count
    global student_overall_percentage
    global student_details
    global test_response
    global section_names_list
    global worksheet_questions
    global qr_db
    global  lapis_qr_question_ids
    global geometry_options
    global doc
    global file_name
    
    try:
        school_code=sc_code
        current_standard=std
        subject_name=s_name.lower()

        # q_list = []
        if subject_name == 'science':
            q_len = 60
            append_char = ["A", "B"]
            tag_name = 'C'+str(current_standard)+'SDT'
        elif subject_name == 'math':
            q_len = 40
            append_char = ["A", "B", "C"]
            tag_name = 'C'+str(current_standard)+'MDT'

        # print(school_code, current_standard, subject_name)
        db.get_info(school_code, current_standard, subject_name)

        roll_numb = db.roll_number()['lapis_roll_number'].values.tolist()
        section_percent = db.section_percentage()
        section_names, section_count = db.section_name_count()
        student_overall_percentage = db.indiv_percentage()
        student_details = db.stu_details()
        test_response = db.get_test_response()
        section_names_list = section_names['section_name'].values.tolist()


        worksheet_questions = db.get_worksheet_questions()

        # data1 = pd.read_csv("C6MDT_questions.csv")
        # worksheet_questions = pd.DataFrame(data1)

        qr_db = db.get_qr()



        lapis_qr_question_ids = qr_db['question_id'].values.tolist()

        # mistake_list = ['C6SDT1', 'C6SDT2', 'C6SDT3', 'C6SDT59']

        # generate_qr()
        print(roll_numb)
        # print("hi")
        # input()
        x=0
        for roll in roll_numb:
            
            # geometry_options = {"margin": "0.7in"} 
            geometry_options = {"top": "2.5cm", "bottom" : "2.5cm", "left" : "1.5cm", "right" : "1.5cm"}
            # geometry_options = {"top": "2.5cm", "bottom" : "2.5cm"}

            doc = Document(geometry_options=geometry_options)
            doc.documentclass = Command('documentclass', options=['12pt', 'a4paper'], arguments=['article'])
            get_lib()
            add_custom_commands()
            generate_qr()
            file_name = print_worksheet(roll)
            doc.generate_pdf(file_name, clean_tex=True)
            print("Done : ",roll)
            x+=1
            if(x==1):
                break
        print("Done and Dusted")
        return (True,"Worksheet generated succesfuly")

    except Exception as e:
        return (False,e)

# print(generate_worksheet(12,6,'math'))


