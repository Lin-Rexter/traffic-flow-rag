import os
import pandas as pd
from io import StringIO
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv
from dateutil import parser, relativedelta

load_dotenv()

# 建立 Supabase (資料庫) 物件
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


# 取得資料集
def get_data(table_name="Live_Data"):
    Live_info = {
        "columns": [
            "section_id",
            "level",
            "update_time",
            "update_interval",
            "travel_time",
            "travel_speed",
        ],
        "dtype": {"section_id": object, "level": object},
    }

    SectionShape_info = {
        "columns": [
            "section_id",
            "AuthorityCode",
            "SrcUpdateTime",
            "update_time",
            "InfoTime",
            "InfoDate",
            "Geometry",
        ],
        "dtype": {"section_id": object, "Geometry": object},
    }

    Section_info = {
        "columns": ["section_id", "section_name"],
        "dtype": {"section_id": object, "section_name": object},
    }

    columns_map = {
        "Live_Data": Live_info,
        "Live_Forecast_Data": Live_info,
        "SectionShape_Data": SectionShape_info,
        "Section_Data": Section_info,
    }

    # 取得所有壅塞資料並轉成CSV
    response = supabase.table(table_name).select("*").csv().execute()

    df = pd.read_csv(
        StringIO(response.data),
        sep=",",
        names=columns_map[table_name]["columns"],
        skiprows=[0],
        dtype=columns_map[table_name]["dtype"],
    )

    if table_name in ["Live_Data", "Live_Forecast_Data"]:
        df["update_time"] = df["update_time"].apply(
            lambda x: (parser.parse(x) + relativedelta.relativedelta(hours=8))
        )  # .strftime('%Y-%m-%d %H:%M:%S')

        df = df[df["update_time"].apply(lambda x: str(x) >= "2024-01-01")]

        df.sort_values(by="update_time", inplace=True)
    else:
        df.sort_values(by="section_id", inplace=True)

    return df


def download(csv_path=None):
    store_data_path = Path(__file__).parents[3].joinpath("data")
    if not store_data_path.exists():
        print("data目錄不存在，將自動創建...")
    store_data_path.mkdir(parents=True, exist_ok=True)

    # Live_Data、Live_Forecast_Data、SectionShape_Data、Section_Data
    tables_list = [
        "Live_Data",
        "Live_Forecast_Data",
        "SectionShape_Data",
        "Section_Data",
    ]
    for table in tables_list:
        print(f"\n下載 {table} 資料集中...")
        df = get_data(table_name=table)
        df.to_csv(
            store_data_path.joinpath(f"{'_'.join(table.split('_')[:-1])}.csv"),
            index=False,
        )
        print(f"{table} 資料集下載完畢")


download()
