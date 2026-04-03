# 🍜 Soto Kwali Mbah Cipto: Cashier Management System

Hi there! [cite_start]Welcome to the **Soto Kwali Mbah Cipto** repository. [cite: 1]

[cite_start]This is a Point of Sale (POS) application built with Python to streamline the ordering process for a traditional Indonesian soup shop. [cite: 1] [cite_start]It helps cashiers record customer orders, calculate totals and change, and generate digital receipts automatically. [cite: 1]

This project features two versions:
1. [cite_start]**Visual Version (GUI):** A modern interface with buttons and tabs built using the KivyMD library. [cite: 1] (Main file: `main_app.py`).
2. [cite_start]**Terminal Version (CLI):** A lightweight, text-based version for quick interactions via the command line. [cite: 1] (Main file: `code.py`).

---

## ✨ Key Features

* [cite_start]**Categorized Menu:** Food and drinks are organized into separate tabs for easy navigation. [cite: 2, 3]
* [cite_start]**Cart Management:** Add items with specific quantities and see your total updated in real-time. [cite: 1, 8]
* [cite_start]**Menu Editor (CRUD):** You can Add, Edit, or Delete menu items directly through the app UI. [cite: 1, 13]
* [cite_start]**Automatic Calculations:** The system handles all the math for totals and change based on the amount paid. [cite: 1]
* [cite_start]**Digital Receipts:** Generates a structured receipt upon successful payment. [cite: 1, 42]
* [cite_start]**Transaction Logging:** All completed sales are automatically logged into `transactions.csv` for easy reporting. [cite: 1]

---

## 📂 Project Structure

Here’s a quick breakdown of the core files:

* [cite_start]`main_app.py` ➔ **The Brain.** Contains the main application logic and GUI management. [cite: 1]
* [cite_start]`sotokiv.kv` ➔ **The Designer.** Handles the styling, layout, and UI components using Kivy language. [cite: 2]
* [cite_start]`code.py` ➔ A standalone CLI version of the cashier system. [cite: 1]
* [cite_start]`makanan_data.json` & `minuman_data.json` ➔ **The Database.** Stores the menu items and prices persistently. [cite: 1]
* [cite_start]`requirements.txt` ➔ Lists all the necessary libraries (like Kivy and KivyMD) to run the project. [cite: 1]

---

## 🚀 Getting Started

Follow these steps to run the application on your local machine:

### 1. Install Dependencies
Make sure you have Python installed. Then, install the required libraries using pip:

```bash
pip install -r requirements.txt
