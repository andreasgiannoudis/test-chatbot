# LLM Chatbot Red Teaming & Vulnerability Assessment Tool

This repository contains an automated framework designed to evaluate the resilience of LLM-backed chat applications against prompt injection, role confusion, and system prompt leakage vulnerabilities. 

The framework consists of two main components:
1. **An automated test execution script** powered by Playwright to simulate various adversarial interaction techniques.
2. **An analytical scoring engine** that parses the responses, identifies risk indicators, and provides structured evaluation reports.

---

## Prerequisites & Installation

### System Requirements
* Python 3.8 or higher
* Node.js binaries (managed automatically via Playwright setup)

### 1. Install Library Dependencies
Install the required browser automation and headless runtime interfaces using `pip`:
```bash
pip install playwright