# Job Application Tracker

就職活動の企業と応募を管理するFastAPIを用いたアプリケーション

## 起動

Python 3.13以上、uv、PostgreSQLを使用します。

1. `uv sync --locked` で依存関係をインストールします。
2. `.env.example`を`.env`にコピーし、`DATABASE_URL`に自分のPostgreSQL接続情報を設定します。
3. 空の学習用DBで `uv run alembic upgrade head` を実行します。既存DBを使う場合は先にマイグレーションの状態を確認してください。
4. `uv run uvicorn main:app --reload` で起動します。

APIドキュメント: <http://127.0.0.1:8000/docs>

## 実装範囲

- Companyの作成・一覧・削除
- Applicationの作成・一覧・更新・削除、ステータス絞り込み
- Pydanticによる入出力検証、SQLAlchemyによるDB操作
- CompanyとApplicationの1対多、外部キー、企業削除時の応募の連動削除
- Alembicによるスキーマ変更履歴
