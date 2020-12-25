from application_logging.logger import App_logger
from datetime import datetime
import json
import os
from os import listdir
import shutil
import re
import pandas as pd


class Prediction_Data_Validation:

    """"
                This Class will be used for the validation done on the Raw Training Data.
    """

    def __init__(self,path):
        self.Batch_Directory = path
        self.schema_path = 'schema_prediction.json'
        self.log_writer = App_logger()


    def valuesFromSchema(self):
        """"
                This methods extract all the required information form the predefined schema file
                returns ---> LengthOfDateStampInFile, LengthOfTimeStampInFile, Column Names, Number of columns
        """

        try:
            with open(self.schema_path,'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            NumberofColumns = dic['NumberofColumns']
            ColumnNames = dic['ColName']

            file = open('Prediction_logs/valuesFromSchemaPredictionlog.txt','a+')
            msg = "LengthOfDateStampInFile---> %s" %LengthOfDateStampInFile + "\t"+ "LengthOfTimeStampInFile---> %s"%LengthOfTimeStampInFile + "\t"+"NumberofColumns---> %s"%NumberofColumns +"\n"
            self.log_writer.log(file,msg)
            print('fetched all the values....from schema_prediction json')
            file.close()

        except ValueError:
            file = open('Prediction_logs/valuesFromSchemaPredictionlog.txt','a+')
            self.log_writer.log(file,'ValueError :: value not found inside the schema_prediction file!!')
            file.close()
            raise ValueError

        except KeyError:
            file = open('Prediction_logs/valuesFromSchemaPredictionlog.txt','a+')
            self.log_writer.log(file,'KeyError :: KeyValue Error Incorrect key passed!!')
            file.close()
            raise KeyError

        except Exception as e:
            file = open('Prediction_logs/valuesFromSchemaPredictionlog.txt', 'a+')
            self.log_writer(file,str(e))
            file.close()
            raise e

        return LengthOfDateStampInFile , LengthOfTimeStampInFile , NumberofColumns , ColumnNames


    def manualRegex(self):
        """"
                This method returns the criteria for the regex validation
                returns ---> regex
        """
        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def validationFileName(self,regex,LengthOfDateStampInFile, LengthOfTimeStampInFile):
        """"
                    This method will validate the training raw csv files ... with the valid name of the files as per given in the schema as
                    agreed with the client.
        """
        self.deleteExistingGoodDataFolder()
        self.deleteExistingBadDataFolder()

        self.createDirectoryForGoodBadRawData()

        onlyfiles = [f for f in listdir(self.Batch_Directory)]
        try :
            file = open('Prediction_logs/nameValidationLog.txt','a+')
            print('entered the validation file name method')
            for filename in onlyfiles:
                if re.match(regex,filename):
                    splitbyDot = re.split('.csv',filename)
                    splitbyDot = (re.split('_',splitbyDot[0]))
                    if len(splitbyDot[1]) == LengthOfDateStampInFile :
                        if len(splitbyDot[2]) == LengthOfTimeStampInFile :
                            shutil.copy('Prediction_Batch_Files/'+filename,'Prediction_Raw_Files_Validated/Good_Raw')
                            self.log_writer.log(file,'Valid File Name! Files moved to Good_Raw Data Folder %s' % filename)
                        else :
                            shutil.copy('Prediction_Batch_Files/'+filename,'Prediction_Raw_Files_Validated/Bad_Raw')
                            self.log_writer.log(file, 'InValid File Name! Files moved to Bad_Raw Data Folder %s' % filename)
                    else :
                        shutil.copy('Prediction_Batch_Files/'+filename,'Prediction_Raw_Files_Validated/Bad_Raw')
                        self.log_writer.log(file, 'InValid File Name! Files moved to Bad_Raw Data Folder %s' % filename)

                else :
                    shutil.copy('Prediction_Batch_Files/'+filename,'Prediction_Raw_Files_Validated/Bad_Raw')
                    self.log_writer.log(file, 'InValid File Name! Files moved to Bad_Raw Data Folder %s' % filename)

            file.close()
            print('exited the validationFileName name method')

        except Exception as e :
            file = open('Prediction_logs/nameValidationLog.txt','a+')
            self.log_writer.log(file,'Error Occurred While validating the File Name :: %s',str(e))
            file.close()
            raise e


    def validateColumnLength(self,NumberofColumns):
        try :
            print('entered validated column length')
            file = open('Prediction_logs/columnValidationLog.txt','a+')
            self.log_writer.log(file,'Validation of columns length started!!!')

            for filename in listdir('Prediction_Raw_Files_Validated/Good_Raw/'):
                csv = pd.read_csv('Prediction_Raw_Files_Validated/Good_Raw/'+filename)
                if csv.shape[1] == NumberofColumns :
                    pass
                else :
                    shutil.move('Prediction_Raw_Files_Validated/Good_Raw/'+filename,'Prediction_Raw_Files_Validated/Bad_Raw')
                    self.log_writer.log(file,'Invalid Column Length!!! Files moved to Bad_Raw folder :: %s' % filename)
            self.log_writer.log(file,'Column length Validation Completed!!!')

        except OSError :
            file = open('Prediction_logs/columnValidationLog.txt','a+')
            self.log_writer.log(file,'OS Error :: %s' % OSError)
            file.close()
            raise OSError

        except Exception as e:
            file = open('Prediction_logs/columnValidationLog.txt','a+')
            self.log_writer.log(file,'Exception error %s' % e)
            file.close()
            raise e
        file.close()
        print('exited validated column length')

    def validateMissingValuesInWholeColumn(self):

        try :
            print('Entered the validate missing values in WHOLE column method')
            file = open('Prediction_logs/MissingValuesInColumn.txt','a+')
            self.log_writer.log(file,'Missing values in whole column started !!')
            for filename in listdir('Prediction_Raw_Files_Validated/Good_Raw'):
                csv = pd.read_csv('Prediction_Raw_Files_Validated/Good_Raw/'+filename)
                count = 0
                for columns in csv:
                    if (len(csv[columns])-csv[columns].count()) == len(csv[columns]) :
                        count+=1
                        shutil.move('Prediction_Raw_Files_Validated/Good_Raw/'+filename,'Prediction_Raw_Files_Validated/Bad_Raw')
                        self.log_writer.log(file,"Column was having all missing values!!! Files moved to Bad Raw Folder :: %s"%filename)
                        break
                if count==0:
                    csv.rename(columns={'Unnamed: 0':'Wafer'},inplace=True)
                    csv.to_csv('Prediction_Raw_Files_Validated/Good_Raw/'+filename,index=None,header=True)
            print('Exited the try of validate missing values in whole column method')

        except OSError:
            print('OS error')
            file = open('Prediction_logs/MissingValuesInColumn.txt','a+')
            self.log_writer.log(file,'Error occurred while validating the column missing values and moving the files OS Error :: %s'% OSError)
            file.close()
            raise OSError
        except Exception as e:
            print('Exception as e')
            file = open('Prediction_logs/MissingValuesInColumn.txt', 'a+')
            self.log_writer.log(file,'Error occurred while validating the column missing values and moving the files  Exception e:: %s'%e)
            raise e

        file.close()
        print('Exited the validate missing values in WHOLE column method')

    def deleteExistingGoodDataFolder(self):

        """"This method will delete the good raw data that we created to store the good raw data after validation so after inserting
            inside the database table we will delete these good and bad raw data folder for space optimization
        """

        try:
            print('entered deleted good raw data folder')
            path = 'Prediction_Raw_Files_Validated/'
            if os.path.isdir(path+'Good_Raw/'):
                shutil.rmtree(path+'Good_Raw/')
                file = open('Prediction_logs/General_log.txt','a+')
                self.log_writer.log(file,'Deleted Good_Raw Data sucessfully!!')
                file.close()

        except OSError as s:
            file = open('Prediction_logs/General_log.txt', 'a+')
            self.log_writer.log(file, 'Error while deleting Good_Raw Data %s'%s)
            file.close()
            raise OSError

    def deleteExistingBadDataFolder(self):

        """"
                    This method will delete the bad raw data that we created to store the bad raw data after validation so after inserting
                    inside the database table we will delete these good and bad raw data folder for space optimization
        """

        try:
            print('entered deleted bad raw data folder')
            path = 'Prediction_Raw_Files_Validated/'
            if os.path.isdir(path+'Bad_Raw/'):
                shutil.rmtree(path+'Bad_Raw/')
                file = open('Prediction_logs/General_log.txt','a+')
                self.log_writer.log(file,'Deleted Bad_Raw Data sucessfully!!')
                file.close()

        except OSError as s:
            file = open('Prediction_logs/General_log.txt', 'a+')
            self.log_writer.log(file, 'Error while deleting Bad_Raw Data %s'%s)
            file.close()
            raise OSError

    def createDirectoryForGoodBadRawData(self):


        try :
            print('entered create directory for good bad raw data')
            path = os.path.join('Prediction_Raw_Files_Validated/','Good_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join('Prediction_Raw_Files_Validated/', 'Bad_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)
            print('exit create directory for good bad raw data')

        except OSError as s:
            file = open('Prediction_logs/General_log.txt','a+')
            self.log_writer.log(file,'Error while creating the Good_Bad Raw data folders.. %s'%s)
            file.close()
            raise OSError


    def moveBadFilesToArchiveBad(self):
        print("inside moveBadFilesToArchiveBad method")
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:

            source = 'Prediction_Raw_Files_Validated/Bad_Raw/'
            if os.path.isdir(source):
                path = "PredictionArchiveBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = 'PredictionArchiveBadData/BadData_' + str(date) + "_" + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)
                file = open("Prediction_logs/General_log.txt", 'a+')
                self.log_writer.log(file, "Bad files moved to archive")
                path = 'Prediction_Raw_Files_Validated/'
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                self.log_writer.log(file, "Bad Raw Data Folder Deleted successfully!!")
                file.close()
        except Exception as e:
            file = open("Prediction_logs/General_log.txt", 'a+')
            self.log_writer.log(file, "Error while moving bad files to archive:: %s" % e)
            file.close()
            raise e





