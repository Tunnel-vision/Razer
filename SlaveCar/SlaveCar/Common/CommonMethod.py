from snownlp import SnowNLP

#情感极性的变化范围是[-1, 1]，-1代表完全负面，1代表完全正面
def divideWords(text):
    blob = SnowNLP(text)
    return blob.sentences
