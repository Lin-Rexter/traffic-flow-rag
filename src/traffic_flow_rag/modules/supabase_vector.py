from llama_index.core import StorageContext
from llama_index.vector_stores.supabase import SupabaseVectorStore


def SupabaseVector():
    vector_store = SupabaseVectorStore(
        postgres_connection_string=(
            "postgresql://postgres.lveubuukxyjsnogftcxj:0tIwhEn2AaJA00Ub@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
        ),
        collection_name="traffic",
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return storage_context
