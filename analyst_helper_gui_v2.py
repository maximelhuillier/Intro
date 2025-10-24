#!/usr/bin/env python3
"""
Interface Graphique AnalystHelper v2.0
Version refactorisée avec workflow manager
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import webbrowser
from pathlib import Path


class AnalystHelperGUI:
    """Interface graphique AnalystHelper v2.0"""

    def __init__(self, root):
        self.root = root
        self.root.title("📊 AnalystHelper v2.0 - Analyse de Dossiers")
        self.root.geometry("900x750")
        self.root.resizable(True, True)

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

        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # ===== EN-TÊTE =====
        header_frame = tk.Frame(self.root, bg='#667eea', height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="📊 AnalystHelper v2.0",
            font=('Arial', 26, 'bold'),
            bg='#667eea',
            fg='white'
        )
        title_label.pack(pady=15)

        subtitle_label = tk.Label(
            header_frame,
            text="Analyse intelligente avec extraction et classification automatique",
            font=('Arial', 12),
            bg='#667eea',
            fg='white'
        )
        subtitle_label.pack()

        version_label = tk.Label(
            header_frame,
            text="🎯 Traitement récursif • Renommage emails • PJ imbriquées • Excel détaillé",
            font=('Arial', 9),
            bg='#667eea',
            fg='white'
        )
        version_label.pack(pady=5)

        # ===== CORPS PRINCIPAL =====
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill='both', expand=True)

        # --- Section 1 : Sélection du dossier ---
        section1 = ttk.LabelFrame(main_frame, text="📁 Dossier à analyser", padding="15")
        section1.pack(fill='x', pady=(0, 15))

        info_label = ttk.Label(
            section1,
            text="⚠️  Tous les fichiers et sous-dossiers seront traités",
            font=('Arial', 9, 'italic'),
            foreground='#e67e22'
        )
        info_label.pack(anchor='w', pady=(0, 10))

        folder_frame = ttk.Frame(section1)
        folder_frame.pack(fill='x')

        ttk.Entry(
            folder_frame,
            textvariable=self.folder_path,
            width=70,
            font=('Arial', 10)
        ).pack(side='left', fill='x', expand=True, padx=(0, 10))

        ttk.Button(
            folder_frame,
            text="📂 Parcourir",
            command=self.browse_folder
        ).pack(side='left')

        # --- Section 2 : Info ---
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️  Que va faire AnalystHelper ?", padding="15")
        info_frame.pack(fill='x', pady=(0, 15))

        features = [
            "✅ Scanner TOUS les fichiers et sous-dossiers récursivement",
            "✅ Renommer les emails : Date_Expéditeur_Destinataire_Objet.msg",
            "✅ Extraire les pièces jointes (y compris emails imbriqués)",
            "✅ Classifier automatiquement :",
            "   • Dossier technique : PDF, DWG, DOC, XLS, ZIP, etc.",
            "   • Correspondance : Emails renommés",
            "   • Autres fichiers : Le reste",
            "✅ Créer un fichier Excel détaillé avec traçabilité complète",
            "✅ Générer un rapport HTML interactif avec graphiques",
            "✅ Détecter et actualiser les traitements précédents",
        ]

        for feature in features:
            ttk.Label(
                info_frame,
                text=feature,
                font=('Arial', 9)
            ).pack(anchor='w', pady=1)

        # --- Section 3 : Actions ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill='x', pady=(15, 10))

        self.start_button = tk.Button(
            action_frame,
            text="🚀 Lancer l'Analyse Complète",
            command=self.start_analysis,
            bg='#667eea',
            fg='white',
            font=('Arial', 14, 'bold'),
            height=2,
            cursor='hand2'
        )
        self.start_button.pack(fill='x')

        # --- Section 4 : Progression ---
        section4 = ttk.LabelFrame(main_frame, text="📊 Progression", padding="15")
        section4.pack(fill='both', expand=True)

        self.progress_bar = ttk.Progressbar(
            section4,
            mode='indeterminate',
            length=300
        )
        self.progress_bar.pack(fill='x', pady=(0, 15))

        self.log_text = scrolledtext.ScrolledText(
            section4,
            height=15,
            font=('Courier', 9),
            bg='#f8f9fa',
            fg='#333333'
        )
        self.log_text.pack(fill='both', expand=True)
        self.log_text.config(state='disabled')

        # --- Section 5 : Résultats ---
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill='x', pady=(15, 0))

        self.open_excel_button = tk.Button(
            result_frame,
            text="📗 Ouvrir le Fichier Excel",
            command=self.open_excel,
            bg='#28a745',
            fg='white',
            font=('Arial', 11, 'bold'),
            state='disabled',
            cursor='hand2'
        )
        self.open_excel_button.pack(side='left', fill='x', expand=True, padx=(0, 5))

        self.open_report_button = tk.Button(
            result_frame,
            text="📄 Ouvrir le Rapport HTML",
            command=self.open_report,
            bg='#17a2b8',
            fg='white',
            font=('Arial', 11, 'bold'),
            state='disabled',
            cursor='hand2'
        )
        self.open_report_button.pack(side='left', fill='x', expand=True, padx=(0, 5))

        self.open_folder_button = tk.Button(
            result_frame,
            text="📂 Ouvrir le Dossier",
            command=self.open_folder,
            bg='#6c757d',
            fg='white',
            font=('Arial', 11, 'bold'),
            state='disabled',
            cursor='hand2'
        )
        self.open_folder_button.pack(side='left', fill='x', expand=True)

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

        # Désactiver le bouton
        self.start_button.config(state='disabled')
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
            self.log("🚀 ANALYST HELPER v2.0 - DÉMARRAGE")
            self.log("=" * 70)
            self.log(f"📁 Dossier : {folder}")
            self.log("")

            # Créer le workflow manager
            self.log("📦 Initialisation du gestionnaire de workflow...")
            workflow = WorkflowManager(str(folder))

            # Étape 2 : Traitement
            self.log("\n" + "=" * 70)
            self.log("📂 TRAITEMENT DES FICHIERS")
            self.log("=" * 70)

            processed = workflow.process_folder(exclude_categories=True)

            # Résultats
            self.log(f"\n✅ Traitement terminé !")
            self.log(f"   📄 Fichiers traités : {workflow.stats['total_files']}")
            self.log(f"   📧 Emails traités : {workflow.stats['total_emails']}")
            self.log(f"   ✏️  Emails renommés : {workflow.stats['emails_renamed']}")
            self.log(f"   📎 Pièces jointes extraites : {workflow.stats['total_attachments']}")

            self.log("\n📊 Répartition par catégorie :")
            for cat, count in workflow.stats['by_category'].items():
                if count > 0:
                    self.log(f"   • {cat}: {count}")

            # Étape 3 : Export Excel
            self.log("\n" + "=" * 70)
            self.log("📗 GÉNÉRATION DU FICHIER EXCEL")
            self.log("=" * 70)

            excel_path = folder / "AnalystHelper_Liste_Complete.xlsx"
            exporter = ExcelExporter(str(excel_path))
            exporter.export(processed, workflow.stats)

            # Étape 4 : Rapport HTML (ancien workflow pour compatibilité)
            self.log("\n" + "=" * 70)
            self.log("📄 GÉNÉRATION DU RAPPORT HTML")
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
            self.log("🎉 ANALYSE TERMINÉE AVEC SUCCÈS")
            self.log("=" * 70)
            self.log(f"\n📂 Résultats disponibles dans : {folder}")
            self.log(f"\n📗 Excel : AnalystHelper_Liste_Complete.xlsx")
            self.log(f"📄 HTML : AnalystHelper_Rapport.html")
            self.log(f"\n✅ Les fichiers sont classés dans :")
            self.log(f"   • Dossier technique/")
            self.log(f"   • Correspondance/")
            self.log(f"   • Autres fichiers/")

            # Activer les boutons de résultat
            self.root.after(0, self.analysis_complete)

        except Exception as e:
            self.log(f"\n❌ ERREUR : {e}")
            import traceback
            self.log(traceback.format_exc())
            self.root.after(0, self.analysis_failed)

    def analysis_complete(self):
        """Appelé quand l'analyse est terminée avec succès"""
        self.progress_bar.stop()
        self.start_button.config(state='normal')
        self.open_excel_button.config(state='normal')
        self.open_report_button.config(state='normal')
        self.open_folder_button.config(state='normal')

        messagebox.showinfo(
            "Succès",
            "L'analyse est terminée !\n\n"
            "✅ Fichiers classés\n"
            "✅ Emails renommés\n"
            "✅ Pièces jointes extraites\n"
            "✅ Excel généré\n"
            "✅ Rapport HTML créé\n\n"
            "Cliquez sur les boutons pour consulter les résultats."
        )

    def analysis_failed(self):
        """Appelé quand l'analyse a échoué"""
        self.progress_bar.stop()
        self.start_button.config(state='normal')

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
