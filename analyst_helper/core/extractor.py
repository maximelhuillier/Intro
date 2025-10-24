"""
Module d'extraction de pièces jointes depuis les emails
Supporte les formats .msg (Outlook) et .eml (standard)
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass


@dataclass
class AttachmentInfo:
    """Information sur une pièce jointe"""
    original_filename: str
    saved_filename: str
    saved_path: str
    size_kb: float
    email_source: str
    email_date: str
    email_subject: str
    extraction_date: str
    is_nested_email: bool = False


class AttachmentExtractor:
    """Extracteur de pièces jointes d'emails"""

    def __init__(self, output_dir: str):
        """
        Initialise l'extracteur

        Args:
            output_dir: Dossier de sortie pour les pièces jointes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.attachments: List[AttachmentInfo] = []
        self.stats = {
            'total_emails_processed': 0,
            'total_attachments_extracted': 0,
            'total_size_mb': 0,
            'errors': 0
        }

    def extract_from_msg(self, msg_path: str, max_recursion: int = 10) -> List[AttachmentInfo]:
        """
        Extrait les pièces jointes d'un fichier .msg

        Args:
            msg_path: Chemin vers le fichier .msg
            max_recursion: Profondeur maximale pour les emails imbriqués

        Returns:
            Liste des pièces jointes extraites
        """
        try:
            import extract_msg
        except ImportError:
            print("❌ Module 'extract-msg' non installé. Installez-le avec: pip install extract-msg")
            return []

        return self._extract_msg_recursive(msg_path, "", max_recursion, 0)

    def _extract_msg_recursive(self, msg_path: str, parent_source: str,
                               max_recursion: int, depth: int) -> List[AttachmentInfo]:
        """
        Extrait récursivement les pièces jointes d'un .msg

        Args:
            msg_path: Chemin vers le fichier .msg
            parent_source: Source parent (pour emails imbriqués)
            max_recursion: Profondeur maximale
            depth: Profondeur actuelle

        Returns:
            Liste des pièces jointes extraites
        """
        if depth > max_recursion:
            print(f"⚠️  Profondeur maximale atteinte pour: {msg_path}")
            return []

        try:
            import extract_msg
            msg = extract_msg.Message(msg_path)

            # Informations sur l'email
            email_subject = msg.subject or "Sans objet"
            email_date = msg.date or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            email_filename = Path(msg_path).name

            # Créer le nom de source
            if parent_source:
                email_source = f"{parent_source} > {email_filename}"
            else:
                email_source = email_filename

            self.stats['total_emails_processed'] += 1
            extracted = []

            # Parcourir les pièces jointes
            for attachment in msg.attachments:
                # Ignorer les images intégrées
                if self._is_embedded_image(attachment):
                    continue

                filename = attachment.longFilename or attachment.shortFilename

                # Si c'est un email imbriqué
                if filename.lower().endswith('.msg'):
                    # Sauvegarder temporairement
                    temp_path = self.output_dir / f"temp_{filename}"
                    attachment.save(customPath=str(self.output_dir), customFilename=f"temp_{filename}")

                    # Extraire récursivement
                    nested = self._extract_msg_recursive(
                        str(temp_path),
                        email_source,
                        max_recursion,
                        depth + 1
                    )
                    extracted.extend(nested)

                    # Déplacer dans Correspondance
                    correspondence_dir = self.output_dir.parent / "Correspondance"
                    correspondence_dir.mkdir(exist_ok=True)
                    final_path = correspondence_dir / filename
                    final_path = self._get_unique_path(final_path)
                    temp_path.rename(final_path)

                else:
                    # Sauvegarder la pièce jointe normale
                    saved_path = self.output_dir / filename
                    saved_path = self._get_unique_path(saved_path)
                    attachment.save(customPath=str(self.output_dir), customFilename=saved_path.name)

                    # Créer l'info de pièce jointe
                    att_info = AttachmentInfo(
                        original_filename=filename,
                        saved_filename=saved_path.name,
                        saved_path=str(saved_path),
                        size_kb=round(saved_path.stat().st_size / 1024, 2),
                        email_source=email_source,
                        email_date=str(email_date),
                        email_subject=email_subject,
                        extraction_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        is_nested_email=depth > 0
                    )

                    extracted.append(att_info)
                    self.stats['total_attachments_extracted'] += 1
                    self.stats['total_size_mb'] += att_info.size_kb / 1024

            msg.close()
            return extracted

        except Exception as e:
            print(f"❌ Erreur extraction {msg_path}: {e}")
            self.stats['errors'] += 1
            return []

    def extract_from_eml(self, eml_path: str) -> List[AttachmentInfo]:
        """
        Extrait les pièces jointes d'un fichier .eml

        Args:
            eml_path: Chemin vers le fichier .eml

        Returns:
            Liste des pièces jointes extraites
        """
        import email
        from email import policy

        try:
            with open(eml_path, 'rb') as f:
                msg = email.message_from_binary_file(f, policy=policy.default)

            email_subject = msg.get('subject', 'Sans objet')
            email_date = msg.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            email_filename = Path(eml_path).name

            self.stats['total_emails_processed'] += 1
            extracted = []

            # Parcourir les pièces jointes
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                filename = part.get_filename()
                if not filename:
                    continue

                # Ignorer les images intégrées
                if part.get_content_disposition() == 'inline':
                    continue

                # Sauvegarder la pièce jointe
                saved_path = self.output_dir / filename
                saved_path = self._get_unique_path(saved_path)

                with open(saved_path, 'wb') as f:
                    f.write(part.get_payload(decode=True))

                # Créer l'info de pièce jointe
                att_info = AttachmentInfo(
                    original_filename=filename,
                    saved_filename=saved_path.name,
                    saved_path=str(saved_path),
                    size_kb=round(saved_path.stat().st_size / 1024, 2),
                    email_source=email_filename,
                    email_date=str(email_date),
                    email_subject=email_subject,
                    extraction_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )

                extracted.append(att_info)
                self.stats['total_attachments_extracted'] += 1
                self.stats['total_size_mb'] += att_info.size_kb / 1024

            return extracted

        except Exception as e:
            print(f"❌ Erreur extraction {eml_path}: {e}")
            self.stats['errors'] += 1
            return []

    def extract_all(self, files: List[str], show_progress: bool = True) -> List[AttachmentInfo]:
        """
        Extrait les pièces jointes de tous les emails

        Args:
            files: Liste des chemins d'emails
            show_progress: Afficher la progression

        Returns:
            Liste de toutes les pièces jointes extraites
        """
        all_attachments = []

        for i, file_path in enumerate(files, 1):
            if show_progress:
                print(f"📧 [{i}/{len(files)}] {Path(file_path).name}")

            ext = Path(file_path).suffix.lower()

            if ext == '.msg':
                attachments = self.extract_from_msg(file_path)
            elif ext == '.eml':
                attachments = self.extract_from_eml(file_path)
            else:
                continue

            all_attachments.extend(attachments)
            self.attachments.extend(attachments)

        if show_progress:
            print(f"\n✅ Extraction terminée:")
            print(f"   - {self.stats['total_emails_processed']} emails traités")
            print(f"   - {self.stats['total_attachments_extracted']} pièces jointes extraites")
            print(f"   - {self.stats['total_size_mb']:.2f} MB")
            if self.stats['errors'] > 0:
                print(f"   - {self.stats['errors']} erreurs")

        return all_attachments

    def _is_embedded_image(self, attachment) -> bool:
        """
        Vérifie si une pièce jointe est une image intégrée

        Args:
            attachment: Pièce jointe à vérifier

        Returns:
            True si c'est une image intégrée
        """
        try:
            filename = (attachment.longFilename or attachment.shortFilename or "").lower()
            # Images intégrées sont souvent petites et avec des noms spécifiques
            if any(x in filename for x in ['image', 'inline', 'icon']):
                # Vérifier la taille (< 50Ko)
                if hasattr(attachment, 'size') and attachment.size < 50000:
                    return True
            return False
        except:
            return False

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

    @staticmethod
    def clean_filename(filename: str) -> str:
        """
        Nettoie un nom de fichier pour le rendre valide

        Args:
            filename: Nom de fichier à nettoyer

        Returns:
            Nom de fichier nettoyé
        """
        # Remplacer les caractères invalides
        invalid_chars = r'[<>:"/\\|?*]'
        cleaned = re.sub(invalid_chars, '_', filename)

        # Remplacer les espaces multiples
        cleaned = re.sub(r'\s+', ' ', cleaned)

        # Limiter la longueur
        if len(cleaned) > 200:
            name, ext = os.path.splitext(cleaned)
            cleaned = name[:200-len(ext)] + ext

        return cleaned.strip()
