from database_module import Database

class Lapis(Database):
    
    def insert_conceptId(self,conceptId_data):
        try:
                for concept in conceptId_data:
                        query="INSERT INTO main.lapis_concept_id(concept_id, concept_name, topic_name, section_name, chapter_tag) VALUES ({}, '{}', '{}', '{}', '{}');".format(concept['concept_id'],concept['concept_name'],concept['topic_name'],concept['section_name'],concept['chapter_tag'])
                        Database.cursor.execute(query)
                        # Database.conn.commit()
                Database.conn.commit()
                return (True,"Data inserted successfuly")
        except Exception as e:
                Database.conn.rollback()
                return (False, str(e)+" Also check 'Concept ID' column, may found duplicate ID.")
          
                
    def insert_lapisQr(self,qr_data):
        try:
                # print(qr_data)
                for qr in qr_data:
                        query="INSERT INTO main.lapis_qr(question_id, video_link, video_description) VALUES ('{}', '{}', '{}');".format(qr['question_id'],qr['video_link'],qr['description'])
                        Database.cursor.execute(query)
                Database.conn.commit()
                return (True,'Data inserted Successfuly')

        except Exception as e:
                Database.conn.rollback()
                return (False,str(e)+" Also check 'Question ID' column, may found duplicate ID.")