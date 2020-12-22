from datetime import datetime
from application_logging.logger import App_logger
from Training_Raw_Data_Validation.rawValidation import Raw_Data_Validation
from Data_Transform_Training.Data_Transformation import Data_Transform
from Data_Training_Insertion_Into_Database.databaseOperations import DBOperation

class train_validation :

    def __init__(self,path):
        print('inside --init-- of training_validation_insertion')

        self.file_object = open("Training_logs/Training_main_log.txt", 'a+')
        self.log_writer = App_logger()
        self.raw_data = Raw_Data_Validation(path)
        self.data_transform = Data_Transform()
        self.dbOperation = DBOperation()

        print('initializd all the objects of the train validation --init--')

    def train_validation(self):

        try :
            print('validation on files started....')
            self.log_writer.log(self.file_object,"Validation on files started!! ")
            LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColumnNames = self.raw_data.valuesFromSchema()


            regex = self.raw_data.manualRegex()

            self.raw_data.validationFileName(regex,LengthOfDateStampInFile, LengthOfTimeStampInFile)

            self.raw_data.validateColumnLength(NumberofColumns)

            self.raw_data.validateMissingValuesInWholeColumn()
            print('back to home after validation completed on WHOLE COLUMN')

            self.log_writer.log(self.file_object,'Validation on files completed!!')
            self.log_writer.log(self.file_object,'Starting Data Transformation process!!')

            self.data_transform.replaceMissingValuesWithNull()

            self.log_writer.log(self.file_object,"Data Transformation Completed Sucessfully!!")
            self.log_writer.log(self.file_object,"Now Creating Training Database and Tables based on the given Schema.json data")

            self.dbOperation.createTableDB('Training',ColumnNames)
            print('tables created done')

            self.log_writer.log(self.file_object,"Tables Created Successfully!!!")
            self.log_writer.log(self.file_object, "Inserting Data into Tables started!!!")

            self.dbOperation.insertIntoTableGoodData('Training')
            print('insertion done sucessfully!!!')

            self.dbOperation.selectDataFromTableIntoCSV('Training')













            print('end of train validation method...')
            self.file_object.close()

        except Exception as e:
            raise e

