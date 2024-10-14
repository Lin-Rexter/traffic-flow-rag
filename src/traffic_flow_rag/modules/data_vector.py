from pathlib import Path
from llama_index.core import (
    KeywordTableIndex,
    VectorStoreIndex,
    StorageContext,
    SimpleDirectoryReader,
    load_index_from_storage,
)
from traffic_flow_rag.modules import supabase_vector


PERSIST_DIR = Path(__file__).parents[3].joinpath("storage")
PERSIST_DIR.mkdir(parents=True, exist_ok=True)


def load_vector(data_location):
    print(f"載入向量資料中({data_location})...")

    if PERSIST_DIR.exists():
        # 載入文件
        documents = SimpleDirectoryReader(
            input_dir=data_location,
            required_exts=[".csv"],
        ).load_data(show_progress=True)

        # storage_context = supabase_vector.SupabaseVector()

        # 建立資料索引
        index = VectorStoreIndex.from_documents(
            documents=documents, show_progress=True
        )  # storage_context=storage_context (Supabase)

        # 儲存向量資料 (本地)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # 載入儲存的向量資料 (本地)
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        # 轉為嵌入索引 (本地)
        index = load_index_from_storage(storage_context)

    return index
