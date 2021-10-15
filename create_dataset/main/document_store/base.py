import logging
from abc import abstractmethod, ABC
from typing import Any, Optional, Dict, List, Union
from create_dataset.main.schema import Document

logger = logging.getLogger(__name__)


class BaseDocumentStore(ABC):
    """
    Base class for implementing Document Stores.
    """
    index: Optional[str]

    @abstractmethod
    def write_documents(self, documents: Union[List[dict], List[Document]], index: Optional[str] = None):
        pass
