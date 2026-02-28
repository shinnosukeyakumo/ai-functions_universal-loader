# AI Functions Invoice Import Demo

`ai_functions` を使って、形式が異なる請求データ（CSV / JSON / Excel）を統一スキーマの `pandas.DataFrame` に変換するサンプルです。

## 概要

このプロジェクトでは、`src/agent.py` の `import_invoice()` が次を行います。

- ファイル形式を判別して読み込み
- 揺れている列名を標準カラムへマッピング
- データ型を正規化
- 重複データを除去
- 事後条件（ポストコンディション）で結果を検証

最終的な出力カラムは以下の4つです。

- `product_name`
- `quantity`（整数）
- `price`（浮動小数点）
- `purchase_date`（datetime64）

## ディレクトリ構成

```text
.
├── src/
│   └── agent.py
└── data/
    ├── _create_data.py
    ├── invoice_varied.csv
    ├── invoice_jp.json
    └── invoice_excel.xlsx
```

## 必要環境

- Python 3.10 以上
- `pandas`
- `openpyxl`
- `ai_functions`

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas openpyxl ai-functions
```

## 実行方法

```bash
python src/agent.py
```

実行時に `data/_create_data.py` がデモ用データを生成し、各ファイルを `import_invoice()` で読み込んで結果を表示します。

## カスタマイズ

- 入力データの種類を増やす場合:
  `import_invoice()` の指示（docstring）に新しいルールを追加
- 検証条件を強化する場合:
  `check_invoice_dataframe()` に条件を追加
- デモデータを変更する場合:
  `data/_create_data.py` を編集
