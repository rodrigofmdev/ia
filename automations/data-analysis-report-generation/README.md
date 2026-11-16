# Order Data Analysis Report

## 🎯 Objective

Turn order data into operational metrics, summary tables, charts, and reports.
Metrics are calculated locally with Python and Pandas; an AI-generated
interpretation is optional.

## ✨ Features

- Load order records from `data.csv`.
- Convert dates and amounts and exclude records with invalid required fields.
- Calculate total order value, average order value, delivery rate, and
  cancellation rate.
- Summarize order counts and total value by category.
- Generate a concise, data-driven interpretation in Brazilian Portuguese.
- Save metrics as JSON, a category summary as CSV, a report as Markdown, and a
  chart as PNG.
- Embed the generated chart in the Markdown report.
- Optionally add an AI-generated interpretation to the report.

## 📂 Project Structure

- `main.py`: command-line options and report generation workflow.
- `analysis.py`: CSV loading, data cleaning, and metric calculations.
- `reporting.py`: Brazilian Portuguese formatting, interpretation, and report
  content, including the optional AI summary.
- `data.csv`: input dataset.
- `requirements.txt`: Python dependencies.

## 📁 Input Data

The script reads `data.csv` from the project folder by default. It expects these
columns: `pedido`, `data`, `categoria`, `regiao`, `valor`, and `status`. The
provided dataset uses Portuguese column names and status values.

## 🚀 How to Run

### 1. Navigate to the project folder

From the repository root, run:

```powershell
cd .\ia\automations\data-analysis-report-generation
```

### 2. Install dependencies

```powershell
py -3.15 -m pip install -r requirements.txt
```

### 3. Run the script

```powershell
py -3.15 .\main.py
```

To analyze a different CSV file, pass its path with `--input`:

```powershell
py -3.15 .\main.py --input .\another_data.csv
```

#### Run from VS Code

The Python extension's **Run Python File** command uses the interpreter
selected in VS Code. To select the interpreter that works with this project:

1. Press `Ctrl+Shift+P` and run **Python: Select Interpreter**.
2. Select **Enter interpreter path**, then choose **Find...**.
3. Select the installed Python executable. In this environment, use:
   `C:\Users\sabri\AppData\Local\Python\pythoncore-3.15-64\python.exe`.
4. Close the existing integrated terminal, open a new one, and run the file again.

Do not select `C:\Users\sabri\.local\bin\python3.15.exe` if Windows Application
Control blocks it. If you select a different Python installation, install the
project dependencies in that environment as well.

#### Optional: AI-generated summary

AI summaries require an OpenAI API key. Create one in your OpenAI account, then
set it in the same PowerShell terminal where you will run the script:

```powershell
$env:OPENAI_API_KEY = "paste-your-api-key-here"
```

Replace `paste-your-api-key-here` with your actual API key. To check that the
variable is set without displaying the key, run:

```powershell
if ($env:OPENAI_API_KEY) { "API key is set" } else { "API key is not set" }
```

Then generate a report with an AI interpretation:

```powershell
py -3.15 .\main.py --ai-summary
```

The environment variable applies only to the current terminal session. Set it
again in a new terminal. Do not share your API key or commit it to the
repository. API usage may incur charges.

## 📄 Results

Each run creates a timestamped folder inside `output`, using the
`YYYY-MM-DD-HH-MM-SS` format (for example, `output/2026-11-16-12-51-02/`).
The generated files are saved in that run's folder:

- `orders_by_category.csv`
- `metrics.json`
- `report.md`
- `order_value_by_category.png`

## ✍️ Author

@rodrigofmdev

- Email: rodrigofmdev@gmail.com
- GitHub: [github.com/rodrigofmdev](https://github.com/rodrigofmdev)
- LinkedIn: [linkedin.com/in/rodrigofmdev](https://linkedin.com/in/rodrigofmdev)
