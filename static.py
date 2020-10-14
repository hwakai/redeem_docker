import platform
import datetime
import numpy as np
import inspect
import math

# ---------------------------------------------------------------------------------------------------
#   グロバル変数
# ---------------------------------------------------------------------------------------------------
REDEEM = "redeem"


# ---------------------------------------------------------------------------------------------------
#   コンケート用の初期 NUMPY 配列を返す
# ---------------------------------------------------------------------------------------------------
def emptyList(fields):
    concatList = np.array([], dtype='O').reshape((0, fields))  # オブジェクトタイプの空NUMPY配列を作成
    return concatList  # コンケート用の初期 NUMPY 配列を返す


# ---------------------------------------------------------------------------------------------------
#   オブジェクトが存在するか否かを返す
# ---------------------------------------------------------------------------------------------------
def exist(object):
    if object is not None:
        return True
    else:
        return False


# ---------------------------------------------------------------------------------------------------
#   クラス名を返す
# ---------------------------------------------------------------------------------------------------
def getClassName(object):
    try:
        return object.__class__.__name__  # クラス名を返す

    except Exception as e:  # 例外
        printError(e)  # エラー表示
        return None  # Noneを返す


# ---------------------------------------------------------------------------------------------------
#   プログレスウインドウのstartNewLevelを呼ぶ
# ---------------------------------------------------------------------------------------------------
def startNewLevel(levels, p=None):
    if p is not None:
        curframe = inspect.currentframe()  # カレントのフレーム取得
        calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
        functionName = calframe[1][3]  # 呼び出し元の関数名
        text = functionName + " "  # テキストに関数名セット
        text += "しばらくお待ちください。"  # テキストにコメント追加
        p.startNewLevel(levels, text)  # プログレスウインドウのstartNewLevelを呼ぶ


# ---------------------------------------------------------------------------------------------------
#   プログレスウインドウのemitを呼ぶ
# ---------------------------------------------------------------------------------------------------
def emit(p, n=1):
    if p is not None:
        p.emit(n)


# ---------------------------------------------------------------------------------------------------
#   プログレスウインドウのendLevelを呼ぶ
# ---------------------------------------------------------------------------------------------------
def endLevel(p):
    if p is not None:
        p.endLevel()

# ---------------------------------------------------------------------------------------------------
#         エラー表示
# ---------------------------------------------------------------------------------------------------
def printError(e):
    curframe = inspect.currentframe()  # カレントのフレーム取得
    calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
    title = calframe[1][3]  # 呼び出し元の関数名
    print("Exception", e.args)  # 例外を表示
    print(title + " Error")  # タイトルを表示
    return

# =======================================================================================================
#   クラス　trainデータとxデータとラベルをKERASの形式に変換したもののパッククラス
# =======================================================================================================
class LabelBaseClass():
    def __init__(self):  # 初期化
        pass

    # ---------------------------------------------------------------------------------------------------
    #   property
    # ---------------------------------------------------------------------------------------------------
    @property
    def length(self):  # データ長
        return len(self.LIST)  # ラベルリストの長さを返す

    # ---------------------------------------------------------------------------------------------------
    # ラベル番号リスト作成
    # ---------------------------------------------------------------------------------------------------
    def getLabelNoList(self):
        try:
            labelNoList = {}  # ラベル番号リスト初期化
            for i, LABEL in enumerate(self.LIST):  # LABEL_LISTを繰り返す
                labelNoList[LABEL] = i  # ラベル番号リストに通し番号をセット
            return labelNoList  # ラベル番号リストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

    # ---------------------------------------------------------------------------------------------------
    #   プレフィックスを付ける
    # ---------------------------------------------------------------------------------------------------
    def addPrefix(self, prefix, PEX_LIST):
        try:
            labelList = prefix + PEX_LIST  # オリジナル部品リストの頭に'R_'を付ける
            return labelList  # ラベルリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

# ---------------------------------------------------------------------------------------------------
#   SR_PARTS_EXCHANGE_TRNの部品名を変換する
# ---------------------------------------------------------------------------------------------------
class PartsNameClass():
    PARTS_NAME_MST = {}
    PARTS_NAME_MST["CH"] = "CH"
    PARTS_NAME_MST["CHG"] = "CHG"
    PARTS_NAME_MST["ENERGY CTRL."] = "ENERGY"
    PARTS_NAME_MST["FM"] = "FM"
    PARTS_NAME_MST["HG LAMP"] = "HG"
    PARTS_NAME_MST["HV CTRL."] = "HV"
    PARTS_NAME_MST["INV. CIRCUIT"] = "INV"
    PARTS_NAME_MST["Line Narrow Modu"] = "LN"
    PARTS_NAME_MST["LN"] = "LN"
    PARTS_NAME_MST["MAIN CTRL."] = "MAIN"
    PARTS_NAME_MST["MM"] = "MM"
    PARTS_NAME_MST["PPM"] = "PPM"
    #    PARTS_NAME_MST["UTILITY CTRL."] = "UTILITY"
    PARTS_NAME_MST["WAVE CTRL."] = "WAVE"
    PARTS_NAME_MST["WINDOW"] = "WINDOW"

    # ---------------------------------------------------------------------------------------------------
    #   有効部品名を取得
    # ---------------------------------------------------------------------------------------------------
    def getValidPartsName(self, name):
        try:
            if name in self.PARTS_NAME_MST:
                return self.PARTS_NAME_MST[name]
            return None

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   クラス　年齢ラベルクラス
# =======================================================================================================
class AgeLabelClass(LabelBaseClass):
    def __init__(self, maxAge, step):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.maxAge = maxAge  # 最大値
        self.step = step  # ステップ
        self.LIST = self.makeLabelList()  # ラベルリスト設定
        self.LAST_AGE = int(self.LIST[-1])  # 最終年齢
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self):
        try:
            labelList = []  # 異常交換部品リストと定期交換部品リストをアペンド
            for i in range(0, self.maxAge, self.step):  # 0からmaxValueまで実行
                labelList += [str(i)]  # ストリング化し追加
            labelList = np.array(labelList)  # numpy配列化
            return labelList  # ラベルリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

    # ---------------------------------------------------------------------------------------------------
    #   ラベルカラーリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeColorList(self):
        try:
            colorList = []
            n = len(self.LIST)
            greenAge = str(int(40 / self.step) * self.step)
            green = self.NO_LIST[greenAge]
            yellowAge = str(int(70 / self.step) * self.step)
            yellow = self.NO_LIST[yellowAge]
            redAge = self.LIST[-1]
            red = self.NO_LIST[redAge]
            for i, LABEL in enumerate(self.LIST):  # LISTを繰り返す
                if i <= green:  # 40以下の時は緑色
                    r = (i / green) * 0.5
                    g = 1.0
                    b = (i / green) * 0.5
                elif i <= yellow:  # 70以下の時は黄色
                    r = 0.95
                    g = 0.95
                    b = ((yellow - i) / (yellow - green)) * 0.8
                elif i <= red:  # 100以下の時は赤色
                    r = 1.0
                    g = ((red - i) / (red - yellow)) * 0.9
                    b = ((red - i) / (red - yellow)) * 0.9
                else:
                    r = (n - 1 - i) / (n - red)  # 100超の時は濃赤色
                    g = 0.0
                    b = 0.0
                colorList.append([r, g, b])  # カラーリストに追加
            return colorList  # カラーリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

# =======================================================================================================
#   クラス　trainデータとxデータとラベルをKERASの形式に変換したもののパッククラス
# =======================================================================================================
class X_LabelClass(LabelBaseClass):
    def __init__(self, UPLOADDIR):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.UPLOADDIR = UPLOADDIR  # 保存ディレクトリ
        self.LIST = self.makeLabelList("WL_ERROR")  # TRAINデータ内のXデータ開始番号とリストをセット
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self, COLUMN_NAME):
        try:
            TABLE_NAME = "COMB_TRAIN"  # 取り出すDescription
            strPath = self.UPLOADDIR + "/combDesc.log"  # Description File Pass
            # データの読み込み
            with open(file=strPath, encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                colName = []  # コラム名を初期化
                for strLine in f:  # ファイルをすべて行単位で読み込む
                    strLine = "".join(strLine.splitlines())  # 改行を削除
                    arrLine = strLine.split("\t")  # strLineをタブで区切りarrLineに格納
                    if arrLine[0] == TABLE_NAME:  # テーブル名と一致するとき
                        colName.append(arrLine[1])  # コラム名リストにアペンド
                colName = np.array(colName)  # コラム名をnumpy配列化
                index = np.where(colName == COLUMN_NAME)[0]  # ターゲットに対する相対ショット割合のインデックス取得
                self.X_BASE = None  # Xデータ開始番号を初期化
                if len(index) > 0:  # インデックスが有る時
                    self.X_BASE = index[0]  # Xデータ開始番号をセット
                    colName = colName[self.X_BASE:]  # Xデータを抽出
                    return np.array(colName)  # コラム名リストをnumpy配列にして返す
                return None  # Noneを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

# -------------------------------------------------------------------------------------------------------
#   学習ビューログクラス
# -------------------------------------------------------------------------------------------------------
class LearnViewLogClass():
    directory = "learnView/"  # ディレクトリ
    AGE_LEARN = directory + "ageLearn.log"  # 年齢学習
    EVT_LEARN = directory + "evtLearn.log"  # イベント学習
    Y_FLAG = directory + "Y_FLAG.log"  # Y_FLAG選択タブ

# -------------------------------------------------------------------------------------------------------
#   学習単位クラス
# -------------------------------------------------------------------------------------------------------
class LearnUnitClass():
    TYPE_CODE = "typeCode"  # タイプコード
    TYPE_ID = "typeId"  # レーザータイプID
    LASER_ID = "laserId"  # レーザーID

# -------------------------------------------------------------------------------------------------------
#   年齢基準クラス
# -------------------------------------------------------------------------------------------------------
class AgeBaseClass():
    MAX = "MAX"  # 最大値
    TARGET = "TARGET"  # ターゲット


# -------------------------------------------------------------------------------------------------------
#   訓練データクラス
# -------------------------------------------------------------------------------------------------------
class TrainTypeClass():
    MIN = 0  # MINタイプMIN
    MAX = 1  # MAXタイプ
    TRAIN = 2  # TRAINタイプ
    TEST = 3  # TESTタイプ
    MERGE = 4  # MERGEタイプ


# -------------------------------------------------------------------------------------------------------
#   ツリータイプクラス
# -------------------------------------------------------------------------------------------------------
class TreeTypeClass():
    MASTER = "MASTER"  # マスター
    SLAVE = "SLAVE"  # スレーブ


    # ---------------------------------------------------------------------------------------------------
    #   書き込みサーバー名リストを返す
    # ---------------------------------------------------------------------------------------------------
    def dstList(self):
        try:
            nameList = []  # サーバー名リスト初期化
            for name in self.nameList:  # サーバー名リストをすべて実行
                if (name == self.LOC_RDM_DBS or  # サーバー名がLOC_RDM_DBSの時
                        name == self.DMY_RDM_DBS or  # サーバー名がDMY_RDM_DBSの時
                        name == self.FDR_RDM_DBS or  # サーバー名がFDR_RDM_DBSの時
                        name == self.FDR_RDM_SSH):  # サーバー名がFDR_RDM_DBSの時
                    nameList += [name]  # サーバー名リストに加える
            return nameList

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

# -------------------------------------------------------------------------------------------------------
#  スーパークラス　ベース設定クラス
# -------------------------------------------------------------------------------------------------------
class BaseConfClass():
    def __init__(self):  # 初期化
        try:
            self.BASE = {}  # ベース辞書
            self.tableNameList = []  # テーブル名リスト
            self.DESC_NAME = {}  # テーブル定義名辞書初期化
            self.DESC_FILE_NAME = {}  # テーブル定義ファイル名辞書初期化
            self.DATE_FIELD = {}  # 日付フィールド辞書初期化
            self.FILE_BLOCK = {}  # ファイルブロック長初期化
            self.LASER_BLOCK = {}  # レーザーブロック長初期化

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   辞書を作成
    # ---------------------------------------------------------------------------------------------------
    def makeDictionalys(self):
        try:
            for name in self.tableNameList:  # テーブル名リストをすべて実行
                self.DESC_NAME[name] = self.BASE[name][2]  # テーブル定義名を追加
                self.DESC_FILE_NAME[name] = self.BASE[name][3]  # テーブル定義ファイル名を追加
                self.DATE_FIELD[name] = self.BASE[name][4]  # 日付フィールドを追加
                self.FILE_BLOCK[name] = self.BASE[name][5]  # ファイルブロック長を追加
                self.LASER_BLOCK[name] = self.BASE[name][6]  # レーザーブロック長を追加
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

# -------------------------------------------------------------------------------------------------------
#   ラベルクラス
# -------------------------------------------------------------------------------------------------------
class LabelClass():
    def __init__(self, parts):  # 初期化
        self.ORG = parts  # オリジナル部品名
        self.REG = 'R_' + parts  # 定期交換
        self.ACC = 'A_' + parts  # 異常交換
        self.PDG = 'P_' + parts  # 稼働中

# -------------------------------------------------------------------------------------------------------
#   学習テーブル設定クラス
# -------------------------------------------------------------------------------------------------------
class LearnConfClass(BaseConfClass):
    def __init__(self, parts, learnType):  # 初期化
        try:
            BaseConfClass.__init__(self)  # スーパークラス初期化
            for i in range(6):
                exec("LTYPE" + str(i) + " = '" + parts + '_' + learnType + str(i) + "'")

            # オブジェクトのインスタンス変数のセットとテーブル名リスト作成
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'parts') and
                             (name != 'i') and
                             (name != 'learnType') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            self.tableNameList = []  # テーブル名リスト
            self.objectList = []  # オブジェクトリスト初期化
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                exec("self.objectList += [self." + objectName + "]")  # オブジェクトリストに追加
                exec("self.tableNameList += [self." + objectName + "]")  # オブジェクトをテーブル名リストに追加

            # ベース辞書作成
            DBSDIR = REDEEM  # DBディレクトリ名
            DESC = "combDesc.log"  # テーブル定義ファイル名
            # SaveDataClass
            for object in self.objectList:
                self.BASE[object] = [DBSDIR, object, "COMB_TRAIN", DESC, "HAPPEN_SHOT", 10000, 20]  # LTYPE0
            self.makeDictionalys()  # 辞書作成

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   学習コンテナクラス
# -------------------------------------------------------------------------------------------------------
class LearnContainerClass():
    def __init__(self, parts, learnType):  # 初期化
        try:
            self.LEARN_CLASS = None  # 学習クラス
            self.MODEL_COMB = None  # MODEL_COMB
            self.LEARN_CONF = LearnConfClass(parts, learnType)  # 学習テーブル設定クラス
            self.length = len(self.LEARN_CONF.nameList)  # モデルコンボ数
            self.MODEL_COMB_LIST = [None] * self.length  # MODEL_COMB_LIST
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

# -------------------------------------------------------------------------------------------------------
#   部品クラス
# -------------------------------------------------------------------------------------------------------
class PartsClass():
    def __init__(self):  # 初期化
        try:
            CH = 'CH'  # チャンバー
            # オブジェクトのインスタンス変数のセット
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

# -------------------------------------------------------------------------------------------------------
#   学習部品コンテナクラス
# -------------------------------------------------------------------------------------------------------
class PartsContainerClass():
    def __init__(self, parts):  # 初期化
        try:
            self.PARTS = parts  # 学習部品クラス
            self.LABEL = LabelClass(parts)  # ラベルクラス
            self.AGE = LearnContainerClass(parts, "AGE")  # AGEコンテナー
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

# -------------------------------------------------------------------------------------------------------
#   グローバル変数
# -------------------------------------------------------------------------------------------------------
class GP():
    if platform.system() == "Windows":
        CRLF = "\r\n" # windows
        SEP_CRLF = "'\\r\\n'" # windows
        UPLOADDIR = "/Uploads/"  # 保存ディレクトリ
    elif platform.system() == "Darwin":
        CRLF = "\n" # macOS
        SEP_CRLF = "'\\n'" # macOS
        UPLOADDIR = "/Uploads/"  # 保存ディレクトリ
    else:
        CRLF = "\n" # unix
        SEP_CRLF = "'\\n'"  # unix
        UPLOADDIR = "/Uploads/"  # 保存ディレクトリ
    MAX_AGE = 100  # CH年齢学習最大値
    AGE_STEP = 5  # 年齢学習ステップ

    PARTS = PartsClass()  # 部品クラス
    CH = PartsContainerClass(PARTS.CH)  # CHコンテナクラス

    LEARN_LOG = LearnViewLogClass()  # 学習ビューログクラス
    AGE_BASE = AgeBaseClass()  # 年齢基準クラス
    AGE_LIST = AgeLabelClass(MAX_AGE, AGE_STEP)  # 年齢学習ラベルリスト設定
    X_LIST = X_LabelClass(UPLOADDIR)  # Xデータラベルリスト設定
    LEARN_UNIT = LearnUnitClass()  # 学習単位
    TRAIN_TYPE = TrainTypeClass()  # 訓練データタイプ
    PARTS_NAME = PartsNameClass()

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self):  # 初期化
        pass


