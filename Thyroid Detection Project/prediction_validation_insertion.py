from datetime import datetime
from application_logging.logger import App_logger
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_Validation
from Data_Transform_Prediction.Data_Transformation_Prediction import Data_Transform_Predict
from Data_Prediction_Insertion_Into_Database.databaseOperations_Predictions import DBOperation





class pred_validation:

    def __init__(self,path):
        print('inside --init-- of pred_validation class')

        self.file_object = open("Prediction_logs/Prediction_main_log.txt", 'a+')
        self.log_writer = App_logger()
        self.raw_data = Prediction_Data_Validation(path)
        self.data_transform = Data_Transform_Predict()
        self.dbOperation = DBOperation()

        print('initializd all the objects of the train validation --init--')


    def prediction_validation(self):

        try:
            self.log_writer.log(self.file_object,"Validation on prediction files started!!!!")
            LengthOfDateStampInFile, LengthOfTimeStampInFile , NumberofColumns, ColumnNames = self.raw_data.valuesFromSchema()
            regex = self.raw_data.manualRegex()
            self.raw_data.validationFileName(regex)
            self.raw_data.validateColumnLength(NumberofColumns)
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "Validation on prediction files completed Successfully!!!")

            self.log_writer.log(self.file_object, "Transformation on prediction files Started !!!")
            print("startintg the data transformation")

            #self.data_transform.replaceMissingValuesWithNull()
            self.data_transform.adding_Quotes_to_String_values()

            self.log_writer.log(self.file_object, "Transformation on prediction files completed Successfully!!!")

            self.log_writer.log(self.file_object, "DB Operation on prediction files Started !!!")
            self.dbOperation.createTableDB('Prediction',ColumnNames)
            self.log_writer.log(self.file_object, "Prediction database & tables created !!!")

            self.log_writer.log(self.file_object, "Inserting data into tables Started !!!")
            self.dbOperation.insertIntoTableGoodData('Prediction')
            self.log_writer.log(self.file_object, "Inserting data into tables completed Successfully !!!")

            self.log_writer.log(self.file_object,"Deleting the Good Data Folder after inserting the good data")
            self.raw_data.deleteExistingGoodDataFolder()
            self.log_writer.log(self.file_object, "Deleting the Good Data Folder completed successfully!!1")

            self.log_writer.log(self.file_object, "Moving Bad_Data Folder into Archived folder and Deleting Bad_Data Folder")
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object,"Moving and Deleting Bad_Data folder completed Successfully!!!")
            self.log_writer.log(self.file_object, "Validation operation completed Successfully!!!")
            self.log_writer.log(self.file_object, "Now Extracting csv file from the DB table !!!")
            self.dbOperation.selectDataFromTableIntoCSV('Prediction')
            self.log_writer.log(self.file_object, "Extracted CSV file Successfully!!!")

            print("Successfully done the validation on the Prediction Files!!!")



            self.file_object.close()

        except Exception as e :
            self.log_writer.log(self.file_object,"Error occurred in prediction validation insertion file :: %s"%str(e))
            self.file_object.close()
            raise e