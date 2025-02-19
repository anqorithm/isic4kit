from .base import BaseISIC4
from .search import ISICSearchMixin
from .loader import ISICLoaderMixin


class ISIC4Classifier(BaseISIC4, ISICSearchMixin, ISICLoaderMixin):
    """ISIC4 Classification handler for economic activities.

    This class combines functionality from BaseISIC4, ISICSearchMixin, and ISICLoaderMixin
    to provide a complete interface for working with ISIC Revision 4 classifications.

    Attributes:
        language (str): The language code for classification descriptions (default: "en")
        sections (list): List of loaded ISIC4 sections

    Raises:
        ValueError: If there is an error loading the ISIC4 classification data
    """

    def __init__(self, language="en"):
        """Initialize the ISIC4 classifier.

        Args:
            language (str, optional): Language code for classifications. Defaults to "en".

        Raises:
            ValueError: If there is an error loading the ISIC4 classification data
        """
        self.language = language
        self.sections = []
        try:
            self._load_data()
        except ValueError as e:
            raise
