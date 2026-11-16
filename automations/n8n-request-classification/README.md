# Project 04 — n8n Request Classification

## 🎯 Objective

Demonstrate an automation workflow that receives a customer request through a
form, uses AI to classify it, and records the result in a spreadsheet.

The project includes a local Python demo that runs without an API key and an
importable n8n workflow for connecting a form, OpenAI, and Google Sheets.

## ✨ Features

- Classify requests by category, priority, and responsible team.
- Run a local keyword-based demo without an API key.
- Optionally classify requests with the OpenAI API from Python.
- Import an n8n workflow that connects a form, OpenAI, and Google Sheets.
- Save local classifications as CSV files in timestamped folders.

## 📂 Project Structure

- `main.py`: demo and optional OpenAI classification entry point.
- `classification.py`: local rules and AI classification.
- `workflow.json`: importable n8n workflow.
- `requirements.txt`: Python dependencies.
- `output/`: timestamped folders containing local CSV results.

## 🚀 How to Run

### 1. Navigate to the project folder

From the repository root, run:

```powershell
cd .\ia\automations\n8n-request-classification
```

### 2. Install dependencies

```powershell
py -3.15 -m pip install -r requirements.txt
```

### 3. Run the default demo

The demo mode runs by default, including when you use VS Code's **Run Python
File** button. It uses local keyword rules and does not require an API key:

```powershell
py -3.15 .\main.py
```

You can provide a different request:

```powershell
py -3.15 .\main.py --demo --request "Fui cobrado duas vezes no cartão."
```

### 4. Run Python classification with AI

Set your OpenAI API key in the same PowerShell terminal:

```powershell
$env:OPENAI_API_KEY = "paste-your-api-key-here"
```

Replace the placeholder with your actual API key. To check that the variable
is set without displaying the key, run:

```powershell
if ($env:OPENAI_API_KEY) { "API key is set" } else { "API key is not set" }
```

Then run:

```powershell
py -3.15 .\main.py --ai --request "Meu pedido está atrasado."
```

The environment variable applies only to the current terminal session. Set it
again in a new terminal. Do not share your API key or commit it to the
repository. API usage may incur charges.

## 🔗 Set Up the n8n Workflow

The Python commands above demonstrate classification and write a local CSV.
To run the form-to-spreadsheet automation in n8n:

1. In n8n, import `workflow.json`.
2. Create a Google spreadsheet with a sheet named `Requests` and these headers
   in the first row:

   `created_at`, `customer_name`, `request`, `category`, `priority`,
   `responsible_team`, `rationale`

3. In the **Classify Request** node, select or create an **HTTP Header Auth**
   credential with the header name `Authorization` and value
   `Bearer YOUR_OPENAI_API_KEY`. The workflow uses `gpt-4o-mini`.
4. In the **Append to Google Sheets** node, select or create a Google Sheets
   credential and replace `REPLACE_WITH_SPREADSHEET_ID` with your spreadsheet
   ID.
5. Test the form using the Form Trigger's test URL. Once verified, publish the
   workflow and use its production form URL.

Credentials are not included in the exported workflow. Store them in n8n's
credential manager; never paste API keys into the workflow JSON or commit them
to the repository.

## 📄 Results

The Python script creates `output/YYYY-MM-DD-HH-MM-SS/classified_request.csv`.
The n8n workflow appends each form submission and its classification to the
configured Google Sheet.

## 🧠 What You'll Learn

- How form submissions can trigger a visual automation.
- How AI classification can be combined with downstream systems.
- How n8n maps data between nodes and appends it to a spreadsheet.
- How local rules can provide a no-API demonstration.

## ✍️ Author

@rodrigofmdev

- Email: rodrigofmdev@gmail.com
- GitHub: [github.com/rodrigofmdev](https://github.com/rodrigofmdev)
- LinkedIn: [linkedin.com/in/rodrigofmdev](https://linkedin.com/in/rodrigofmdev)
