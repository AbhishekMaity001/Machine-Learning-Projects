from datetime import datetime
from os import listdir
import pandas as pd
from application_logging.logger import App_logger

class Data_Transform():

    def __init__(self):
        self.goodDataPath = "Training_Raw_Files_Validated/Good_Raw"
        self.log_writer = App_logger()

    def replaceMissingValuesWithNull(self):

        file = open('Training_logs/data_transformation_log.txt','a+')

        try :
            print('Entered Missing values with null')
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for filename in onlyfiles:
                df = pd.read_csv(self.goodDataPath+'/'+filename)
                df.fillna('NULL',inplace=True)
                df['Wafer'] = df['Wafer'].str[6:]
                df.to_csv(self.goodDataPath+"/"+filename, index=None, header=True)
                self.log_writer.log(file,'Data Transformation done successfully!! %s' % filename)

        except Exception as e:
            print('Exception as e error')
            file = open('Training_logs/data_transformation_log.txt', 'a+')
            self.log_writer.log(file,'Error while doing Data Transformation!! %s'%e)
            file.close()

        file.close()
        print('Exited Missing values with null')