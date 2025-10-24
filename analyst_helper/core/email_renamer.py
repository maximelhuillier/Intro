"""
Module de renommage intelligent des emails
Renomme les emails au format : Date_Expéditeur_Destinataire_Objet.msg
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple


class EmailRenamer:
    """Renommeur intelligent d'emails"""

    @staticmethod
    def clean_string(text: str, max_length: int = 50) -> str:
        """
        Nettoie une chaîne pour un nom de fichier

        Args:
            text: Texte à nettoyer
            max_length: Longueur maximale

        Returns:
            Texte nettoyé
        """
        if not text:
            return "Inconnu"

        # Supprimer les caractères invalides pour Windows
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        cleaned = re.sub(invalid_chars, '_', text)

        # Supprimer les espaces multiples
        cleaned = re.sub(r'\s+', ' ', cleaned)

        # Supprimer les underscores multiples
        cleaned = re.sub(r'_+', '_', cleaned)

        # Trim
        cleaned = cleaned.strip(' _.')

        # Limiter la longueur
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length].rsplit(' ', 1)[0]

        return cleaned or "Inconnu"

    @staticmethod
    def extract_name_from_email(email_address: str) -> str:
        """
        Extrait le nom depuis une adresse email

        Args:
            email_address: Adresse email (ex: "John Doe <john@example.com>")

        Returns:
            Nom extrait
        """
        if not email_address:
            return "Inconnu"

        # Format : "Nom <email@domain.com>"
        match = re.search(r'^(.+?)\s*<', email_address)
        if match:
            return match.group(1).strip()

        # Format : "email@domain.com"
        match = re.search(r'^([^@]+)@', email_address)
        if match:
            # Convertir john.doe en John Doe
            name = match.group(1).replace('.', ' ').replace('_', ' ')
            return name.title()

        return email_address.split('<')[0].strip() or "Inconnu"

    def rename_msg_file(self, msg_path: str) -> Tuple[str, str]:
        """
        Renomme un fichier .msg selon le format intelligent

        Args:
            msg_path: Chemin du fichier .msg

        Returns:
            Tuple (nouveau_nom, chemin_complet)
        """
        try:
            import extract_msg
        except ImportError:
            # Si extract_msg n'est pas disponible, retourner nom basique
            return self._basic_rename(msg_path)

        try:
            msg = extract_msg.Message(msg_path)

            # Extraire les informations
            date = self._extract_date(msg)
            sender = self._extract_sender(msg)
            recipient = self._extract_recipient(msg)
            subject = self._extract_subject(msg)

            msg.close()

            # Construire le nom
            new_name = self._build_filename(date, sender, recipient, subject)

            # Chemin complet
            parent = Path(msg_path).parent
            new_path = parent / new_name

            # Gérer les doublons
            new_path = self._get_unique_path(new_path)

            return new_name, str(new_path)

        except Exception as e:
            print(f"[WARN] Erreur renommage {Path(msg_path).name}: {e}")
            return self._basic_rename(msg_path)

    def _extract_date(self, msg) -> str:
        """Extrait la date au format YYYYMMDD"""
        try:
            if hasattr(msg, 'date') and msg.date:
                if isinstance(msg.date, str):
                    # Tenter de parser la date string
                    date_obj = datetime.strptime(msg.date[:10], '%Y-%m-%d')
                else:
                    date_obj = msg.date
                return date_obj.strftime('%Y%m%d')
        except:
            pass

        return datetime.now().strftime('%Y%m%d')

    def _extract_sender(self, msg) -> str:
        """Extrait l'expéditeur"""
        try:
            if hasattr(msg, 'sender') and msg.sender:
                return self.extract_name_from_email(msg.sender)
        except:
            pass

        return "Inconnu"

    def _extract_recipient(self, msg) -> str:
        """Extrait le destinataire principal"""
        try:
            if hasattr(msg, 'to') and msg.to:
                # Prendre le premier destinataire
                recipients = msg.to.split(';')[0].strip()
                return self.extract_name_from_email(recipients)
        except:
            pass

        return "Tous"

    def _extract_subject(self, msg) -> str:
        """Extrait l'objet"""
        try:
            if hasattr(msg, 'subject') and msg.subject:
                return msg.subject
        except:
            pass

        return "SansObjet"

    def _build_filename(self, date: str, sender: str, recipient: str, subject: str) -> str:
        """
        Construit le nom de fichier

        Format: YYYYMMDD_Expéditeur_Destinataire_Objet.msg
        """
        sender_clean = self.clean_string(sender, 30)
        recipient_clean = self.clean_string(recipient, 30)
        subject_clean = self.clean_string(subject, 50)

        filename = f"{date}_{sender_clean}_{recipient_clean}_{subject_clean}.msg"

        # Sécurité : limiter à 255 caractères (limite Windows)
        if len(filename) > 255:
            # Réduire l'objet
            max_subject = 255 - len(f"{date}_{sender_clean}_{recipient_clean}_.msg")
            subject_clean = subject_clean[:max_subject]
            filename = f"{date}_{sender_clean}_{recipient_clean}_{subject_clean}.msg"

        return filename

    def _basic_rename(self, msg_path: str) -> Tuple[str, str]:
        """Renommage basique si extract_msg échoue"""
        path = Path(msg_path)
        date = datetime.now().strftime('%Y%m%d')
        new_name = f"{date}_{path.stem}.msg"
        new_path = path.parent / new_name
        return new_name, str(new_path)

    def _get_unique_path(self, path: Path) -> Path:
        """Génère un chemin unique si le fichier existe déjà"""
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
