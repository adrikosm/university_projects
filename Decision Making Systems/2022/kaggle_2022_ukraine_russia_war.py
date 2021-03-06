# -*- coding: utf-8 -*-
"""Kaggle_2022_Ukraine_Russia War.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F5cWXGgDRjoTyHfIffbmu_mHGzP7WlJX

# ΣΥΣΤΗΜΑΤΑ ΛΗΨΗΣ ΑΠΟΦΕΑΣΕΩΝ
## Εκφωνηση 1  
### Ανδρεας Μαυροπουλος 217129

### Dataset Info
Tracking:
- Personnel
- Prisoner of War
- Armored Personnel Carrier
- Multiple Rocket Launcher
- Aircraft
- Anti-aircraft warfare
- Drone
- Field Artillery
- Fuel Tank
- Helicopter
- Military Auto
- Naval Ship
- Tank

Acronyms:
- POW - Prisoner of War,
- MRL - Multiple Rocket Launcher,
- BUK - Buk Missile System,
- APC - Armored Personnel Carrier,
- drone: UAV - Unmanned Aerial Vehicle, RPA - Remotely Piloted Vehicle. Dataset History
"""

# GENERAL IMPORTS
import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error,accuracy_score,f1_score
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import LassoCV
from sklearn.model_selection import RandomizedSearchCV,GridSearchCV


# IMPORTS FOR EDA
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.interpolate import UnivariateSpline

"""# Task 1
import and fix dataset
"""

equipment_loss = pd.read_csv('/content/drive/MyDrive/Kaggle/2022 Ukraine Russia War/russia_losses_equipment.csv')

personel_loss = pd.read_csv('/content/drive/MyDrive/Kaggle/2022 Ukraine Russia War/russia_losses_personnel.csv')

equipment_loss.head()

personel_loss.head()

"""Firstly fix the equipment loss dataframe"""

# CREATE A SINGLE COLUMN FOR AIRCRAFTS
equipment_loss['Aircrafts'] = equipment_loss['aircraft'] + equipment_loss['helicopter']

# CREATE A SINGLE COLUMN FOR TANKS
equipment_loss['Tanks'] = equipment_loss['tank'] + equipment_loss['fuel tank']

# DROP UNNECCESARY COLUMNS
equipment_loss = equipment_loss.drop(['date','aircraft', 'helicopter','tank','fuel tank','vehicles and fuel tanks','greatest losses direction','mobile SRBM system'], axis = 1)

# FILL MISSING VALUES
equipment_loss = equipment_loss.replace('nan', np.nan).fillna(0)

# equipment_loss.dtypes

# Turn float values to integer
equipment_loss[['military auto', 'special equipment','cruise missiles','Tanks']] = equipment_loss[['military auto', 'special equipment','cruise missiles','Tanks']].astype(int)

"""Now lets fix the personel dataframe"""

# DROP UNNECCESARY COLUMNS
personel_loss = personel_loss.drop(['date','personnel*'],axis=1)

# ADD DEATHS PER DAY COLUMN
deaths_per_day=[]
for index,item in enumerate(personel_loss['personnel']):
  if index==0:
    deaths_per_day.append(item)
  else:
    deaths_per_day.append(item-personel_loss['personnel'][index-1])

personel_loss['deaths per day'] = deaths_per_day

"""# Task 2
EDA

Firstly Plot out the personel loss dataframe

"""

# View total deaths in relation to days
fig = go.Figure()

fig.add_trace(go.Scatter(x=personel_loss['day'], y=personel_loss['personnel'],
                    mode='lines+markers+text',
                    name='Russian troops',
                    line_shape='spline',
                    textposition="bottom center"))

fig.update_layout(title="Total Deaths",
                  xaxis_title="Days",
                  yaxis_title="Deaths")
fig.show()

# Plot out the new daily deaths
fig = plt.figure(figsize = (20, 14))
plt.bar(personel_loss['day'],personel_loss['deaths per day'],width=0.6,)

 
plt.xlabel("Days")
plt.ylabel("Deaths")
plt.title("Deaths per Day")
plt.show()

# Plot out a correleation heatmap

fig = plt.figure(figsize = (18, 12))
heatmap = sns.heatmap(personel_loss.corr(), vmin=-1, vmax=1, annot=True)
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12);
plt.show()

# View Prisoners in relation to deaths
total_deaths = personel_loss['personnel'][len(personel_loss)-1]
prisoners = personel_loss['POW'][len(personel_loss)-1]

fig = go.Figure(data=[go.Pie(labels=['deaths','Prisoners'], values=[total_deaths,prisoners], textinfo='label',
                             insidetextorientation='radial'
)])

fig.show()

"""Time to plot out the Equipment loss dataframe"""

def add_fig_trace(x,y,label):
  return fig.add_trace(go.Scatter(x=x, y=y,
                    mode='lines+markers+text',
                    name=label,
                    line_shape='spline',
                    textposition="bottom center"))

# Plot out the important russina losses per day
fig = go.Figure()

for index , item in enumerate(equipment_loss):
  if index != 0:
    add_fig_trace(equipment_loss['day'],equipment_loss[item],item)

fig.update_layout(title="Russian losses",
                  xaxis_title="Day",
                  yaxis_title="Losses",)

fig.show()

# Lets try to plot them out separately

# Lets plot out only the aerial 


fig = go.Figure()


add_fig_trace(equipment_loss['day'],equipment_loss['Aircrafts'],'Aircrafts')

add_fig_trace(equipment_loss['day'],equipment_loss['drone'],'Drones')


fig.update_layout(title="Russian Aerian losses",
                  xaxis_title="Day",
                  yaxis_title="Losses",)

fig.show()

# Lets plot out only the Ammunition 

fig = go.Figure()


add_fig_trace(equipment_loss['day'],equipment_loss['anti-aircraft warfare'],'anti-aircraft warfare')

add_fig_trace(equipment_loss['day'],equipment_loss['special equipment'],'special equipment')

add_fig_trace(equipment_loss['day'],equipment_loss['cruise missiles'],'cruise missiles')


fig.update_layout(title="Russian Ammunition losses",
                  xaxis_title="Day",
                  yaxis_title="Losses",)

fig.show()

# View Aerian Relation
aircrafts = equipment_loss['Aircrafts'][len(equipment_loss)-1]
drones = equipment_loss['drone'][len(equipment_loss)-1]


fig = go.Figure(data=[go.Pie(labels=['Aircrafts','Drones'], values=[aircrafts,drones], textinfo='label',
                             insidetextorientation='radial',
)])

fig.show()

"""## Τα 3 features
Αρχικα απο το personel loss dataframe θα παρω το `personel`. 
Στην συνεχεια απο το equipment loss dataframe θα παρω τα `APC` και `Field Artillery`. Η επιλογες μου εγιναν με βαση το correleation heatmap οπου προσεξα οτι αυτες οι τιμες εχουν την καλυτερη σχεση μεταξυ τους και των ημερων.

# Task 3

Lets setup the personel loss train test datasets
"""

# Plots out the predictions in a scatter plot
def plot_predictions(train_data,
                     train_labels,
                     test_data,
                     test_labels,
                     prediction_data,
                     predictions,
                     isPred):
  """
  Plots training data,test data
  and compares predictions to ground truth labels
  """
  plt.figure(figsize=(18,10))
  # Plot the training data in blue
  plt.scatter(train_data,train_labels,c="b",label="Training data")
  # Plot the testing data in green
  plt.scatter(test_data,test_labels,c="g",label="Testing data")
  # Plot the models predictions in red
  if isPred:
    plt.scatter(prediction_data,predictions,c="r",label="Predictions")
  # Show legend
  plt.legend()
  plt.show();

# Makes a train test split and normalizes data
def make_data(X,y,normal):

  X_train, X_test, y_train, y_test = train_test_split(
      X, 
      y, 
      test_size=0.2)
  
  # Setup unseen values
  unseen_values = pd.DataFrame([123,124,125,126,127,128,129,130])
  # size_of_X = int(len(X)*0.8)
  # size_of_y = int(len(y)*0.8)

  # X_train = X[:size_of_X]
  # X_test  = X[size_of_X:]
  # y_train = y[:size_of_y]
  # y_test  = y[size_of_X:]



  X_train = pd.DataFrame(X_train)
  X_test = pd.DataFrame(X_test)
  y_train = pd.DataFrame(y_train)
  y_test = pd.DataFrame(y_test)

  # Normalize data
  if normal:
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    unseen_values = scaler.transform(unseen_values)





  return X_train, X_test, y_train, y_test,unseen_values

plt.figure(figsize=(10,6))

 
X_train, X_test, y_train, y_test ,unseen_values = make_data(personel_loss['day'],personel_loss['personnel'],normal=False)


plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 None,
                 None,
                 False)

"""## Personnel Model 1 Linear Regression

"""

reg = LinearRegression().fit(X_train,y_train)
y_pred_reg  = reg.predict(X_test)

print("Accuracy : " , accuracy_score(y_test, np.argmax(y_pred_reg, axis=1)) )
print("F1",f1_score(y_test,np.argmax(y_pred_reg, axis=1), average='micro'))
print("R^2 : ", r2_score(y_test, y_pred_reg))
print("MAE :", mean_absolute_error(y_test,y_pred_reg))
print("RMSE:",np.sqrt(mean_squared_error(y_test, y_pred_reg)))

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 X_test,
                 y_pred_reg,
                 True)

y_pred = reg.predict(unseen_values)

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 unseen_values,
                 y_pred,
                 True)

"""## Personnel Model 2 Lasso Regression with crossvalidation"""

lasso = LassoCV().fit(X_train, y_train.values.reshape(len(y_train),))

y_pred_lasso = lasso.predict(X_test)

int_pred = []
for item in y_pred_lasso:
  int_pred.append(int(item))


print("Accuracy : " , accuracy_score(y_test, int_pred) )
print("F1",f1_score(y_test,int_pred, average='micro'))
print("R^2 : ", r2_score(y_test, y_pred_lasso))
print("MAE :", mean_absolute_error(y_test,y_pred_lasso))
print("RMSE:",np.sqrt(mean_squared_error(y_test, y_pred_lasso)))

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 X_test,
                 y_pred_lasso,
                 True)

y_pred = lasso.predict(unseen_values)

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 unseen_values,
                 y_pred,
                 True)

#plot size
plt.figure(figsize = (15, 15))

#add plot for training
plt.plot(X_train,y_train,alpha=0.7,linestyle='none',marker='*',markersize=5,color='blue',label=r'Train',zorder=7)

#addd plot for testing
plt.plot(X_test,y_test,alpha=0.6,linestyle='none',marker='o',markersize=6,color='green',label=r'Test')

#add plot for lasso model
plt.plot(X_test,y_pred_lasso,alpha=0.5,linestyle='none',marker='d',markersize=7,color='red',label='Lasso Regression')

#add plot for linear model
plt.plot(X_test,y_pred_reg,alpha=0.4,linestyle='none',marker='+',markersize=8,color='yellow',label='Linear Regression')

#rotate axis
plt.xticks(rotation = 90)
plt.legend()
plt.title("Comparison plot of Linear and Lasso Models")
plt.show()

"""## Time to move on to equipment loss 
Strating with APC
"""

X_train, X_test, y_train, y_test ,unseen_values = make_data(equipment_loss['day'],equipment_loss['APC'],normal=False)

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 None,
                 None,
                 False)

"""## APC Model 1 Linear Regression"""

apc_reg = LinearRegression().fit(X_train,y_train)
y_pred_reg  = apc_reg.predict(X_test)
int_pred_reg = []

for item in y_pred_reg:
  int_pred_reg.append(int(item))

print("Accuracy : " , accuracy_score(y_test, int_pred_reg) )
print("F1",f1_score(y_test,int_pred_reg, average='micro'))
print("R^2 : ", r2_score(y_test, int_pred_reg))
print("MAE :", mean_absolute_error(y_test,int_pred_reg))
print("RMSE:",np.sqrt(mean_squared_error(y_test, int_pred_reg)))

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 X_test,
                 y_pred_reg,
                 True)

y_pred = apc_reg.predict(unseen_values)

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 unseen_values,
                 y_pred,
                 True)

"""## APC MODEL 2 lasso regression"""

apc_lasso = LassoCV(alphas = [0.0001, 0.001,0.01, 0.1, 1, 10]).fit(X_train, y_train)

y_pred_lasso = apc_lasso.predict(X_test)

int_pred_lasso = []
for item in y_pred_lasso:
  int_pred_lasso.append(int(item))

print("Accuracy : " , accuracy_score(y_test, int_pred_lasso))
print("F1",f1_score(y_test,int_pred_lasso, average='micro'))
print("R^2 : ", r2_score(y_test, int_pred_lasso))
print("MAE :", mean_absolute_error(y_test,int_pred_lasso))
print("RMSE:",np.sqrt(mean_squared_error(y_test, int_pred_lasso)))

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 X_test,
                 y_pred_lasso,
                 True)

#plot size
plt.figure(figsize = (15, 15))

#add plot for training
plt.plot(X_train,y_train,alpha=0.7,linestyle='none',marker='*',markersize=5,color='blue',label=r'Train',zorder=7)

#addd plot for testing
plt.plot(X_test,y_test,alpha=0.6,linestyle='none',marker='o',markersize=6,color='green',label=r'Test')

#add plot for lasso model
plt.plot(X_test,y_pred_lasso,alpha=0.5,linestyle='none',marker='d',markersize=7,color='red',label='Lasso Regression')

#add plot for linear model
plt.plot(X_test,y_pred_reg,alpha=0.4,linestyle='none',marker='+',markersize=8,color='yellow',label='Linear Regression')

#rotate axis
plt.xticks(rotation = 90)
plt.legend()
plt.title("Comparison plot of Linear and Lasso Models")
plt.show()

"""## Field Aritllery Model 1 CatBoost

"""

!pip install catboost
!pip install xgboost

from catboost import CatBoostRegressor

# Get artilery field data
X_train, X_test, y_train, y_test ,unseen_values = make_data(equipment_loss['day'],equipment_loss['field artillery'],normal=True)

cat_boost_model = CatBoostRegressor()
cat_boost_model.fit(X_train,y_train)

y_pred_cat = cat_boost_model.predict(X_test)

int_cat_pred = []

for item in y_pred_cat:
  int_cat_pred.append(int(item))

# Get all values in order to plot them out later
cat_acc = accuracy_score(y_test, int_cat_pred)
cat_f1 = f1_score(y_test,int_cat_pred, average='micro')
cat_r2 = r2_score(y_test, int_cat_pred)
cat_mae = mean_absolute_error(y_test,int_cat_pred)
cat_rmse = np.sqrt(mean_squared_error(y_test, int_cat_pred))

print("Accuracy : " ,cat_acc )
print("F1",cat_f1)
print("R^2 : ", cat_r2)
print("MAE :", cat_mae)
print("RMSE:",cat_rmse)

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 X_test,
                 y_pred_cat,
                 True)

y_pred = cat_boost_model.predict(unseen_values)

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 unseen_values,
                 y_pred,
                 True)

"""## Field Artillery Model 2"""

from xgboost import XGBRegressor

# create an xgboost regression model
xg_boost_model = XGBRegressor()
xg_boost_model.fit(X_train,y_train)

y_pred_xg = xg_boost_model.predict(X_test)

int_xg_pred = []

for item in y_pred_xg:
  int_xg_pred.append(int(item))

# Get all values in order to plot them later
xg_acc = accuracy_score(y_test, int_xg_pred)
xg_f1 = f1_score(y_test,int_xg_pred, average='micro')
xg_r2 = r2_score(y_test, int_xg_pred)
xg_mae = mean_absolute_error(y_test,int_xg_pred)
xg_rmse = np.sqrt(mean_squared_error(y_test, int_xg_pred))

print("Accuracy : " , xg_acc)
print("F1",xg_f1)
print("R^2 : ", xg_r2)
print("MAE :", xg_mae)
print("RMSE:",xg_rmse)

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 X_test,
                 int_xg_pred,
                 True)

y_pred = xg_boost_model.predict(unseen_values)

plot_predictions(X_train,
                 y_train,
                 X_test,
                 y_test,
                 unseen_values,
                 y_pred,
                 True)

#plot size
plt.figure(figsize = (15, 15))

#add plot for training
plt.plot(X_train,y_train,alpha=0.7,linestyle='none',marker='*',markersize=5,color='blue',label=r'Train',zorder=7)

#addd plot for testing
plt.plot(X_test,y_test,alpha=0.6,linestyle='none',marker='o',markersize=6,color='green',label=r'Test')

#add plot for lasso model
plt.plot(X_test,y_pred_cat,alpha=0.5,linestyle='none',marker='d',markersize=7,color='red',label='CatBoost')

#add plot for linear model
plt.plot(X_test,y_pred_xg,alpha=0.4,linestyle='none',marker='+',markersize=8,color='red',label='XGBoost')

#rotate axis
plt.xticks(rotation = 90)
plt.legend()
plt.title("Comparison plot of Linear and Lasso Models")
plt.show()

model_results = [["Cat Boost",cat_acc,cat_f1,
                  cat_r2,cat_mae,cat_rmse],
                 ["XG Boost",xg_acc,xg_f1,
                  xg_r2,xg_mae,xg_rmse]]
model_results

# Now Lets put the model results into a dataframe
model_results_df = pd.DataFrame(model_results,columns=["model","accuracy","f1",'R^2','MAE','RMSE'])
model_results_df

model_results_df.plot(x="model",y=['R^2','MAE','RMSE'],kind="bar",figsize=(10,6))
plt.title("Field Artillery Model")
plt.xticks(rotation="horizontal");

model_results_df.plot(x="model",y=["accuracy","f1"],kind="bar",figsize=(10,6))
plt.xticks(rotation="horizontal");