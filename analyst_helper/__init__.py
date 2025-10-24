"""
AnalystHelper - Outil d'aide à l'analyse de dossiers
Permet de scanner, classifier et extraire des documents et pièces jointes
"""

__version__ = "1.0.0"
__author__ = "AnalystHelper"

from .core.scanner import FolderScanner
from .core.extractor import AttachmentExtractor
from .core.classifier import FileClassifier
from .core.reporter import HTMLReporter

__all__ = [
    'FolderScanner',
    'AttachmentExtractor',
    'FileClassifier',
    'HTMLReporter'
]
