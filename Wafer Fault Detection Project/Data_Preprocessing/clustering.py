from application_logging.logger import App_logger
from File_Operations.file_methods import File_Operation

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from kneed import KneeLocator





class KMeansClustering :

    def __init__(self):
        self.log_writer = App_logger()


    def elbow_plot(self,data):
        file = open("Training_logs/Model_Training_Log.txt",'a+')
        self.log_writer.log(file,"Entered the elbow_plot method !!! ")
        wcss=[]

        try:
            print("Entered the elbow_plot method !!! ")
            for i in range (1,11):
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)  # initializing the KMeans object
                kmeans.fit(data)  # fitting the data to the KMeans Algorithm
                wcss.append(kmeans.inertia_)

            plt.plot(range(1,11),wcss) # plotting wcss graph
            plt.xlabel('No. of clusters---->')
            plt.ylabel('WCSS ---->')
            plt.title('Elbow Plot')
            plt.savefig('preprocessing_data/elbow_plot.PNG')

            self.kn = KneeLocator(range(1,11), wcss, curve='convex', direction='decreasing')
            self.log_writer.log(file,"The optimal number of clusters got from KneeLocator is : %s . Now Exiting the elbow plot method"%str(self.kn.knee))
            file.close()
            return self.kn.knee

        except Exception as e :
            self.log_writer.log(file,"Error occurred while calculating the optimum number of clusters %s"% str(e))
            file.close()
            raise e

    def create_clusters(self,data,number_of_clusters):

        file = open("Training_logs/Model_Training_Log.txt",'a+')
        self.data = data

        try :
            print("Entered the create_clusters method !!! ")
            self.kmeans = KMeans(n_clusters=number_of_clusters,init='k-means++',random_state=97) # fitting the method
            self.ymeans = self.kmeans.fit_predict(data) # dividing the data into clusters

            self.file_op = File_Operation()
            self.save_model = self.file_op.save_model(self.kmeans,'KMeans') # saving the model file
            self.data['Cluster']  = self.ymeans
            self.log_writer.log(file,"Successfully created "+ str(self.kn.knee) + '  Clusters . Exited the create_cluster method of KMeansClustering class')
            file.close()
            print("Exited the create_clusters method !!! ")
            return self.data


        except Exception as e:
            print('create cluster exception method')
            self.log_writer.log(file,"Error occurred while creating the clusters in create_clusters method :: %s" + str(e))
            file.close()
            raise e



