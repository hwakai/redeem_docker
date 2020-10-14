import os
import numpy as np
from numpy import random
import gc
from kerasImport import *
from staticImport import *
from gpiBase import GpiBaseClass


# =======================================================================================================
#   クラス　HistoryClass
# =======================================================================================================
class HistoryClass():
    def __init__(self):  # 初期化
        self.history = {'acc': [], 'val_acc': [], 'loss': [], 'val_loss': [], 'epochs': 0, 'learnType': ''}  # ヒストリーを初期化

    # ---------------------------------------------------------------------------------------------------
    #   オリジナルタブのパラメーターをインスタンス変数に転写する
    # ---------------------------------------------------------------------------------------------------
    def appendHistory(self, his):
        try:
            self.history['acc'] += his.history['acc']  # acc配列をヒストリーに追加
            self.history['val_acc'] += his.history['val_acc']  # val_acc配列をヒストリーに追加
            self.history['loss'] += his.history['loss']  # loss配列をヒストリーに追加
            self.history['val_loss'] += his.history['val_loss']  # val_loss配列をヒストリーに追加

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return  # 終了

    # ---------------------------------------------------------------------------------------------------
    #   オリジナルタブのパラメーターをインスタンス変数に転写する
    # ---------------------------------------------------------------------------------------------------
    def initialize(self):
        try:
            self.history['acc'].clear()  # acc配列をクリア
            self.history['val_acc'].clear()  # val_acc配列をクリア
            self.history['loss'].clear()  # loss配列をクリア
            self.history['val_loss'].clear()  # val_loss配列をクリア
            self.history['epochs'] = 0  # epochsをクリア

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return  # 終了


# =======================================================================================================
#   クラス モデルコンボクラス
# =======================================================================================================
class ModelCombClass(GpiBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            GpiBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.SAVE_MODEL = SaveModelClass(TABLE_NAME)  # SAVE_DATAを生成
            self.SAVE_DATA = SaveDataClass(TABLE_NAME)  # SAVE_DATAを生成

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def initialize(self):
        try:
            self.SAVE_MODEL.initialize()  # SAVE_MODELを初期化する
            self.SAVE_DATA.initialize()  # SAVE_DATA削除

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   学習単位と学習単位名をセットして保存パスをセットする
    # ---------------------------------------------------------------------------------------------------
    def setLearnUnit(self):
        try:
            self.SAVE_MODEL.setLearnUnit()  # SAVE_MODEL保存パスをセットする
            self.SAVE_DATA.setLearnUnit()  # SAVE_DATA保存パスをセットする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   モデルの読み込み
    # ---------------------------------------------------------------------------------------------------
    def loadModel(self, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if self.SAVE_MODEL.loadModel():  # SAVE_MODELを読み込に成功した時
                self.SAVE_DATA.loadData(p)  # 保存データをファイルから読み込む
                self.endLevel(p)  # 現レベルの終了
                return True  # 成功を返す
            self.endLevel(p)  # 現レベルの終了
            return False  # 失敗を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習データ保存
    # ---------------------------------------------------------------------------------------------------
    def saveModel(self, SRC_MODEL, p=None):
        try:
            self.startNewLevel(2, p)  # 新しいレベルの進捗開始
            self.SAVE_MODEL.saveModel(SRC_MODEL.SAVE_MODEL, p)  # モデルを保存
            return self.returnResult(True, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # 例外を表示


# =======================================================================================================
#   クラス 保存ベースクラス
# =======================================================================================================
class SaveBaseClass(GpiBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            GpiBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   パラメータの設定
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self, laserIdList, parameter):
        try:
            parameter.setClassVar(self)  # メンバーのパラメータデータをセット
            self.MY_LASER_LIST = laserIdList  # レーザーIDリストを転写

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習単位と学習単位名をセットして保存パスをセットする
    # ---------------------------------------------------------------------------------------------------
    def setLearnUnit(self):
        try:
            # 学習タイプから学習結果の保存パスをセット
            outputDir = GP.UPLOADDIR  # 親ディレクトリ
            if not os.path.exists(outputDir):  # ディレクトリの有無を確認
                os.makedirs(outputDir)  # 途中のディレクトリを含めてディレクトリを作成
            self.learnModelPath = outputDir + "Model.log"  # 学習モデルパス
            self.learnWeightPath = outputDir + "Weight.log"  # 学習モデル係数パス
            self.learnHistoryPath = outputDir + "History.log"  # 学習ヒストリーパス

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス 保存モデルクラス
# =======================================================================================================
class SaveModelClass(SaveBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            SaveBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.MODEL = None  # モデル初期化
            self.HISTORY = None  # ヒストリー初期化
            self.SCORE = None  # スコア初期化
            self.HISTORY = HistoryClass()  # ヒストリー生成

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def initialize(self):
        try:
            self.HISTORY.initialize()  # ヒストリーを初期化する
            self.MODEL = None  # モデル初期化
            self.SCORE = None  # スコア初期化

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   モデルの読み込み
    # ---------------------------------------------------------------------------------------------------
    def loadModel(self, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            # 学習済みモデルの読み込み
            if os.path.exists(self.learnModelPath):  # ファイルが有る時
                self.MODEL = model_from_json(open(self.learnModelPath, 'r').read())  # モデルを読み込む
            if os.path.exists(self.learnWeightPath):  # ファイルが有る時
                self.MODEL.load_weights(self.learnWeightPath)  # モデルに係数を読み込む
            # HISTORYの読み込み
            if os.path.exists(self.learnHistoryPath):  # ファイルが有る時
                self.loadHistory(self.learnHistoryPath)  # ヒストリーの読み込み
                history = self.HISTORY.history  # history辞書転写
                self.SCORE = history['score']  # スコアインスタンス変数にセット
                self.SCORE = [history['loss'][-1], history['acc'][-1]]  # スコアインスタンス変数にセット
                self.LOSE = history['loss'][-1]  # ロスインスタンス変数にセット
                self.LEARNED_TYPE = history['learnType']  # 学習タイプインスタンス変数にセット
                self.EPOCHS = history['epochs']  # エポックスインスタンス変数にセット
                self.MODEL.compile(loss='categorical_crossentropy', optimizer='sgd',
                                   metrics=['accuracy'])  # モデルをコンパイルする
                self.endLevel(p)  # 現レベルの終了
                return True  # 成功を返す
            self.endLevel(p)  # 現レベルの終了
            return False  # 失敗を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    # Historyの保存
    # ---------------------------------------------------------------------------------------------------
    def saveHistory(self, SRC_MODEL):
        try:
            history = SRC_MODEL.HISTORY.history
            historyPath = self.learnHistoryPath
            acc = history['acc']
            val_acc = history['val_acc']
            loss = history['loss']
            val_loss = history['val_loss']
            score = history['score']
            epochs = history['epochs']

            acc_Str = ",".join(np.array(acc, dtype='str')) + "\n"
            val_acc_Str = ",".join(np.array(val_acc, dtype='str')) + "\n"
            loss_Str = ",".join(np.array(loss, dtype='str')) + "\n"
            val_loss_Str = ",".join(np.array(val_loss, dtype='str')) + "\n"
            score_Str = ",".join(np.array(score, dtype='str')) + "\n"
            epochs_Str = str(epochs) + "\n"
            strLines = acc_Str + val_acc_Str + loss_Str + val_loss_Str + score_Str + epochs_Str
            dirName = os.path.dirname(historyPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            with open(file=historyPath, mode="w", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                f.writelines(strLines)

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # =========================================================
    # Historyの読み込み
    # =========================================================
    def loadHistory(self, historyPath):
        try:
            self.HISTORY.initialize()  # ヒストリー初期化
            history = self.HISTORY.history  # history辞書転写
            with open(file=historyPath, mode="r", encoding="utf-8") as file:  # "utf-8"でファイルをオープン
                acc_Str = "".join(file.readline().splitlines()).split(",")  # accストリング配列を読み込む
                val_acc_Str = "".join(file.readline().splitlines()).split(",")  # val_accストリング配列を読み込む
                loss_Str = "".join(file.readline().splitlines()).split(",")  # lossストリング配列を読み込む
                val_loss_Str = "".join(file.readline().splitlines()).split(",")  # VALロスストリング配列を読み込む
                score_Str = "".join(file.readline().splitlines()).split(",")  # スコアストリング配列を読み込む
                epochs_Str = file.readline().splitlines()  # epochsストリングを読み込む
                learnType_Str = file.readline().splitlines()  # learnTypeストリングを読み込む
            acc = [float(s) for s in acc_Str]  # acc配列を作成
            val_acc = [float(s) for s in val_acc_Str]  # val_acc配列を作成
            loss = [float(s) for s in loss_Str]  # loss配列を作成
            val_loss = [float(s) for s in val_loss_Str]  # VALロス配列を作成
            score = [float(s) for s in score_Str]  # スコア配列を作成
            epochs = int(epochs_Str[0])  # エポックスを作成
            learnType = learnType_Str[0]  # learnTypeを作成
            history['acc'] = acc  # acc配列をヒストリーにセット
            history['val_acc'] = val_acc  # val_acc配列をヒストリーにセット
            history['loss'] = loss  # loss配列をヒストリーにセット
            history['val_loss'] = val_loss  # val_loss配列をヒストリーにセット
            history['score'] = score  # score配列をヒストリーにセット
            history['epochs'] = epochs  # epochs配列をヒストリーにセット
            history['learnType'] = learnType  # learnType配列をヒストリーにセット
            return history  # ヒストリーを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   モデルの保存
    # ---------------------------------------------------------------------------------------------------
    def saveModel(self, SRC_MODEL, p=None):
        try:
            # モデルの保存
            dirName = os.path.dirname(self.learnModelPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            with open(self.learnModelPath, "w", encoding="utf-8") as file:  # "utf-8"でファイルをオープン
                file.write(SRC_MODEL.MODEL.to_json())  # モデルを保存
            SRC_MODEL.MODEL.save_weights(self.learnWeightPath)  # モデルの係数を保存
            self.saveHistory(SRC_MODEL)  # HISTORYの保存
            self.emit(p)  # 進捗バーに進捗を送る

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス　SaveDataClass
# =======================================================================================================
class SaveDataClass(SaveBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            SaveBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.MINMAX_DATA = MinmaxClass(TABLE_NAME)  # MINMAX_DATA生成
            self.SOURCE_DATA = TrainClass(TABLE_NAME)  # SOURCE_DATA生成
            self.TRAIN_DATA = TrainClass(TABLE_NAME)  # TRAIN_DATA生成
            self.TEST_DATA = TrainClass(TABLE_NAME)  # TEST_DATA生成

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習ターゲットパス
    # ---------------------------------------------------------------------------------------------------
    @property
    def targetPath(self):  # ターゲットパス
        tgtDir = GP.UPLOADDIR + self.DBSDIR + "/" + self.SOURCE + "/" + self.UNIT_NAME + "/"  # ターゲットディレクトリ作成
        strPath = tgtDir + self.TABLE_NAME + ".log"  # ターゲットパス作成
        return strPath  # ターゲットパスを返す

    @property
    def dockerPath(self):  # dockerパス
        tgtDir = "/Uploads/"  # ターゲットディレクトリ作成
        strPath = tgtDir + "learndata.log"  # ターゲットパス作成
        return strPath  # ターゲットパスを返す
        return None

    # ---------------------------------------------------------------------------------------------------
    #   保存データをDBから読み込む
    # ---------------------------------------------------------------------------------------------------
    def loadData(self, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            strPath = self.dockerPath
            self.flatBase = self.loadFromCsvFile(self, strPath, p)  # ファイルからフラットなリストをロード
            if self.flatBase is not None:  # ベースリストが有る時
                MINVAL = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.MIN][0]  # ベースリストから最小値を取得
                MAXVAL = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.MAX][0]  # ベースリストから最大値を取得
                self.MINMAX_DATA.makeBase(MINVAL, MAXVAL)  # MINMAX_DATAフラットベース作成
                flatBase = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.TRAIN]  # ベースリストから訓練データを取得
                self.TRAIN_DATA.flatBase = flatBase  # 訓練データのフラットベースををセット
                flatBase = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.TEST]  # ベースリストから評価データを取得
                self.TEST_DATA.flatBase = flatBase  # 評価データのフラットベースををセット
                flatBase = self.flatBase[
                    (self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.TRAIN) |  # ベースリストからソースデータを取得
                    (self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.TEST)]  # ベースリストからソースデータを取得
                self.SOURCE_DATA.flatBase = flatBase  # ソースデータのフラットベースををセット
                self.TRAIN_DATA.setTrainData(GP.CURPARTS.LABEL_LIST.NO_LIST)  # 訓練データをセットする
                self.TEST_DATA.setTrainData(GP.CURPARTS.LABEL_LIST.NO_LIST)  # 訓練データをセットする
                return self.returnResult(True, p)  # 実行時間を表示してからデータを返す
            return self.returnResult(None, p)  # Noneを表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してから(None,None)を返す

    # ---------------------------------------------------------------------------------------------------
    #   メモリーの解放
    # ---------------------------------------------------------------------------------------------------
    def initialize(self, p=None):
        try:
            self.startNewLevel(4, p)  # 新しいレベルの進捗開始
            self.releaseBase()  # SAVE_DATA削除
            self.MINMAX_DATA.releaseBase(p)  # メモリーの解放
            self.SOURCE_DATA.releaseBase(p)  # メモリーの解放
            self.TRAIN_DATA.releaseBase(p)  # メモリーの解放
            self.TEST_DATA.releaseBase(p)  # メモリーの解放
            gc.collect()  # メモリーを解放する
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

# =======================================================================================================
#   クラス　MinmaxClass
# =======================================================================================================
class MinmaxClass(GpiBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            GpiBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.flatBase = None  # フラットベースを初期化
            self.MINVAL = None  # 最小値を初期化
            self.MAXVAL = None  # 最大値を初期化

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   フラットベース作成
    # ---------------------------------------------------------------------------------------------------
    def makeBase(self, minVal, maxVal):
        try:
            minVal[self.TRAIN_TYPE] = GP.TRAIN_TYPE.MIN
            maxVal[self.TRAIN_TYPE] = GP.TRAIN_TYPE.MAX
            self.MINVAL = minVal  # ラベル毎の最小値をセット
            self.MAXVAL = maxVal  # ラベル毎の最大値をセット
            self.flatBase = np.concatenate([[minVal], [maxVal]])  # 最小値配列と最大値配列を結合

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ベース変数を削除してメモリーを解放する
    # ---------------------------------------------------------------------------------------------------
    def releaseBase(self, p=None):
        try:
            if self.flatBase is not None:  # フラットベースが有る時
                del self.flatBase  # メモリーの解放
                self.flatBase = None  # フラットベースを初期化する
            if self.MINVAL is not None:  # MINVAL有る時
                del self.MINVAL  # メモリーの解放
                self.MINVAL = None  # 最小値を初期化
            if self.MAXVAL is not None:  # MAXVAL有る時
                del self.MAXVAL  # メモリーの解放
                self.MAXVAL = None  # 最大値を初期化
            gc.collect()  # メモリーを解放する
            self.emit(p)  # 進捗を進める

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示


# =======================================================================================================
#   クラス　TrainClass
# =======================================================================================================
class TrainClass(GpiBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            GpiBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.flatBase = None  # ベースリストの初期化
            self.trainX = None  # 訓練Xデータ初期化
            self.trainY = None  # 訓練Yデータ初期化

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ベース変数を削除してメモリーを解放する
    # ---------------------------------------------------------------------------------------------------
    def releaseBase(self, p=None):
        try:
            if self.flatBase is not None:  # フラットベースが有る時
                del self.flatBase  # フラットベースを削除
                self.flatBase = None  # フラットベースを初期化する
            if self.trainX is not None:  # 訓練Xデータが有る時
                del self.trainX  # 訓練Xデータのメモリーを解放する
                self.trainX = None  # 訓練Xデータを初期化する
            if self.trainY is not None:  # 訓練Yデータが有る時
                del self.trainY  # 訓練Yデータのメモリーを解放する
                self.trainY = None  # 訓練Yデータを初期化する
            gc.collect()  # メモリーを解放する
            self.emit(p)  # 進捗を進める

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   trainXを抽出してtrainYにkeras形式のラベルをセットする
    # ---------------------------------------------------------------------------------------------------
    def setTrainData(self, labelNoList):
        try:
            if self.flatBase is not None and len(self.flatBase) > 0:  # フラットベースが有る時
                train = self.flatBase  # 訓練
                self.trainX = np.array(train[:, GP.X_LIST.X_BASE:],'float')  # 訓練Xデータをセットする
                n_label = len(labelNoList)  # ラベル数
                if train is None:  # trainが無いとき
                    keras_y = np.array([], dtype='O').reshape((0, n_label))  # 空のkeras形式のラベルをセット
                else:  # trainが有る時
                    if len(train) == 0:  # trainが無いとき
                        keras_y = np.array([], dtype='O').reshape((0, n_label))  # 空のkeras形式のラベルをセット
                    else:  # trainが有るとき
                        labelNo = [labelNoList[label] for label in train[:, self.LABEL]]  # ラベル番号を取得
                        keras_y = np.array(to_categorical(labelNo, n_label), dtype='int')  # ラベル番号をKERASの形式に変換
#                        keras_y = [list(np.eye(1, n_label,labelNoList[label]).reshape(-1)) for label in train[:, self.LABEL]]  # ラベル番号を取得
#                        keras_y = np.array(keras_y, 'int')
                self.trainY = keras_y  # keras形式のラベルをtrainYにセットする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   訓練データタイプセット
    # ---------------------------------------------------------------------------------------------------
    def setTrainType(self, trainType):
        try:
            if self.flatBase is not None:  # フラットベースが有る時
                self.flatBase[:, self.TRAIN_TYPE] = trainType  # 訓練データタイプセット

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   保存データをDBから読み込む
    # ---------------------------------------------------------------------------------------------------
    def loadData(self, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            self.flatBase = GP.SVR.DBSServer.getLocFlatList(self, p)  # DBからフラットなリストをロード
            return self.returnResult(self.flatBase is not None, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してから(None,None)を返す

