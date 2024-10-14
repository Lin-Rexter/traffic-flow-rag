import os
from pathlib import Path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Document,
    StorageContext,
    Settings,
)
from llama_index.core.node_parser import SentenceSplitter

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# from llama_index.embeddings.voyageai import VoyageEmbedding
# from llama_index.postprocessor.voyageai_rerank import VoyageAIRerank
import textwrap
from traffic_flow_rag.modules import prompts, llm, data_vector
from dotenv import load_dotenv

load_dotenv()


def setup_rag():
    # 載入資料集
    data_folder = Path(__file__).parents[2].joinpath("data")

    # 設置嵌入模型
    """
    Settings.embed_model = VoyageEmbedding(
        model_name="voyage-multilingual-2",
        voyage_api_key=os.environ.get("VOYAGE_API_KEY"),
        embed_batch_size=100
    )
    """
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-m3", embed_batch_size=100
    )

    # 建立語言模型(使用Llama 3.2 3B)
    Settings.llm = llm.Ollama_llm()

    Settings.text_splitter = SentenceSplitter(chunk_size=1024)
    Settings.chunk_size = 512
    Settings.chunk_overlap = 50

    # 資料集轉換成向量資料(儲存在supabase_vector向量資料庫)
    index = data_vector.load_vector(data_location=data_folder)

    print(index)


setup_rag()
"""


# 建立向量索引引擎
query_engine = index.as_query_engine(
    refine_template=prompts.message_template()
)
return query_engine
"""
"""
global rag_engine
rag_engine = None
def rag_ask():
    response = None
    try:
        # 向量查詢
        response = rag_engine.query("請問高雄目前最塞的壅塞路段?")
        print(response)
    except Exception:
        try:
            # 初始建立RAG向量查詢
            print("初始建立RAG向量查詢中...")
            rag_engine = setup_rag()
        except Exception as e:
            response = e
    return response

rag_ask()
"""
