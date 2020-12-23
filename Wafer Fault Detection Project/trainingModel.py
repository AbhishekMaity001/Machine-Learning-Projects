""""
            This is the main entry for the training of the Machine Learning Model
"""
from application_logging.logger import App_logger
from data_ingestion import data_loader
from Data_Preprocessing.Preprocessing import Preprocessor

class trainModel :

    def __init__(self):
        self.log_writer = App_logger()
        self.file_object = open('Training_logs/Model_Training_Log.txt','a+')

    def trainingModel(self):

        self.log_writer.log(self.file_object,"Start of the Training !!!!!")
        try :
            print('loading the data')
            data_getter = data_loader.Data_Getter() # object init
            data = data_getter.get_data() # calling the method
            print('data loaded in data variable!!')

            """"Starting the Preprocessing on the data"""

            print('entering the preprocessing method')
            preprocessor = Preprocessor() # object init
            data = preprocessor.remove_columns(data,['Wafer']) # removing the first column because that will not contribute to our output
            print('the new data is --->',data.columns)

            X,Y = preprocessor.separate_label_feature(data,'Output')
            print("got the X and Y features")

            null_present = preprocessor.is_null_present(X)
            print(null_present)

            if(null_present):
                X = preprocessor.impute_Missing_Values(X)

            print('imputed')
            cols_to_drop = preprocessor.get_columns_with_zero_std_dev(X)
            print("done cols_to_drop")

            X = preprocessor.remove_columns(data, cols_to_drop)
            print('now we will enter clustering approach')









        except Exception as e :
            print('Exception as e')
            raise e