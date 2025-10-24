"""
Module de scan d'arborescence de dossiers
Permet de parcourir récursivement les dossiers et collecter les métadonnées
"""

import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class FileInfo:
    """Information sur un fichier"""
    name: str
    path: str
    relative_path: str
    extension: str
    size_bytes: int
    size_kb: float
    size_mb: float
    created_date: str
    modified_date: str
    file_type: str
    depth: int
    parent_folder: str
    is_email: bool = False
    email_source: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convertit en dictionnaire"""
        return asdict(self)


class FolderScanner:
    """Scanner d'arborescence de dossiers"""

    # Extensions par catégorie
    TECHNICAL_EXTENSIONS = {'.pdf', '.dwg', '.dxf', '.doc', '.docx', '.xls', '.xlsx',
                           '.ppt', '.pptx', '.odt', '.ods', '.odp'}
    EMAIL_EXTENSIONS = {'.msg', '.eml'}
    ARCHIVE_EXTENSIONS = {'.zip', '.rar', '.7z', '.tar', '.gz'}
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'}

    def __init__(self, root_path: str, max_depth: int = 50):
        """
        Initialise le scanner

        Args:
            root_path: Chemin racine à scanner
            max_depth: Profondeur maximale de récursion
        """
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self.files: List[FileInfo] = []
        self.stats = {
            'total_files': 0,
            'total_size_mb': 0,
            'total_emails': 0,
            'total_folders': 0,
            'by_type': {},
            'by_extension': {}
        }

    def scan(self, exclude_folders: Optional[List[str]] = None) -> List[FileInfo]:
        """
        Scanne le dossier racine

        Args:
            exclude_folders: Liste des dossiers à exclure

        Returns:
            Liste des fichiers trouvés
        """
        if exclude_folders is None:
            exclude_folders = []

        print(f"🔍 Scan de: {self.root_path}")
        self.files = []
        self._scan_directory(self.root_path, 0, exclude_folders)
        self._compute_stats()

        print(f"✅ Scan terminé: {self.stats['total_files']} fichiers trouvés")
        return self.files

    def _scan_directory(self, directory: Path, depth: int, exclude_folders: List[str]):
        """
        Scanne un dossier récursivement

        Args:
            directory: Dossier à scanner
            depth: Profondeur actuelle
            exclude_folders: Dossiers à exclure
        """
        if depth > self.max_depth:
            print(f"⚠️  Profondeur maximale atteinte pour: {directory}")
            return

        try:
            for entry in os.scandir(directory):
                # Ignorer les dossiers exclus
                if entry.name in exclude_folders:
                    continue

                if entry.is_file():
                    file_info = self._create_file_info(entry, depth)
                    if file_info:
                        self.files.append(file_info)

                elif entry.is_dir():
                    self.stats['total_folders'] += 1
                    self._scan_directory(Path(entry.path), depth + 1, exclude_folders)

        except PermissionError:
            print(f"⚠️  Accès refusé: {directory}")
        except Exception as e:
            print(f"❌ Erreur lors du scan de {directory}: {e}")

    def _create_file_info(self, entry: os.DirEntry, depth: int) -> Optional[FileInfo]:
        """
        Crée un objet FileInfo à partir d'une entrée

        Args:
            entry: Entrée du système de fichiers
            depth: Profondeur dans l'arborescence

        Returns:
            FileInfo ou None en cas d'erreur
        """
        try:
            stat = entry.stat()
            file_path = Path(entry.path)
            extension = file_path.suffix.lower()

            # Déterminer le type de fichier
            file_type = self._classify_file(extension)
            is_email = extension in self.EMAIL_EXTENSIONS

            return FileInfo(
                name=entry.name,
                path=str(file_path),
                relative_path=str(file_path.relative_to(self.root_path)),
                extension=extension,
                size_bytes=stat.st_size,
                size_kb=round(stat.st_size / 1024, 2),
                size_mb=round(stat.st_size / (1024 * 1024), 2),
                created_date=datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                modified_date=datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                file_type=file_type,
                depth=depth,
                parent_folder=file_path.parent.name,
                is_email=is_email
            )

        except Exception as e:
            print(f"⚠️  Erreur lecture fichier {entry.name}: {e}")
            return None

    def _classify_file(self, extension: str) -> str:
        """
        Classifie un fichier selon son extension

        Args:
            extension: Extension du fichier

        Returns:
            Type de fichier
        """
        if extension in self.TECHNICAL_EXTENSIONS:
            return "Dossier technique"
        elif extension in self.EMAIL_EXTENSIONS:
            return "Correspondance"
        elif extension in self.ARCHIVE_EXTENSIONS:
            return "Archive"
        elif extension in self.IMAGE_EXTENSIONS:
            return "Image"
        else:
            return "Autres fichiers"

    def _compute_stats(self):
        """Calcule les statistiques sur les fichiers scannés"""
        self.stats['total_files'] = len(self.files)
        self.stats['total_size_mb'] = sum(f.size_mb for f in self.files)
        self.stats['total_emails'] = sum(1 for f in self.files if f.is_email)

        # Stats par type
        for file in self.files:
            self.stats['by_type'][file.file_type] = \
                self.stats['by_type'].get(file.file_type, 0) + 1
            self.stats['by_extension'][file.extension] = \
                self.stats['by_extension'].get(file.extension, 0) + 1

    def export_to_json(self, output_path: str):
        """
        Exporte les résultats en JSON

        Args:
            output_path: Chemin du fichier de sortie
        """
        data = {
            'root_path': str(self.root_path),
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'stats': self.stats,
            'files': [f.to_dict() for f in self.files]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"📄 Export JSON: {output_path}")

    def export_to_csv(self, output_path: str):
        """
        Exporte les résultats en CSV

        Args:
            output_path: Chemin du fichier de sortie
        """
        import csv

        if not self.files:
            print("⚠️  Aucun fichier à exporter")
            return

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=self.files[0].to_dict().keys())
            writer.writeheader()
            for file in self.files:
                writer.writerow(file.to_dict())

        print(f"📊 Export CSV: {output_path}")

    def get_tree_structure(self, max_depth: int = 3) -> str:
        """
        Génère une représentation textuelle de l'arborescence

        Args:
            max_depth: Profondeur maximale à afficher

        Returns:
            Arborescence sous forme de texte
        """
        tree = {}

        for file in self.files:
            if file.depth > max_depth:
                continue

            parts = Path(file.relative_path).parts
            current = tree

            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            if '_files' not in current:
                current['_files'] = []
            current['_files'].append(file.name)

        return self._format_tree(tree)

    def _format_tree(self, tree: dict, prefix: str = "", is_last: bool = True) -> str:
        """
        Formate l'arborescence pour l'affichage

        Args:
            tree: Dictionnaire représentant l'arborescence
            prefix: Préfixe pour l'indentation
            is_last: Si c'est le dernier élément

        Returns:
            Arborescence formatée
        """
        result = []
        items = [(k, v) for k, v in tree.items() if k != '_files']
        files = tree.get('_files', [])

        for i, (name, subtree) in enumerate(items):
            is_last_item = (i == len(items) - 1) and not files
            connector = "└── " if is_last_item else "├── "
            result.append(f"{prefix}{connector}📁 {name}")

            extension = "    " if is_last_item else "│   "
            result.append(self._format_tree(subtree, prefix + extension, is_last_item))

        for i, filename in enumerate(files):
            is_last_file = i == len(files) - 1
            connector = "└── " if is_last_file else "├── "
            result.append(f"{prefix}{connector}📄 {filename}")

        return "\n".join(result)
