import nest_asyncio
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Document,
    StorageContext,
    Settings,
)
from llama_index.core.bridge.pydantic import BaseModel, ConfigDict
from llama_index.llms.lmstudio import LMStudio

# from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.llms import ChatMessage
from llama_index.llms.ollama import Ollama

nest_asyncio.apply()


class Traffic(BaseModel):
    """回答高速公路名稱、壅塞狀況、相關資訊"""

    model_config = ConfigDict(protected_namespaces=())
    name: str
    congestion_info: str


def Ollama_llm(struct=False, ask=None):
    llm = Ollama(model="llama3.2")

    if struct:
        llm = llm.as_structured_llm(Traffic)

    if ask:
        response = llm.chat(messages=ask)
        return response.message.content

    return llm


def LMStudio_llm(ask):
    llm = LMStudio(
        model_name="llama-3.2-3b-instruct-q8_0-gguf",
        base_url="http://localhost:5000/v1",
        temperature=0.7,
    )
    sllm = llm.as_structured_llm(Traffic)
    response = sllm.chat(messages=ask)
    return response.message.content
