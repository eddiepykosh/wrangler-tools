import sqlite3
from datetime import datetime, timedelta
import calendar
import pytz
import os

class TransactionReporter:
    def __init__(self, db_path, timezone='UTC'):
        self.db_path = db_path
        self.timezone = timezone

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def get_totals_for_daterange(self, start_date, end_date):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        category_query = """
        SELECT
            c.name,
            SUM(r.amount) as total
        FROM categories c
        JOIN receipt_categories rc ON c.id = rc.category_id
        JOIN receipts r ON rc.receipt_id = r.id
        WHERE DATE(r.date) BETWEEN ? AND ?
        GROUP BY c.name
        ORDER BY total DESC
        """
        total_query = """
        SELECT SUM(amount)
        FROM receipts
        WHERE DATE(date) BETWEEN ? AND ?
        """
        cursor.execute(category_query, (start_date, end_date))
        categories = cursor.fetchall()
        cursor.execute(total_query, (start_date, end_date))
        grand_total = cursor.fetchone()[0] or 0
        conn.close()
        return categories, grand_total

    def generate_report_section(self, title, start_date, end_date):
        categories, grand_total = self.get_totals_for_daterange(start_date, end_date)
        section = f"\n{title}\n"
        section += "=" * len(title) + "\n"
        if categories:
            for category, total in categories:
                section += f"{category}: ${total:.2f}\n"
            section += f"Total: ${grand_total:.2f}\n"
        else:
            section += "No transactions found for this period.\n"
        return section

    def generate_full_report(self):
        tz = pytz.timezone(self.timezone)
        now = datetime.now(tz)
        last_24h = now - timedelta(days=1)
        last_7d = now - timedelta(days=7)
        last_30d = now - timedelta(days=30)
        monday = now - timedelta(days=now.weekday())
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        sunday = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)
        first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day = calendar.monthrange(now.year, now.month)[1]
        end_of_month = now.replace(day=last_day, hour=23, minute=59, second=59)
        report = "Transaction Report\n"
        report += "=" * 50 + "\n"
        report += f"Generated on: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        report += "=" * 50 + "\n"
        report += self.generate_report_section(
            "Last 24 Hours",
            last_24h.strftime('%Y-%m-%d %H:%M:%S'),
            now.strftime('%Y-%m-%d %H:%M:%S')
        )
        report += self.generate_report_section(
            "Last 7 Days",
            last_7d.strftime('%Y-%m-%d %H:%M:%S'),
            now.strftime('%Y-%m-%d %H:%M:%S')
        )
        report += self.generate_report_section(
            "Last 30 Days",
            last_30d.strftime('%Y-%m-%d %H:%M:%S'),
            now.strftime('%Y-%m-%d %H:%M:%S')
        )
        report += self.generate_report_section(
            "Current Week (Monday-Sunday)",
            monday.strftime('%Y-%m-%d %H:%M:%S'),
            sunday.strftime('%Y-%m-%d %H:%M:%S')
        )
        report += self.generate_report_section(
            f"Current Month ({now.strftime('%B %Y')})",
            first_of_month.strftime('%Y-%m-%d %H:%M:%S'),
            end_of_month.strftime('%Y-%m-%d %H:%M:%S')
        )
        return report
