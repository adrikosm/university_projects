# -*- coding: utf-8 -*-
"""Kaggle_Personal_Key_Indicators_of_Heart_Disease.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z9PLTmB9H5eQS0wFxVTCtg9gH0EBC4n5

# ΣΥΣΤΗΜΑΤΑ ΛΗΨΗΣ ΑΠΟΦΕΑΣΕΩΝ
## Εκφωνηση 2
### Ανδρεας Μαυροπουλος 217129
"""

# General Imports
import numpy as np 
import pandas as pd 



# Modles from Scikit-Learn
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Model evaluations
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.model_selection import RandomizedSearchCV,GridSearchCV
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,r2_score,mean_absolute_error,mean_squared_error



# IMPORTS FOR EDA
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import seaborn as sns
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.interpolate import UnivariateSpline

# REMOVE WARNING MESSAGES
import warnings
warnings.filterwarnings('ignore')

"""# Task 1
Import and Fix Dataaset
"""

heart_disease = pd.read_csv("/content/drive/MyDrive/Kaggle/Personal Key Indicators of Heart Disease/heart_2020_cleaned.csv")
heart_disease.head()

heart_disease['AgeCategory'] = heart_disease['AgeCategory'].replace({'55-59':57, '80 or older':80, '65-69':67,
                                                                    '75-79':77,'40-44':42,'70-74':72,'60-64':62,
                                                                    '50-54':52,'45-49':47,'18-24':21,'35-39':37,
                                                                    '30-34':32,'25-29':27})

heart_disease.isnull().sum()

heart_disease.info()

"""## Fix Dataset by:


1.   Turing yes or no categories to 0 and 1
2.   Making the sex 0 for females and 1 for males
3.   Turning Race into a list of numbers where
          
          > 0 = White
          > 1 = Black
          > 2 = Asian
          > 3 = American
          > 4 = Indian/Alaskan Native
          > 5 = Other
          > 6 = Hispanic


4. Turning GenHealth into a list of numbers where
          > 0 = Very good
          > 1 = Fair
          > 2 = Good
          > 3 = Poor
          > 4 = Excellent

5. Turn AgeCategory into a list of numbers where we take the median age in order to get better values
          > 21  = 18-24
          > 27 = 25-29
          > 32  = 30-34
          > 37  = 35-39
          > 42  = 40-44
          > 47  = 45-49
          > 52  = 50-54
          > 57  = 55-59
          > 62  = 60-64
          > 67  = 65-69
          > 72 = 70-74
          > 77 = 75-79
          > 80 = 80 or older

## Task 2 Exploratory EDA
will fix dataset as said above after EDA so we can have a better look at it
"""

fig = make_subplots(
    rows=7, cols=2, subplot_titles=("HeartDisease", "Smoking",
                                    "AlcoholDrinking","Stroke",
                                    "DiffWalking", "Sex",
                                    'Race', 'Diabetic',
                                    'PhysicalActivity','GenHealth',
                                    'Asthma', 'KidneyDisease',
                                    'SkinCancer'),
    specs=[[{"type": "domain"}, {"type": "domain"}],
           [{"type": "domain"}, {"type": "domain"}],
           [{"type": "domain"}, {"type": "domain"}],
           [{"type": "domain"}, {"type": "domain"}],
           [{"type": "domain"}, {"type": "domain"}],
           [{"type": "domain"}, {"type": "domain"}],
           [{"type": "domain"}, {"type": "domain"}]],
)

colours = ['#4285f4', '#ea4335', '#fbbc05', '#34a853']

fig.add_trace(go.Pie(labels=np.array(heart_disease['HeartDisease'].value_counts().index),
                     values=[x for x in heart_disease['HeartDisease'].value_counts()], hole=.35,
                     textinfo='label+percent', rotation=-45, marker_colors=colours),
              row=1, col=1)

fig.add_trace(go.Pie(labels=np.array(heart_disease['Smoking'].value_counts().index),
                     values=[x for x in heart_disease['Smoking'].value_counts()], hole=.35,
                     textinfo='label+percent', marker_colors=colours),
              row=1, col=2)

fig.add_trace(go.Pie(labels=np.array(heart_disease['AlcoholDrinking'].value_counts().index),
                     values=[x for x in heart_disease['AlcoholDrinking'].value_counts()], hole=.35,
                     textinfo='label+percent', rotation=-45, marker_colors=colours),
              row=2, col=1)

fig.add_trace(go.Pie(labels=np.array(heart_disease['Stroke'].value_counts().index),
                     values=[x for x in heart_disease['Stroke'].value_counts()], hole=.35,
                     textinfo='label+percent', rotation=-45, marker_colors=colours),
              row=2, col=2)

fig.add_trace(go.Pie(labels=np.array(heart_disease['DiffWalking'].value_counts().index),
                     values=[x for x in heart_disease['DiffWalking'].value_counts()], hole=.35,
                     textinfo='label+percent', marker_colors=colours),
              row=3, col=1)

fig.add_trace(go.Pie(labels=np.array(heart_disease['Sex'].value_counts().index),
                     values=[x for x in heart_disease['Sex'].value_counts()], hole=.35,
                     textinfo='label+percent', marker_colors=colours),
              row=3, col=2)

fig.add_trace(go.Pie(labels=np.array(heart_disease['Race'].value_counts().index),
                     values=[x for x in heart_disease['Race'].value_counts()], hole=.35,
                     textinfo='label+percent', rotation=-45, marker_colors=colours),
              row=4, col=1)

fig.add_trace(go.Pie(labels=np.array(heart_disease['PhysicalActivity'].value_counts().index),
                     values=[x for x in heart_disease['PhysicalActivity'].value_counts()], hole=.35,
                     textinfo='label+percent', marker_colors=colours),
              row=4, col=2)

fig.add_trace(go.Pie(labels=np.array(heart_disease['Diabetic'].value_counts().index),
                     values=[x for x in heart_disease['Diabetic'].value_counts()], hole=.35,
                     textinfo='label+percent', rotation=-45, marker_colors=colours),
              row=5, col=1)

fig.add_trace(go.Pie(labels=np.array(heart_disease['GenHealth'].value_counts().index),
                     values=[x for x in heart_disease['GenHealth'].value_counts()], hole=.35,
                     textinfo='label+percent', marker_colors=colours),
              row=5, col=2)

fig.add_trace(go.Pie(labels=np.array(heart_disease['Asthma'].value_counts().index),
                     values=[x for x in heart_disease['Asthma'].value_counts()], hole=.35,
                     textinfo='label+percent', rotation=-45, marker_colors=colours),
              row=6, col=1)

fig.add_trace(go.Pie(labels=np.array(heart_disease['KidneyDisease'].value_counts().index),
                     values=[x for x in heart_disease['KidneyDisease'].value_counts()], hole=.35,
                     textinfo='label+percent', rotation=-45, marker_colors=colours),
              row=6, col=2)

fig.add_trace(go.Pie(labels=np.array(heart_disease['SkinCancer'].value_counts().index),
                     values=[x for x in heart_disease['SkinCancer'].value_counts()], hole=.35,
                     textinfo='label+percent', rotation=-45, marker_colors=colours),
              row=7, col=1)


fig.update_layout(height=3200, font=dict(size=14), showlegend=False)

fig.show()

heart_disease.describe()[1:][['BMI','PhysicalHealth','MentalHealth', 'AgeCategory', 'SleepTime']].T.style.background_gradient(cmap='Blues')

fig, ax = plt.subplots(figsize = (10,6))

ax.hist(heart_disease[heart_disease["HeartDisease"]=='No']["Sex"], bins=3, alpha=0.8, color="#4285f4", label="No HeartDisease")
ax.hist(heart_disease[heart_disease["HeartDisease"]=='Yes']["Sex"], bins=3, alpha=1, color="#ea4335", label="HeartDisease")

ax.set_xlabel("Sex")
ax.set_ylabel("Frequency")

ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.);

fig, ax = plt.subplots(figsize = (10,6))

ax.hist(heart_disease[heart_disease["HeartDisease"]=='No']["Race"], bins=12, alpha=0.8, color="#4285f4", label="No HeartDisease")
ax.hist(heart_disease[heart_disease["HeartDisease"]=='Yes']["Race"], bins=12, alpha=1, color="#ea4335", label="HeartDisease")

ax.set_xlabel("Race")
ax.set_ylabel("Frequency")

ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=1.);

fig, ax = plt.subplots(figsize = (10,6))

ax.hist(heart_disease[heart_disease["HeartDisease"]=='No']["GenHealth"], bins=12, alpha=0.8, color="#4285f4", label="No HeartDisease")
ax.hist(heart_disease[heart_disease["HeartDisease"]=='Yes']["GenHealth"], bins=12, alpha=1, color="#ea4335", label="HeartDisease")

ax.set_xlabel("Race")
ax.set_ylabel("Frequency")

ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=1.);

fig, ax = plt.subplots(figsize = (10,6))

ax.hist(heart_disease[heart_disease["HeartDisease"]=='No']["Smoking"], bins=3, alpha=0.8, color="#4285f4", label="No HeartDisease")
ax.hist(heart_disease[heart_disease["HeartDisease"]=='Yes']["Smoking"], bins=3, alpha=1, color="#ea4335", label="HeartDisease")

ax.set_xlabel("Smoking")
ax.set_ylabel("Frequency")

ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.);

fig, ax = plt.subplots(figsize = (10,6))

ax.hist(heart_disease[heart_disease["HeartDisease"]=='No']["AlcoholDrinking"], bins=3, alpha=0.8, color="#4285f4", label="No HeartDisease")
ax.hist(heart_disease[heart_disease["HeartDisease"]=='Yes']["AlcoholDrinking"], bins=3, alpha=1, color="#ea4335", label="HeartDisease")

ax.set_xlabel("AlcoholDrinking")
ax.set_ylabel("Frequency")

ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.);

plt.figure(figsize=(18,25))
for index,item in enumerate(['BMI','PhysicalHealth','MentalHealth', 'AgeCategory', 'SleepTime']):
  plt.subplot(6,3,index+1)
  sns.distplot(heart_disease[item],kde=True)
  plt.xlabel(item)
  plt.ylabel("Count")

plt.figure(figsize=(10,6))

# Scatter with positive examples
plt.scatter(heart_disease.AgeCategory[heart_disease.HeartDisease=='Yes'],
            heart_disease.BMI[heart_disease.HeartDisease=='Yes'],
            color="salmon");

# Scatter with negative examples
plt.scatter(heart_disease.AgeCategory[heart_disease.HeartDisease=='No'],
            heart_disease.BMI[heart_disease.HeartDisease=='No'],
            color="lightblue")

# Add some helpfull info
plt.title("Heart Disease in function of AgeCategory and max BMI")
plt.xlabel("Age"),
plt.ylabel("BMI")
plt.legend(["Disease","No Disease"]);

plt.figure(figsize=(12,6))
heart_disease.AgeCategory.plot.hist();



plt.figure(figsize=(12,6))
heart_disease.MentalHealth.plot.hist();

"""### Fix the dataframe in order to be ready for model use"""

# Lets start with the easy ones first
# Turn all yes and no columns to 0 and 1

heart_disease = heart_disease.replace({'No': 0, 'Yes': 1})
heart_disease['Sex'] = heart_disease['Sex'].replace({'Female': 0, 'Male': 1})
heart_disease['Race'] = heart_disease['Race'].replace({'White': 0 , 'Black': 1,
                                                       'Asian': 2, 'American': 3,
                                                       'American Indian/Alaskan Native': 4,
                                                       'Other':5, 'Hispanic':6})
heart_disease['GenHealth'] =  heart_disease['GenHealth'].replace({'Very good': 1, 'Fair': 2,
                                                                      'Good': 3, 'Poor':4,
                                                                      'Excellent':5})

heart_disease['Diabetic'] = heart_disease['Diabetic'].replace({'No, borderline diabetes':0,'Yes (during pregnancy)': 1})
heart_disease.head()

heart_disease.info()

# Plot out a correleation heatmap

corr_matrix = heart_disease.corr()

fig,ax = plt.subplots(figsize=(25,20))
ax = sns.heatmap(corr_matrix,
                 annot=True,
                 linewidths=0.5,
                 fmt=".2f",
                 cmap='YlGnBu');

"""## Task 3 Model Building
First make a train test split
"""

X = heart_disease.drop('HeartDisease',axis=1)
y = heart_disease['HeartDisease']


X_train , X_test, y_train, y_test = train_test_split(X,y,test_size=0.1)
# Scale Data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

y_train

"""## Model 1 Random Forest Classifier
Create a gridSearchCV to find best RandomForestCLassifier
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# random_forest_grid = {"n_estimators": np.arange(10,100,10),
#                       "max_depth":[None,3,5,10],
#                       "min_samples_split":np.arange(2,20,2),
#                       "min_samples_leaf":np.arange(2,20,2)}
# 
# random_forest_model = RandomizedSearchCV(RandomForestClassifier(),
#                                          param_distributions=random_forest_grid,
#                                          cv=2,
#                                          n_iter=30,
#                                          verbose = True)
# random_forest_model.fit(X_train,y_train)

random_forest_pred = random_forest_model.predict(X_test)



forest_acc = accuracy_score(y_test, random_forest_pred)
forest_f1 = f1_score(y_test,random_forest_pred)
forest_r2 = r2_score(y_test,random_forest_pred)
forest_mae = mean_absolute_error(y_test,random_forest_pred)
forest_rmse = np.sqrt(mean_squared_error(y_test, random_forest_pred))

print("Accuracy : " ,forest_acc )
print("F1",forest_f1)
print("R^2 : ", forest_r2)
print("MAE :", forest_mae)
print("RMSE:",forest_rmse)

"""## Model 2 CatBoostClassifier"""

!pip install catboost

# Commented out IPython magic to ensure Python compatibility.
# %%time
# from catboost import CatBoostClassifier
# 
# cat_boost_model = CatBoostClassifier(task_type='GPU',iterations=100)
# cat_boost_model.fit(X_train,y_train)

cat_pred = cat_boost_model.predict(X_test)

cat_acc = accuracy_score(y_test,cat_pred)
cat_f1 = f1_score(y_test,cat_pred)
cat_r2 = r2_score(y_test,cat_pred)
cat_mae = mean_absolute_error(y_test,cat_pred)
cat_rmse = np.sqrt(mean_squared_error(y_test, cat_pred))

print("Accuracy : " ,cat_acc )
print("F1",cat_f1)
print("R^2 : ", cat_r2)
print("MAE :", cat_mae)
print("RMSE:",cat_rmse)

model_results = [['Cat Boost',cat_acc,cat_f1,cat_r2,cat_mae,cat_rmse],
                 ['Random Forest',forest_acc,forest_f1,forest_r2,forest_mae,forest_rmse]]
model_results

model_results_df = pd.DataFrame(model_results,columns=["model","accuracy","f1",'R^2','MAE','RMSE'])
model_results_df

model_results_df.plot(x="model",y=['MAE','RMSE',"f1"],kind="bar",figsize=(10,6))
plt.title("Field Artillery Model")
plt.xticks(rotation="horizontal");

model_results_df.plot(x="model",y=["accuracy"],kind="bar",figsize=(10,6))
plt.xticks(rotation="horizontal");

