from create_dataset.main.pipeline import TranslationPipeline
from create_dataset.main.document_store import ElasticsearchDocumentStore

if __name__ == "__main__":
    index = 'test_es2'
    # create a document store
    document_store = ElasticsearchDocumentStore(index=index, create_index=False)
    # initialize a pipeline
    pipeline = TranslationPipeline(document_store=document_store)
    # start pipeline for ingestion
    pipeline.start_pipeline()
    # read final document store
    data = pipeline.read_document_store(print_val=False)