# 🎓 IamBEE.23

A Python-based command-line chatbot for querying  using natural language.
It supports **voice responses ("text-to-speech")** and answers common operational queries like registration count, admissions, eligibility, fees, and discounts.

---

## 🚀 Features

* 📊 Reads student data from a CSV file (`Dump.csv`)
* 🗣️ Text-to-Speech support using `pyttsx3`
* 🤖 Natural language intent detection (English + Hinglish)
* ⚡ Instant counts & summaries for:

  * Registration
  * Admissions
  * Admission Cancelled
  * Batch Assigned / No Batch
  * Eligible / Not Eligible
  * Fees-based queries
  * Discount-based queries

---

## 📁 Project Structure

```
.
├── Index.py
├── Dump.csv
├── intent_model.pkl
└── README.md
```

---

## 🧾 CSV Requirements

Your CSV file **must contain** the following columns:

| Column Name            |
| ---------------------- |
| fees_paid              |
| status                 |
| free_admission         |
| ay26_enrollment_status |
| form_status            |
| batch                  |
| eligibility_status     |
| % discount             |

> ⚠️ Column names are **case-sensitive**

---

## 🛠️ Installation

### 1️⃣ Install Python Dependencies

```bash
pip install pandas pyttsx3
```

---

## ▶️ How to Run

```bash
python index.py
```

OR (if file name is different)

```bash
python <your_file_name>.py
```

---

## 💬 Supported Queries (Examples)

### 🔹 Registration

```
registration
total students
how many students
```

### 🔹 Admission

```
admission
admitted students
```

### 🔹 Admission Cancelled

```
admission cancelled
```

### 🔹 Batch

```
students with batch
students without batch
```

### 🔹 Eligibility

```
eligible students
not eligible students
```

### 🔹 Fees Queries

```
fees more than 5000
fees less than 3000
fees between 5000 and 10000
```

### 🔹 Discount Queries

```
discount more than 50
discount less than 30
discount between 20 and 60
```

(Hinglish also supported: *zyada, kam, kitne, niche, upar*)

---

## 🗣️ Voice Output

* Bot speaks the **main result**
* Display shows **detailed criteria**
* Speech speed optimized for clarity

---

## 🧠 Logic Highlights

* **Registration Criteria**

  * `fees_paid > 3499`
  * `status == Active`
  * `free_admission == False`

* **Admission**

  * Registration criteria +
  * `ay26_enrollment_status` contains `"Admission"`

* **Batch Logic**

  * `"No Batch"` keyword detection

---

## ❌ Exit Command

```
exit
quit
bye
```

---

## 🔐 Error Handling

* Missing CSV → clean exit
* Missing column → clear error message
* Invalid input → user-friendly prompt

---

## 📌 Author

Built by **Ambikesh Srivastav**
Designed for **operations, analytics & quick decision making**

---

## 📄 License

