これは、Slack Bolt for Python + AWS Lambda（SAM)にて、Workflowステップを提供するカスタムアプリのサンプルです。

よければ https://kikumoto.hatenablog.com/entry/2022/11/09/081734 も参照ください。

# Slack アプリの準備

https://api.slack.com/apps にて Slack App を作成する必要がありますが、ここではその手順は割愛します。

https://api.slack.com/workflows/steps も参照ください。

なお、本サンプルで必要となる Bot Token Scopes は以下の通りです。

* chat:write
* workflow.steps:execute

# AWS Systems Manager パラメータストアへの登録

Bot Token などを AWS Systems Manager パラメータストアに設定する必要があります。

* 名前： /slackapp/bolt-workflowstep-sample/SLACK_BOT_TOKEN
    * タイプ： 安全な文字列
    * 値： 作成した Slack App の Bot User OAuth Token
* 名前： /slackapp/bolt-workflowstep-sample/SLACK_SIGNING_SECRET
    * タイプ： 安全な文字列
    * 値： 作成した Slack App の Signing Secret

# samconfig.toml の修正

samconfig.toml 内の `s3_bucket` を適宜設定します。

# ビルド＆デプロイ

sam コマンドがインストールされている前提です。

ビルド
```
sam build
```

デプロイ
```
sam deploy
```

となります。

デプロイ後、発行される URL の末尾に `/slack/events` を加えたものを Slack App の方に設定します。
エンドポイントURLについては https://slack.dev/bolt-python/ja-jp/tutorial/getting-started-http#setting-up-events を参照ください。

# ライセンス

MIT となります。LICENSE ファイルを参照ください。