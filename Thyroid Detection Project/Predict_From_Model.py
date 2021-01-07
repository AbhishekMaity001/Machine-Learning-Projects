import pandas as pd
from application_logging.logger import App_logger
from File_Operations.file_methods import File_Operation
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_Validation
from data_ingestion.data_loader_prediction import Data_Getter
from Data_Preprocessing.Prediction_Preprocessing import Preprocessor
import pickle

class prediction:
    def __init__(self,path):
        self.log_writer = App_logger()
        self.file_object = open("Prediction_logs/Prediction_main_log.txt",'a+')
        self.data_getter = Data_Getter()
        self.preprocessor = Preprocessor()
        self.file_operation = File_Operation()
        if path is not None :
            self.pred_data_val = Prediction_Data_Validation(path)

    def prediction_From_Model(self):

        try :
            self.pred_data_val.delete_Prediction_File()
            self.log_writer.log(self.file_object,"Start of predictions!!!")
            data = self.data_getter.get_data()



            #cols_to_drop = self.preprocessor.get_columns_with_zero_std_dev(data)
            cols_to_drop = ['TSH_measured', 'T3_measured', 'TT4_measured', 'T4U_measured',
                            'FTI_measured', 'TBG_measured', 'TBG', 'TSH']
            data = self.preprocessor.remove_columns(data,cols_to_drop)

            data = self.preprocessor.replaceInvalidValuesWithNaN(data)

            data = self.preprocessor.encodeCategoricaldata(data)

            is_null_present = self.preprocessor.is_null_present(data)
            if(is_null_present):
                data = self.preprocessor.impute_Missing_Values(data)

            kmeans = self.file_operation.load_model('KMeans')
            clusters = kmeans.predict(data)
            data['clusters'] = clusters
            clusters = data['clusters'].unique()
            result=[]
            with open('EncoderPickle/enc.pickle', 'rb') as ff: #let's load the encoder pickle file to decode the values
                encoder = pickle.load(ff)

            for i in clusters:
                cluster_data = data[data['clusters']==i]
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                model_name = self.file_operation.find_correct_model_file(i)
                model = self.file_operation.load_model(model_name)
                for val in (encoder.inverse_transform(model.predict(cluster_data))):
                    result.append(val)
            result = pd.DataFrame(result, columns=['Predictions'])
            path = "Prediction_Output_File/Predictions.csv"
            result.to_csv(path, header=True)
            self.log_writer.log(self.file_object,'Successful End of Predictions!!! :) ')

        except Exception as e:
            self.log_writer.log(self.file_object,"Error occurred while doing the Predictions !! %s"%e)
            self.file_object.close()
            raise e

        return path