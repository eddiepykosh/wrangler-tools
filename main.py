import os
from dotenv import load_dotenv
from export_to_csv import DatabaseExporter
from reporting import TransactionReporter
from email_utils import send_email_with_attachments

load_dotenv()

def main():
    db_path = os.getenv('DB_PATH')
    timezone = os.getenv('TIMEZONE', 'UTC')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('SMTP_FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')

    # Generate report text
    reporter = TransactionReporter(db_path, timezone)
    report = reporter.generate_full_report()

    # Export CSVs and collect file paths
    exporter = DatabaseExporter()
    csv_files = exporter.export_all()

    # Send email with report and CSV attachments
    subject = f"Transaction Report - {timezone}"
    send_email_with_attachments(
        subject=subject,
        body=report,
        from_email=from_email,
        to_email=to_email,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        smtp_username=smtp_username,
        smtp_password=smtp_password,
        attachment_paths=csv_files
    )

if __name__ == "__main__":
    main()
