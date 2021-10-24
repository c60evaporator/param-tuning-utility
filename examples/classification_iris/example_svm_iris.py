# %% SVC, GridSearch, no argument
import parent_import
from muscle_tuning import SVMClassifierTuning
import seaborn as sns
iris = sns.load_dataset("iris")
OBJECTIVE_VARIALBLE = 'species'  # 目的変数
USE_EXPLANATORY = ['petal_width', 'petal_length', 'sepal_width', 'sepal_length']  # 説明変数
y = iris[OBJECTIVE_VARIALBLE].values
X = iris[USE_EXPLANATORY].values
tuning = SVMClassifierTuning(X, y, USE_EXPLANATORY, y_colname=OBJECTIVE_VARIALBLE)
tuning.plot_first_validation_curve()
tuning.grid_search_tuning()
tuning.plot_search_history()
tuning.plot_search_map()
tuning.plot_best_learning_curve()
tuning.plot_best_validation_curve()
tuning.plot_param_importances()

# %% SVC, RandomSearch, no argument
import parent_import
from muscle_tuning import SVMClassifierTuning
import seaborn as sns
iris = sns.load_dataset("iris")
OBJECTIVE_VARIALBLE = 'species'  # 目的変数
USE_EXPLANATORY = ['petal_width', 'petal_length', 'sepal_width', 'sepal_length']  # 説明変数
y = iris[OBJECTIVE_VARIALBLE].values
X = iris[USE_EXPLANATORY].values
tuning = SVMClassifierTuning(X, y, USE_EXPLANATORY, y_colname=OBJECTIVE_VARIALBLE)
tuning.random_search_tuning()
tuning.plot_search_history()
tuning.plot_search_map()
tuning.plot_best_learning_curve()
tuning.plot_best_validation_curve()
tuning.plot_param_importances()

# %% SVC, BayesianOptimization, no argument
import parent_import
from muscle_tuning import SVMClassifierTuning
import seaborn as sns
iris = sns.load_dataset("iris")
OBJECTIVE_VARIALBLE = 'species'  # 目的変数
USE_EXPLANATORY = ['petal_width', 'petal_length', 'sepal_width', 'sepal_length']  # 説明変数
y = iris[OBJECTIVE_VARIALBLE].values
X = iris[USE_EXPLANATORY].values
tuning = SVMClassifierTuning(X, y, USE_EXPLANATORY, y_colname=OBJECTIVE_VARIALBLE)
tuning.bayes_opt_tuning()
tuning.plot_search_history()
tuning.plot_search_map()
tuning.plot_best_learning_curve()
tuning.plot_best_validation_curve()
tuning.plot_param_importances()

# %% SVC, Optuna, no argument
import parent_import
from muscle_tuning import SVMClassifierTuning
import seaborn as sns
iris = sns.load_dataset("iris")
OBJECTIVE_VARIALBLE = 'species'  # 目的変数
USE_EXPLANATORY = ['petal_width', 'petal_length', 'sepal_width', 'sepal_length']  # 説明変数
y = iris[OBJECTIVE_VARIALBLE].values
X = iris[USE_EXPLANATORY].values
tuning = SVMClassifierTuning(X, y, USE_EXPLANATORY, y_colname=OBJECTIVE_VARIALBLE)
tuning.optuna_tuning()
tuning.plot_search_history()
tuning.plot_search_map()
tuning.plot_best_learning_curve()
tuning.plot_best_validation_curve()
tuning.plot_param_importances()