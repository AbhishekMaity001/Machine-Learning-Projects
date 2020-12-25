from datetime import datetime
from application_logging.logger import App_logger
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_Validation
#from Data_Transform_Training.Data_Transformation import Data_Transform
from Data_Training_Insertion_Into_Database.databaseOperations import DBOperation





class pred_validation:

    def __init__(self,path):
        print('inside --init-- of pred_validation class')
        self.file_object = open("Prediction_logs/Prediction_main_log.txt", 'a+')
        self.log_writer = App_logger()
        self.raw_data = Prediction_Data_Validation(path)
        #self.data_transform = Data_Transform_Predict()
        self.dbOperation = DBOperation()

        print('initializd all the objects of the train validation --init--')
