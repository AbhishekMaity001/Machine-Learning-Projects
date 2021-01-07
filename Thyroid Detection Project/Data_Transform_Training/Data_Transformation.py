from application_logging.logger import App_logger
import os
import pandas as pd



class Data_Transform:

    def __init__(self):
        self.goodDataPath = 'Training_Raw_Files_Validated/Good_Raw'
        self.log_writer = App_logger()

    def adding_Quotes_to_String_values(self):

        file = open('Training_logs/adding_Quotes_to_String_values.txt','a+')

        try:
            self.log_writer.log(file,"Adding Quotes to String Values Started !!!")
            onlyfiles = os.listdir(self.goodDataPath)
            for f in onlyfiles:
                df = pd.read_csv(self.goodDataPath +'/'+ f)
                column = ['sex', 'on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_medication', 'sick', 'pregnant',
                          'thyroid_surgery', 'I131_treatment', 'query_hypothyroid', 'query_hyperthyroid', 'lithium',
                          'goitre', 'tumor', 'hypopituitary', 'psych', 'TSH_measured', 'T3_measured', 'TT4_measured',
                          'T4U_measured', 'FTI_measured', 'TBG_measured', 'TBG', 'referral_source', 'Class']

                for col in df.columns :
                    if col in column:
                        df[col] = df[col].apply(lambda x : "'"+str(x)+"'")
                    if col not in column :
                        df[col] = df[col].replace('?',"'?'")
                df.to_csv(self.goodDataPath+"/"+f,index=None,header=True)
                self.log_writer.log(file,"Quotes added successfully!!")
            file.close()

        except Exception as e:
            self.log_writer.log(file,"Error while adding Quotes !! %s"%e)
            file.close()
