"""
AnalystHelper - Outil d'aide à l'analyse de dossiers
Permet de scanner, classifier et extraire des documents et pièces jointes
"""

__version__ = "2.0.0"
__author__ = "AnalystHelper"

from .core.scanner import FolderScanner
from .core.extractor import AttachmentExtractor
from .core.classifier import FileClassifier
from .core.reporter import HTMLReporter
from .core.workflow_manager import WorkflowManager
from .core.email_renamer import EmailRenamer
from .core.excel_exporter import ExcelExporter

__all__ = [
    'FolderScanner',
    'AttachmentExtractor',
    'FileClassifier',
    'HTMLReporter',
    'WorkflowManager',
    'EmailRenamer',
    'ExcelExporter'
]
