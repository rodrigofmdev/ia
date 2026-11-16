# Customer Service Agent with Tools

## 🎯 Objective

Demonstrate the difference between a basic chatbot and an agent that can
select and execute specific tools (*tool calling*).

The agent can look up a fictional order or check a fictional exchange policy.
It cannot modify order data or perform financial operations.

## ✨ Features

- Look up orders in a local fictional dataset.
- Check the fictional exchange policy.
- Let the AI model select an available tool.
- Validate and execute only allowlisted, read-only tools.
- Return tool results to the model to formulate an answer.
- Run a local demonstration without an API key.
- Save each interaction and its tool calls as JSON.

## 📂 Project Structure

- `main.py`: command-line interface, demo flow, and AI tool-calling loop.
- `tools.py`: read-only tools, tool definitions, and tool execution allowlist.
- `data/orders_demo.json`: fictional order records.
- `requirements.txt`: Python dependencies.
- `output/`: timestamped folders containing interaction logs.

## 🚀 How to Run

### 1. Navigate to the project folder

From the repository root, run:

```powershell
cd .\ia\automations\customer-service-tools-agent
```

### 2. Install dependencies

```powershell
py -3.15 -m pip install -r requirements.txt
```

### 3. Run without an API

By default, the script runs in demo mode and uses simple local rules to select
a tool. This is also the mode used when you run `main.py` with the VS Code
**Run Python File** button:

```powershell
py -3.15 .\main.py
```

You can also specify `--demo` explicitly:

```powershell
py -3.15 .\main.py --demo
```

Ask about a specific order:

```powershell
py -3.15 .\main.py --demo --pergunta "Onde está o pedido 1002?"
```

Ask about the exchange policy:

```powershell
py -3.15 .\main.py --demo --pergunta "Qual é a política de troca?"
```

### 4. Run with AI

AI mode uses the OpenAI API to choose whether to call an available tool. Set
your API key in the same PowerShell terminal, then use the `--ai` option:

```powershell
$env:OPENAI_API_KEY = "paste-your-api-key-here"
```

Replace the placeholder with your actual API key. To check that the variable
is set without displaying the key, run:

```powershell
if ($env:OPENAI_API_KEY) { "API key is set" } else { "API key is not set" }
```

Then ask a question:

```powershell
py -3.15 .\main.py --ai --pergunta "Onde está o pedido 1002?"
```

The environment variable applies only to the current terminal session. Set it
again in a new terminal. Do not share your API key or commit it to the
repository. API usage may incur charges.

## 📄 Results

Each run creates a timestamped folder inside `output`, using the
`YYYY-MM-DD-HH-MM-SS` format. The `interaction.json` file records the mode,
question, selected tool calls, results, and final answer.

## 🧠 What You'll Learn

- The difference between a chatbot and a tool-using agent.
- How to define functions that a model can request.
- How to validate and control tool execution.
- How tool results are returned to a model for a final answer.
- Why an agent's permissions should be limited.

## 🔒 Safety and Limitations

The dataset and exchange policy are fictional. All available tools are
read-only: they do not modify orders, cancel purchases, approve refunds, or
perform transactions.

A real system would need to authenticate users, authorize each lookup, log tool
calls, protect personal data, and require human approval for consequential
actions.

## ✍️ Author

@rodrigofmdev

- Email: rodrigofmdev@gmail.com
- GitHub: [github.com/rodrigofmdev](https://github.com/rodrigofmdev)
- LinkedIn: [linkedin.com/in/rodrigofmdev](https://linkedin.com/in/rodrigofmdev)
