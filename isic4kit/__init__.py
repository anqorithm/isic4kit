"""ISIC4Kit: A toolkit for ISIC 2019 skin lesion classification.

This package provides tools and utilities for working with the ISIC 2019
skin lesion classification challenge dataset and models.

Classes:
    ISIC4Classifier: Main classifier for skin lesion images.
"""

from .isic4 import ISIC4Classifier

__all__ = ["ISIC4Classifier"]
