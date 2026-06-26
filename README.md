# AI Agent (Function Calling + Python Tools)

This project is a simple **agentic AI system** built with the Gemini API that can:
- Explore files in a restricted working directory
- Read file contents
- Write and modify files
- Execute Python scripts safely
- Iteratively solve tasks using tool calls

---

## 🚀 Features

The agent supports 4 core tools:

### 📁 File System Tools
- List files in a directory
- Read file contents
- Write/overwrite files

### 🐍 Execution Tool
- Run Python files with optional arguments
- Capture stdout/stderr safely with timeout protection

### 🤖 Agent Loop
- Multi-step reasoning loop
- The model can call tools repeatedly
- Results are fed back into the conversation

---

## 🧠 How it works

1. User sends a prompt
2. Gemini decides whether to:
   - respond directly, or
   - call a function (tool)
3. Python executes the function
4. Result is sent back to the model
5. Loop continues until final answer

---

## 📂 Project Structure

