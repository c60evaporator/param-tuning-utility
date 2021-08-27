# %% plot_search_history(), no argument
import parent_import
from param_tuning import LGBMRegressorTuning
from sklearn.datasets import load_boston
import pandas as pd
# Load dataset
USE_EXPLANATORY = ['CRIM', 'NOX', 'RM', 'DIS', 'LSTAT']
df_boston = pd.DataFrame(load_boston().data, columns=load_boston().feature_names)
X = df_boston[USE_EXPLANATORY].values
y = load_boston().target
tuning = LGBMRegressorTuning(X, y, USE_EXPLANATORY)
best_params, best_score = tuning.optuna_tuning()
###### Run plot_search_history() ######
tuning.plot_search_history()

# %% plot_search_history(), Set x_axis to 'time'
import parent_import
from param_tuning import LGBMRegressorTuning
from sklearn.datasets import load_boston
import pandas as pd
# Load dataset
USE_EXPLANATORY = ['CRIM', 'NOX', 'RM', 'DIS', 'LSTAT']
df_boston = pd.DataFrame(load_boston().data, columns=load_boston().feature_names)
X = df_boston[USE_EXPLANATORY].values
y = load_boston().target
tuning = LGBMRegressorTuning(X, y, USE_EXPLANATORY)
best_params, best_score = tuning.optuna_tuning()
###### Run plot_search_history() ######
tuning.plot_search_history(x_axis='time')