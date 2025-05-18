import sqlite3
import csv
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class DatabaseExporter:
    def __init__(self):
        self.db_path = os.getenv('DB_PATH')
        self.output_dir = os.getenv('CSV_OUTPUT_DIR', 'exports')
        Path(self.output_dir).mkdir(exist_ok=True)

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def export_users(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, display_name FROM Users")
        users = cursor.fetchall()
        output_path = os.path.join(self.output_dir, 'users.csv')
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'display_name'])
            writer.writerows(users)
        conn.close()
        return output_path

    def export_categories(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        output_path = os.path.join(self.output_dir, 'categories.csv')
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'name'])
            writer.writerows(categories)
        conn.close()
        return output_path

    def export_receipts(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, created_by, name, amount, date, status FROM receipts")
        receipts = cursor.fetchall()
        output_path = os.path.join(self.output_dir, 'receipts.csv')
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'created_by', 'name', 'amount', 'date', 'status'])
            writer.writerows(receipts)
        conn.close()
        return output_path

    def export_receipt_categories(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT receipt_id, category_id FROM receipt_categories")
        receipt_categories = cursor.fetchall()
        output_path = os.path.join(self.output_dir, 'receipt_categories.csv')
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['receipt_id', 'category_id'])
            writer.writerows(receipt_categories)
        conn.close()
        return output_path

    def export_receipts_with_details(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT
            r.id,
            u.display_name as created_by,
            r.name,
            r.amount,
            r.date,
            r.status,
            GROUP_CONCAT(c.name) as categories
        FROM receipts r
        LEFT JOIN Users u ON r.created_by = u.id
        LEFT JOIN receipt_categories rc ON r.id = rc.receipt_id
        LEFT JOIN categories c ON rc.category_id = c.id
        GROUP BY r.id
        ORDER BY r.date DESC
        """
        cursor.execute(query)
        detailed_receipts = cursor.fetchall()
        output_path = os.path.join(self.output_dir, 'receipts_detailed.csv')
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'created_by', 'name', 'amount', 'date', 'status', 'categories'])
            writer.writerows(detailed_receipts)
        conn.close()
        return output_path

    def export_all(self):
        files = []
        files.append(self.export_users())
        files.append(self.export_categories())
        files.append(self.export_receipts())
        files.append(self.export_receipt_categories())
        files.append(self.export_receipts_with_details())
        return files
