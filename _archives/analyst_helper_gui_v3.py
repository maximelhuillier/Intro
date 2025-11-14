#!/usr/bin/env python3
"""
Interface Graphique AnalystHelper v3.0
Version avec design moderne et professionnel
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import webbrowser
from pathlib import Path


class ModernButton(tk.Canvas):
    """Bouton moderne avec effets visuels"""

    def __init__(self, parent, text, command, bg_color, hover_color, text_color='white', **kwargs):
        super().__init__(parent, height=50, bd=0, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text = text
        self.is_enabled = True

        self.draw_button(bg_color)

        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)

    def draw_button(self, color):
        """Dessine le bouton avec ombre"""
        self.delete('all')
        width = self.winfo_reqwidth() or 400

        # Ombre
        self.create_rectangle(2, 2, width-2, 48, fill='#d0d0d0', outline='')

        # Bouton principal
        self.create_rectangle(0, 0, width-4, 46, fill=color, outline='', tags='button')

        # Texte
        self.create_text(width/2-2, 23, text=self.text, fill=self.text_color,
                        font=('Segoe UI', 12, 'bold'), tags='text')

    def on_enter(self, event):
        if self.is_enabled:
            self.draw_button(self.hover_color)
            self.config(cursor='hand2')

    def on_leave(self, event):
        if self.is_enabled:
            self.draw_button(self.bg_color)
            self.config(cursor='')

    def on_click(self, event):
        if self.is_enabled and self.command:
            self.command()

    def set_state(self, state):
        """Active ou désactive le bouton"""
        self.is_enabled = (state == 'normal')
        if not self.is_enabled:
            self.draw_button('#cccccc')
        else:
            self.draw_button(self.bg_color)


class AnalystHelperGUI:
    """Interface graphique AnalystHelper v3.0 - Design Moderne"""

    def __init__(self, root):
        self.root = root
        self.root.title("AnalystHelper v3.0 - Analyse Professionnelle")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)

        # Définir couleurs du thème
        self.colors = {
            'primary': '#4A90E2',      # Bleu moderne
            'primary_dark': '#357ABD',  # Bleu foncé
            'success': '#2ECC71',       # Vert
            'success_dark': '#27AE60',  # Vert foncé
            'info': '#3498DB',          # Bleu info
            'info_dark': '#2980B9',     # Bleu info foncé
            'secondary': '#95A5A6',     # Gris
            'secondary_dark': '#7F8C8D',# Gris foncé
            'background': '#F5F7FA',    # Fond clair
            'card': '#FFFFFF',          # Blanc
            'text': '#2C3E50',          # Texte foncé
            'text_light': '#7F8C8D',    # Texte clair
            'border': '#E1E8ED',        # Bordure
            'warning': '#F39C12',       # Orange
        }

        # Configuration du style
        self.root.configure(bg=self.colors['background'])

        # Variables
        self.folder_path = tk.StringVar()

        # Créer l'interface
        self.create_widgets()
        self.center_window()

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Crée tous les widgets de l'interface"""

        # Style moderne
        style = ttk.Style()
        style.theme_use('clam')

        # Styles personnalisés
        style.configure('Card.TFrame', background=self.colors['card'], relief='flat')
        style.configure('Main.TFrame', background=self.colors['background'])
        style.configure('Header.TLabel', background=self.colors['primary'],
                       foreground='white', font=('Segoe UI', 11))
        style.configure('Title.TLabel', foreground=self.colors['text'],
                       font=('Segoe UI', 10, 'bold'))
        style.configure('Info.TLabel', foreground=self.colors['text_light'],
                       font=('Segoe UI', 9))

        # ===== EN-TÊTE MODERNE =====
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=140)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Titre principal
        title_label = tk.Label(
            header_frame,
            text="AnalystHelper",
            font=('Segoe UI', 32, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(pady=(20, 5))

        # Sous-titre
        subtitle_label = tk.Label(
            header_frame,
            text="Analyse intelligente et classification automatique de vos dossiers",
            font=('Segoe UI', 13),
            bg=self.colors['primary'],
            fg='white'
        )
        subtitle_label.pack(pady=(0, 5))

        # Version
        version_label = tk.Label(
            header_frame,
            text="v3.0 - Design Professionnel",
            font=('Segoe UI', 9),
            bg=self.colors['primary'],
            fg='#E8F4FD'
        )
        version_label.pack()

        # ===== CONTENEUR PRINCIPAL =====
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, padx=30, pady=30)

        # ===== CARD 1 : Sélection du dossier =====
        card1 = self.create_card(main_container)
        card1.pack(fill='x', pady=(0, 20))

        # Titre de la card
        card1_title = tk.Label(
            card1,
            text="Dossier à analyser",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        card1_title.pack(anchor='w', pady=(0, 10))

        # Info
        info_label = tk.Label(
            card1,
            text="Tous les fichiers et sous-dossiers seront traités récursivement",
            font=('Segoe UI', 9, 'italic'),
            bg=self.colors['card'],
            fg=self.colors['warning']
        )
        info_label.pack(anchor='w', pady=(0, 15))

        # Frame pour l'entry et le bouton
        folder_frame = tk.Frame(card1, bg=self.colors['card'])
        folder_frame.pack(fill='x')

        # Entry moderne
        entry_style = ttk.Style()
        entry_style.configure('Modern.TEntry',
                            fieldbackground='white',
                            borderwidth=1)

        self.folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.folder_path,
            font=('Segoe UI', 11),
            style='Modern.TEntry'
        )
        self.folder_entry.pack(side='left', fill='x', expand=True, ipady=8)

        # Bouton parcourir
        browse_btn = tk.Button(
            folder_frame,
            text="Parcourir",
            command=self.browse_folder,
            bg=self.colors['info'],
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10
        )
        browse_btn.pack(side='left', padx=(10, 0))

        # ===== CARD 2 : Fonctionnalités =====
        card2 = self.create_card(main_container)
        card2.pack(fill='x', pady=(0, 20))

        card2_title = tk.Label(
            card2,
            text="Fonctionnalités",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        card2_title.pack(anchor='w', pady=(0, 15))

        # Liste des fonctionnalités avec icônes
        features = [
            ("Scan récursif", "Analyse tous les fichiers et sous-dossiers"),
            ("Renommage emails", "Format : Date_Expediteur_Destinataire_Objet.msg"),
            ("Extraction PJ", "Pièces jointes + emails imbriqués"),
            ("Classification auto", "Dossier technique / Correspondance / Autres"),
            ("Export Excel", "Traçabilité complète avec origine et destination"),
            ("Rapport HTML", "Visualisation interactive avec graphiques"),
            ("Détection doublons", "Actualise les traitements précédents"),
        ]

        features_container = tk.Frame(card2, bg=self.colors['card'])
        features_container.pack(fill='x')

        for idx, (title, desc) in enumerate(features):
            feature_frame = tk.Frame(features_container, bg=self.colors['card'])
            feature_frame.pack(fill='x', pady=5)

            # Puce
            bullet = tk.Label(
                feature_frame,
                text="●",
                font=('Segoe UI', 14),
                bg=self.colors['card'],
                fg=self.colors['success']
            )
            bullet.pack(side='left', padx=(0, 10))

            # Texte
            text_frame = tk.Frame(feature_frame, bg=self.colors['card'])
            text_frame.pack(side='left', fill='x', expand=True)

            tk.Label(
                text_frame,
                text=title,
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['text']
            ).pack(anchor='w')

            tk.Label(
                text_frame,
                text=desc,
                font=('Segoe UI', 9),
                bg=self.colors['card'],
                fg=self.colors['text_light']
            ).pack(anchor='w')

        # ===== BOUTON PRINCIPAL =====
        button_container = tk.Frame(main_container, bg=self.colors['background'])
        button_container.pack(fill='x', pady=(0, 20))

        self.start_button = ModernButton(
            button_container,
            text="Lancer l'Analyse Complète",
            command=self.start_analysis,
            bg_color=self.colors['success'],
            hover_color=self.colors['success_dark'],
            width=400
        )
        self.start_button.pack(fill='x', ipady=5)

        # ===== CARD 3 : Progression =====
        card3 = self.create_card(main_container)
        card3.pack(fill='both', expand=True, pady=(0, 20))

        card3_title = tk.Label(
            card3,
            text="Progression",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        card3_title.pack(anchor='w', pady=(0, 15))

        # Barre de progression
        self.progress_bar = ttk.Progressbar(
            card3,
            mode='indeterminate',
            length=300
        )
        self.progress_bar.pack(fill='x', pady=(0, 15))

        # Zone de log
        log_frame = tk.Frame(card3, bg='#2C3E50', relief='flat', bd=1)
        log_frame.pack(fill='both', expand=True)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            font=('Consolas', 9),
            bg='#2C3E50',
            fg='#ECF0F1',
            insertbackground='white',
            relief='flat',
            padx=10,
            pady=10
        )
        self.log_text.pack(fill='both', expand=True)
        self.log_text.config(state='disabled')

        # ===== BOUTONS DE RÉSULTATS =====
        result_frame = tk.Frame(main_container, bg=self.colors['background'])
        result_frame.pack(fill='x')

        # Excel
        self.open_excel_button = tk.Button(
            result_frame,
            text="Ouvrir Excel",
            command=self.open_excel,
            bg=self.colors['success'],
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            state='disabled',
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=12
        )
        self.open_excel_button.pack(side='left', fill='x', expand=True, padx=(0, 10))

        # HTML
        self.open_report_button = tk.Button(
            result_frame,
            text="Ouvrir Rapport HTML",
            command=self.open_report,
            bg=self.colors['info'],
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            state='disabled',
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=12
        )
        self.open_report_button.pack(side='left', fill='x', expand=True, padx=(0, 10))

        # Dossier
        self.open_folder_button = tk.Button(
            result_frame,
            text="Ouvrir Dossier",
            command=self.open_folder,
            bg=self.colors['secondary'],
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            state='disabled',
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=12
        )
        self.open_folder_button.pack(side='left', fill='x', expand=True)

    def create_card(self, parent):
        """Crée une card moderne avec ombre"""
        # Conteneur avec ombre
        shadow_frame = tk.Frame(parent, bg='#D0D0D0')
        shadow_frame.pack_propagate(False)

        # Card principale
        card = tk.Frame(shadow_frame, bg=self.colors['card'], relief='flat')
        card.pack(fill='both', expand=True, padx=2, pady=2)

        # Padding interne
        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill='both', expand=True, padx=25, pady=20)

        return content

    def browse_folder(self):
        """Ouvre un dialogue pour sélectionner le dossier"""
        folder = filedialog.askdirectory(title="Sélectionner le dossier à analyser")
        if folder:
            self.folder_path.set(folder)

    def log(self, message):
        """Ajoute un message au log"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        self.root.update()

    def start_analysis(self):
        """Lance l'analyse dans un thread séparé"""
        # Validation
        if not self.folder_path.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un dossier à analyser")
            return

        if not os.path.isdir(self.folder_path.get()):
            messagebox.showerror("Erreur", "Le dossier sélectionné n'existe pas")
            return

        # Confirmation
        result = messagebox.askyesno(
            "Confirmation",
            f"Analyser le dossier :\n{self.folder_path.get()}\n\n"
            "Les fichiers seront classés directement dans :\n"
            "• Dossier technique/\n"
            "• Correspondance/\n"
            "• Autres fichiers/\n\n"
            "Continuer ?"
        )

        if not result:
            return

        # Désactiver les boutons
        self.start_button.set_state('disabled')
        self.open_excel_button.config(state='disabled')
        self.open_report_button.config(state='disabled')
        self.open_folder_button.config(state='disabled')

        # Démarrer la progression
        self.progress_bar.start()

        # Effacer le log
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state='disabled')

        # Lancer dans un thread
        thread = threading.Thread(target=self.run_analysis)
        thread.daemon = True
        thread.start()

    def run_analysis(self):
        """Exécute l'analyse (dans un thread séparé)"""
        try:
            from analyst_helper import WorkflowManager, ExcelExporter
            from analyst_helper.core.reporter import HTMLReporter

            folder = Path(self.folder_path.get())

            # Étape 1 : Initialisation
            self.log("=" * 70)
            self.log("ANALYST HELPER v3.0 - DEMARRAGE")
            self.log("=" * 70)
            self.log(f"Dossier : {folder}")
            self.log("")

            # Créer le workflow manager
            self.log("Initialisation du gestionnaire de workflow...")
            workflow = WorkflowManager(str(folder))

            # Étape 2 : Traitement
            self.log("\n" + "=" * 70)
            self.log("TRAITEMENT DES FICHIERS")
            self.log("=" * 70)

            processed = workflow.process_folder(exclude_categories=True)

            # Résultats
            self.log(f"\nTraitement termine !")
            self.log(f"   Fichiers traites : {workflow.stats['total_files']}")
            self.log(f"   Emails traites : {workflow.stats['total_emails']}")
            self.log(f"   Emails renommes : {workflow.stats['emails_renamed']}")
            self.log(f"   Pieces jointes extraites : {workflow.stats['total_attachments']}")

            self.log("\nRepartition par categorie :")
            for cat, count in workflow.stats['by_category'].items():
                if count > 0:
                    self.log(f"   • {cat}: {count}")

            # Étape 3 : Export Excel
            self.log("\n" + "=" * 70)
            self.log("GENERATION DU FICHIER EXCEL")
            self.log("=" * 70)

            excel_path = folder / "AnalystHelper_Liste_Complete.xlsx"
            exporter = ExcelExporter(str(excel_path))
            exporter.export(processed, workflow.stats)

            # Étape 4 : Rapport HTML
            self.log("\n" + "=" * 70)
            self.log("GENERATION DU RAPPORT HTML")
            self.log("=" * 70)

            # Scanner pour le rapport HTML
            from analyst_helper import FolderScanner
            scanner = FolderScanner(str(folder))
            files = scanner.scan(exclude_folders=list(workflow.CATEGORIES.keys()))

            html_path = folder / "AnalystHelper_Rapport.html"
            reporter = HTMLReporter(str(html_path))
            reporter.generate_report(
                files=files,
                stats=scanner.stats,
                title=f"Analyse - {folder.name}"
            )

            # Fin
            self.log("\n" + "=" * 70)
            self.log("ANALYSE TERMINEE AVEC SUCCES")
            self.log("=" * 70)
            self.log(f"\nResultats disponibles dans : {folder}")
            self.log(f"\nExcel : AnalystHelper_Liste_Complete.xlsx")
            self.log(f"HTML : AnalystHelper_Rapport.html")
            self.log(f"\nLes fichiers sont classes dans :")
            self.log(f"   • Dossier technique/")
            self.log(f"   • Correspondance/")
            self.log(f"   • Autres fichiers/")

            # Activer les boutons de résultat
            self.root.after(0, self.analysis_complete)

        except Exception as e:
            self.log(f"\nERREUR : {e}")
            import traceback
            self.log(traceback.format_exc())
            self.root.after(0, self.analysis_failed)

    def analysis_complete(self):
        """Appelé quand l'analyse est terminée avec succès"""
        self.progress_bar.stop()
        self.start_button.set_state('normal')
        self.open_excel_button.config(state='normal')
        self.open_report_button.config(state='normal')
        self.open_folder_button.config(state='normal')

        messagebox.showinfo(
            "Succès",
            "L'analyse est terminée !\n\n"
            "✓ Fichiers classés\n"
            "✓ Emails renommés\n"
            "✓ Pièces jointes extraites\n"
            "✓ Excel généré\n"
            "✓ Rapport HTML créé\n\n"
            "Cliquez sur les boutons pour consulter les résultats."
        )

    def analysis_failed(self):
        """Appelé quand l'analyse a échoué"""
        self.progress_bar.stop()
        self.start_button.set_state('normal')

        messagebox.showerror(
            "Erreur",
            "L'analyse a échoué.\n\n"
            "Consultez les messages d'erreur dans la fenêtre de progression."
        )

    def open_excel(self):
        """Ouvre le fichier Excel"""
        excel_path = Path(self.folder_path.get()) / "AnalystHelper_Liste_Complete.xlsx"
        if excel_path.exists():
            os.startfile(excel_path)
        else:
            messagebox.showerror("Erreur", "Le fichier Excel n'existe pas encore")

    def open_report(self):
        """Ouvre le rapport HTML"""
        report_path = Path(self.folder_path.get()) / "AnalystHelper_Rapport.html"
        if report_path.exists():
            webbrowser.open(f'file://{report_path.resolve()}')
        else:
            messagebox.showerror("Erreur", "Le rapport n'existe pas encore")

    def open_folder(self):
        """Ouvre le dossier"""
        folder = Path(self.folder_path.get())
        if folder.exists():
            os.startfile(folder)
        else:
            messagebox.showerror("Erreur", "Le dossier n'existe pas")


def main():
    """Fonction principale"""
    root = tk.Tk()
    app = AnalystHelperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
