"""
Gestionnaire de workflow complet pour AnalystHelper
Gère la détection d'exécutions précédentes, l'extraction et la classification
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, asdict

from .scanner import FileInfo
from .email_renamer import EmailRenamer


@dataclass
class ProcessedFile:
    """Informations sur un fichier traité"""
    original_path: str
    classified_path: str
    file_type: str
    size_kb: float
    processed_date: str
    source_email: Optional[str] = None  # Si c'est une PJ, nom de l'email source
    is_attachment: bool = False


class WorkflowManager:
    """Gestionnaire de workflow complet"""

    # Catégories de classification
    CATEGORIES = {
        "Dossier technique": ['.pdf', '.dwg', '.dxf', '.doc', '.docx', '.xls', '.xlsx',
                              '.ppt', '.pptx', '.odt', '.ods', '.odp', '.zip', '.rar'],
        "Correspondance": ['.msg', '.eml'],
        "Autres fichiers": []  # Catch-all
    }

    def __init__(self, root_folder: str):
        """
        Initialise le gestionnaire

        Args:
            root_folder: Dossier racine à traiter
        """
        self.root_folder = Path(root_folder).resolve()
        self.state_file = self.root_folder / ".analyst_helper_state.json"
        self.email_renamer = EmailRenamer()

        # Créer les dossiers de catégories directement dans le dossier racine
        self.category_folders = {}
        for category in self.CATEGORIES.keys():
            folder = self.root_folder / category
            folder.mkdir(exist_ok=True)
            self.category_folders[category] = folder

        # État du traitement
        self.processed_files: List[ProcessedFile] = []
        self.stats = {
            'total_files': 0,
            'total_attachments': 0,
            'total_emails': 0,
            'emails_renamed': 0,
            'by_category': {cat: 0 for cat in self.CATEGORIES.keys()}
        }

    def load_previous_state(self) -> bool:
        """
        Charge l'état d'une exécution précédente

        Returns:
            True si un état précédent a été trouvé
        """
        if not self.state_file.exists():
            return False

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Charger les fichiers déjà traités
            for item in data.get('processed_files', []):
                self.processed_files.append(ProcessedFile(**item))

            print(f"[INFO] Etat precedent charge : {len(self.processed_files)} fichiers deja traites")
            return True

        except Exception as e:
            print(f"[WARN] Erreur chargement etat : {e}")
            return False

    def save_state(self):
        """Sauvegarde l'état actuel"""
        try:
            data = {
                'last_run': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'root_folder': str(self.root_folder),
                'stats': self.stats,
                'processed_files': [asdict(f) for f in self.processed_files]
            }

            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Rendre le fichier caché sur Windows
            try:
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(str(self.state_file), 2)  # FILE_ATTRIBUTE_HIDDEN
            except:
                pass

        except Exception as e:
            print(f"[WARN] Erreur sauvegarde etat : {e}")

    def is_already_processed(self, file_path: str) -> bool:
        """
        Vérifie si un fichier a déjà été traité

        Args:
            file_path: Chemin du fichier

        Returns:
            True si déjà traité
        """
        file_path_str = str(Path(file_path).resolve())

        for pf in self.processed_files:
            if pf.original_path == file_path_str:
                # Vérifier que le fichier classé existe toujours
                if Path(pf.classified_path).exists():
                    return True

        return False

    def get_category(self, extension: str) -> str:
        """Détermine la catégorie d'un fichier"""
        ext = extension.lower()

        for category, extensions in self.CATEGORIES.items():
            if ext in extensions:
                return category

        return "Autres fichiers"

    def classify_file(self, source_path: str, is_attachment: bool = False,
                     source_email: Optional[str] = None) -> Optional[ProcessedFile]:
        """
        Classifie un fichier dans la bonne catégorie

        Args:
            source_path: Chemin source du fichier
            is_attachment: Si c'est une PJ
            source_email: Email source si PJ

        Returns:
            ProcessedFile ou None
        """
        source = Path(source_path)

        if not source.exists():
            return None

        # Vérifier si déjà traité
        if self.is_already_processed(str(source)):
            print(f"[SKIP] Deja traite : {source.name}")
            return None

        # Déterminer la catégorie
        category = self.get_category(source.suffix)
        dest_folder = self.category_folders[category]

        # Copier le fichier
        dest_path = dest_folder / source.name
        dest_path = self._get_unique_path(dest_path)

        try:
            shutil.copy2(source, dest_path)

            # Créer l'objet ProcessedFile
            processed = ProcessedFile(
                original_path=str(source.resolve()),
                classified_path=str(dest_path),
                file_type=category,
                size_kb=round(source.stat().st_size / 1024, 2),
                processed_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                source_email=source_email,
                is_attachment=is_attachment
            )

            self.processed_files.append(processed)
            self.stats['total_files'] += 1
            self.stats['by_category'][category] += 1

            if is_attachment:
                self.stats['total_attachments'] += 1

            return processed

        except Exception as e:
            print(f"[ERROR] Erreur copie {source.name}: {e}")
            return None

    def process_email(self, email_path: str, is_attachment: bool = False,
                     parent_email: Optional[str] = None, depth: int = 0) -> Optional[ProcessedFile]:
        """
        Traite un email : renommage + extraction PJ récursive

        Args:
            email_path: Chemin de l'email
            is_attachment: Si c'est une PJ d'un autre email
            parent_email: Email parent si imbriqué
            depth: Profondeur de récursion

        Returns:
            ProcessedFile ou None
        """
        if depth > 10:  # Limite de récursion
            print(f"[WARN] Profondeur max atteinte pour {email_path}")
            return None

        email_file = Path(email_path)

        if not email_file.exists():
            return None

        # Vérifier si déjà traité
        if self.is_already_processed(str(email_file)):
            print(f"[SKIP] Email deja traite : {email_file.name}")
            return None

        try:
            import extract_msg
        except ImportError:
            print("[WARN] extract-msg non disponible, copie simple de l'email")
            return self.classify_file(str(email_file), is_attachment, parent_email)

        try:
            # Renommer l'email
            new_name, _ = self.email_renamer.rename_msg_file(str(email_file))

            # Classifier l'email renommé
            dest_folder = self.category_folders["Correspondance"]
            dest_path = dest_folder / new_name
            dest_path = self._get_unique_path(dest_path)

            shutil.copy2(email_file, dest_path)

            # Créer ProcessedFile
            processed = ProcessedFile(
                original_path=str(email_file.resolve()),
                classified_path=str(dest_path),
                file_type="Correspondance",
                size_kb=round(email_file.stat().st_size / 1024, 2),
                processed_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                source_email=parent_email,
                is_attachment=is_attachment
            )

            self.processed_files.append(processed)
            self.stats['total_emails'] += 1
            self.stats['emails_renamed'] += 1
            self.stats['by_category']["Correspondance"] += 1

            # Extraire les PJ de cet email
            self._extract_attachments_from_email(
                str(dest_path),
                new_name,
                depth + 1
            )

            return processed

        except Exception as e:
            print(f"[ERROR] Erreur traitement email {email_file.name}: {e}")
            # Fallback : copie simple
            return self.classify_file(str(email_file), is_attachment, parent_email)

    def _extract_attachments_from_email(self, email_path: str, email_name: str, depth: int):
        """
        Extrait et classifie les PJ d'un email

        Args:
            email_path: Chemin de l'email
            email_name: Nom de l'email (pour traçabilité)
            depth: Profondeur de récursion
        """
        try:
            import extract_msg

            msg = extract_msg.Message(email_path)

            for att in msg.attachments:
                # Ignorer les images intégrées
                if self._is_embedded_image(att):
                    continue

                filename = att.longFilename or att.shortFilename

                # Sauvegarder temporairement la PJ
                temp_dir = Path(email_path).parent / ".temp_attachments"
                temp_dir.mkdir(exist_ok=True)
                temp_path = temp_dir / filename
                temp_path = self._get_unique_path(temp_path)

                att.save(customPath=str(temp_dir), customFilename=temp_path.name)

                # Si c'est un email imbriqué
                if temp_path.suffix.lower() in ['.msg', '.eml']:
                    # Traiter récursivement
                    self.process_email(
                        str(temp_path),
                        is_attachment=True,
                        parent_email=email_name,
                        depth=depth
                    )
                else:
                    # Classifier la PJ
                    self.classify_file(
                        str(temp_path),
                        is_attachment=True,
                        source_email=email_name
                    )

                # Supprimer le temp
                temp_path.unlink(missing_ok=True)

            # Nettoyer le dossier temp
            if temp_dir.exists() and not any(temp_dir.iterdir()):
                temp_dir.rmdir()

            msg.close()

        except Exception as e:
            print(f"[WARN] Erreur extraction PJ de {email_name}: {e}")

    def _is_embedded_image(self, attachment) -> bool:
        """Vérifie si c'est une image intégrée"""
        try:
            filename = (attachment.longFilename or attachment.shortFilename or "").lower()
            if any(x in filename for x in ['image', 'inline', 'icon']):
                if hasattr(attachment, 'size') and attachment.size < 50000:
                    return True
        except:
            pass
        return False

    def _get_unique_path(self, path: Path) -> Path:
        """Génère un chemin unique"""
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

    def process_folder(self, exclude_categories: bool = True) -> List[ProcessedFile]:
        """
        Traite tous les fichiers du dossier racine

        Args:
            exclude_categories: Exclure les dossiers de catégories du scan

        Returns:
            Liste des fichiers traités
        """
        # Charger l'état précédent
        self.load_previous_state()

        # Scanner tous les fichiers
        for file_path in self.root_folder.rglob('*'):
            if not file_path.is_file():
                continue

            # Ignorer les fichiers cachés et de config
            if file_path.name.startswith('.'):
                continue

            # Ignorer les fichiers dans les dossiers de catégories si demandé
            if exclude_categories:
                try:
                    file_path.relative_to(self.root_folder / "Dossier technique")
                    continue
                except ValueError:
                    pass

                try:
                    file_path.relative_to(self.root_folder / "Correspondance")
                    continue
                except ValueError:
                    pass

                try:
                    file_path.relative_to(self.root_folder / "Autres fichiers")
                    continue
                except ValueError:
                    pass

            # Traiter selon le type
            if file_path.suffix.lower() in ['.msg', '.eml']:
                self.process_email(str(file_path))
            else:
                self.classify_file(str(file_path))

        # Sauvegarder l'état
        self.save_state()

        return self.processed_files
