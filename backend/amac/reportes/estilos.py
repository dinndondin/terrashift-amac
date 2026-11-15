"""Componente amac.reportes.estilos; lógica extraída de report_generator.py."""




_CSS = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        background: #f5f7fa;
        padding: 20px;
    }
    .report-container {
        max-width: 900px;
        margin: 0 auto;
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        overflow: hidden;
    }
    .header {
        background: linear-gradient(135deg, #1a7a3a 0%, #2d9b4e 100%);
        color: white;
        padding: 30px 40px;
    }
    .header h1 {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .header .subtitle {
        font-size: 14px;
        opacity: 0.9;
    }
    .header .meta {
        margin-top: 15px;
        font-size: 13px;
        opacity: 0.8;
    }
    .content { padding: 30px 40px; }
    .section {
        margin-bottom: 30px;
        border-bottom: 1px solid #eee;
        padding-bottom: 25px;
    }
    .section:last-child { border-bottom: none; }
    .section h2 {
        color: #1a7a3a;
        font-size: 20px;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e8f5e9;
    }
    .section h3 {
        color: #444;
        font-size: 16px;
        margin: 12px 0 8px 0;
    }
    .summary-box {
        background: #e8f5e9;
        border-left: 4px solid #1a7a3a;
        padding: 15px 20px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
    }
    .alert-box {
        padding: 12px 18px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 14px;
    }
    .alert-warning {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        color: #e65100;
    }
    .alert-danger {
        background: #ffebee;
        border-left: 4px solid #f44336;
        color: #c62828;
    }
    .alert-info {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #0d47a1;
    }
    .alert-success {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        color: #1b5e20;
    }
    .data-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        margin: 15px 0;
    }
    .data-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .data-card .value {
        font-size: 24px;
        font-weight: 700;
        color: #1a7a3a;
    }
    .data-card .label {
        font-size: 12px;
        color: #666;
        margin-top: 4px;
    }
    .score-bar {
        width: 100%;
        height: 8px;
        background: #e0e0e0;
        border-radius: 4px;
        overflow: hidden;
        margin: 4px 0;
    }
    .score-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s;
    }
    .score-high { background: #4caf50; }
    .score-medium { background: #ff9800; }
    .score-low { background: #f44336; }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
    }
    th, td {
        padding: 10px 12px;
        text-align: left;
        border-bottom: 1px solid #eee;
        font-size: 14px;
    }
    th {
        background: #f8f9fa;
        font-weight: 600;
        color: #555;
    }
    ul { padding-left: 20px; margin: 8px 0; }
    li { margin-bottom: 4px; font-size: 14px; }
    .footer {
        background: #f8f9fa;
        padding: 20px 40px;
        font-size: 12px;
        color: #888;
        text-align: center;
    }
    .action-item {
        display: flex;
        align-items: flex-start;
        padding: 10px 0;
        border-bottom: 1px dashed #e0e0e0;
    }
    .action-number {
        background: #1a7a3a;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        margin-right: 12px;
        flex-shrink: 0;
    }
</style>
"""
