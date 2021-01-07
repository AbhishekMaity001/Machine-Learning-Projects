import os
import shutil
import pickle
from application_logging.logger import App_logger

class File_Operation :

    def __init__(self):
        self.log_writer = App_logger()
        self.model_directory = 'models/'

    def save_model(self,model,file_name):

        file = open("Training_logs/Model_Training_Log.txt",'a+')
        self.log_writer.log(file,"Entered the save_model method of the File_Operation class now saving the model....")

        try :
            print("Entered the save_model method !!! ")
            path = os.path.join(self.model_directory , file_name)
            if(os.path.isdir(path)) :
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else :
                os.makedirs(path)

            with open(path + '/'+ file_name + '.sav', 'wb') as f :
                pickle.dump(model,f)
            self.log_writer.log(file,"Model saved successfully in the models folder name : %s"%file_name)
            print("Exited the save_model method !!! ")
            file.close()
            return  'success'

        except Exception as e :
            self.log_writer.log(file, "error occurred while saving the model  %s" % str(e))
            file.close()
            raise e

    def find_correct_model_file(self,cluster_number):

        f = open("Training_logs/Model_Training_Log.txt",'a+')
        self.log_writer.log(f,"Entered the find_correct_model_method for finding the correct model!!!")
        try :
            self.cluster_number = cluster_number
            self.model_directory = self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.model_directory)
            for self.file in self.list_of_files :
                try :
                    if (self.file.index(str(self.cluster_number))!=-1) :
                        self.model_name = self.file

                except :
                    continue
            self.model_name = self.model_name.split('.')[0]
            self.log_writer.log(f,"Exited the find_correct_model_method after finding the correct model---->")
            return self.model_name

        except Exception as e :
            self.log_writer.log(f,"Error occured while finding the correct model :: %s"% str(e))
            raise e


    def load_model(self,filename):

        file = open('Prediction_logs/Prediction_main_log.txt','a+')
        self.log_writer.log(file,"Entered the load_model method of File_Operation class!!!!")
        try:
            with open(self.model_directory+filename+'/'+filename+'.sav','rb') as f :
                self.log_writer.log(file,"Model loaded : %s .sav Successfully."%filename)
                file.close()
                print('Model loaded successfully now exiting the load_model method!!!!')
                return pickle.load(f)
        except Exception as e:
            self.log_writer.log(file,"Error while loading the file :: %s"%e)
            file.close()
            raise e











