# Intelligent Request Triage

## 🎯 Objective

Organize customer service requests by category, priority, and responsible team.
Requests can be classified locally with keyword rules or optionally with
generative AI.

## ✨ Features

- Read requests from `data.csv`.
- Classify requests by category, priority, and responsible team.
- Use local keyword rules or the OpenAI API.
- Fall back to local rules if AI classification fails.
- Save results as a CSV file in a timestamped output folder.

## 📂 Project Structure

- `main.py`: command-line options, input processing, and output generation.
- `classification.py`: keyword-based and AI-based classification.
- `data.csv`: input requests.
- `requirements.txt`: Python dependencies.
- `output/`: timestamped folders containing generated results.

## 🚀 How to Run

### 1. Navigate to the project folder

From the repository root, run:

```powershell
cd .\ia\automations\intelligent-request-triage
```

### 2. Install dependencies

```powershell
py -3.15 -m pip install -r requirements.txt
```

### 3. Run the script

```powershell
py -3.15 .\main.py
```

Each run creates a folder inside `output` using the
`YYYY-MM-DD-HH-MM-SS` format and saves `results.csv` there. For example:

```text
output\2026-11-16-13-10-25\results.csv
```

To use a different input CSV or specify an output file, pass `--entry` and
`--output`:

```powershell
py -3.15 .\main.py --entry .\data.csv --output .\custom-results.csv
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

#### Optional: AI-based classification

AI classification requires an OpenAI API key. Create one in your OpenAI
account, then set it in the same PowerShell terminal where you will run the
script:

```powershell
$env:OPENAI_API_KEY = "paste-your-api-key-here"
```

Replace the placeholder with your actual API key. To check that the variable
is set without displaying the key, run:

```powershell
if ($env:OPENAI_API_KEY) { "API key is set" } else { "API key is not set" }
```

Then run the script in the same terminal:

```powershell
py -3.15 .\main.py --mode ia
```

The environment variable applies only to the current terminal session. Set it
again in a new terminal. Do not share your API key or commit it to the
repository. API usage may incur charges.

## 📄 Results

Each output CSV includes the request ID, category, priority, assigned team,
classification rationale, and requested classification method.

## ✍️ Author

@rodrigofmdev

- Email: rodrigofmdev@gmail.com
- GitHub: [github.com/rodrigofmdev](https://github.com/rodrigofmdev)
- LinkedIn: [linkedin.com/in/rodrigofmdev](https://linkedin.com/in/rodrigofmdev)
