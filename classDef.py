import os
import numpy as np
from staticImport import *
from distutils.util import strtobool

#=======================================================================================================
#   スーパークラス パラメータクラス
#=======================================================================================================
class ParameterClass():
    def __init__(self, logPath):                                                                        # 初期化
        try:
            self.logPath =logPath                                                                       # ログファイル名

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   パラメーターをインスタンス変数に転写する
    #---------------------------------------------------------------------------------------------------
    def setClassVar(self, object):
        try:
            for objectName in self.nameList:                                                            # ローカル変数名リストをすべて実行
                exec("object." + objectName + " = self." + objectName)                                  # オブジェクトのインスタンス変数のセット
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   ログファイルのデータを読み込む
    #---------------------------------------------------------------------------------------------------
    def loadData(self):
        try:
            if self.logPath is not None:                                                                # ログパスが有る時
                if os.path.isfile(self.logPath) and os.path.getsize(self.logPath) > 0:                  # ファイルが有る時
                    with open(file=self.logPath,mode="r",encoding="utf-8") as f:                        # "utf-8"でファイルをオープン
                        for objectName in self.nameList:                                                # オブジェクト名リストをすべて実行
                            exec("self.object = " + "self." + objectName)                               # インスタンス変数のセット
                            if type(self.object) == type([]):                                           # タイプが"list"の時
                                for i, data in enumerate(self.object):                                  # リストをすべて実行
                                    self.var = f.readline()                                             # ファイルから一行読み込む
                                    self.var = self.var.strip()                                         # 改行を取り除く
                                    if type(data) == type(''):                                          # タイプが"str"の時
                                        self.object[i] = self.var                                       # インスタンス変数のセット
                                    elif type(data) == type(0):                                         # タイプが"int"の時
                                        self.object[i] = int(self.var)                                  # インスタンス変数のセット
                                    elif type(data) == type(0.0):                                       # タイプが"float"の時
                                       self.object[i] = float(self.var)                                 # インスタンス変数のセット
                                    elif type(data) == type(True):                                      # タイプが"bool"の時
                                        self.object[i] = bool(strtobool(self.var))                      # インスタンス変数のセット
                                    else:                                                               # その他の時
                                        self.object[i] = self.var                                       # インスタンス変数のセット
                            else:                                                                       # タイプが"list"でない時
                                ttt = type(self.object)
                                self.var = f.readline()                                                 # ファイルから一行読み込む
                                self.var = self.var.strip()                                             # 改行を取り除く
                                if type(self.object) == type(''):                                       # タイプが"str"の時
                                    exec("self." + objectName + " = self.var")                          # インスタンス変数のセット
                                elif type(self.object) == type(0):                                      # タイプが"int"の時
                                    exec("self." + objectName + " = int(self.var)")                     # インスタンス変数のセット
                                elif type(self.object) == type(0.0):                                    # タイプが"float"の時
                                    exec("self." + objectName + " = float(self.var)")                   # インスタンス変数のセット
                                elif type(self.object) == type(True):                                   # タイプが"bool"の時
                                    exec("self." + objectName + " = bool(strtobool(self.var))")         # インスタンス変数のセット
                                else:                                                                   # その他の時
                                    exec("self." + objectName + " = self.var")                          # インスタンス変数のセット
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

#=======================================================================================================
#   クラス チャンバー年齢学習パラメータクラス
#=======================================================================================================
class LearnAgeParameterClass(ParameterClass):
    def __init__(self, logPath):                                                                        # 初期化
        try:
            ParameterClass.__init__(self, logPath)                                                     # スーパークラスの初期化
            AGE_BASE      = GP.AGE_BASE.TARGET                                                          # 年齢基準
            HIDDEN_LAYERS = 5                                                                           # 隠れ層数
            DROPOUT       = 0.05                                                                        # ドロップアウト
            LEARN_PARTS   = GP.PARTS.CH                                                                 # 学習部品
            LEARN_UNIT    = GP.LEARN_UNIT.TYPE_ID                                                       # 学習単位
            USE_ABNORMAL  = False                                                                       # 異常値使用フラグ
            SAVE_FLAG     = False                                                                       # 保存フラグ
            SAMPLES       = 10000                                                                       # ラベル毎のデータ数
            SAMPLE_RATIO_0 = 0.7                                                                        # 上位のデータサンプル割合）
            SAMPLE_RATIO_N = 0.9                                                                        # 次回以後上位のデータサンプル割合）
            INIT_EPOCHS   = 30                                                                          # 初期エポック数
            CUT_EPOCHS    = 30                                                                          # カットエポック数
            CUT_TRIALS    = 4                                                                           # カット回数
            BATCH_SIZE    = 100                                                                         # バッチサイズ
            VERBOSE       = 0                                                                           # VERBOSE
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                                (name != 'logPath') and
                                (name != '__pydevd_ret_val_dict')]                                      # ローカル変数名リストを作成
            for objectName in self.nameList:                                                            # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)                                         # オブジェクトのインスタンス変数のセット
            self.loadData()                                                                             # パラメータをログファイルから読込
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

#=======================================================================================================
#   クラス チャンバー年齢学習パラメータクラス
#=======================================================================================================
class AgeLearnParameterClass(LearnAgeParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None
    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if AgeLearnParameterClass._singleton is None:                                               # シングルトンが無いとき
                LearnAgeParameterClass.__init__(self, GP.LEARN_LOG.AGE_LEARN)                           # スーパークラスの初期化
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if AgeLearnParameterClass._singleton is None:                                                   # シングルトンが無いとき
            AgeLearnParameterClass._singleton = AgeLearnParameterClass()                                # インスタンスを生成してシングルトンにセット
        return AgeLearnParameterClass._singleton                                                        # シングルトンがを返す


