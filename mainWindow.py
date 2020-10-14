from modelComb import *
from ageLearn import *
from gpiBase import GpiBaseClass

#=======================================================================================================
#   クラス メインウインドウ
#=======================================================================================================
class MainWindow(GpiBaseClass):
    def __init__(self):                                                                                 # 初期化
        try:
            GpiBaseClass.__init__(self, None)                                                      # スーパークラスの初期化
            self.preReadDone = False                                                                    # 事前読み込みフラグを偽にする
            self.setContainer()                                                                         # コンテナ設定
            self.subDoneFlag = True                                                                     # 事前読み込みフラグを真にする

            CURPARTS = GP.CURPARTS  # 学習部品をセット
            CURPARTS.LABEL_LIST = GP.AGE_LIST  # ラベルリストをセット
            CURPARTS.OUT_LIST = GP.AGE_LIST  # 出力ラベルリストをセット
            CURPARTS.LEARN_CLASS.stop = False  # 学習クラスのストップフラグ初期化
            CURPARTS.MODEL_COMB_LIST = CURPARTS.AGE.MODEL_COMB_LIST  # モデルコンボをセット
            CURPARTS.LEARN_CLASS.learn()  # 学習

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   コンテナ設定
    #---------------------------------------------------------------------------------------------------
    def setContainer(self):
        try:
            # 学習クラスコンテナ設定
            ageLearn = AgeLearnClass.getInstance()                                                      # AGE学習クラス            evtLearn = EvtLearnClass.getInstance()                                                              # EVT学習クラス
            object = GP.CH
            object.LEARN_CLASS = ageLearn                                                               # AGE学習クラス
            GP.CURPARTS = object                                                                        # 部品転写
            conf = object.AGE.LEARN_CONF.objectList[0]                                                  # AGEオブジェクトリストをすべて実行
            object.MODEL_COMB = ModelCombClass(conf)                                                    # モデルコンボリスト生成
            object.MODEL_COMB.setLearnUnit()                                                            # 学習単位と学習単位名をセット
            pass

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                           # 例外を表示
            pass

