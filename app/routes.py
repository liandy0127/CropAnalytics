from flask import request, render_template, redirect, url_for
from app.utils import get_table_names, export_table_to_csv  # upload_file_to_db (commented out)
from app import app

@app.route('/')
def index():
    tables = get_table_names()
    return render_template('index.html', tables=tables)

@app.route('/export_table', methods=['POST'])
def export_table():
    table_name = request.form['table_name']
    export_path = request.form['export_path']
    
    if not table_name or not export_path:
        return "Please provide both table name and export path", 400
    
    try:
        export_file_path = export_table_to_csv(table_name, export_path)
        return f"Table {table_name} exported to {export_file_path}", 200
    except Exception as e:
        return str(e), 500

# @app.route('/upload_file', methods=['POST'])
# def upload_file():
#     table_name = request.form['category']
#     file = request.files['dataFile']
    
#     if not table_name or not file:
#         return "Please provide both table name and file", 400
    
#     file_path = f"/path/to/upload/{file.filename}"  # Adjust the path as necessary
#     file.save(file_path)
    
#     try:
#         upload_file_to_db(file_path, table_name)
#         return f"File {file.filename} uploaded to {table_name}", 200
#     except Exception as e:
#         return str(e), 500
