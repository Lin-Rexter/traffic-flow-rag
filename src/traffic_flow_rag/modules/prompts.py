from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core import ChatPromptTemplate


def message_template():
    refine_prompt_str = (
        "We have the opportunity to refine the original answer "
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{context_msg}\n"
        "------------\n"
        "Given the new context, refine the original answer to better "
        "answer the question: {query_str}. "
        "If the context isn't useful, output the original answer again.\n"
        "Original Answer: {existing_answer}"
    )

    chat_refine_msgs = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=("你是一位對台灣高速公路非常了解的專家，會回答使用者所要查詢的路段壅塞資訊及路段名稱等資訊"),
        ),
        ChatMessage(role=MessageRole.USER, content=refine_prompt_str),
    ]
    refine_template = ChatPromptTemplate(chat_refine_msgs)

    return refine_template
