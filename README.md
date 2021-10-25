# # Agriculture Datasets Creation for downstream fine-tuning tasks

# Document Store for your data

Create a document store by Inheriting the Base Document class. ElasticSearch is the Document Storage of our choice. Hence, this has been implemented.

# Pipeline

Create a new pipeline for processing of your dataset. 
You need to define a process_dataset() function for your new pipleine. If required, define end_process() for any cleaning up operations or logging at the end of your ingestion pipeline.
Call pipeline.start_pipeline() for processing and ingestion to your data store.

# Read Document Store

After running your pipeline, read your document store by calling pipeline.read_document_store() to traverse through the created dataset.
