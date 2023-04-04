import pandas as pd
import numpy as np
import re

file=open('C8M - LaPIS Workbook\main.tex','r',newline='',encoding='utf-8').read()
quedata = re.findall(r'\%start-of-the-question(.*?)\%end-of-the-question', file, re.S)
conceptIdList=[]
questionIdList=[]
questionList=[]
answerList=[]
hintsList=[]
errorloc = []

tag_name = input('tag name (Ex: C6SDT) ')

subject = input('Subject: ')

q_list = []
if subject == 'science':
    q_len = 60
    append_char = ["A", "B"]
elif subject == 'math':
    q_len = 40
    append_char = ["A", "B", "C"]




for i in range(1, (q_len+1)):
    id = tag_name + str(i)
    for j in range(len(append_char)):
        dr = ''
        dr = dr+id+append_char[j]
        q_list.append(dr)



def main():
    try:
        for i in range(0,len(quedata)):

            string = re.sub('\n', '', quedata[i])
            string = quedata[i]

           

            # the below code removes every occurance of { and } we need to look back again in this thing
            # because we may not want to remove every occurance of it
            # string = re.sub(r'[\{*\}*]','',string)
            
            split_string = re.split(r'%#', string)
            
            new_list = [x for x in split_string if x != '']

            # for content in range(len(new_list)):
            #     print(new_list[content])
            #     input()
            
            
            if len(new_list) < 5:
                cid = '{}'
                conceptIdList.append(cid)
                if re.search(r'\\questionID',new_list[1]):
                    qid=re.sub(r'\\questionID','',new_list[1])
                    qid=qid.split('}',1)[1]
                    qid=re.sub(r'[\{\}]','',qid)
                    questionIdList.append(qid)
                    
                    if qid == q_list[i]:
                        errorloc.append('Pass')
                    else:
                        errorloc.append('Missing')

                question = '{}'
                questionList.append(question)
                hint = '{}'
                hintsList.append(hint)
                answerList.append('Error')
                pass

            else:
                answerList.append('Pass')
                # print(re.search(r'\\conceptID',new_list[0]))
                # print(re.sub(r'\\conceptID','',new_list[0]))

                # to extract the concept id if there exists a better way please let me know
                if re.search(r'\\conceptID',new_list[0]):
                    cid=re.sub(r'\\conceptID','',new_list[0])
                    conceptIdList.append(cid)
                
                    

                
                
                if re.search(r'\\questionID',new_list[1]):
                    qid=re.sub(r'\\questionID','',new_list[1])
                    qid=qid.split('}',1)[1]
                    qid=re.sub(r'[\{\}]','',qid)
                    questionIdList.append(qid)
                    
                    if qid == q_list[i]:
                        errorloc.append('Pass')
                    else:
                        errorloc.append('Missing')
                
            
                # to extract the question id and question if there exists a better way please let me know
                if re.search(r'\\question',new_list[2]):
                    q_split = re.split(r'\\question', new_list[2])
                    # question=re.sub(r'[\\a-z\{+\}+%]','',new_list[1])
                    question=re.sub(r'\\question','',q_split[1])
                    questionList.append(question)
        

                if re.search(r'\\hints',new_list[3]):
                    h_split = re.split(r'\\hints', new_list[3])
                    hint=re.sub(r'\\hints','',h_split[1])
                    hintsList.append(hint)
    finally:
        df={}
        df['question_id'] = questionIdList
        df['id_error'] = errorloc
        df['content_error'] = answerList
        df['concept_id'] =conceptIdList
        df['question'] = questionList
        df['hint'] =hintsList  

        # print(hintsList)
        newdf=pd.DataFrame.from_dict(df,orient='index')
        newdf=newdf.transpose()
        print(newdf)
        newdf.to_csv('C8MDT_questions.csv',index=False)

       
            
main()






