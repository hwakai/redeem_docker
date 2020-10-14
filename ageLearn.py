from static import *
from classDef import AgeLearnParameterClass
from gpiBase import GpiBaseClass
from gpiBase import ProgressWindowClass
from kerasImport import *

#=======================================================================================================
#   LearnBaseClass クラス
#=======================================================================================================
class LearnBaseClass(GpiBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        GpiBaseClass.__init__(self, TABLE_NAME)                                                    # スーパークラスの初期化
        try:
            self.progress = ProgressWindowClass()                                                       # 進捗ダイアローグ生成
            self.trainX = None                                                                          # 訓練X初期化
            self.trainY = None                                                                          # 訓練Y初期化
            self.testX = None                                                                           # 評価X初期化
            self.testY = None                                                                           # 評価Y初期化
            self.stop = False                                                                          # ストップフラグ初期化

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   訓練データセット
    #---------------------------------------------------------------------------------------------------
    def setSelfData(self, SAVE_DATA):
        try:
            self.trainX = SAVE_DATA.TRAIN_DATA.trainX                                                   # 訓練X
            self.trainY = SAVE_DATA.TRAIN_DATA.trainY                                                   # 訓練Y
            self.testX = SAVE_DATA.TEST_DATA.trainX                                                     # 評価X
            self.testY = SAVE_DATA.TEST_DATA.trainY                                                     # 評価Y
            if (self.trainX is not None and
                self.trainY is not None and
                self.testX is not None and
                self.testY is not None):                                                                # データパックがすべて有る時
                return True                                                                             # 結果を返す
            self.showNone()                                                                            # None表示
            return False                                                                                # 偽を返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return False

    #---------------------------------------------------------------------------------------------------
    #   学習
    #---------------------------------------------------------------------------------------------------
    def fit(self, exeEpochs, p=None):
        try:
#            from keras import backend as K
            """
            print(K.backend())
            from keras.backend.tensorflow_backend import tf
            num_cores = 8
            num_CPU = 1
            num_GPU = 1
            config = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=num_cores,
                                    inter_op_parallelism_threads=num_cores,
                                    allow_soft_placement=True,
                                    device_count={'CPU': num_CPU,
                                                  'GPU': num_GPU}
                                    )
            session = tf.compat.v1.Session(config=config)
            K.set_session(session)
            #seed = 0
            #tf.session_with_seed(seed, disable_gpu=T, disable_parallel_cpu=F)
            """
            self.startNewLevel(exeEpochs, p)                                                            # 新しいレベルの進捗開始
            SAVE_MODEL = GP.CURPARTS.MODEL_COMB.SAVE_MODEL                                              # 保存モデルを転写
            history = SAVE_MODEL.HISTORY.history                                                        # historyの転写
            self.monitorCallBack.epoch = 0                                                              # コールバックのエポック初期化
            self.monitorCallBack.epochs = exeEpochs                                                     # コールバックのエポック数セット
            his = SAVE_MODEL.MODEL.fit(self.trainX, self.trainY,                                        # 訓練データ
                                    batch_size=self.BATCH_SIZE,                                         # ミニバッチサイズ
                                    epochs=exeEpochs,                                                   # エポック
                                    verbose=self.VERBOSE,                                               # 0:出力しない 1:プログレスバー 2:エポックごと
                                    validation_data=(self.testX, self.testY),                           # 評価データ
                                    callbacks=[self.monitorCallBack])                                   # コールバック
            history["score"] = SAVE_MODEL.SCORE                                                         # 正解率セット
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラーを表示
            pass

    #---------------------------------------------------------------------------------------------------
    # makeModelFunctional
    #---------------------------------------------------------------------------------------------------
    def makeModelFunctional(self, p=None):
        try:
            y_dim = len(GP.CURPARTS.LABEL_LIST.LIST)                                                        # 出力次元 labelList数
            nodes = y_dim                                                                               # ノード数
            x_dim = GP.X_LIST.length                                                                    # 入力次元
            dropOut = self.DROPOUT                                                                      # ドロップアウト転写
            input1 = Input(shape=(x_dim,))                                                              # 入力層
            x1 = Dense(x_dim,kernel_initializer='random_uniform')(input1)                               # Dense
#            x1 = Dense(x_dim,kernel_initializer='random_normal')(input1)                               # Dense
            x1 = BatchNormalization()(x1)                                                               # BatchNormalization
            x1 = Dropout(dropOut)(x1)                                                                   # ドロップアウト
            x1 = Activation('relu')(x1)                                                                 # Activation relu
            for i in range(int(self.HIDDEN_LAYERS)):                                                    # 隠れ層数すべて実行
#                x1 = Dense(int(nodes+x_dim))(x1)                                                       # 出力層を加える
                x1 = Dense(int(nodes))(x1)                                                              # 出力層を加える
                x1 = BatchNormalization()(x1)                                                           # BatchNormalization
                x1 = Dropout(dropOut)(x1)
                x1 = Activation('relu')(x1)                                                             # Activation relu
            output = Dense(nodes)(x1)                                                                   # 出力層を加える
            output = BatchNormalization()(output)                                                       # BatchNormalization
            output = Activation('softmax')(output)                                                      # softmax関数を加える
            model = Model(inputs=input1, outputs=output)                                                # モデル生成
            model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy'])         # モデルコンパイル

            # モデルを可視化する。
#            plot_model(model, to_file='model1.png',show_shapes = False)                                 # 概要モデルをプロット
#            plot_model(model, to_file='model2.png',show_shapes = True)                                  # 詳細モデルをプロット
            self.emit(p)                                                                                     # 進捗バーに進捗を送る
            return model                                                                                # モデルを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

#=======================================================================================================
#   クラス AgeLearnBaseClass
#=======================================================================================================
class AgeLearnBaseClass(LearnBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        try:
            LearnBaseClass.__init__(self, TABLE_NAME)                                                   # スーパークラスの初期化
            self.parameter = AgeLearnParameterClass.getInstance()                                       # パラメータをセット            self.treeWidget = GP.TREE.AGE_LEARN                                                         # ツリーウイジェット

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # エラー表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   学習
    #---------------------------------------------------------------------------------------------------
    def learn(self):
        try:
            p = self.progress                                                                           # 進捗バー
            self.parameter.setClassVar(self)
            self.startNewLevel(3, p)                                                                    # 新しいレベルの進捗開始
            CURPARTS = GP.CURPARTS                                                                      # コンテナ転写
            MODEL_COMB = CURPARTS.MODEL_COMB                                                            # モデルコンボを転写
            SAVE_MODEL = MODEL_COMB.SAVE_MODEL                                                          # 保存モデルを転写
            SAVE_DATA = MODEL_COMB.SAVE_DATA                                                            # 保存モデルを転写
            MODEL_COMB.initialize()                                                                     # モデルコンボ初期化
            if SAVE_DATA.loadData():                                                                    # 訓練データの読込
                self.setSelfData(SAVE_DATA)                                                             # 自身の訓練データをセットして結果を返す
                SAVE_MODEL.MODEL = self.makeModelFunctional()                                           # モデルの新規作成
#                SAVE_MODEL.MODEL._make_predict_function()                                                # predictを速くする
                SAVE_MODEL.HISTORY.history['epochs'] = self.INIT_EPOCHS                                 # 初期エポック結果保存用
                self.monitorCallBack = MonitorCallBack(self, p)                                         # モニターコールバック
                self.fit(self.INIT_EPOCHS, p)                                                           # 初期学習
                SAVE_MODEL.saveModel(SAVE_MODEL, p)  # モデルを保存
                MODEL_COMB.initialize()                                                                 # メモリーの解放
                self.endLevel(p)                                                                        # 現レベルの終了
                return                                                                                  # 終了
            self.showNone(p)                                                                            # None表示
            return                                                                                      # データが無かったら終了

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                        # エラー表示
            return

#=======================================================================================================
#   クラス　AgeLearnClass
#=======================================================================================================
class AgeLearnClass(AgeLearnBaseClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None                                                                                   # シングルトン初期化

    #---------------------------------------------------------------------------------------------------
    #   初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if AgeLearnClass._singleton is None:                                                        # クラス変数の_singletonの有無を確認
                AgeLearnBaseClass.__init__(self, GP.CH.AGE.LEARN_CONF.LTYPE0)                           # CH学習クラスの生成
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if AgeLearnClass._singleton is None:                                                            # クラス変数の_singletonの有無を確認
            AgeLearnClass._singleton = AgeLearnClass()                                                  # クラスを生成して_singletonにセット
        return AgeLearnClass._singleton                                                                 # _singletonを返す

#=======================================================================================================
#   クラス　モニターコールバッククラス
#=======================================================================================================
class MonitorCallBack(callbacks.Callback):
    def __init__(self, parent, p):                                                                      # 初期化
        try:
            self.parent = parent                                                                        # ペアレントをセット
            self.VERBOSE = parent.VERBOSE                                                               # VERBOSE転写
            self.p = p                                                                                  # プログレス
            self.last_loss = 10                                                                         # 直前ロス初期化
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    # epoch完了時 (進捗表示)
    #---------------------------------------------------------------------------------------------------
    def on_epoch_end(self, epoch, logs={}):
        try:
            SAVE_MODEL = GP.CURPARTS.MODEL_COMB.SAVE_MODEL                                              # SAVE_MODELを転写
            history = SAVE_MODEL.HISTORY.history                                                        # ヒストリーを転写
            # ロス
            acc = logs.get('accuracy') if logs.get('accuracy') else 0.0                                 # accuracy
            val_acc = logs.get('val_accuracy') if logs.get('val_accuracy') else 0.0                     # val_accuracy
            loss = logs.get('loss') if logs.get('loss') else 0.0                                        # loss
            val_loss = logs.get('val_loss') if logs.get('val_loss') else 0.0                            # val_loss
            history['acc']      += [acc]                                                                # acc配列をヒストリーに追加
            history['val_acc']  += [val_acc]                                                            # val_acc配列をヒストリーに追加
            history['loss']     += [loss]                                                               # loss配列をヒストリーに追加
            history['val_loss'] += [val_loss]                                                           # val_loss配列をヒストリーに追加
            SAVE_MODEL.SCORE = [val_loss, val_acc]                                                      # スコアセット
            self.epoch += 1                                                                             # エポックを加算
            if self.VERBOSE == 0:                                                                       # VRBOSEが0の時
                print(str(self.epoch) + '/' + str(self.epochs))                                         # エポック表示
            # ストップ
            """
            if loss > self.last_loss + 1.02:                                                            # ロスが前回より一定値以上の時
                self.model.stop_training = True                                                         # ストップ
                history['acc']      = history['acc'][0:-3]                                              # acc配列の最後から三つを取り除く
                history['val_acc']  = history['val_acc'][0:-3]                                          # val_acc配列の最後から三つを取り除く
                history['loss']     = history['loss'][0:-3]                                             # loss配列の最後から三つを取り除く
                history['val_loss'] = history['val_loss'][0:-3]                                         # val_loss配列の最後から三つを取り除く
                loss = history['loss'][0:-1]                                                            # 最終ロス更新
            """
            # ストップフラグによるストップ
            if self.parent.stop == True:                                                                # ストップフラグがセットされている時
                self.model.stop_training = True                                                         # ストップ
            self.last_loss = loss                                                                       # 最終ロス更新
            emit(self.p)                                                                                # 進捗バーに進捗を送る
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

#=======================================================================================================
#   StopCallBack クラス
#=======================================================================================================
class StopCallBack(callbacks.Callback):
    def __init__(self):                                                                                 # 初期化
        try:
            self.last_loss = 10
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    # epoch完了時 (進捗表示)
    def on_epoch_end(self, epoch, logs={}):
        loss = logs.get('loss') if logs.get('loss') else 0.0
        if loss > self.last_loss + 0.02:
            self.model.stop_training = True
        self.last_loss = loss
        pass

