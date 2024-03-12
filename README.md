# もくじ  
1. 概要  
2. 動作環境  
3. 操作方法
4. 初期設定
5. プログラムの仕組み
6. 今後の展望


# 概要  
GoogleAPIを使用し、epubの本文を英語に翻訳するプログラムです 
DeepLのAPIを使用する関数も含まれています
英語以外にも多数の言語に対応しています  
APIはGoogle,DeepLともに有料で、現在はDGIが支払う扱いになっています  
プロジェクトとして本格始動した場合、どのプロジェクト扱いになるか再度決定して稟議を通す必要があります  


# 動作環境
Windows 10  
python 3.11  
Googleサービスアカウント  google-ocr-auto@digital-publishing-386907.iam.gserviceaccount.com  
  
  
# 操作方法  
## 1. venvの起動  
コマンドラインでの操作  
`venv\Scripts\Activate`

## 2. pythonの実行
コマンドラインでの操作
`python AITranslation.py`

## 3. epubの指定  
コマンドラインでの操作  
`input the path:(翻訳したいepubの絶対パス)`  

## 4. 出力
カレントディレクトリにepubの本文が英語に翻訳されたxhtmlが出てきます

## 5. 統合
手動で操作
xhtmlを統合し、翻訳されたepubを作ります


# 初期設定
## 1. venvの作成
コマンドラインでの操作  
`python -m venv venv`  

## 2. venvの起動  
コマンドラインでの操作  
`venv\Scripts\Activate`  

## 3. ライブラリのインストール
コマンドラインでの操作
`pip install -r requirements.txt`

## 4. Googleサービスアカウントの設定（このスクリプトで使用するアカウントは設定済み）
ブラウザで操作  
1. Google Cloudコンソールにアクセスhttps://console.cloud.google.com/  
2. プロジェクトを作成  
3. 作成したプロジェクトを選択しAPIとサービス→認証情報を選択  
4. メニューの一番下にある「サービスアカウントの管理」を選択  
5. 「サービスアカウントの新規作成」をクリック  
6. 名前を入力
7. ロールを選択→編集者
8. 続行をクリック
9. APIの認証情報の画面に戻るので、入力したサービスアカウントが「有効」になっていることを確認する  
10. 有効になっているサービスアカウントのメールアドレスをクリックする  
11. 「キー」のタブを開き、「鍵を追加」をクリックする  
12. 「秘密鍵を作成」のタブが開くので、「JSON」を選択  
13. JSONがダウンロードされるので、IZUMI_4_1の`service_account.Credentials.from_service_account_info`でダウンロードされたJSONを読み込めるようにする
>このスクリプトではcredential.jsonがサービスアカウントの情報を保持しpythonに読み込ませています


# プログラムの仕組み
## 1. epubを読み込む
ebooklibによって指定されたパスのepubを読み込み、内部にあるxhtmlを取得します  
xhtmlをBeautifulSoupで読み込み、本文の内容とタグを取得します  

## 2. APIで翻訳  
GoogleAPIまたはDeepLAPIに通し、取得した本文を翻訳します

## 3. 出力
本文の翻訳内容を元のタグに戻し、xhtmlの形で出力します  

  
# 今後の展望
## 1. コマンドラインでの入力を可能にする
現状のinputでパスを入力する形だとbat化できないので、コマンドラインでepubのパスを入力できるようにします  

## 2. 出力をepubにする
xhtmlを統合する労力がかなりかかるので、ebooklibで自動化してepubが出力されるようにします

## 3. 翻訳APIの模索
現在はGoogleAPIとDeepLAPIを使えるようにしています  
ただし、以前佐藤サラ圭さんにネイティブチェックをしていただいたところ、不自然さがあると指摘を受けました  
最適で自然な翻訳ができるAPIを模索する余地があります
