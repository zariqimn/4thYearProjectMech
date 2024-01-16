#find environment path
# activate env
#cd file dir
#run python or ipython


import numpy as np
import torch
import tensorflow as tf
import os
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from botorch.models import SingleTaskGP, ModelListGP
from gpytorch.mlls.exact_marginal_log_likelihood import ExactMarginalLogLikelihood
from botorch import fit_gpytorch_model
from botorch.acquisition.monte_carlo import qExpectedImprovement
from botorch.acquisition.analytic import ProbabilityOfImprovement
from botorch.optim import optimize_acqf
from botorch.posteriors import PosteriorList
from ax.service.ax_client import AxClient
from ax.service.utils.instantiation import ObjectiveProperties

import torch

from ax.utils.notebook.plotting import render, init_notebook_plotting
from ax.plot.pareto_utils import compute_posterior_pareto_frontier
from ax.plot.pareto_frontier import plot_pareto_frontier
init_notebook_plotting()


os.chdir(os.path.dirname(__file__))
df1 = pd.read_csv('FinalDataset.csv')
######
X = df1[['shell thickness','cell size', 'relative density']]
Y = df1[['Internal Energy','Plastic Dissipation', 'mass']]
scaler = StandardScaler()
X = scaler.fit_transform(X)
scaler1 = StandardScaler()
Y = scaler1.fit_transform(Y)


X_train,X_test, y_train, y_test = train_test_split(X,Y, test_size=0.2,random_state=42)
####
model = Sequential()
model.add(Dense(15,input_shape=(3,)))
model.add(Dense(15,activation='relu'))
model.add(Dense(15,activation='relu'))
model.add(Dense(15,activation='relu'))
model.add(Dense(15,activation='relu'))
model.add(Dense(15,activation='relu'))
model.add(Dense(3,))
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.003),loss ='mse',metrics=['mae'])
model.summary()
#earlystopper = EarlyStopping(monitor='val_loss',min_delta=0, patience=15,verbose=1, mode='auto')
history = model.fit(X_train,y_train,epochs=1000, validation_split=0.2,verbose=0)


ax_client = AxClient()
ax_client.create_experiment(
    name="mobo_experiment",
    parameters=[
        {
            "name": "x1",
            "type": "range",
            "bounds": [-1.8501, 1.3318],
        },
        {
            "name": "x2",
            "type": "range",
            "bounds": [-2.0700, -1.4010],
        },
        {
            "name": "x3",
            "type": "range",
            "bounds": [-2.0902,1.3669],
        }
    ],
    objectives={
        # `threshold` arguments are optional
        "a": ObjectiveProperties(minimize=False ), 
        "b": ObjectiveProperties(minimize=True)
    },
    overwrite_existing_experiment=True,
    is_test=True,
)

def evaluate(parameters):

    result = model.predict(np.array([[parameters.get("x1"), parameters.get("x2"), parameters.get("x3")]]))
    obj1, obj2 = torch.tensor(result[0,0]), torch.tensor(result[0,2])
    return {"a": (obj1.item(), 0.0), "b": (obj2.item(), 0.0)}

for i in range(200):
    parameters, trial_index = ax_client.get_next_trial()
    # Local evaluation here can be replaced with deployment to external system.
    ax_client.complete_trial(trial_index=trial_index, raw_data=evaluate(parameters))


objectives = ax_client.experiment.optimization_config.objective.objectives
frontier = compute_posterior_pareto_frontier(
    experiment=ax_client.experiment,
    data=ax_client.experiment.fetch_data(),
    primary_objective=objectives[1].metric,
    secondary_objective=objectives[0].metric,
    absolute_metrics=["a", "b"],
    num_points=20,
)
render(plot_pareto_frontier(frontier, CI_level=0.90))

pareto_solutions = list(ax_client.get_pareto_optimal_parameters().values())
parameter_solutions = []
SEA = []
PD = []
for i in range(len(pareto_solutions)):
    pareto_solutions_parameter = np.array(list(pareto_solutions[i][0].values())).reshape(-1,3)
    pareto_objective = model.predict(pareto_solutions_parameter)
    true_pareto_objective = scaler1.inverse_transform(pareto_objective)
    calculate_sea = true_pareto_objective[0][0]/true_pareto_objective[0][2]
    plastic_ratio = true_pareto_objective[0][1]/true_pareto_objective[0][0]
    SEA_pd = plastic_ratio
    if SEA_pd<1.0:
        SEA.append(calculate_sea)
        PD.append(SEA_pd)
        parameter_solutions.append(pareto_solutions_parameter)


max_SEA = max(SEA)
max_SEA_index = SEA.index(max_SEA)
best_parameter = parameter_solutions[max_SEA_index]
best_parameter = scaler.inverse_transform(best_parameter)
print(f"best combination of parameters is: {best_parameter}")

xxx = model.predict(np.array(parameter_solutions).reshape(-1,3))
xxx =scaler1.inverse_transform(xxx)
import matplotlib.pyplot as plt
import seaborn as sns

Y1 = scaler1.inverse_transform(y_test)
Y2 = scaler1.inverse_transform(y_train)
sns.scatterplot(x = Y1[:,0]*1e-6, y= Y1[:,2]*1e6,color='brown', marker='x', s=30)
sns.scatterplot(x = Y2[:,0]*1e-6, y= Y2[:,2]*1e6,color='brown', marker='x', s=30)
sns.lineplot(x=xxx[:,0]*1e-6, y=xxx[:,2]*1e6)
plt.title('Pareto Frontier of Energy Absorption vs mass')
plt.xlabel('Energy Absorption (kJ)')
plt.ylabel('scaled mass (g)')