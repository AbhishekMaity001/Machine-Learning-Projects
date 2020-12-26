import pandas as pd
from application_logging.logger import App_logger


class Data_Getter :

    def __init__(self):
        self.log_writer = App_logger()
        self.prediction_file = 'Prediction_File_From_DB/InputFile.csv'

    def get_data(self):

        try :
            file = open('Prediction_logs/Prediction_main_log.txt','a+')
            self.log_writer.log(file,"Entered the get_data method of Data_Getter class ")
            self.data = pd.read_csv(self.prediction_file)
            self.log_writer.log(file,"Data Loaded successfully!!!")
            file.close()
            return self.data
        except Exception as e:
            file = open('Prediction_logs/Prediction_main_log.txt','a+')
            self.log_writer.log(file,"Error while loading the file :: %s "%e)
            file.close()
            raise e
