"""
Module de classification et organisation des fichiers
Copie les fichiers dans des dossiers par catégorie
"""

import shutil
from pathlib import Path
from typing import List, Dict, Optional
from .scanner import FileInfo


class FileClassifier:
    """Classificateur et organisateur de fichiers"""

    DEFAULT_CATEGORIES = {
        "Dossier technique": ['.pdf', '.dwg', '.dxf', '.doc', '.docx', '.xls', '.xlsx',
                             '.ppt', '.pptx', '.odt', '.ods', '.odp'],
        "Correspondance": ['.msg', '.eml'],
        "Autres fichiers": []  # Catch-all
    }

    def __init__(self, output_dir: str, categories: Optional[Dict[str, List[str]]] = None):
        """
        Initialise le classificateur

        Args:
            output_dir: Dossier de sortie
            categories: Dictionnaire de catégories personnalisées
        """
        self.output_dir = Path(output_dir)
        self.categories = categories or self.DEFAULT_CATEGORIES
        self.stats = {
            'total_copied': 0,
            'total_size_mb': 0,
            'by_category': {},
            'errors': 0
        }

        # Créer les dossiers de catégories
        self._create_category_folders()

    def _create_category_folders(self):
        """Crée les dossiers pour chaque catégorie"""
        for category in self.categories.keys():
            category_path = self.output_dir / category
            category_path.mkdir(parents=True, exist_ok=True)
            self.stats['by_category'][category] = 0

    def classify_file(self, file_info: FileInfo, copy: bool = True,
                     preserve_structure: bool = False) -> Optional[str]:
        """
        Classifie et copie un fichier

        Args:
            file_info: Information sur le fichier
            copy: Si True, copie le fichier, sinon retourne juste la catégorie
            preserve_structure: Préserver la structure de dossiers

        Returns:
            Chemin de destination ou None en cas d'erreur
        """
        category = self._get_category(file_info.extension)

        if not copy:
            return category

        try:
            # Déterminer le chemin de destination
            if preserve_structure:
                # Préserver la structure relative
                relative_parent = Path(file_info.relative_path).parent
                dest_dir = self.output_dir / category / relative_parent
                dest_dir.mkdir(parents=True, exist_ok=True)
            else:
                dest_dir = self.output_dir / category

            dest_path = dest_dir / file_info.name
            dest_path = self._get_unique_path(dest_path)

            # Copier le fichier
            shutil.copy2(file_info.path, dest_path)

            # Mettre à jour les stats
            self.stats['total_copied'] += 1
            self.stats['total_size_mb'] += file_info.size_mb
            self.stats['by_category'][category] += 1

            return str(dest_path)

        except Exception as e:
            print(f"❌ Erreur copie {file_info.name}: {e}")
            self.stats['errors'] += 1
            return None

    def classify_all(self, files: List[FileInfo], copy: bool = True,
                    preserve_structure: bool = False, show_progress: bool = True) -> Dict[str, str]:
        """
        Classifie tous les fichiers

        Args:
            files: Liste des fichiers à classifier
            copy: Copier les fichiers
            preserve_structure: Préserver la structure
            show_progress: Afficher la progression

        Returns:
            Dictionnaire {chemin_source: chemin_destination}
        """
        results = {}

        for i, file_info in enumerate(files, 1):
            if show_progress and i % 10 == 0:
                print(f"📁 Classification: {i}/{len(files)} fichiers")

            dest_path = self.classify_file(file_info, copy, preserve_structure)
            if dest_path:
                results[file_info.path] = dest_path

        if show_progress:
            print(f"\n✅ Classification terminée:")
            print(f"   - {self.stats['total_copied']} fichiers copiés")
            print(f"   - {self.stats['total_size_mb']:.2f} MB")
            for category, count in self.stats['by_category'].items():
                if count > 0:
                    print(f"   - {category}: {count} fichiers")
            if self.stats['errors'] > 0:
                print(f"   - {self.stats['errors']} erreurs")

        return results

    def _get_category(self, extension: str) -> str:
        """
        Détermine la catégorie d'un fichier

        Args:
            extension: Extension du fichier

        Returns:
            Nom de la catégorie
        """
        extension = extension.lower()

        for category, extensions in self.categories.items():
            if extension in extensions:
                return category

        # Par défaut, "Autres fichiers"
        return "Autres fichiers"

    def _get_unique_path(self, path: Path) -> Path:
        """
        Génère un chemin unique si le fichier existe déjà

        Args:
            path: Chemin original

        Returns:
            Chemin unique
        """
        if not path.exists():
            return path

        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        counter = 1

        while True:
            new_path = parent / f"{stem}_{counter}{suffix}"
            if not new_path.exists():
                return new_path
            counter += 1

    def get_report(self) -> str:
        """
        Génère un rapport de classification

        Returns:
            Rapport textuel
        """
        lines = [
            "=" * 50,
            "RAPPORT DE CLASSIFICATION",
            "=" * 50,
            f"Fichiers copiés: {self.stats['total_copied']}",
            f"Taille totale: {self.stats['total_size_mb']:.2f} MB",
            "",
            "Répartition par catégorie:",
        ]

        for category, count in sorted(self.stats['by_category'].items()):
            if count > 0:
                percentage = (count / self.stats['total_copied'] * 100) if self.stats['total_copied'] > 0 else 0
                lines.append(f"  {category:.<30} {count:>4} ({percentage:.1f}%)")

        if self.stats['errors'] > 0:
            lines.append(f"\n⚠️  Erreurs: {self.stats['errors']}")

        lines.append("=" * 50)
        return "\n".join(lines)
