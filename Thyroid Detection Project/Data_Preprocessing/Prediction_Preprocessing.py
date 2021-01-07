import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
from application_logging.logger import App_logger
import pickle





class Preprocessor:

    def __init__(self):
        self.log_writer = App_logger()

    def remove_columns(self,data,columns):
        try :
            print('inside the remove column method')
            file_object = open('Prediction_logs/Prediction_main_log.txt', 'a+')
            self.log_writer.log(file_object,"Entered the Remove column method of the Preprocessor class---->")
            self.data = data
            self.columns = columns
            self.useful_data = self.data.drop(labels=columns,axis=1)
            self.log_writer.log(file_object,"Sucessfully removed the columns and returned the useful_data")
            file_object.close()
            print('sucessfully exit the remove_columns method')
            return self.useful_data


        except Exception as e:
            file_object = open('Prediction_logs/Prediction_main_log.txt', 'a+')
            self.log_writer.log(file_object,"Error while removing the columns --->  :: %s"%e)
            file_object.close()
            raise e

    def separate_label_feature(self,data,label_column_name):

        try :
            print('inside separate_label_features')
            file_object = open('Training_logs/Model_Training_Log.txt', 'a+')
            self.log_writer.log(file_object,'Entered the separate_label_feature method of preprocessor class')
            self.X = data.drop(labels=label_column_name,axis=1)
            self.Y = data[label_column_name]
            self.log_writer.log(file_object, 'Exit the separate_label_feature method of preprocessor class')
            file_object.close()
            print('Exited separate_label_features')
            return self.X,self.Y
        except Exception as e:
            file_object = open('Training_logs/Model_Training_Log.txt', 'a+')
            self.log_writer.log(file_object, 'Error occured in separate_label_feature method of preprocessor class :: %s' % str(e))
            file_object.close()
            raise e

    def is_null_present(self,data):

        try :
            print('inside is_null_present')
            file_object = open('Prediction_logs/Prediction_main_log.txt', 'a+')
            self.log_writer.log(file_object, 'Entered the is_null_present method of preprocessor class')
            self.null_present = False
            self.null_counts = data.isnull().sum()
            for i in self.null_counts :
                if i>0:
                    self.null_present = True
                    break

            if (self.null_present):
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isnull().sum())
                dataframe_with_null.to_csv('preprocessing_data/null_values.csv')
                self.log_writer.log(file_object,"Found the null values and stored a csv file as null_values.csv now exiting the is_null_present method")

            file_object.close()
            print('exit is_null_present')
            return self.null_present

        except Exception as e:

            file_object = open('Prediction_logs/Prediction_main_log.txt', 'a+')

            self.log_writer.log(file_object,"Error while finding the missing values :: %s"% str(e))
            file_object.close()
            raise e

    def impute_Missing_Values(self,data):

        file_object = open('Prediction_logs/Prediction_main_log.txt', 'a+')
        self.data = data
        self.log_writer.log(file_object,"Entered the imputer method of KNN")
        try :
            imputer = KNNImputer(n_neighbors=3,weights='uniform',missing_values=np.nan)
            self.new_array = imputer.fit_transform(self.data)
            self.new_data = pd.DataFrame(data=self.new_array,columns=self.data.columns)
            self.log_writer.log(file_object,"Successfully imputed the NaN values now exiting the method!!")
            file_object.close()
            print('exiting imputer KNN')
            return self.new_data

        except Exception as e:
            file_object = open('Prediction_logs/Prediction_main_log.txt', 'a+')
            self.log_writer.log(file_object,"Error while imputing the missing values :: %s"%str(e))
            raise e

    def get_columns_with_zero_std_dev(self,data):
        file_object = open('Prediction_logs/Prediction_main_log.txt', 'a+')
        self.log_writer.log(file_object,"Entered the get_columns_with_zero_std_dev method !!!")
        self.data_n = data.describe()
        self.columns = data.columns
        self.col_to_drop = []
        try :
            for x in self.columns:
                if (self.data_n[x]['std'] == 0) :
                    self.col_to_drop.append(x)
            self.log_writer.log(file_object,"Appended the columns with 0 std dev to col_to_drop Successfully now exit the method!!!")
            file_object.close()
            print('exiting the zero std_Dev')
            return self.col_to_drop

        except Exception as e:
            self.log_writer.log(file_object,"Error occurred while getting columns with 0 std dev :: %s" % str(e))
            file_object.close()
            raise e

    def replaceInvalidValuesWithNaN(self,data):

        file = open('Prediction_logs/Model_Training_Log.txt','a+')
        try :
            self.log_writer.log(file,"Starting to replace the invalid ? values with np.NaN")
            for col in data.columns:
                cnt = data[col][data[col] == '?'].count()
                if cnt!=0:
                    data[col] = data[col].replace('?',np.nan)
            file.close()
            return data
        except Exception as e:
            self.log_writer.log(file,"Error Occurred while replacing the ? to np.NaN :: %s"%str(e))
            file.close()
            raise e

    def encodeCategoricaldata(self,data):

        data['sex'] = data['sex'].map({'F':0, 'M':1})
        cat_data = data.drop(['age','T3','TT4','T4U','FTI','sex'],axis=1) # dropping the values with int and float type

        for column in cat_data.columns :
            if (data[column].nunique()) == 1:
                if data[column].unique()[0] == 'f' or data[column].unique()[0] == 'F':  # map the variables same as we did in training i.e. if only 'f' comes map as 0 as done in training
                    data[column] = data[column].map({data[column].unique()[0]: 0})
                else:
                    data[column] = data[column].map({data[column].unique()[0]: 1})
            elif (data[column].nunique()) == 2:
                data[column] = data[column].map({'f': 0, 't': 1})

        data = pd.get_dummies(data,columns=['referral_source'])

        return data



