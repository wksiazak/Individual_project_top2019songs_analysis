import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

#file top10s.csc includes top spotify songs from 2010 till 2019 - all machine learning methods will be based on this data set
spotify_data_2010_2019 = pd.read_csv('top10s.csv', encoding= 'ISO-8859-1', index_col=0)
pd.set_option('display.max_columns', None)
#print(spotify_data_2010_2019)

#adding column to count data in pivot table
number = 1
elements = 603
the_list = [number]*elements
#print(the_list)
spotify_data_2010_2019['number'] = the_list
#print(spotify_data_2010_2019)
#print(spotify_data_2010_2019.dtypes) "title", "artist", "top genre" are object type

#based on below pivot table we can verify which top genre was the most popular in particular year
table = pd.pivot_table(spotify_data_2010_2019, columns= 'year', index = 'top genre', values = 'number', aggfunc=np.count_nonzero )
table.fillna(0)
print(table)

#we can also check top songs in total by top genre
popular_genre=spotify_data_2010_2019.groupby('top genre').size().unique
print(popular_genre)

#check if data includes nulls
nulls_summary = spotify_data_2010_2019.isnull().any()
#print(nulls_summary) # after checking there are no null in our dataset

#correlation
spotify_data_2010_2019_corr = spotify_data_2010_2019.drop(columns=['title', 'artist','top genre', 'number'])
#print(spotify_data_2010_2019_corr.dtypes) - just for check if we have numeric data
corr_metrics = spotify_data_2010_2019_corr.corr()
#print(corr_metrics)
sn.heatmap(corr_metrics, annot=True)
plt.show() # heatmap shows the highest correlation around +/- 0,56 between acous and nrgy & dnce and val &


# Define our features
features = spotify_data_2010_2019_corr

# Define our labels
labels = spotify_data_2010_2019["top genre"]


# Scale the features and set the values to a new variable
scaler = StandardScaler()
scaled_train_features = scaler.fit_transform(features)

# I will create class to test machine learning algorithms
class Classifiers:
    def labelsMapping (self, columnToMap):
        labels_mapping = {label: idx for idx, label in enumerate(np.unique(columnToMap))}
        columnToMap2 = columnToMap.map(labels_mapping)
        print(columnToMap2)
        return columnToMap2
    def splitDatasetIntoTrainAndTest(self, X, y, train_split_percent = 0.6):
        X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=train_split_percent)
        return X_train, X_test, y_train, y_test
        print(y_train)
    def trainAndTestClassifier(self, clf, X_train, X_test, y_train):
        print(clf)
        # trenowanie
        clf.fit(X_train, y_train)
        # testowanie
        y_pred = clf.predict(X_test)
        return y_pred
    def getClassificationScore(self, clf_name ,y_test, y_pred):
        print("Nazwa klasyfikatora: " + clf_name)
        print(accuracy_score(y_test, y_pred))
        #print(confusion_matrix(y_test, y_pred))


c= Classifiers()
labels_mapped=c.labelsMapping(labels)
#print(labels_mapped)
X_train, X_test, y_train, y_test = c.splitDatasetIntoTrainAndTest(X = scaled_train_features, y=labels_mapped, train_split_percent = 0.6)
y_pred_tree_train  = c.trainAndTestClassifier(DecisionTreeClassifier(),X_train,X_train,y_train)
y_pred_tree_test  = c.trainAndTestClassifier(DecisionTreeClassifier(),X_train,X_test,y_train )
y_pred_knn5_train = c.trainAndTestClassifier(KNeighborsClassifier(n_neighbors=10), X_train,X_train,y_train)
y_pred_knn5_test = c.trainAndTestClassifier(KNeighborsClassifier(n_neighbors=10), X_train,X_test,y_train)
y_pred_svm_lin_train = c.trainAndTestClassifier(SVC(kernel='linear'), X_train,X_train,y_train)
y_pred_svm_lin_test = c.trainAndTestClassifier(SVC(kernel='linear'), X_train,X_test,y_train)
y_pred_svm_rbf_train = c.trainAndTestClassifier(SVC(kernel='rbf', gamma='auto'), X_train,X_train,y_train)
y_pred_svm_rbf_test = c.trainAndTestClassifier(SVC(kernel='rbf', gamma='auto'), X_train,X_test,y_train)
c.getClassificationScore("DT trenowanie", y_train, y_pred_tree_train)
c.getClassificationScore("DT testowanie", y_test, y_pred_tree_test)
c.getClassificationScore("kNN-5 trenowanie", y_train, y_pred_knn5_train)
c.getClassificationScore("kNN-5 testowanie", y_test, y_pred_knn5_test)
c.getClassificationScore("SVM-linear trenowanie", y_train, y_pred_svm_lin_train)
c.getClassificationScore("SVM-linear testowanie", y_test, y_pred_svm_lin_test)
c.getClassificationScore("SVM-rbf trenowanie", y_train, y_pred_svm_rbf_train)
c.getClassificationScore("SVM-rbf testowanie", y_test, y_pred_svm_rbf_test)

#PCA - principal component analysis
pca = PCA()
pca.fit(scaled_train_features)
exp_variance = pca.explained_variance_ratio_

print("Explained variance ratios are: ", pca.explained_variance_ratio_)
print("Total of component is: ", pca.n_components_)

# plot the explained variance using a barplot
fig, ax = plt.subplots()
ax.bar(range(11), exp_variance)
ax.set_xlabel('Principal Component #')
plt.show()

# Calculate the cumulative explained variance
cum_exp_variance = np.cumsum(exp_variance)

# Plot the cumulative explained variance and draw a dashed line at 0.90.
fig, ax = plt.subplots()
ax.plot(range(11), cum_exp_variance)
ax.axhline(y=0.9, linestyle='--')
n_components = 8
plt.show()

# Perform PCA with the chosen number of components and project data onto components
pca = PCA(n_components, random_state=10)
pca.fit(scaled_train_features)
pca_projection = pca.transform(scaled_train_features)

# Split our data
train_features, test_features, train_labels, test_labels = train_test_split(pca_projection, labels_mapped, random_state=10)

# Train our decision tree & knn &SVC(rbf)
tree = DecisionTreeClassifier(random_state=10)
tree.fit(train_features, train_labels)

knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(train_features, train_labels)

SVC_rbf = SVC(kernel='rbf', gamma='auto')
SVC_rbf.fit(train_features, train_labels)

# Predict the labels for the test data
pred_labels_tree = tree.predict(test_features)
pred_labels_knn = knn.predict(test_features)
pred_labels_SVC_rbf = knn.predict(test_features)

acc_score_tree_PCA = accuracy_score(test_labels, pred_labels_tree)
acc_score_knn_PCA = accuracy_score(test_labels, pred_labels_knn)
acc_score_SVC_rbf_PCA = accuracy_score(test_labels, pred_labels_SVC_rbf)
print("DT testowanie PCA",acc_score_tree_PCA)
print("Knn testowanie PCA", acc_score_knn_PCA)
print("SVC_rbf testowanie PCA", acc_score_SVC_rbf_PCA)

