from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score
from application_logging.logger import App_logger

class Model_Finder :
    def __init__(self):
        self.log_writer = App_logger()
        self.rf = RandomForestClassifier()
        self.xgb = XGBClassifier()

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

    def get_best_params_for_XGBoost(self,train_x,train_y):
        print('inside get_best_params_for_XGBoost')

        file = open("Training_logs/Model_Training_Log.txt", 'a+')
        self.log_writer.log(file, "Entered the get_best_params_for_XGBoost method!!!")
        try :
            self.param_grid_xgboost = {
                'learning_rate' : [0.1,0.01], # [0.1,0.01,0.001,0.0001,0.005,0.5]
                'max_depth' : [5,10], # [5,10,13,12,15,20]
                'n_estimators' : [100] # [10,50,100,200,300]
            }

            self.grid = GridSearchCV(self.xgb,param_grid=self.param_grid_xgboost,verbose=3,cv=2)
            self.grid.fit(train_x,train_y)
            # Now extracting the best params from the gridsearch
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            self.xgb = XGBClassifier(learning_rate=self.learning_rate, max_depth=self.max_depth, n_estimators=self.n_estimators)
            self.xgb.fit(train_x,train_y)

            self.log_writer.log(file, "The Best params of XG Boost are" + str(self.grid.best_params_) + " Now Exiting the XG Boost method")
            file.close()
            return self.xgb

        except Exception as e:
            self.log_writer.log(file,"Error occured while choosing the best params for XG Boost classifier :: %s" % str(e))
            file.close()
            raise e

    def get_best_model(self,train_x,train_y,test_x,test_y):

        print('inside get_best_model_method')
        file = open("Training_logs/Model_Training_Log.txt", 'a+')
        self.log_writer.log(file, "Entered the get_best_model method!!!")

        try :
            self.xgboost = self.get_best_params_for_XGBoost(train_x,train_y)
            self.xgboost_predictions = self.xgboost.predict(test_x)

            # If test_y is having only 1 category label then in that case the ROC AUC score will throw an error so ...use accuracy in that case.
            if (test_y.nunique() == 1) :
                self.xgboost_score = accuracy_score(test_y, self.xgboost_predictions)
                self.log_writer.log(file, "The Accuracy Score for XG-BOOST is : %s "% str(self.xgboost_score))
            else :
                self.xgboost_score = roc_auc_score(test_y, self.xgboost_predictions)
                self.log_writer.log(file, "The ROC AUC Score for XG-BOOST is : %s " % str(self.xgboost_score))


            self.random_forest = self.get_best_params_for_RandomForest(train_x,train_y)
            self.random_forest_predictions = self.random_forest.predict(test_x)

            # If test_y is having only 1 category label then in that case the ROC AUC score will throw an error so ...use accuracy in that case.
            if (test_y.nunique() == 1):
                self.random_forest_score = accuracy_score(test_y, self.random_forest_predictions)
                self.log_writer.log(file, "The Accuracy Score for RANDOM FOREST is : %s " % str(self.random_forest_score))
            else:
                self.random_forest_score = roc_auc_score(test_y, self.random_forest_predictions)
                self.log_writer.log(file, "The ROC AUC Score for RANDOM FOREST is : %s " % str(self.random_forest_score))


            if (self.random_forest_score < self.xgboost_score) :

                return 'XGBoost' , self.xgboost

            else :
                return 'RandomForest' , self.random_forest


        except Exception as e :
            self.log_writer.log(file, "Error occurred in the get_best_model method!!! :: %e"% str(e))
            raise e













