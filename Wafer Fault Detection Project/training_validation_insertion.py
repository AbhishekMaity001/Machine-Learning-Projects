from datetime import datetime
from application_logging.logger import App_logger
from Training_Raw_Data_Validation.rawValidation import Raw_Data_Validation

class train_validation :

    def __init__(self,path):
        print('inside --init-- of training_validation_insertion')

        self.file_object = open("Training_logs/Training_main_log.txt", 'a+')
        self.log_writer = App_logger()
        self.raw_data = Raw_Data_Validation(path)

        print('initializd all the objects of the train validation --init--')

    def train_validation(self):

        try :
            print('validation on files started....')
            self.log_writer.log(self.file_object,"Validation on files started!! ")
            LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColumnNames = self.raw_data.valuesFromSchema()
            self.file_object.close()

            regex = self.raw_data.manualRegex()

            self.raw_data.validationFileName(regex,LengthOfDateStampInFile, LengthOfTimeStampInFile)

            self.raw_data.validateColumnLength(NumberofColumns)

            self.raw_data





            print('end of train validation method...')

        except Exception as e:
            raise e

