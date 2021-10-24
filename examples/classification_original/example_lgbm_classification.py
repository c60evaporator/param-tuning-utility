# %% LGBMClassifier, GridSearch, no argument
import parent_import
from muscle_tuning import LGBMClassifierTuning
import pandas as pd
df_clf = pd.read_csv('../sample_data/nba_nfl_2.csv')
OBJECTIVE_VARIALBLE = 'league'  # 目的変数
USE_EXPLANATORY = ['height', 'weight']  # 説明変数
y = df_clf[OBJECTIVE_VARIALBLE].values
X = df_clf[USE_EXPLANATORY].values
tuning = LGBMClassifierTuning(X, y, USE_EXPLANATORY, y_colname=OBJECTIVE_VARIALBLE)
tuning.plot_first_validation_curve()
tuning.grid_search_tuning()
tuning.plot_search_history()
tuning.plot_search_map()
tuning.plot_best_learning_curve()
tuning.plot_best_validation_curve()
tuning.plot_param_importances()

# %% LGBMClassifier, RandomSearch, no argument
import parent_import
from muscle_tuning import LGBMClassifierTuning
import pandas as pd
df_clf = pd.read_csv('../sample_data/nba_nfl_2.csv')
OBJECTIVE_VARIALBLE = 'league'  # 目的変数
USE_EXPLANATORY = ['height', 'weight']  # 説明変数
y = df_clf[OBJECTIVE_VARIALBLE].values
X = df_clf[USE_EXPLANATORY].values
tuning = LGBMClassifierTuning(X, y, USE_EXPLANATORY, y_colname=OBJECTIVE_VARIALBLE)
tuning.random_search_tuning()
tuning.plot_search_history()
tuning.plot_search_map()
tuning.plot_best_learning_curve()
tuning.plot_best_validation_curve()
tuning.plot_param_importances()

# %% LGBMClassifier, BayesianOptimization, no argument
import parent_import
from muscle_tuning import LGBMClassifierTuning
import pandas as pd
df_clf = pd.read_csv('../sample_data/nba_nfl_2.csv')
OBJECTIVE_VARIALBLE = 'league'  # 目的変数
USE_EXPLANATORY = ['height', 'weight']  # 説明変数
y = df_clf[OBJECTIVE_VARIALBLE].values
X = df_clf[USE_EXPLANATORY].values
tuning = LGBMClassifierTuning(X, y, USE_EXPLANATORY, y_colname=OBJECTIVE_VARIALBLE)
tuning.bayes_opt_tuning()
tuning.plot_search_history()
tuning.plot_search_map()
tuning.plot_best_learning_curve()
tuning.plot_best_validation_curve()
tuning.plot_param_importances()

# %% LGBMClassifier, Optuna, no argument
import parent_import
from muscle_tuning import LGBMClassifierTuning
import pandas as pd
df_clf = pd.read_csv('../sample_data/nba_nfl_2.csv')
OBJECTIVE_VARIALBLE = 'league'  # 目的変数
USE_EXPLANATORY = ['height', 'weight']  # 説明変数
y = df_clf[OBJECTIVE_VARIALBLE].values
X = df_clf[USE_EXPLANATORY].values
tuning = LGBMClassifierTuning(X, y, USE_EXPLANATORY, y_colname=OBJECTIVE_VARIALBLE)
tuning.optuna_tuning()
tuning.plot_search_history()
tuning.plot_search_map()
tuning.plot_best_learning_curve()
tuning.plot_best_validation_curve()
tuning.plot_param_importances()
# %%
