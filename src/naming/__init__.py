"""
Filename generation module (swappable)
"""

from .base import FilenameGenerator
from .template_generator import TemplateFilenameGenerator

__all__ = ['FilenameGenerator', 'TemplateFilenameGenerator']
