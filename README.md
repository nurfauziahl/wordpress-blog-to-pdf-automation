# Blog to PDF Automation (WordPress)

## 📌 Project Overview
Manually saving hundreds of blog posts into PDFs is extremely time-consuming.  
In this project, I built a **Python automation pipeline** that converts WordPress blog posts into clean, structured PDF files and merges them into a single document.

Instead of clicking **500+ times**, the entire process is handled automatically using a WordPress REST API–driven workflow.

This repository demonstrates:
- Web data extraction
- API-based content collection
- Automated PDF generation
- PDF merging and file management

---

## 🎯 Problem Statement
A WordPress health blog contains **500+ published articles**.  
Manually saving each article as a PDF would take **hours or days** and is highly error-prone.

---

## ✅ Solution
I developed a Python-based automation that:

1. Fetches all blog post URLs using the **WordPress REST API**
2. Converts each article page into a PDF using **wkhtmltopdf**
3. Automatically merges multiple PDFs into a single compiled document
4. Supports **resume & skip logic** to avoid reprocessing existing files

For portfolio demonstration, the script is configured to generate **10 sample PDFs**, but it can scale to the full dataset.

---

## 🧰 Tech Stack
- **Python 3**
- **requests** – REST API communication
- **BeautifulSoup** – HTML parsing (optional / fallback)
- **wkhtmltopdf** – HTML to PDF rendering
- **pdfkit** – Python wrapper for wkhtmltopdf
- **pypdf** – PDF merging

---

## 📂 Project Structure
```text
drthomashealthblog_to_pdf/
├─ src/
│  ├─ main.py          # Orchestrates the full workflow
│  ├─ wp_api.py        # Fetches post URLs from WordPress REST API
│  ├─ renderer.py      # Converts URLs to PDFs
│  ├─ merger.py        # Merges PDFs
│  └─ utils.py         # Helper utilities (slug generation, etc.)
│
├─ data/
│  ├─ intermediate/    # Individual PDF files (generated)
│  └─ output/          # Final merged PDF
│
├─ logs/               # Failed URL logs (optional)
├─ requirements.txt
├─ .gitignore
└─ README.md
```

# 📑 Blog to PDF: Automated Archiving Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Automation](https://img.shields.io/badge/Focus-Automation-green?style=for-the-badge)

---

## ✨ Key Features

* **API-Driven Scraping:** Uses the official WordPress REST API endpoints for reliable data extraction (no fragile HTML parsing).
* **Smart Resume Logic:** Skips already generated PDFs to save time if the script is restarted.
* **Rate Limiting:** Includes polite delays to avoid overloading the target server.
* **Automated Merging:** Combines hundreds of individual PDFs into one organized file (`drthomashealthblog-full.pdf`).
* **Scalable:** Designed to handle anywhere from 10 to 500+ documents seamlessly.

---

## 🛠️ Prerequisites

Before running the script, ensure you have the following installed:

1.  **Python 3.14.2**
2.  **wkhtmltopdf** (System-level dependency required for PDF generation)

To verify `wkhtmltopdf` installation:
```bash
wkhtmltopdf --version

## ▶️ How to Run

Follow these steps to set up and run the automation pipeline.

---

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/drthomashealthblog_to_pdf.git
cd drthomashealthblog_to_pdf
```

---

### 2️⃣ Set Up Virtual Environment
It is recommended to run this project in an isolated Python environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows users:**
```bash
.venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Script
Execute the main module to start the fetching and conversion process:

```bash
python -m src.main
```

> **Note:**  
> By default, the script generates **10 sample PDFs** for demonstration purposes.  
> This value can be adjusted inside `main.py`.

---

## 📂 Output Structure

The script automatically organizes files as follows:

```text
data/
├── intermediate/
│   └── pdf/
│       ├── 0001-p-12345.pdf   # Individual article PDFs
│       └── ...
└── output/
    └── drthomashealthblog-full.pdf   # Final merged PDF
```

---

## ⚠️ Ethical & Technical Notes

- **Compliance:**  
  This tool strictly uses public **WordPress REST API** endpoints.

- **Rate Limits:**  
  The script implements request delays to respect the host server’s resources.

- **Purpose:**  
  Intended solely for **offline archiving** and **automation demonstration**.

- **Ownership:**  
  All generated content remains the property of the original publisher.

---

## 👤 Author

**Nur Fauziah**  
Pharmacist | Healthcare Data & Automation  

Specializing in replacing manual clinical and business workflows with efficient Python-based solutions.

**Focus:**  
Python · Data Processing · Workflow Automation  

**Connect:**  
[www.linkedin.com/in/nurfauziahl]
