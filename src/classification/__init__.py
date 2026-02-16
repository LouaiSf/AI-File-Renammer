"""
Document classification module (swappable)
"""

from .base import DocumentClassifier
from .rule_based_classifier import RuleBasedClassifier

__all__ = ['DocumentClassifier', 'RuleBasedClassifier']
