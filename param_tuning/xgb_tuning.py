from sklearn.model_selection import cross_val_score
import time
import xgboost as xgb

from .param_tuning import ParamTuning

class XGBRegressorTuning(ParamTuning):
    """
    XGBoost回帰チューニング用クラス
    """

    # 共通定数
    SEED = 42  # デフォルト乱数シード
    SEEDS = [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]  # デフォルト複数乱数シード
    CV_NUM = 5  # 最適化時のクロスバリデーションのデフォルト分割数
    
    # 学習器のインスタンス (XGBoost)
    ESTIMATOR = xgb.XGBRegressor()
    # 学習時のパラメータのデフォルト値
    FIT_PARAMS = {'verbose': 0,  # 学習中のコマンドライン出力
                  'early_stopping_rounds': 10,  # 学習時、評価指標がこの回数連続で改善しなくなった時点でストップ
                  'eval_metric': 'rmse'  # early_stopping_roundsの評価指標
                  }
    # 最適化で最大化するデフォルト評価指標('r2', 'neg_mean_squared_error', 'neg_mean_squared_log_error')
    SCORING = 'neg_mean_squared_error'

    # 最適化対象外パラメータ
    NOT_OPT_PARAMS = {'objective': 'reg:squarederror',  # 最小化させるべき損失関数
                      'random_state': SEED,  # 乱数シード
                      'booster': 'gbtree',  # ブースター
                      'n_estimators': 10000  # 最大学習サイクル数（評価指標がearly_stopping_rounds連続で改善しなければ打ち切り）
                      }

    # グリッドサーチ用パラメータ
    CV_PARAMS_GRID = {'learning_rate': [0.01, 0.1, 0.3],  # 過学習のバランス(高いほど過学習寄り、低いほど汎化寄り）別名eta
                      'min_child_weight': [2, 5, 10],  # 葉に割り当てるスコアwiの合計の最小値。これを下回った場合、それ以上の分割を行わない
                      'max_depth': [2, 4, 9],  # 木の深さの最大値
                      'colsample_bytree': [0.2, 0.5, 1.0],  # 列のサブサンプリングを行う比率
                      'subsample': [0.2, 0.5, 0.8],  # 木を構築する前にデータのサブサンプリングを行う比率。1なら全データ使用、0.5なら半分のデータ使用
                      'reg_lambda': [0.1, 1]
                      }

    # ランダムサーチ用パラメータ
    N_ITER_RANDOM = 450  # ランダムサーチの試行数
    CV_PARAMS_RANDOM = {'learning_rate': [0.01, 0.02, 0.05, 0.1, 0.2, 0.3],
                        'min_child_weight': [2, 3, 4, 5, 6, 7, 8, 9, 10],
                        'max_depth': [2, 3, 4, 5, 6, 7, 8, 9],
                        'colsample_bytree': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        'subsample': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        'reg_alpha': [0.001, 0.003, 0.01, 0.03, 0.1],
                        'reg_lambda': [0.001, 0.003, 0.01, 0.03, 0.1],
                        'gamma': [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1]
                        }

    # ベイズ最適化用パラメータ
    N_ITER_BAYES = 120  # BayesianOptimizationの試行数
    INIT_POINTS = 10  # BayesianOptimizationの初期観測点の個数(ランダムな探索を何回行うか)
    ACQ = 'ei'  # BayesianOptimizationの獲得関数(https://ohke.hateblo.jp/entry/2018/08/04/230000)
    N_ITER_OPTUNA = 300  # Optunaの試行数
    BAYES_PARAMS = {'learning_rate': (0.01, 0.3),
                    'min_child_weight': (2, 10),
                    'max_depth': (2, 9),
                    'colsample_bytree': (0.2, 1.0),
                    'subsample': (0.2, 1.0),
                    'reg_alpha': (0.001, 0.1),
                    'reg_lambda': (0.001, 0.1),
                    'gamma': (0.0001, 0.1)
                    }
    INT_PARAMS = ['min_child_weight', 'max_depth']  # 整数型のパラメータのリスト(ベイズ最適化時は都度int型変換する)

    # 範囲選択検証曲線用パラメータ範囲
    VALIDATION_CURVE_PARAMS = {'subsample': [0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0],
                               'colsample_bytree': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                               'reg_alpha': [0, 0.0001, 0.001, 0.01, 0.03, 0.1, 0.3, 1.0],
                               'reg_lambda': [0, 0.0001, 0.001, 0.01, 0.03, 0.1, 0.3, 1.0],
                               'learning_rate': [0, 0.0001, 0.001, 0.01, 0.03, 0.1, 0.3, 1.0],
                               'min_child_weight': [1, 3, 5, 7, 9, 11, 13, 15],
                               'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                               'gamma': [0, 0.0001, 0.001, 0.01, 0.03, 0.1, 0.3, 1.0]
                               }
    # 検証曲線表示等で使用するパラメータのスケール('linear', 'log')
    PARAM_SCALES = {'subsample': 'linear',
                    'colsample_bytree': 'linear',
                    'reg_alpha': 'log',
                    'reg_lambda': 'log',
                    'learning_rate': 'log',
                    'min_child_weight': 'linear',
                    'max_depth': 'linear',
                    'gamma': 'log'
                    }
    
    def _additional_init(self, eval_data_source = 'all', **kwargs):
        """
        初期化時の追加処理
        
        Parameters
        ----------
        eval_data_source : str
            XGBoostのfit_paramsに渡すeval_setのデータ
            'all'なら全データ、'valid'ならテストデータ、'train'なら学習データ
        """
        # eval_dataをテストデータから取得
        self.eval_data_source = eval_data_source
        return

    def _train_param_generation(self, src_fit_params):
        """
        入力データから学習時パラメータの生成 (eval_set)
        
        Parameters
        ----------
        src_fit_params : Dict
            処理前の学習時パラメータ
        """

        # src_fit_paramsにeval_setが存在しないとき、入力データをそのまま追加
        if 'eval_set' not in src_fit_params:
            src_fit_params['eval_set'] =[(self.X, self.y)]

        return src_fit_params

    def _bayes_evaluate(self, **kwargs):
        """
         ベイズ最適化時の評価指標算出メソッド
        """
        # 最適化対象のパラメータ
        params = kwargs
        params = self._pow10_conversion(params, self.param_scales)  # 対数パラメータは10のべき乗に変換
        params = self._int_conversion(params, self.int_params)  # 整数パラメータはint型に変換
        params.update(self.not_opt_params)  # 最適化対象以外のパラメータも追加
        # XGBoostのモデル作成
        estimator = self.estimator
        estimator.set_params(**params)

        # eval_data_sourceに全データ指定時(cross_val_scoreでクロスバリデーション)
        if self.eval_data_source == 'all':
            scores = cross_val_score(estimator, self.X, self.y, cv=self.cv,
                                    scoring=self.scoring, fit_params=self.fit_params, n_jobs=-1)
            val = scores.mean()
        # eval_data_sourceに学習orテストデータ指定時(スクラッチでクロスバリデーション)
        else:
            scores = self._scratch_cross_val(estimator, self.eval_data_source)
            val = sum(scores)/len(scores)
        # 所要時間測定
        self.elapsed_times.append(time.time() - self.start_time)

        return val

    def _optuna_evaluate(self, trial):
        """
        Optuna最適化時の評価指標算出メソッド
        """
        # パラメータ格納
        params = {}
        for k, v in self.tuning_params.items():
            log = True if self.param_scales[k] == 'log' else False  # 変数のスケールを指定（対数スケールならTrue）
            if k in self.int_params:  # int型のとき
                params[k] = trial.suggest_int(k, v[0], v[1], log=log)
            else:  # float型のとき
                params[k] = trial.suggest_float(k, v[0], v[1], log=log)
        params.update(self.not_opt_params)  # 最適化対象以外のパラメータも追加
        # XGBoostのモデル作成
        estimator = self.estimator
        estimator.set_params(**params)
        
        # eval_data_sourceに全データ指定時(cross_val_scoreでクロスバリデーション)
        if self.eval_data_source == 'all':
            scores = cross_val_score(estimator, self.X, self.y, cv=self.cv,
                                    scoring=self.scoring, fit_params=self.fit_params, n_jobs=-1)
            val = scores.mean()

        # eval_data_sourceに学習orテストデータ指定時(スクラッチでクロスバリデーション)
        else:
            scores = self._scratch_cross_val(estimator, self.eval_data_source)
            val = sum(scores)/len(scores)
        
        return val