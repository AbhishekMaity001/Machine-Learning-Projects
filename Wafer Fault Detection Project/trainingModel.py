""""
            This is the main entry for the training of the Machine Learning Model
"""
from application_logging.logger import App_logger
from data_ingestion import data_loader
from Data_Preprocessing.Preprocessing import Preprocessor
from Data_Preprocessing.clustering import KMeansClustering
from best_model_finder.tuner import Model_Finder
from File_Operations.file_methods import File_Operation

from sklearn.model_selection import train_test_split

class trainModel :

    def __init__(self):
        self.log_writer = App_logger()
        self.file_object = open('Training_logs/Model_Training_Log.txt','a+')

    def trainingModel(self):

        self.log_writer.log(self.file_object,"Start of the Training Model !!!!!")
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

            X = preprocessor.remove_columns(X, cols_to_drop)
            print('now we will enter clustering approach')

            """"---------Applying the Clustering Approach---------"""
            kmeans = KMeansClustering()
            number_of_clusters = kmeans.elbow_plot(X)

            # Dividing the Clusters  after getting the number_of_clusters
            X = kmeans.create_clusters(X,number_of_clusters)

            # Now joining the Y label back to X data
            X['Labels'] = Y

            # now fetching the total number of clusters
            list_of_clusters = X['Cluster'].unique()

            """"<------Now iterating through all the clusters and looking for the best model suited for each of the cluster------>"""
            print('now entering the for loop of list_of_clusters')

            for i in list_of_clusters:
                cluster_data = X[X['Cluster']==i] # filtering the data for each cluster

                cluster_features = cluster_data.drop(['Labels','Cluster'],axis=1)
                cluster_labels = cluster_data['Labels']

                x_train, x_test, y_train, y_test = train_test_split(cluster_features,cluster_labels,test_size=0.33,random_state=97)

                # getting the best model for the current cluster
                model_finder = Model_Finder() # object init
                best_model_name , best_model = model_finder.get_best_model(x_train,y_train,x_test,y_test)

                file_op = File_Operation()
                save_model = file_op.save_model(best_model,best_model_name+str(i))

            self.log_writer.log(self.file_object,"Successful End of Training :)")
            self.file_object.close()


            print('END----------->')










        except Exception as e :
            print('Exception as e')
            raise e