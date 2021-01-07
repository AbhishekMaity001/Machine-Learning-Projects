from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from application_logging.logger import App_logger

class Model_Finder :
    def __init__(self):
        self.log_writer = App_logger()
        self.rf = RandomForestClassifier()
        self.knn = KNeighborsClassifier()

    def get_best_params_for_RandomForest(self,train_x,train_y):

        print('get_best_params_for_RandomForest')
        file=open("Training_logs/Model_Training_Log.txt",'a+')
        self.log_writer.log(file,"Entered the get_best_params_for_RandomForest method!!!")

        try :
            self.param_grid = {'n_estimators' : [10,20], #[10,20,30,50,70,80,100]
                               'criterion' : ['gini'], #['gini','entropy']
                               'max_depth' : range(2,4,1),
                               'max_features' : ['auto','log2']}
            self.grid = GridSearchCV(self.rf,param_grid=self.param_grid,cv=2,verbose=3)
            self.grid.fit(train_x,train_y)

            # extracting the best parameters from the grid search cv model
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']

            self.rf = RandomForestClassifier(n_estimators=self.n_estimators,
                                             criterion=self.criterion,
                                             max_depth=self.max_depth,
                                             max_features=self.max_features)
            self.rf.fit(train_x,train_y)
            self.log_writer.log(file,"The Best params of Random Forest are" + str(self.grid.best_params_) +" Now Exiting the Random Forest method")
            file.close()
            return self.rf

        except Exception as e:
            self.log_writer.log(file,"Error occured while choosing the best params for random forest classifier :: %s" %str(e))
            file.close()
            raise e

    def get_best_params_for_KNN(self,train_x,train_y):
        print('inside get_best_params_for_KNN')

        file = open("Training_logs/Model_Training_Log.txt", 'a+')
        self.log_writer.log(file, "Entered the get_best_params_for_KNN method!!!")
        try :
            self.param_grid_knn = {
                'algorithm' : ['ball_tree','kd_tree','brute'], # [0.1,0.01,0.001,0.0001,0.005,0.5]
                'leaf_size' : [5,10], # [5,10,13,12,15,20]
                'n_neighbors' : [3,6,10], # [10,50,100,200,300]
                'p' : [1,2]
            }

            self.grid = GridSearchCV(self.knn,param_grid=self.param_grid_knn,verbose=3,cv=2)
            self.grid.fit(train_x,train_y)
            # Now extracting the best params from the gridsearch
            self.algorithm = self.grid.best_params_['algorithm']
            self.leaf_size = self.grid.best_params_['leaf_size']
            self.n_neighbors = self.grid.best_params_['n_neighbors']
            self.p = self.grid.best_params_['p']

            self.knn = KNeighborsClassifier(algorithm=self.algorithm,leaf_size=self.leaf_size,n_neighbors=self.n_neighbors,p=self.p)
            self.knn.fit(train_x,train_y)

            self.log_writer.log(file, "The Best params of KNN are" + str(self.grid.best_params_) + " Now Exiting the KNN method")
            file.close()
            return self.knn

        except Exception as e:
            self.log_writer.log(file,"Error occured while choosing the best params for KNN classifier :: %s" % str(e))
            file.close()
            raise e

    def get_best_model(self,train_x,train_y,test_x,test_y):

        print('inside get_best_model_method')
        file = open("Training_logs/Model_Training_Log.txt", 'a+')
        self.log_writer.log(file, "Entered the get_best_model method!!!")

        try :
            self.knn = self.get_best_params_for_KNN(train_x,train_y)
            self.knn_predictions = self.knn.predict_proba(test_x)

            # If test_y is having only 1 category label then in that case the ROC AUC score will throw an error so ...use accuracy in that case.
            if (test_y.nunique() == 1) :
                self.knn_score = accuracy_score(test_y, self.knn_predictions)
                self.log_writer.log(file, "The Accuracy Score for KNN is : %s "% str(self.knn_score))
            else :
                self.knn_score = roc_auc_score(test_y, self.knn_predictions,multi_class='ovr')
                self.log_writer.log(file, "The ROC AUC Score for KNN is : %s " % str(self.knn_score))


            self.random_forest = self.get_best_params_for_RandomForest(train_x,train_y)
            self.random_forest_predictions = self.random_forest.predict_proba(test_x)

            # If test_y is having only 1 category label then in that case the ROC AUC score will throw an error so ...use accuracy in that case.
            if (test_y.nunique() == 1):
                self.random_forest_score = accuracy_score(test_y, self.random_forest_predictions)
                self.log_writer.log(file, "The Accuracy Score for RANDOM FOREST is : %s " % str(self.random_forest_score))
            else:
                self.random_forest_score = roc_auc_score(test_y, self.random_forest_predictions,multi_class='ovr')
                self.log_writer.log(file, "The ROC AUC Score for RANDOM FOREST is : %s " % str(self.random_forest_score))


            if (self.random_forest_score < self.knn_score) :

                return 'KNN' , self.knn_score

            else :
                return 'RandomForest' , self.random_forest


        except Exception as e :
            self.log_writer.log(file, "Error occurred in the get_best_model method!!! :: %e "% str(e))
            raise e













