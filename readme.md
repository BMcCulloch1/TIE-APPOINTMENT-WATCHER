# TIE Appointment Watcher – Lleida, Spain

This script monitors appointment availability for "Toma de Huellas" (TIE fingerprinting) in Lleida, Spain via Spain’s extranjería website. If a slot is available, it sends a Telegram notification with a screenshot and HTML snapshot.

---

## Features

- Automates extranjería form flow using Playwright  
- Detects appointment availability and session rejections  
- Sends Telegram alerts with images and HTML  
- Meant to run hourly via cron (e.g. on AWS EC2)

---

## Setup

1. Clone the repo and install dependencies:

   ```
   git clone https://github.com/YOUR_USERNAME/tie-watcher.git
   cd tie-watcher

   python3 -m venv venv
   source venv/bin/activate

   pip install -r requirements.txt
   python3 -m playwright install
   ```

2. Create a `.env` file in the root:

   ```
   NIE=NIE
   FULL_NAME=FULL_NAME
   COUNTRY_VALUE=COUNTRY_CODE 
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   ```

   To find the correct COUNTRY_VALUE, inspect the country dropdown in the extranjería form. Example: Andorra = 133

3. Run manually with:

   ```
   python3 main.py
   ```

---

4. Running via Script

   Instead of manually activating the virtual environment and running the script, you can use the provided `run.sh` script:

   This script will:

- Create and activate a virtual environment (if it doesn't exist)
- Install dependencies
- Run the bot

> Make sure `run.sh` is executable:
> 
> ```bash
> chmod +x run.sh
> ```

    
## Expected Behavior

- If an appointment is available:
  - Telegram alert is sent
  - `artifacts/result.png` and `result.html` are saved

- If not:
  - Console logs: “No appointments available.”

---

## Folder Structure

```
tie-watcher/
├── src/ 
│   ├── utils/
│   │   └── stealth.py
│   ├── main.py
│   ├── pages.py
│   ├── detect.py
│   ├── notify.py
│   ├── storage.py
│   ├── tie_selectors.py
│   └── stealth.py
├── test/  
│   └── test_notify.py
│   └── test_pages.py
│   └── test_tele.py
├── artifacts/ 
│   ├── result.png
│   ├── result.html
│   └── debug.har
├── .env
├── .gitignore
├── run.sh
├── requirements.txt
└── readme.md

```

---

## Deployment

- Use `crontab -e` to schedule hourly runs  
- Ideal for deployment on AWS EC2  
- Add `.env`, `__pycache__`, and `artifacts/` to `.gitignore`

---

## Disclaimer

This tool is for **personal use only** and is **not affiliated** with the Spanish government.  
Use responsibly and avoid abuse of public appointment systems.