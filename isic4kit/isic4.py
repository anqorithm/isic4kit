from .base import BaseISIC4
from .search import ISICSearchMixin
from .loader import ISICLoaderMixin

class ISIC4Classifier(BaseISIC4, ISICSearchMixin, ISICLoaderMixin):
    """Main class for working with ISIC4 classification data."""

    def __init__(self, language="en"):
        """Initialize ISIC4 instance.

        Args:
            language (str): Language code for ISIC descriptions. Defaults to "en".

        Raises:
            ValueError: If the specified language is not supported.
        """
        self.language = language
        self.sections = []
        try:
            self._load_data()
        except ValueError as e:
            raise
