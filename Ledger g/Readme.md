# 🍊 KhataBook - Custom Installment Ledger & CRM Application

A professional, custom-built credit management ledger and CRM system designed specifically for manual, installment-based merchant shops. It replaces paper ledger books with an automated audit trail, dynamic balance recalculation, and robust relational checking.

## 🚀 Key Technical Highlights
* **Automated Audit Trails:** Implemented atomic transaction states using Python decorators. Financial updates are calculated dynamically using database aggregations rather than static modifications to prevent ledger mismatch errors.
* **Complex Data Modeling:** Designed a multi-relational database structure separating Customers, Products, independent Guarantor tracking, and individual active Sales Agreements.
* **Custom Responsive UI:** Built completely utilizing pure semantic HTML5 and performance-optimized CSS variables featuring a premium Dark Mode aesthetic with a vibrant color contrast tailored for immediate shop readability.

## 🛠️ Tech Stack
* **Backend Framework:** Django 
* **Environment Manager:** `uv` (Ultra-fast virtual environment tooling)
* **Database Engine:** SQLite (Local development) / Migratable to PostgreSQL/MySQL
* **Frontend styling:** Pure Vanilla CSS

## 📊 Database Architecture Design
The application handles multi-purchase workflows gracefully. If a customer buys an item on installments today and returns next month for a separate asset, the system instantiates separate structural billing instances (rows) instead of corrupting primary customer profile logs.

* **Customer:** Basic identification records enforced by strict unique indexing on Pakistan CNIC and verified mobile records.
* **Product:** Catalog values utilizing `models.PROTECT` behaviors to guarantee historic sale values are preserved even if standard stock items get archived.
* **Sale (Contract Engine):** Computes active variables such as down payments, contract terms, and expected tracking states dynamically.
* **Payment:** Represents isolated ledger credits contributing toward individual underlying contract rows.