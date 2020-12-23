import sqlite3
import shutil
import os
from os import listdir
import csv
from datetime import datetime
from application_logging.logger import App_logger





class DBOperation():

    def __init__(self):
        self.path = 'Training_Database/'
        self.goodFilePath = 'Training_Raw_Files_Validated/Good_Raw'
        self.badFilePath = 'Training_Raw_Files_Validated/Bad_Raw'
        self.log_writer = App_logger()

    def dataBaseConnection(self,DatabaseName):

        """"
                    This method you will pass any db name so that it will connect that db then return that connection object
        """

        try :
            conn = sqlite3.connect(self.path+DatabaseName+'.db')
            file = open('Training_logs/Database_Connection_log.txt','a+')
            self.log_writer.log(file,"Database connected sucessfully!!---> %s"%DatabaseName)
            file.close()

        except ConnectionError:
            file = open('Training_logs/Database_Connection_log.txt','a+')
            self.log_writer.log(file, "Database connection error!!---> %s" % ConnectionError)
            file.close()

        return conn

    def createTableDB(self,DatabaseName,column_names):

        try :
            print('inside table create method')
            conn = self.dataBaseConnection(DatabaseName)
            c = conn.cursor()
            c.execute("SELECT count(name) from sqlite_master WHERE type='table' AND name = 'Good_Raw_Data' ")
            if c.fetchone()[0]==1 :
                conn.close()
                file = open('Training_logs/create_Table_DB_log.txt','a+')
                self.log_writer.log(file,'Tables created successfully!!!')
                file.close()

                f = open('Training_logs/Database_Connection_log.txt','a+')
                self.log_writer.log(f,"Database closed successfully!!!----> %s"%DatabaseName)
                f.close()

            else :
                for key in column_names.keys():
                    type = column_names[key]
                    try :
                        conn.execute('ALTER table Good_Raw_Data ADD COLUMN "{colname}" {datatype} '.format(colname=key,datatype=type))

                    except :
                        conn.execute('CREATE TABLE Good_Raw_Data ({colname} {datatype})'.format(colname=key,datatype=type))

                conn.close()
                file = open('Training_logs/create_Table_DB_log.txt','a+')
                self.log_writer.log(file,"Tables created successfully!!!")
                file.close()

                f = open('Training_logs/Database_Connection_log.txt', 'a+')
                self.log_writer.log(f, "Database closed successfully!!!----> %s" % DatabaseName)
                f.close()

        except Exception as e:

            file = open('Training_logs/create_Table_DB_log.txt', 'a+')
            self.log_writer.log(file, "Tables creating error !!! %s"%e)
            file.close()
            conn.close()
            f = open('Training_logs/Database_Connection_log.txt', 'a+')
            self.log_writer.log(f, "Database closed successfully!!!----> %s" % DatabaseName)
            f.close()
            raise e

    def insertIntoTableGoodData(self,DatabaseName):

        print('inside insert into table good data')

        conn = self.dataBaseConnection(DatabaseName)
        goodFilePath = self.goodFilePath
        badFilePath = self.badFilePath

        onlyfiles = [f for f in listdir(goodFilePath)]
        file = open('Training_logs/insert_Table_log.txt', 'a+')
        for f in onlyfiles :
            try :
                with open(goodFilePath+'/'+f,'r') as fl:
                    next(fl)
                    reader = csv.reader(fl,delimiter="\n")
                    for line in enumerate(reader) :
                        for row in (line[1]):
                            try :
                                conn.execute("INSERT INTO Good_Raw_Data values ({values}) ".format(values=row))
                                self.log_writer.log(file,"%s File Loaded Successfully "%fl)
                                conn.commit()

                            except Exception as e:
                                raise e

            except Exception as e:

                conn.rollback()
                self.log_writer.log(file,"Error while inserting into the table %s "%e)
                shutil.move(goodFilePath +'/'+f, badFilePath)
                self.log_writer.log(file,"File Moved Successfully %s"%f)
                file.close()
                conn.close()
        file.close()
        conn.close()

    def selectDataFromTableIntoCSV(self,DatabaseName):

        print('inside the extration csv method')

        self.fileFromDB = 'Training_File_From_DB/'
        self.fileName = 'InputFile.csv'
        file = open('Training_logs/ExportToCsv.txt','a+')
        try :
            conn = self.dataBaseConnection(DatabaseName)
            sqlQuery = "SELECT * FROM Good_Raw_Data"
            cursor = conn.cursor()
            cursor.execute(sqlQuery)

            results = cursor.fetchall()

            #now lets get the headers of the file fiest
            headers = [i[0] for i in cursor.description]

            if not os.path.isdir(self.fileFromDB):
                os.makedirs(self.fileFromDB)

            csvFile = csv.writer(open(self.fileFromDB + self.fileName, 'w', newline=''), delimiter=',',
                             lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.log_writer.log(file,"File Exported Successfully!!!")
            file.close()

        except Exception as e:
            self.log_writer.log(file,"Error while exporting :: %s"%e)
            file.close()