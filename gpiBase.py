import time
import gc
from static import *
import os
import numpy as np
import csv

# =======================================================================================================
#   クラス　TableDescClass
# =======================================================================================================
class TableDescClass():
    def __init__(self):  # スーパークラスの初期化
        self.tableName = ""  # テーブル名初期化
        self.columnNr = 0  # コラム数初期化
        self.colName = []  # コラム名初期化
        self.colType = []  # コラムタイプ初期化
        self.isNullable = []  # isNullable初期化
        self.colKey = []  # コラムキー初期化
        self.colDefault = []  # コラムデフォールト初期化
        self.extra = []  # エクストラ初期化

    # ---------------------------------------------------------------------------------------------------
    #   descTableからすべてのカラムを追加する
    # ---------------------------------------------------------------------------------------------------
    def appendAllColumn(self, row):
        self.columnNr = self.columnNr + 1  # コラム数更新　
        self.tableName = row[0]  # コラム名アペンド
        self.colName.append(row[1])  # コラム名アペンド
        self.colType.append(row[2])  # コラムタイプアペンド
        self.isNullable.append(row[3])  # isNullableアペンド
        self.colKey.append(row[4])  # コラムキーアペンド
        self.colDefault.append(row[5])  # コラムデフォールトアペンド
        self.extra.append(row[6])  # エクストラアペンド

# =======================================================================================================
#   スーパークラス　GPIベースクラス
# =======================================================================================================
class GpiBaseClass():
    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, TABLE_NAME):
        try:
            self.TABLE_NAME = TABLE_NAME  # テーブル名（学習データに関しては仮設定）
            self.flatBase = None                                                                        # 事前読み込みフラットベース
            self.HISTORY = None  # 学習履歴初期化
            self.SCORE = None  # スコア初期化
            self.LOSE = None  # ロス初期化
            self.FILE_BLOCK = None  # ファイルブロック長セット
            self.LASER_BLOCK = None  # レーザーブロック長セット
            self.DESC_NAME = None  # ディスクリプション名初期化
            self.DESC_FILE_NAME = None  # ディスクリプション定義ファイル名初期化
            self.DATE_FIELD = None  # 日付フィールド初期化
            self.tableDesc = None  # テーブルデスクリプションを初期化
            self.PREFIX = ""  # テーブル名の前置句
            self.LENGTH = 0  # コラム長初期化
            if TABLE_NAME is not None and TABLE_NAME != '':  # テーブル名が有る時
                CONF_TABLE = GP.CH.AGE.LEARN_CONF  # GP.CH.PCOMB_CONFをテーブルにセット
                if CONF_TABLE is not None:  # 設定テーブルが有る時
                    self.DESC_NAME = 'COMB_TRAIN'  # ディスクリプション名セット
                    self.FILE_BLOCK = CONF_TABLE.FILE_BLOCK[TABLE_NAME]  # ファイルブロック長セット
                    if self.DESC_NAME is not None and self.DESC_NAME != '':  # ディスクリプション名が有る時
                        self.DESC_FILE_NAME = CONF_TABLE.DESC_FILE_NAME[TABLE_NAME]  # ディスクリプション定義ファイル名セット
                        if self.DESC_FILE_NAME is not None and self.DESC_FILE_NAME != '':  # ディスクリプション名が有る時
                            self.tableDesc = self.getTableDescFromDesc()  # テーブルデスクリプションをセット
                            if self.tableDesc is not None:  # テーブルデスクリプションが有る時
                                self.LENGTH = self.tableDesc.columnNr  # コラム長セット                                for field in self.tableDesc.colName:  # テーブルデスクリプションをすべて実行
                                for i, field in enumerate(self.tableDesc.colName):  # テーブルデスクリプションをすべて実行
                                    exec("self." + field + " = " + str(i))  # フィールド番号変数設定
                    self.DATE_FIELD = CONF_TABLE.DATE_FIELD[TABLE_NAME]  # 日付フィールドセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    # テーブルリストを作成してから テーブルを作成する
    # ---------------------------------------------------------------------------------------------------
    def getTableDescFromDesc(self):
        try:
            descTable = self.makeDescTableFromCsv()  # ダンプのdescTableを作成する
            if descTable is not None:
                tableDescList = self.makeTableDesc(descTable)  # テーブルデスクリプションリスト作成
                tableDesc = self.getTableDesc(tableDescList)  # テーブルデスクリプションを取得
                return tableDesc
            self.showNone()  # Noneを表示

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    # tableDesc作成
    # ---------------------------------------------------------------------------------------------------
    def makeTableDesc(self, descTable):
        try:
            rowNo = 0  # 行番号初期化
            tableNo = -1  # テーブル番号初期化
            previousName = ""  # 直前の値を初期化
            tableDescList = []  # テーブルデスクリプションリスト初期化
            for row in descTable:  # descTable内    のすべての行を実行
                if rowNo > 0:  # 行番号を確認
                    TABLE_NAME = row[0]  # TABLE_NAME
                    COLUMN_NAME = row[1]  # COLUMN_NAME
                    if TABLE_NAME != previousName:  # TABLE_NAMEと直前の値を確認
                        previousName = TABLE_NAME  # 直前の値をTABLE_NAMEに更新する
                        tableNo = tableNo + 1  # テーブル番号加算
                        td = TableDescClass()  # テーブルデスクリプション生成
                        td.appendAllColumn(row)  # テーブルデスクリプションにコラム追加
                        tableDescList.append(td)  # テーブルデスクリプションリストにテーブルデスクリプションを追加
                    else:  # TABLE_NAMEと直前の値が同じ時
                        td.appendAllColumn(row)  # テーブルデスクリプションにコラム追加
                rowNo = rowNo + 1  # 行番号加算
            return tableDescList  # テーブルデスクリプションリストを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   指定した名前のtableDescを返す
    # ---------------------------------------------------------------------------------------------------
    def getTableDesc(self, tableDescList):
        try:
            tableDesc = None  # テーブルデスクリプション初期化
            for td in tableDescList:  # テーブルデスクリプションリストをすべて実行
                if td.tableName == self.DESC_NAME:  # テーブルデスクリプションのテーブル名がデスクリプション名の時
                    td.tableName = self.TABLE_NAME  # テーブルデスクリプションのテーブル名をテーブル名にする
                    tableDesc = td  # テーブルデスクリプション転写
                    break  # ブレーク
            return tableDesc  # テーブルデスクリプションを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   descTableをCSVから作成する
    # ---------------------------------------------------------------------------------------------------
    def makeDescTableFromCsv(self):
        try:
            strPath = GP.UPLOADDIR + "/" + self.DESC_FILE_NAME  # Description File Pass
            # データの読み込み
            with open(file=strPath, encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                descTable = []  # デスクリプションテーブル初期化
                for strLine in f:  # 一行毎にファイルをすべて読み込む
                    strLine = "".join(strLine.splitlines())  # 改行を削除
                    arrLine = strLine.split("\t")  # strLineをタブで区切りarrLineに格納
                    descTable.append(arrLine)  # デスクリプションテーブルにアペンド
                return descTable  # デスクリプションテーブルを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   呼び出し元のメソッド名を返す
    # ---------------------------------------------------------------------------------------------------
    def getParentMethodName(self, p=None):
        try:
            curframe = inspect.currentframe()  # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
            method = calframe[1][3]  # 呼び出し元の関数名
            return method  # 関数名を返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   このクラス名を返す
    # ---------------------------------------------------------------------------------------------------
    def getClassName(self):
        try:
            return self.__class__.__name__  # クラス名を返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #        実行時間表示(秒)
    # ---------------------------------------------------------------------------------------------------
    def showElapsedTime(self, curframe, calframe, text, p=None):
        try:
            title = calframe[1][3]  # 呼び出し元の関数名
            if p is not None:
                endTime = time.time()  # 終了時刻取得
                elapsed = round(endTime - p.startTime[p.level], 6)  # 実行時間を計算
                print(title + text + str(p.level) + " 実行時間 = " + str(elapsed) + "秒")                 # タイトルと実行時間を表示
            else:
                print(title + text)                                                                     # タイトルと実行時間を表示

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #        実行時間表示(秒)
    # ---------------------------------------------------------------------------------------------------
    def endLevel(self, p=None):
        try:
            curframe = inspect.currentframe()  # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
            self.showElapsedTime(curframe, calframe, " END   ", p)  # 実行時間表示(秒)
            if p is not None:   p.endLevel()

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #         エラー時実行時間表示(秒)
    # ---------------------------------------------------------------------------------------------------
    def showError(self, e, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            print("Exception", e.args)                                                                  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return

        except Exception as e:                                                                          # 例外
            print(e)                                                                                    # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #         エラー表示
    # ---------------------------------------------------------------------------------------------------
    def printError(self, e):
        curframe = inspect.currentframe()  # カレントのフレーム取得
        calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
        title = calframe[1][3]  # 呼び出し元の関数名
        print("Exception", e.args)  # 例外を表示
        print(title + " ERROR")  # タイトルを表示
        return

    # ---------------------------------------------------------------------------------------------------
    #         None時実行時間表示(秒)
    # ---------------------------------------------------------------------------------------------------
    def showNone(self, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   プログレスウインドウのstartNewLevelを呼ぶ
    # ---------------------------------------------------------------------------------------------------
    def startNewLevel(self, maxCount, p=None):
        try:
            if p is not None:
                p.level += 1  # 進捗レベル更新
                p.startTime[p.level] = time.time()  # タイマー番号の開始時刻を現在の時刻にセット
                curframe = inspect.currentframe()  # カレントのフレーム取得
                calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
                title = calframe[1][3]  # 呼び出し元の関数名
                print(title + " STRAT " + str(p.level))  # タイトルを表示
                functionName = calframe[1][3]  # 呼び出し元の関数名
                className = self.getClassName()  # クラス名取得
                className = className.replace("Class", "")  # "Class"を削除
                text = className + ":"  # テキストにクラス名セット
                text += functionName + " "  # テキストに関数名追加
                try:
                    if self.TABLE_NAME is not None:  # テーブル名が有る時
                        text += self.TABLE_NAME + " "  # テキストにテーブル名追加
                except Exception as e:  # 例外
                    pass
                p.showCurrLevel(maxCount, text)  # カレントのレベルを表示

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   プログレスウインドウのemitを呼ぶ
    # ---------------------------------------------------------------------------------------------------
    def emit(self, p, n=1):
        if p is not None:
            p.emit(n)

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してからデータを返す
    #   データが無い時はNoneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnData(self, retData, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            if retData is not None:  # データが有る時
                self.showElapsedTime(curframe, calframe, " END  ", p)                                   # タイトルと実行時間を表示
                if p is not None:   p.endLevel()
                return retData                                                                          # データを返す
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None                                                                                 # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してからデータを返す
    #   データが無い時はNoneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnList(self, retData, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            if retData is not None and len(retData) > 0:                                                # データが有る時
                self.showElapsedTime(curframe, calframe, " END  ", p)                                   # タイトルと実行時間を表示
                if p is not None:   p.endLevel()
                return retData                                                                          # データを返す
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e,p)                                                                        # エラー表示
            return None                                                                                 # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してからデータを返す
    #   データが無い時はNoneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnList2(self, retData0, retData1, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            if retData0 is not None and len(retData0) > 0 and retData1 is not None:                     # データが有る時
                self.showElapsedTime(curframe, calframe, " END  ", p)                                   # タイトルと実行時間を表示
                if p is not None:   p.endLevel()
                return retData0, retData1                                                               # データを返す
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None, None                                                                           # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return None, None                                                                           # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してから結果を返す
    #   データが無い時はNoneを表示してからFalseを返す
    # ---------------------------------------------------------------------------------------------------
    def returnResult(self, result, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            if result is not None:                                                                      # データが有る時
                self.showElapsedTime(curframe, calframe, " END  ", p)                                   # タイトルと実行時間を表示
                if p is not None:   p.endLevel()
                return result                                                                           # データを返す
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return False                                                                                # 失敗を返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return False  # 失敗を返す

    # ---------------------------------------------------------------------------------------------------
    #   Noneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnNone(self, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   Noneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnNone2(self, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            self.showElapsedTime(curframe, calframe, " NONE ", p)  # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None, None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None, None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   エラーを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnError(self, e, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            print("Exception", e.args)                                                                  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   エラーを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnError2(self, e, p=None):
        try:
            curframe = inspect.currentframe()  # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
            print("Exception", e.args)                                                                  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None, None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None, None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   エラーを表示してからFalseを返す
    # ---------------------------------------------------------------------------------------------------
    def returnResultError(self, e, p=None):
        try:
            curframe = inspect.currentframe()  # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
            print("Exception", e.args)                                                                  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return False  # Falseを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return False  # Falseを返す

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してから結果を返す
    #   データが無い時はNoneを表示してからFalseを返す
    # ---------------------------------------------------------------------------------------------------
    def returnError2(self, e, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            print("Exception", e.args)  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return (None, None)  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return (None, None)  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトを削除してメモリーを解放する
    # ---------------------------------------------------------------------------------------------------
    def deleteObject(self, object):
        try:
            del object  # フラットベースを削除
            gc.collect()  # メモリーを解放する

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   ベース変数を削除してメモリーを解放する
    #---------------------------------------------------------------------------------------------------
    def releaseBase(self, p=None):
        try:
            if self.flatBase is not None:                                                               # フラットベースが有る時
                del self.flatBase                                                                       # フラットベースを削除
                self.flatBase = None                                                                    # フラットベースを初期化する

            gc.collect()                                                                                # メモリーを解放する
            self.emit(p)                                                                                     # 進捗を進める

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトの設定を使ってファイルからフラットなリストを取得。
    # ---------------------------------------------------------------------------------------------------
    def loadFromCsvFile(self, object, strPath, p=None):
        try:
            tableDesc = object.tableDesc  # テーブルデスクリプションを転写
            self.startNewLevel(tableDesc.columnNr, p)  # 新しいレベルの進捗開始
            if os.path.exists(strPath):  # DBにテーブルが有る時
                with open(file=strPath, mode="r", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                    reader = csv.reader(f, delimiter="\t", lineterminator='\n')  # CSVリーダー設定
                    flatList = [row for row in reader]  # 全て読み込む
                    flatList = np.array(flatList[1:], 'O')
                    for column in range(tableDesc.columnNr):  # コラム数をすべて実行
                        COLUMN_NAME = tableDesc.colName[column]  # コラム名を取得
                        COLUMN_TYPE = tableDesc.colType[column]  # コラムタイプを取得
                        if "int" in COLUMN_TYPE:
                            flatList[:, column] = np.array(flatList[:, column], 'int')
                        elif "float" in COLUMN_TYPE:
                            flatList[:, column] = np.array(flatList[:, column], 'float')
                        else:
                            pass
                        self.emit(p)
                return self.returnResult(flatList, p)  # 実行時間を表示してからデータを返す
            return self.returnNone(p)  # Noneを表示してからデータを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return self.returnNone(p)  # Noneを表示してからデータを返す


# =======================================================================================================
#   クラス プログレスウインドウ
# =======================================================================================================
class ProgressWindowClass(GpiBaseClass):
    def __init__(self):  # 初期化
        try:
            GpiBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.levels = 6  # レベル数
            self.startTime = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 実行時間計測用配列
            self.level = -1  # 進捗レベル初期化
            self.progressCount = [0] * self.levels  # 現レベルの進捗度初期化
            self.maxCount = [0] * self.levels  # 現レベルの最大カウント

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   カレントのレベルを表示
    # ---------------------------------------------------------------------------------------------------
    def showCurrLevel(self, maxCount, subTitle):
        try:
            self.maxCount[self.level] = maxCount + 1  # 現レベルの最大カウント
            self.progressCount[self.level] = 1  # 現レベルの進捗度初期化
            print(subTitle)

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ***************************************************************************************************
    #   イベント処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   新レベル開始シグナルイベント処理
    # ---------------------------------------------------------------------------------------------------
    def startNewLevel(self, maxCount, subText):
        try:
            self.level += 1  # 進捗レベル更新
            self.showCurrLevel(maxCount, subText)  # カレントのレベルを表示

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   現レベル終了シグナルイベント処理
    # ---------------------------------------------------------------------------------------------------
    def endLevel(self):
        try:
            if self.progressCount[self.level] != self.maxCount[self.level]:  # 進捗カウントが最大カウントに達していない時
                self.progressCount[self.level] = self.maxCount[self.level] - 1  # 進捗カウントを終了カウント－１にする
                self.emit()  # プログレスシグナル処理を呼ぶ
            if self.level == 0:  # 進捗レベルが0の時
                self.level -= 1  # 進捗レベル更新
            else:  # 進捗レベルが1以上の時
                self.level -= 1  # 進捗レベル更新
                self.emit()  # 上位レベルの進捗を進める

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   プログレスシグナルイベント処理
    # ---------------------------------------------------------------------------------------------------
    def emit(self, n=1):
        try:
            self.progressCount[self.level] += n  # 現レベルの進捗度初期化
            print(self.level)

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

