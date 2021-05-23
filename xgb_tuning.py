from param_tuning import ParamTuning
from sklearn.model_selection import cross_val_score
from sklearn.metrics import check_scoring
import copy
import xgboost as xgb

class XGBRegressorTuning(ParamTuning):
    """
    XGBoost回帰チューニング用クラス
    """

    # 共通定数
    SEED = 42  # デフォルト乱数シード
    SEEDS = [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]  # デフォルト複数乱数シード
    CV_NUM = 5  # 最適化時のクロスバリデーションのデフォルト分割数
    
    # 学習器のインスタンス (XGBoost)
    CV_MODEL = xgb.XGBRegressor()
    # 学習時のパラメータのデフォルト値
    FIT_PARAMS = {'verbose': 0,  # 学習中のコマンドライン出力
                  'early_stopping_rounds': 20  # 学習時、評価指標がこの回数連続で改善しなくなった時点でストップ
                  }
    # 最適化で最大化するデフォルト評価指標('r2', 'neg_mean_squared_error', 'neg_mean_squared_log_error')
    SCORING = 'neg_mean_squared_error'

    # 最適化対象外パラメータ
    NOT_OPT_PARAMS = {'eval_metric': ['rmse'],  # データの評価指標
                      'objective': ['reg:squarederror'],  # 最小化させるべき損失関数
                      'random_state': [SEED],  # 乱数シード
                      'booster': ['gbtree'],  # ブースター
                      'n_estimators': [10000]  # 最大学習サイクル数（評価指標がearly_stopping_rounds連続で改善しなければ打ち切り）
                      }

    # グリッドサーチ用パラメータ
    CV_PARAMS_GRID = {'learning_rate': [0.1, 0.3, 0.5],  # 過学習のバランス(高いほど過学習寄り、低いほど汎化寄り）別名eta
                      'min_child_weight': [1, 5, 15],  # 葉に割り当てるスコアwiの合計の最小値。これを下回った場合、それ以上の分割を行わない
                      'max_depth': [3, 5, 7],  # 木の深さの最大値
                      'colsample_bytree': [0.5, 0.8, 1.0],  # 列のサブサンプリングを行う比率
                      'subsample': [0.5, 0.8, 1.0]  # 木を構築する前にデータのサブサンプリングを行う比率。1 なら全データ使用、0.5なら半分のデータ使用
                      }
    CV_PARAMS_GRID.update(NOT_OPT_PARAMS)  # 最適化対象外パラメータを追加

    # ランダムサーチ用パラメータ
    N_ITER_RANDOM = 200  # ランダムサーチの繰り返し回数
    CV_PARAMS_RANDOM = {'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5],
                        'min_child_weight': [1, 3, 5, 7, 9, 11, 13, 15],
                        'max_depth': [3, 4, 5, 6, 7],
                        'colsample_bytree': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        'subsample': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
                        }
    CV_PARAMS_RANDOM.update(NOT_OPT_PARAMS)  # 最適化対象外パラメータを追加

    # ベイズ最適化用パラメータ
    N_ITER_BAYES = 100  # ベイズ最適化の繰り返し回数
    INIT_POINTS = 10  # 初期観測点の個数(ランダムな探索を何回行うか)
    ACQ = 'ei'  # 獲得関数(https://ohke.hateblo.jp/entry/2018/08/04/230000)
    BAYES_PARAMS = {'learning_rate': (0.1, 0.3),
                    'min_child_weight': (1, 15),
                    'max_depth': (3, 7),
                    'colsample_bytree': (0.5, 1),
                    'subsample': (0.5, 1)
                    }
    INT_PARAMS = ['min_child_weight', 'max_depth']  # 整数型のパラメータのリスト(ベイズ最適化時は都度int型変換する)
    BAYES_NOT_OPT_PARAMS = {k: v[0] for k, v in NOT_OPT_PARAMS.items()}  # ベイズ最適化対象外パラメータ

    # 範囲選択検証曲線用パラメータ範囲
    VALIDATION_CURVE_PARAMS = {'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5],
                        'min_child_weight': [1, 3, 5, 7, 9, 11, 13, 15],
                        'max_depth': [3, 4, 5, 6, 7],
                        'colsample_bytree': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        'subsample': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
                        }
    # 検証曲線表示等で使用するパラメータのスケール('linear', 'log')
    PARAM_SCALES = {'learning_rate': 'linear',
                    'min_child_weight': 'linear',
                    'max_depth': 'linear',
                    'colsample_bytree': 'linear',
                    'subsample': 'linear'
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
        params = self._int_conversion(params, self.int_params)  # 整数パラメータはint型に変換
        params.update(self.bayes_not_opt_params)  # 最適化対象以外のパラメータも追加
        # XGBoostのモデル作成
        cv_model = copy.deepcopy(self.cv_model)
        cv_model.set_params(**params)

        # eval_data_sourceに全データ指定時(cross_val_scoreでクロスバリデーション)
        if self.eval_data_source == 'all':
            scores = cross_val_score(cv_model, self.X, self.y, cv=self.cv,
                                    scoring=self.scoring, fit_params=self.fit_params, n_jobs=-1)
            val = scores.mean()

        # eval_data_sourceに学習orテストデータ指定時(スクラッチでクロスバリデーション)
        else:
            scores = self._scratch_cross_val(cv_model, self.eval_data_source)
            val = sum(scores)/len(scores)

        return val