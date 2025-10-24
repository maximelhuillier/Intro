#!/usr/bin/env python3
"""
Interface Graphique pour AnalystHelper
Permet d'utiliser l'outil sans connaître Python
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import webbrowser
from pathlib import Path


class AnalystHelperGUI:
    """Interface graphique pour AnalystHelper"""

    def __init__(self, root):
        self.root = root
        self.root.title("📊 AnalystHelper - Analyse de Dossiers")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Variables
        self.folder_path = tk.StringVar()
        self.output_path = tk.StringVar(value=str(Path.home() / "AnalystHelper_Output"))
        self.do_classify = tk.BooleanVar(value=True)
        self.do_extract = tk.BooleanVar(value=True)
        self.exclude_folders = tk.StringVar(value=".git, node_modules, __pycache__, temp")

        # Créer l'interface
        self.create_widgets()

        # Centrer la fenêtre
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
        header_frame = tk.Frame(self.root, bg='#667eea', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="📊 AnalystHelper",
            font=('Arial', 24, 'bold'),
            bg='#667eea',
            fg='white'
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            header_frame,
            text="Analysez vos dossiers en quelques clics",
            font=('Arial', 12),
            bg='#667eea',
            fg='white'
        )
        subtitle_label.pack()

        # ===== CORPS PRINCIPAL =====
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill='both', expand=True)

        # --- Section 1 : Sélection du dossier ---
        section1 = ttk.LabelFrame(main_frame, text="📁 Dossier à analyser", padding="10")
        section1.pack(fill='x', pady=(0, 10))

        folder_frame = ttk.Frame(section1)
        folder_frame.pack(fill='x')

        ttk.Entry(
            folder_frame,
            textvariable=self.folder_path,
            width=60,
            font=('Arial', 10)
        ).pack(side='left', fill='x', expand=True, padx=(0, 5))

        ttk.Button(
            folder_frame,
            text="📂 Parcourir",
            command=self.browse_folder
        ).pack(side='left')

        # --- Section 2 : Options ---
        section2 = ttk.LabelFrame(main_frame, text="⚙️ Options", padding="10")
        section2.pack(fill='x', pady=(0, 10))

        ttk.Checkbutton(
            section2,
            text="📁 Classifier les fichiers par type (Dossier technique, Correspondance, Autres)",
            variable=self.do_classify
        ).pack(anchor='w', pady=2)

        ttk.Checkbutton(
            section2,
            text="📎 Extraire les pièces jointes des emails (.msg, .eml)",
            variable=self.do_extract
        ).pack(anchor='w', pady=2)

        # Dossiers à exclure
        exclude_frame = ttk.Frame(section2)
        exclude_frame.pack(fill='x', pady=(10, 0))

        ttk.Label(
            exclude_frame,
            text="🚫 Dossiers à exclure (séparés par des virgules) :",
            font=('Arial', 9)
        ).pack(anchor='w')

        ttk.Entry(
            exclude_frame,
            textvariable=self.exclude_folders,
            width=60,
            font=('Arial', 9)
        ).pack(fill='x', pady=(5, 0))

        # --- Section 3 : Dossier de sortie ---
        section3 = ttk.LabelFrame(main_frame, text="💾 Dossier de sortie", padding="10")
        section3.pack(fill='x', pady=(0, 10))

        output_frame = ttk.Frame(section3)
        output_frame.pack(fill='x')

        ttk.Entry(
            output_frame,
            textvariable=self.output_path,
            width=60,
            font=('Arial', 10)
        ).pack(side='left', fill='x', expand=True, padx=(0, 5))

        ttk.Button(
            output_frame,
            text="📂 Changer",
            command=self.browse_output
        ).pack(side='left')

        # --- Section 4 : Actions ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill='x', pady=(10, 10))

        self.start_button = tk.Button(
            action_frame,
            text="🚀 Lancer l'Analyse",
            command=self.start_analysis,
            bg='#667eea',
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2,
            cursor='hand2'
        )
        self.start_button.pack(fill='x')

        # --- Section 5 : Progression ---
        section4 = ttk.LabelFrame(main_frame, text="📊 Progression", padding="10")
        section4.pack(fill='both', expand=True)

        self.progress_bar = ttk.Progressbar(
            section4,
            mode='indeterminate',
            length=300
        )
        self.progress_bar.pack(fill='x', pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(
            section4,
            height=12,
            font=('Courier', 9),
            bg='#f8f9fa',
            fg='#333333'
        )
        self.log_text.pack(fill='both', expand=True)
        self.log_text.config(state='disabled')

        # --- Section 6 : Résultats ---
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill='x', pady=(10, 0))

        self.open_report_button = tk.Button(
            result_frame,
            text="📄 Ouvrir le Rapport HTML",
            command=self.open_report,
            bg='#28a745',
            fg='white',
            font=('Arial', 11, 'bold'),
            state='disabled',
            cursor='hand2'
        )
        self.open_report_button.pack(side='left', fill='x', expand=True, padx=(0, 5))

        self.open_folder_button = tk.Button(
            result_frame,
            text="📂 Ouvrir le Dossier",
            command=self.open_output_folder,
            bg='#17a2b8',
            fg='white',
            font=('Arial', 11, 'bold'),
            state='disabled',
            cursor='hand2'
        )
        self.open_folder_button.pack(side='left', fill='x', expand=True)

    def browse_folder(self):
        """Ouvre un dialogue pour sélectionner le dossier à analyser"""
        folder = filedialog.askdirectory(title="Sélectionner le dossier à analyser")
        if folder:
            self.folder_path.set(folder)

    def browse_output(self):
        """Ouvre un dialogue pour sélectionner le dossier de sortie"""
        folder = filedialog.askdirectory(title="Sélectionner le dossier de sortie")
        if folder:
            self.output_path.set(folder)

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
            f"Les résultats seront enregistrés dans :\n{self.output_path.get()}\n\n"
            "Continuer ?"
        )

        if not result:
            return

        # Désactiver le bouton
        self.start_button.config(state='disabled')
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
            from analyst_helper import FolderScanner, FileClassifier, AttachmentExtractor, HTMLReporter

            output_dir = Path(self.output_path.get())
            output_dir.mkdir(parents=True, exist_ok=True)

            # Récupérer les dossiers à exclure
            exclude = [f.strip() for f in self.exclude_folders.get().split(',') if f.strip()]

            # Étape 1 : Scanner
            self.log("=" * 60)
            self.log("ÉTAPE 1/4 : SCAN DU DOSSIER")
            self.log("=" * 60)

            scanner = FolderScanner(self.folder_path.get())
            files = scanner.scan(exclude_folders=exclude)

            self.log(f"✅ {len(files)} fichiers trouvés")
            self.log(f"   Taille totale : {scanner.stats['total_size_mb']:.2f} MB")
            self.log(f"   Emails : {scanner.stats['total_emails']}")

            # Export CSV/JSON
            scanner.export_to_csv(str(output_dir / "fichiers.csv"))
            scanner.export_to_json(str(output_dir / "fichiers.json"))

            # Étape 2 : Classification
            if self.do_classify.get():
                self.log("\n" + "=" * 60)
                self.log("ÉTAPE 2/4 : CLASSIFICATION DES FICHIERS")
                self.log("=" * 60)

                classifier = FileClassifier(str(output_dir / "fichiers_classés"))
                classifier.classify_all(files, copy=True)

                self.log(f"✅ {classifier.stats['total_copied']} fichiers classés")
                for category, count in classifier.stats['by_category'].items():
                    if count > 0:
                        self.log(f"   {category}: {count}")
            else:
                self.log("\n⏭️  Classification ignorée")

            # Étape 3 : Extraction PJ
            attachments = []
            if self.do_extract.get() and scanner.stats['total_emails'] > 0:
                self.log("\n" + "=" * 60)
                self.log("ÉTAPE 3/4 : EXTRACTION DES PIÈCES JOINTES")
                self.log("=" * 60)

                extractor = AttachmentExtractor(str(output_dir / "pièces_jointes"))
                email_files = [f.path for f in files if f.is_email]

                try:
                    attachments = extractor.extract_all(email_files, show_progress=False)
                    self.log(f"✅ {len(attachments)} pièces jointes extraites")
                except ImportError:
                    self.log("⚠️  Module 'extract-msg' non installé")
                    self.log("   Installation : pip install extract-msg")
                except Exception as e:
                    self.log(f"❌ Erreur lors de l'extraction : {e}")
            else:
                self.log("\n⏭️  Extraction de PJ ignorée")

            # Étape 4 : Rapport HTML
            self.log("\n" + "=" * 60)
            self.log("ÉTAPE 4/4 : GÉNÉRATION DU RAPPORT HTML")
            self.log("=" * 60)

            reporter = HTMLReporter(str(output_dir / "rapport_analyse.html"))
            reporter.generate_report(
                files=files,
                attachments=attachments,
                stats=scanner.stats,
                title=f"Analyse - {Path(self.folder_path.get()).name}"
            )

            self.log("✅ Rapport HTML généré")

            # Fin
            self.log("\n" + "=" * 60)
            self.log("✅ ANALYSE TERMINÉE")
            self.log("=" * 60)
            self.log(f"\n📂 Résultats disponibles dans :")
            self.log(f"   {output_dir}")

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
        self.open_report_button.config(state='normal')
        self.open_folder_button.config(state='normal')

        messagebox.showinfo(
            "Succès",
            "L'analyse est terminée !\n\n"
            "Cliquez sur 'Ouvrir le Rapport HTML' pour voir les résultats."
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

    def open_report(self):
        """Ouvre le rapport HTML dans le navigateur"""
        report_path = Path(self.output_path.get()) / "rapport_analyse.html"
        if report_path.exists():
            webbrowser.open(f'file://{report_path.resolve()}')
        else:
            messagebox.showerror("Erreur", "Le rapport n'existe pas encore")

    def open_output_folder(self):
        """Ouvre le dossier de sortie"""
        output_dir = Path(self.output_path.get())
        if output_dir.exists():
            if sys.platform == 'win32':
                os.startfile(output_dir)
            elif sys.platform == 'darwin':
                os.system(f'open "{output_dir}"')
            else:
                os.system(f'xdg-open "{output_dir}"')
        else:
            messagebox.showerror("Erreur", "Le dossier de sortie n'existe pas encore")


def main():
    """Fonction principale"""
    root = tk.Tk()

    # Icône (optionnel)
    try:
        # Si vous avez un fichier icon.ico
        root.iconbitmap('icon.ico')
    except:
        pass

    app = AnalystHelperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
