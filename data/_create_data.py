import json
import os
from pathlib import Path

import pandas as pd


def create_demo_files(data_dir: str | Path) -> list[Path]:
    """
    data_dir 配下に、列名ゆれ＆中身バラバラのデータファイルを生成する。
    - CSV: 英語カラム揺れ（item_name, qty, PriceUSD, purchased_at）
    - JSON: 日本語カラム（商品名, 数量, 値段, 購入日）
    - Excel: 別名カラム（Product, Count, Amount(USD), Date）＋シート名 purchases
    """
    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok=True)

    csv_path = data_dir / "invoice_varied.csv"
    json_path = data_dir / "invoice_jp.json"
    xlsx_path = data_dir / "invoice_excel.xlsx"

    # 既存ファイル削除
    for p in [csv_path, json_path, xlsx_path]:
        if p.exists():
            os.remove(p)

    # ----------------------------
    # 1) CSV（英語揺れ + 余計な列あり）
    # ----------------------------
    csv_rows = [
        # item_name, qty, PriceUSD, purchased_at, note(余計)
        ["MCU-ESP32-DEVKIT-V2", "8", "$9.25", "2024/01/09", "promo"],
        ["LED-5MM-RED-20MA", "200", "0.10", "2024-01-06", ""],
        ["CAP-ELEC-100UF-25V", "50", "0.25", "2024-01-02", "bulk"],
    ]
    df_csv = pd.DataFrame(csv_rows, columns=["item_name", "qty", "PriceUSD", "purchased_at", "note"])
    df_csv.to_csv(csv_path, index=False)

    # ----------------------------
    # 2) JSON（日本語カラム + 金額のカンマ/通貨文字 + 余計な列あり）
    # ----------------------------
    json_data = [
        {"商品名": "SBC-RPI4-4GB-MODEL-B", "数量": "3", "値段": "45,000", "購入日": "2024-01-11", "通貨": "JPY"},
        {"商品名": "PROTO-BB-830-TIE-PT", "数量": 20, "値段": "3.50", "購入日": "2024/01/14", "メモ": "for lab"},
        {"商品名": "WIRE-JMP-MM-65PCS-KIT", "数量": "10", "値段": "¥5.25", "購入日": "2024-01-15"},
    ]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # ----------------------------
    # 3) Excel（別名カラム + 日付が混在 + 余計な列あり）
    # ----------------------------
    excel_rows = [
        # Product, Count, Amount(USD), Date, Supplier(余計)
        ["MCU-ARDUINO-UNO-R3-v2", 7, "24.00", "2024-01-05", "ACME"],
        ["TRANS-NPN-2N2222A-TO92", "150", "$0.15", "2024/01/10", "PartsCo"],
        ["RES-CF-10K-0.25W-5%", 100, "0.05", "01-01-2024", "Resistive Inc."],
    ]
    df_xlsx = pd.DataFrame(excel_rows, columns=["Product", "Count", "Amount(USD)", "Date", "Supplier"])
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df_xlsx.to_excel(writer, index=False, sheet_name="purchases")

    return [csv_path, json_path, xlsx_path]