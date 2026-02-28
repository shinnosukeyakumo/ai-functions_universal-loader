"""
標準的なプログラミング手法では実現が難しいタスクを、
Python連携のAI Functionsを使って解決する例です。

AI Functionは、未知の形式のファイルを入力として受け取り、
動的にコードを書いて実行し、DataFrameへ変換します。

生成されたDataFrameの構造は、ワークフローの後続処理と
互換性があることを保証するため、ポストコンディション（事後条件）で検証されます。
"""

from __future__ import annotations

from pathlib import Path

from pandas import DataFrame, api
from ai_functions import ai_function


def check_invoice_dataframe(df: DataFrame):
    """ポストコンディション：DataFrameの構造を検証する。"""
    # 必須カラムが含まれていることを確認
    assert {"product_name", "quantity", "price", "purchase_date"}.issubset(df.columns)

    # 各カラムのデータ型を確認
    assert api.types.is_integer_dtype(df["quantity"]), "quantity は整数型である必要があります"
    assert api.types.is_float_dtype(df["price"]), "price は浮動小数点型である必要があります"
    assert api.types.is_datetime64_any_dtype(
        df["purchase_date"]
    ), "purchase_date は datetime64 型である必要があります"

    # product_name・price・purchase_date の組み合わせが一意であることを確認
    assert (
        not df.duplicated(subset=["product_name", "price", "purchase_date"]).any()
    ), "product_name・price・purchase_date の組み合わせは一意である必要があります"


@ai_function(
    post_conditions=[check_invoice_dataframe],
    code_execution_mode="local",
    # CSV / JSON / Excel を読み込むための最低限の設定（Excelはopenpyxlが必要）
    code_executor_additional_imports=["pandas", "sqlite3", "openpyxl"],
    code_executor_kwargs={"timeout_seconds": 10},
)
def import_invoice(path: str) -> DataFrame:
    """
    `{path}` にあるファイルには、CSV・JSON・Excel（.xlsx）のいずれか形式の購入ログが含まれています。
    ファイルごとにカラム名や形式は異なる可能性があります。

    タスク:
    - ファイル形式に応じて読み込む。
    - カラム名が異なっていても、以下の正規フィールドに対応する列を特定すること：
        - product_name
        - quantity
        - price
        - purchase_date
    - 最終的に以下のカラムを持つDataFrameを返すこと：
        ['product_name','quantity','price','purchase_date']

    正規化ルール:
    - product_name: 文字列型
    - quantity: 整数型（必要に応じて型変換・クリーニングする）
    - price: 浮動小数点型（通貨記号やカンマを除去して変換する）
    - purchase_date: datetime64型（一般的な日付形式を解析する）
    - 上記4フィールドにマッピングできない行は削除する
    - (product_name, price, purchase_date) の組み合わせが重複する場合は最初の1件のみ残す
    """


def _project_root() -> Path:
    # src/agent.py → 親ディレクトリが src → さらにその親がプロジェクトルート
    return Path(__file__).resolve().parents[1]


def _data_dir() -> Path:
    # プロジェクトルート配下の data ディレクトリを返す
    return _project_root() / "data"


if __name__ == "__main__":
    import sys

    # data/_create_data.py を import できるように、プロジェクトルートを sys.path に追加
    root = _project_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from data._create_data import create_demo_files

    data_dir = _data_dir()
    data_dir.mkdir(exist_ok=True)

    # data/ 配下にデモ用データ（csv / json / xlsx）を生成
    filenames = create_demo_files(data_dir)

    # 生成したファイルを順に読み込む
    results: list[DataFrame] = []
    for filename in filenames:
        print(f"===== {filename.name} からデータを読み込み中 =====")
        df = import_invoice(str(filename))
        results.append(df)

    # 結果を表示
    for filename, df in zip(filenames, results):
        print(f"\n===== {filename.name} の解析結果 =====")
        print(df)