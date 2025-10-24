"""
Module de génération de rapports HTML interactifs
Génère des rapports avec tableaux, graphiques et arborescence
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from .scanner import FileInfo
from .extractor import AttachmentInfo


class HTMLReporter:
    """Générateur de rapports HTML interactifs"""

    def __init__(self, output_path: str):
        """
        Initialise le générateur de rapports

        Args:
            output_path: Chemin du fichier HTML de sortie
        """
        self.output_path = Path(output_path)
        self.files: List[FileInfo] = []
        self.attachments: List[AttachmentInfo] = []
        self.stats: Dict = {}

    def generate_report(self, files: List[FileInfo],
                       attachments: Optional[List[AttachmentInfo]] = None,
                       stats: Optional[Dict] = None,
                       title: str = "Rapport d'Analyse"):
        """
        Génère le rapport HTML complet

        Args:
            files: Liste des fichiers
            attachments: Liste des pièces jointes (optionnel)
            stats: Statistiques (optionnel)
            title: Titre du rapport
        """
        self.files = files
        self.attachments = attachments or []
        self.stats = stats or {}

        html = self._generate_html(title)

        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"📊 Rapport HTML généré: {self.output_path}")

    def _generate_html(self, title: str) -> str:
        """
        Génère le code HTML complet

        Args:
            title: Titre du rapport

        Returns:
            Code HTML
        """
        return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    <div class="container">
        {self._generate_header(title)}
        {self._generate_stats_cards()}
        {self._generate_charts_section()}
        {self._generate_files_table()}
        {self._generate_attachments_section()}
        {self._generate_footer()}
    </div>

    <script>
        {self._generate_javascript()}
    </script>
</body>
</html>
"""

    def _get_css(self) -> str:
        """Retourne le CSS du rapport"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        header p {
            opacity: 0.9;
            font-size: 1.1em;
        }

        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }

        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        }

        .stat-card .icon {
            font-size: 3em;
            margin-bottom: 10px;
        }

        .stat-card .value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }

        .stat-card .label {
            color: #666;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .section {
            padding: 40px;
        }

        .section h2 {
            font-size: 1.8em;
            margin-bottom: 25px;
            color: #333;
            border-left: 5px solid #667eea;
            padding-left: 15px;
        }

        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }

        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .chart-container h3 {
            margin-bottom: 15px;
            color: #555;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        thead {
            background: #667eea;
            color: white;
        }

        th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
        }

        th:hover {
            background: #5568d3;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }

        tbody tr:hover {
            background: #f8f9fa;
        }

        tbody tr:last-child td {
            border-bottom: none;
        }

        .filter-container {
            margin: 20px 0;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }

        .filter-input {
            flex: 1;
            min-width: 250px;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 1em;
            transition: border-color 0.3s ease;
        }

        .filter-input:focus {
            outline: none;
            border-color: #667eea;
        }

        .filter-select {
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 1em;
            background: white;
            cursor: pointer;
        }

        .export-btn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .export-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }

        footer {
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }

        .badge-technical {
            background: #d4edda;
            color: #155724;
        }

        .badge-correspondence {
            background: #d1ecf1;
            color: #0c5460;
        }

        .badge-other {
            background: #f8d7da;
            color: #721c24;
        }

        @media (max-width: 768px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }

            .stats-container {
                grid-template-columns: 1fr;
            }

            header h1 {
                font-size: 1.8em;
            }
        }
        """

    def _generate_header(self, title: str) -> str:
        """Génère l'en-tête du rapport"""
        generation_date = datetime.now().strftime('%d/%m/%Y à %H:%M:%S')
        return f"""
        <header>
            <h1>📊 {title}</h1>
            <p>Généré le {generation_date}</p>
        </header>
        """

    def _generate_stats_cards(self) -> str:
        """Génère les cartes de statistiques"""
        total_files = len(self.files)
        total_size_mb = sum(f.size_mb for f in self.files)
        total_emails = sum(1 for f in self.files if f.is_email)
        total_attachments = len(self.attachments)

        return f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="icon">📁</div>
                <div class="value">{total_files}</div>
                <div class="label">Fichiers</div>
            </div>
            <div class="stat-card">
                <div class="icon">💾</div>
                <div class="value">{total_size_mb:.1f} MB</div>
                <div class="label">Taille totale</div>
            </div>
            <div class="stat-card">
                <div class="icon">📧</div>
                <div class="value">{total_emails}</div>
                <div class="label">Emails</div>
            </div>
            <div class="stat-card">
                <div class="icon">📎</div>
                <div class="value">{total_attachments}</div>
                <div class="label">Pièces jointes</div>
            </div>
        </div>
        """

    def _generate_charts_section(self) -> str:
        """Génère la section des graphiques"""
        return """
        <div class="section">
            <h2>📈 Visualisations</h2>
            <div class="charts-grid">
                <div class="chart-container">
                    <h3>Répartition par type</h3>
                    <canvas id="typeChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Répartition par extension</h3>
                    <canvas id="extensionChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Top 10 - Fichiers par taille</h3>
                    <canvas id="sizeChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Distribution temporelle</h3>
                    <canvas id="dateChart"></canvas>
                </div>
            </div>
        </div>
        """

    def _generate_files_table(self) -> str:
        """Génère le tableau des fichiers"""
        rows = []
        for file in self.files:
            badge_class = {
                "Dossier technique": "badge-technical",
                "Correspondance": "badge-correspondence",
                "Autres fichiers": "badge-other"
            }.get(file.file_type, "badge-other")

            rows.append(f"""
            <tr>
                <td><span class="badge {badge_class}">{file.file_type}</span></td>
                <td><a href="file:///{file.path}" target="_blank">{file.name}</a></td>
                <td>{file.extension}</td>
                <td>{file.size_kb:.2f} KB</td>
                <td>{file.modified_date}</td>
                <td>{file.parent_folder}</td>
            </tr>
            """)

        return f"""
        <div class="section">
            <h2>📋 Liste des fichiers</h2>
            <div class="filter-container">
                <input type="text" id="searchInput" class="filter-input" placeholder="🔍 Rechercher un fichier...">
                <select id="typeFilter" class="filter-select">
                    <option value="">Tous les types</option>
                    <option value="Dossier technique">Dossier technique</option>
                    <option value="Correspondance">Correspondance</option>
                    <option value="Autres fichiers">Autres fichiers</option>
                </select>
                <button class="export-btn" onclick="exportToCSV()">📥 Exporter CSV</button>
            </div>
            <table id="filesTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Type ⬍</th>
                        <th onclick="sortTable(1)">Nom ⬍</th>
                        <th onclick="sortTable(2)">Extension ⬍</th>
                        <th onclick="sortTable(3)">Taille ⬍</th>
                        <th onclick="sortTable(4)">Modifié le ⬍</th>
                        <th onclick="sortTable(5)">Dossier ⬍</th>
                    </tr>
                </thead>
                <tbody id="filesTableBody">
                    {''.join(rows)}
                </tbody>
            </table>
        </div>
        """

    def _generate_attachments_section(self) -> str:
        """Génère la section des pièces jointes"""
        if not self.attachments:
            return ""

        rows = []
        for att in self.attachments:
            rows.append(f"""
            <tr>
                <td><a href="file:///{att.saved_path}" target="_blank">{att.saved_filename}</a></td>
                <td>{att.size_kb:.2f} KB</td>
                <td>{att.email_source}</td>
                <td>{att.email_subject}</td>
                <td>{att.email_date}</td>
            </tr>
            """)

        return f"""
        <div class="section">
            <h2>📎 Pièces jointes extraites</h2>
            <table>
                <thead>
                    <tr>
                        <th>Fichier</th>
                        <th>Taille</th>
                        <th>Email source</th>
                        <th>Sujet</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        </div>
        """

    def _generate_footer(self) -> str:
        """Génère le pied de page"""
        return """
        <footer>
            <p>Généré par <strong>AnalystHelper</strong> - Outil d'aide à l'analyse de dossiers</p>
        </footer>
        """

    def _generate_javascript(self) -> str:
        """Génère le JavaScript pour l'interactivité"""
        # Préparer les données pour les graphiques
        type_data = {}
        extension_data = {}
        for file in self.files:
            type_data[file.file_type] = type_data.get(file.file_type, 0) + 1
            extension_data[file.extension] = extension_data.get(file.extension, 0) + 1

        # Top 10 fichiers par taille
        sorted_files = sorted(self.files, key=lambda f: f.size_mb, reverse=True)[:10]

        # Distribution par mois
        date_data = {}
        for file in self.files:
            month = file.modified_date[:7]  # YYYY-MM
            date_data[month] = date_data.get(month, 0) + 1

        return f"""
        // Données
        const filesData = {json.dumps([f.to_dict() for f in self.files])};
        const typeData = {json.dumps(type_data)};
        const extensionData = {json.dumps(extension_data)};

        // Graphique par type
        new Chart(document.getElementById('typeChart'), {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(typeData),
                datasets: [{{
                    data: Object.values(typeData),
                    backgroundColor: ['#4CAF50', '#2196F3', '#FF9800']
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'bottom' }}
                }}
            }}
        }});

        // Graphique par extension (top 10)
        const topExtensions = Object.entries(extensionData)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);

        new Chart(document.getElementById('extensionChart'), {{
            type: 'bar',
            data: {{
                labels: topExtensions.map(e => e[0]),
                datasets: [{{
                    label: 'Nombre de fichiers',
                    data: topExtensions.map(e => e[1]),
                    backgroundColor: '#667eea'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});

        // Graphique par taille
        new Chart(document.getElementById('sizeChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps([f.name[:20] + '...' if len(f.name) > 20 else f.name for f in sorted_files])},
                datasets: [{{
                    label: 'Taille (MB)',
                    data: {json.dumps([f.size_mb for f in sorted_files])},
                    backgroundColor: '#764ba2'
                }}]
            }},
            options: {{
                responsive: true,
                indexAxis: 'y',
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});

        // Graphique temporel
        const dateData = {json.dumps(date_data)};
        const sortedDates = Object.keys(dateData).sort();

        new Chart(document.getElementById('dateChart'), {{
            type: 'line',
            data: {{
                labels: sortedDates,
                datasets: [{{
                    label: 'Fichiers modifiés',
                    data: sortedDates.map(d => dateData[d]),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});

        // Filtrage du tableau
        document.getElementById('searchInput').addEventListener('keyup', filterTable);
        document.getElementById('typeFilter').addEventListener('change', filterTable);

        function filterTable() {{
            const searchValue = document.getElementById('searchInput').value.toLowerCase();
            const typeValue = document.getElementById('typeFilter').value;
            const tbody = document.getElementById('filesTableBody');
            const rows = tbody.getElementsByTagName('tr');

            for (let row of rows) {{
                const cells = row.getElementsByTagName('td');
                const type = cells[0].textContent;
                const name = cells[1].textContent.toLowerCase();

                const matchSearch = name.includes(searchValue);
                const matchType = !typeValue || type.includes(typeValue);

                row.style.display = (matchSearch && matchType) ? '' : 'none';
            }}
        }}

        // Tri du tableau
        function sortTable(columnIndex) {{
            const table = document.getElementById('filesTable');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));

            rows.sort((a, b) => {{
                const aValue = a.cells[columnIndex].textContent;
                const bValue = b.cells[columnIndex].textContent;

                if (columnIndex === 3) {{ // Taille
                    return parseFloat(bValue) - parseFloat(aValue);
                }}
                return aValue.localeCompare(bValue);
            }});

            rows.forEach(row => tbody.appendChild(row));
        }}

        // Export CSV
        function exportToCSV() {{
            const rows = [
                ['Type', 'Nom', 'Extension', 'Taille (KB)', 'Modifié le', 'Dossier', 'Chemin'],
                ...filesData.map(f => [
                    f.file_type,
                    f.name,
                    f.extension,
                    f.size_kb,
                    f.modified_date,
                    f.parent_folder,
                    f.path
                ])
            ];

            const csv = rows.map(row => row.map(cell =>
                `"${{String(cell).replace(/"/g, '""')}}"`
            ).join(',')).join('\\n');

            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'fichiers_' + new Date().toISOString().slice(0,10) + '.csv';
            link.click();
        }}
        """
