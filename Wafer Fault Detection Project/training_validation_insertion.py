from datetime import datetime
from application_logging.logger import App_logger

class train_validation :

    def __init__(self,path):
        print('inside init')

        self.file_object = open("Training_logs/Training_main_log.txt", 'a+')
        self.log_writer = App_logger()

    def train_validation(self):

        try :
            self.log_writer.log(self.file_object,"Validation on files started!! ")
            print('end')

        except Exception as e:
            return e

