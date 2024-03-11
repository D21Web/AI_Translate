#API経由でepubのAI翻訳を行う
##必要なライブラリのインポート
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import requests
import uuid

##サービスの取得
def GetService():
    ObjService = service_account.Credentials.from_service_account_file("credential.json")
    return ObjService

##翻訳クライアントの取得
def GetTranslateClient():
    ObjService = GetService()
    ObjClient = translate.Client(credentials=ObjService)
    return ObjClient

##翻訳の実施
###Google翻訳
def TextTranslateGoogle(StrText,ObjClient = None,StrTarget = "en"):
    if isinstance(StrText,bytes):
        StrText = StrText.decode("utf-8")
    if ObjClient is None:
        ObjClient = GetTranslateClient()
    DictResult = ObjClient.translate(StrText,target_language = StrTarget)
    StrResult = DictResult["translatedText"]
    return StrResult
###DeepL翻訳
def TextTranslateDeepL(StrText,StrSource = "ja",StrTarget="en"):
    STR_API_KEY = "42bdd638-1d25-730b-8fc6-563f0b2b128f:fx"
    STR_URL_DEEPL = "https://api-free.deepl.com/v2/translate"
    DictParameters = {
        "auth_key" : STR_API_KEY,
        "text" : StrText,
        "source_lang" : StrSource,
        "target_lang" : StrTarget
    }
    ObjRequest = requests.post(STR_URL_DEEPL,data=DictParameters)
    DictResult = ObjRequest.json()
    return DictResult["translations"][0]["text"]
###Microsoft翻訳
def TextTranslateMicrosoft(StrText,StrSource = "ja",StrTarget = "en"):
    STR_SUBSCRIPTION_KEY = "0f911f3fb9e449ef8b870f5e8b796370"
    STR_URL_MICROSOFT = "https://api.cognitive.microsofttranslator.com/translate"
    STR_LOCATION = "japaneast"
    DictPatemeters = {
        "api-version":"3.0",
        "from":StrSource,
        "to":[StrTarget]
    }
    DictHeaders = {
        "Ocp-Apim-Subscription-Key" : STR_SUBSCRIPTION_KEY,
        'Ocp-Apim-Subscription-Region' : STR_LOCATION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    ListBody = [
        {
            "text" : StrText
        }
    ]
    ObjRequest = requests.post(STR_URL_MICROSOFT,params = DictPatemeters , headers= DictHeaders,json = ListBody)
    DictResult = ObjRequest.json()
    return DictResult[0]["translations"][0]["text"]
##書籍のxhtml一覧とそのソースコードの取得
def GetEpubSource(StrFilePath):
    ObjEbook = epub.read_epub(StrFilePath)
    ListXhtmlName = []
    ListContent = []
    for ObjItem in ObjEbook.get_items():
        if ObjItem.get_type() == ebooklib.ITEM_DOCUMENT:
            ListXhtmlName.append(ObjItem.file_name)
            ListContent.append(ObjItem.get_content().decode())
    return ListXhtmlName,ListContent
##htmlの翻訳すべき箇所とそうでない箇所を分ける
def SplitHtml(StrContent):
    ListHtmlSplit = []
    ListBoolTranslated = []
    StrSplitHtml = ""
    BoolTranslated = False
    BoolTranslatedBefore = False
    for StrCharCurrent in StrContent:
        BoolTranslatedBefore = BoolTranslated
        if len(StrCharCurrent) == len(StrCharCurrent.encode("utf-8")):
            BoolTranslated = False
        else:
            BoolTranslated = True
        if BoolTranslatedBefore == BoolTranslated:
            StrSplitHtml += StrCharCurrent
        else:
            ListHtmlSplit.append(StrSplitHtml)
            ListBoolTranslated.append(BoolTranslatedBefore)
            StrSplitHtml = StrCharCurrent
    if not StrSplitHtml in ListHtmlSplit:
        ListHtmlSplit.append(StrSplitHtml)
        ListBoolTranslated.append(BoolTranslated)
    return ListHtmlSplit , ListBoolTranslated

##htmlを翻訳する
def TranslateHtml(StrContent,TextTranslate,StrTarget = "en"):
    ListHtmlSplit , ListBoolTranslated = SplitHtml(StrContent)
    ListOut = []
    for IntHtmlCnt in range(len(ListHtmlSplit)):
        BoolTranslated = ListBoolTranslated[IntHtmlCnt]
        StrHtml = ListHtmlSplit[IntHtmlCnt]
        if BoolTranslated:
            StrHtml = TextTranslate(StrHtml,StrTarget = StrTarget)
        ListOut.append(StrHtml)
    return "".join(ListOut)

