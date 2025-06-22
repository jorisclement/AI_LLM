# 📧 Email Generator from Excel using Jinja2

This Python script automates the creation of personalized email text files using data from an Excel spreadsheet and a Jinja2 template. It is especially useful for generating bulk emails or letters for clients or contacts.

---

## ✨ Features

- Load client data from an Excel file.
- Use a Jinja2 template to render personalized content.
- Output one `.txt` file per client into a specified folder.
- Command-line interface with customizable input and output options.

---

## 📂 Project Structure

```
llm_app_excel/

├── email_to_client/
│   ├── output.txt      # (output files go here)
├── LLM_excel.py
├── email_template.j2
├── dossier_client.xlsx  # (Here is the excel input file)
└── README.md
```

---

## 🔧 Requirements

- Python 3.8+
- `pandas`
- `jinja2`
- `lmstudio` (for optional LLM interaction)

Install dependencies:

```bash
pip install -r requirement.txt
```

---

## 🚀 Usage

### Basic command

```bash
python LLM_excel.py --excel ./llm_app_excel/output.xlsx
```

### Full command with all options

```bash
python LLM_excel.py \
  --excel ./llm_app_excel/output.xlsx \
  --outfolder ./llm_app_excel/email_to_client \
  --template email_template.j2 \
  --templatedir ./llm_app_excel
```

---

## 📝 Template Format

The Jinja2 template (`email_template.j2`) should use variable placeholders matching the Excel columns, for example:

```jinja2
Hello {{ name }} {{ surname }},

We are writing to confirm your registration with the fiscal number {{ fisc_num }}.

Your email: {{ email }}  
Address: {{ address }}

Thank you!
```

---

## 📊 Excel File Format

Your Excel file (`output.xlsx`) should contain at least the following columns:

- `client` *(used as an iterator, values can be anything)*
- `Nom`
- `Prénom`
- `email`
- `Numéro fiscal`
- `Adresse`

---

## 🧠 Optional: LLM Interaction

The script includes a placeholder for querying a local language model using `lmstudio`, though it’s not used in the email generation by default.

You can adapt the `ask_LLM()` function for advanced tasks like tone checking, summary, or content improvement.

---

## 📄 License

MIT License.
Free to use, modify, and distribute this project.

---

## 🤝 Contributing

Pull requests and issues are welcome. If you find a bug or have a feature request, open an issue or create a PR.

---

## 👨‍💻 Author

Built by Joris CLEMENT — Powered by Python