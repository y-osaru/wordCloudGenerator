from wordcloud import WordCloud
import MeCab
import glob
import os
from datetime import datetime as dt

def loadInputFilePaths():
  """
  inputにあるtxtファイルの一覧取得
  """
  inputFilePaths = glob.glob("input/*.txt")
  return inputFilePaths

def loadTextFromFile(inputFilePath):
  """
  inputファイルの中身を読み込み
  """
  data = open(inputFilePath,"rb").read()
  text = data.decode("utf-8")

  return text

def createOutputFilePath(inputFilePath):
  """
  出力ファイルパス作成
  """
  inputFileName = os.path.basename(inputFilePath)
  outputFileName = inputFileName.split(".")[0] + "_" + dt.now().strftime("%Y%m%d") + ".png"
  outputFilePath = "output/" + outputFileName

  return outputFilePath

def analyzeMorphological(text):
  """
  形態素解析実行
  """
  mecab = MeCab.Tagger()
  node = mecab.parseToNode(text)

  resultWords = []

  while node:
    #単語
    word = node.surface
    #品詞
    parts = node.feature.split(",")[0]
    if parts in ["動詞","副詞","形容詞","名詞","形状詞"]:
      resultWords.append(word)
    node = node.next
  
  return resultWords

def generateWordCloud(resultWords,outputFilePath):
  """
  ワードクラウド作成
  """
  #スペース区切りで1行
  words = " ".join(resultWords)
  wc = WordCloud(background_color="white",font_path="font/YuGothM.ttc",width=400,height=300)
  wc.generate(words)

  wc.to_file(outputFilePath)

def main():
  #対象ファイル抽出
  inputFilePaths = loadInputFilePaths()

  for inputFilePath in inputFilePaths:
    #テキスト読み込み
    text = loadTextFromFile(inputFilePath)
    #形態素解析
    resultWords = analyzeMorphological(text)
    #ワードクラウド作成
    generateWordCloud(resultWords,createOutputFilePath(inputFilePath))

if __name__ == "__main__":
  main()