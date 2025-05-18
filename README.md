<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Developed By Perplexity AI

# Receipt Wrangler Reporting \& Export Tool

This utility is designed as a companion for the [Receipt Wrangler](https://github.com/Receipt-Wrangler) project. It enables advanced reporting and CSV export of your Receipt Wrangler data, and can automatically email you summary reports and database exports.

---

## About

**Receipt Wrangler** is a self-hosted receipt manager with features like OCR/AI receipt scanning, smart categorization, collaborative expense tracking, and seamless workflow integration[^4][^3]. This tool extends your Receipt Wrangler deployment by providing:

- Automated summary reports (by category, over multiple date ranges)
- CSV exports of all key tables and relationships
- Email delivery of reports and exports

---

## Features

- **Automated Transaction Reports:**
Summarizes expenses by category for the last 24 hours, 7 days, 30 days, current week, and current month.
- **CSV Export:**
Exports users, categories, receipts, receipt-categories, and detailed receipt data to CSV files.
- **Email Delivery:**
Sends the generated report and CSV exports to your configured email address.
- **Easy Integration:**
Designed to work directly with your Receipt Wrangler SQLite database.

---

## Project Structure

```
/app
  ├── main.py
  ├── export_to_csv.py
  ├── reporting.py
  ├── email_utils.py
  ├── requirements.txt
  └── ...
```


---

## Prerequisites

- **Receipt Wrangler** instance with access to its SQLite database.
- Python 3.11+
- Docker (optional, for containerized deployment)

---

## Setup

### 1. Environment Variables

Create a `.env` file in the project root with the following:

```env
DB_PATH=/app/your_receipt_wrangler_db.sqlite
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
SMTP_FROM_EMAIL=your_email@example.com
TO_EMAIL=recipient@example.com
TIMEZONE=America/New_York
CSV_OUTPUT_DIR=exports
```

- Adjust `DB_PATH` to point to your Receipt Wrangler SQLite file.
- Set SMTP values to match your email provider.
- `TIMEZONE` should be a valid [tz database name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
- `CSV_OUTPUT_DIR` is optional (defaults to `exports`).

---

### 2. Install Dependencies

If running locally:

```bash
pip install -r requirements.txt
```

If using Docker, dependencies are installed automatically.

---

### 3. Running the Application

#### **With Docker**

Build and run:

```bash
docker build -t receipt-reporter .
docker run --env-file .env receipt-reporter
```


#### **Locally**

```bash
python main.py
```


---

## Usage

- **Automated Report \& Email:**
Running `main.py` will generate a summary report and email it (with CSV attachments) to the configured recipient.
- **Manual CSV Export:**
You can run the export utility directly for manual exports:

```bash
python export_to_csv.py
```

This will generate CSVs for all tables in the directory specified by `CSV_OUTPUT_DIR`.

---

## Output

- **Email:**
The recipient will receive an email with the transaction summary and CSVs attached.
- **CSV Files:**
    - `users.csv`
    - `categories.csv`
    - `receipts.csv`
    - `receipt_categories.csv`
    - `receipts_detailed.csv`

All CSVs are saved to the `exports/` directory (or your configured output directory).

---

## Requirements

- Python 3.11+
- Access to a Receipt Wrangler SQLite database with the following tables:
    - `Users`
    - `categories`
    - `receipts`
    - `receipt_categories`

---

## Integration with Receipt Wrangler

This tool is intended for use alongside your [Receipt Wrangler](https://github.com/Receipt-Wrangler) deployment.
It does not modify your Receipt Wrangler data, but provides enhanced reporting and export capabilities for analysis, backup, or migration[^4][^3].

---

## License

MIT License (or your chosen license)

---

## Author

Developed By Perplexity AI

---

*For questions or issues, please open an issue or contact the maintainer.*

<div style="text-align: center">⁂</div>

[^1]: export_to_csv.py

[^2]: main.py

[^3]: https://github.com/Receipt-Wrangler

[^4]: https://www.reddit.com/r/selfhosted/comments/15kxfqk/introducing_receipt_wrangler_a_selfhosted_receipt/

[^5]: https://receiptwrangler.io/docs/5.x/development/installation/

[^6]: https://receiptwrangler.io

[^7]: https://selfhostedworld.com/software/receipt-wrangler

[^8]: https://github.com/Receipt-Wrangler/receipt-wrangler-api

[^9]: https://mariushosting.com/how-to-install-receipt-wrangler-on-your-synology-nas/

[^10]: https://www.facts.dev/p/receipt-wrangler/

[^11]: https://formable.app/receipt-wrangler/

[^12]: https://forums.unraid.net/topic/158730-receipt-wrangler-mariadb-setup/

