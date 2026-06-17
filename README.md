# 🚗 Vehicle Owner Contact QR System (₹0/Month Masked System)

This is a **mobile-first, production-ready web application** and **high-resolution QR generator system** that allows anyone to contact you by scanning a QR sticker pasted on your vehicle's rear windshield. 

To protect your privacy, the webpage **masks your phone number**. When a visitor scans the QR code, they submit an alert through a web form, which is routed via a **free Vercel Serverless Function** to your personal **Telegram Bot**. Your phone number is **never** exposed to the visitor. If you choose to respond, you can trigger a direct phone call or WhatsApp back to them with one tap from your private Telegram notification.

---

## 🌟 Key Features

- **100% Phone Number Masking**: The visitor's browser never receives your phone number. All routing is done server-side on Vercel's secure servers.
- **Vercel Serverless Architecture**: Operates entirely within Vercel's free limits, assuring a **lifetime recurring cost of ₹0/month**.
- **Mobile-First Glassmorphic UI**: Translucent styling with beautiful gradients, custom status dots, active states, and mobile-responsive tap actions.
- **Predefined Alert Scenarios**: Quick-select actions:
  - 🚗 *Blocking Access*
  - 💡 *Lights Left ON*
  - 🅿️ *Parking Issue*
  - 🚨 *Emergency*
- **Browser Geolocation Integration**: An optional checkbox to share location. When checked, the browser queries the GPS coordinates and appends a Google Maps navigation link to your alert.
- **Custom Alert Input**: A textbox for typing any custom notification, with a real-time character counter.
- **Quick Return Dialing**: Telegram notifications contain pre-formulated deep links:
  - `Call Visitor Now` (opens your dialer with their number)
  - `WhatsApp Visitor Now` (starts a chat with them using a pre-filled template)
- **High-Resolution Generator**: Local Python compiler outputs sticker layouts in PNG (300 DPI) and infinite-scale SVG vector formats.

---

## 📂 Project Structure

```
Car Scanner/
├── api/
│   └── send-message.js   # Serverless API to bridge submissions to Telegram
├── assets/              # Output folder for generated images (PNG/SVG)
│   ├── qr_code.png       # Raw QR code (PNG)
│   ├── qr_code.svg       # Raw QR code (Vector SVG)
│   ├── sticker_design.png # Print-ready windshield sticker design (300 DPI PNG)
│   └── sticker_design.svg # Print-ready windshield sticker design (Vector SVG)
├── vercel.json          # Routing instructions for Vercel
├── index.html           # Main landing page structure & client script
├── styles.css           # Glassmorphic stylesheet
├── generate_qr.py       # Python generator for QR assets
├── deploy.sh            # Automation script for local testing & git helpers
└── README.md            # System guide (this file)
```

---

## 💰 Cost Analysis & Estimates

| Service Type | Provider | Cost | Purpose |
| :--- | :--- | :--- | :--- |
| **Hosting & API** | Vercel (Free Tier) | **₹0 / Month** | Hosts landing page and serverless function |
| **Alert Forwarding** | Telegram Bot API | **₹0 / Month** | Relays notification securely to your phone |
| **Database** | None | **₹0 / Month** | Not needed. Relayed in real-time |
| **QR Generation** | Local python script | **₹0 / Month** | Compiles print graphics locally |
| **Total Recurring Cost** | | **₹0 / Month** | **100% Free Lifetime Privacy** |

---

## 🤖 Step 1: Create a Free Telegram Bot (Takes 1 Minute)

To receive alerts, your serverless API needs to know which Telegram account to notify.

1. **Get Bot Token**:
   - Open Telegram and search for the official **`@BotFather`** account.
   - Send the message: `/newbot`
   - Follow the prompts to give your bot a name and username (e.g. `SatyamCarBot`).
   - BotFather will reply with an **HTTP API Token** (e.g. `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`). Copy this.
2. **Get Your Chat ID**:
   - In Telegram, search for the account **`@userinfobot`**.
   - Send any message to it. It will reply with your personal **Id** (a number like `987654321`). Copy this.
3. **Start the Bot**:
   - Search for your bot's username (e.g., `@YourCustomCarBot`) on Telegram.
   - Open the chat and click **Start** or send `/start` (this authorizes the bot to message you).

---

## 🚀 Step 2: Run & Deploy the Project

### Option A: Run Locally (Test the Design)
1. Open your terminal in this workspace: `/Users/satyampandey/Car Scanner`
2. Run the launcher:
   ```bash
   ./deploy.sh
   ```
3. Type **`1`** to boot the local server at **`http://localhost:8085`**. 
4. *Note: In local test mode, alerts are logged in the browser console. To test Telegram delivery, you will deploy to Vercel.*

---

### Option B: Deploy to Vercel Free Tier (Recommended)

1. Create a free [Vercel account](https://vercel.com).
2. Install the Vercel CLI on your machine:
   ```bash
   npm install -g vercel
   ```
3. Run the deployment script:
   ```bash
   ./deploy.sh
   ```
4. Choose **`3`** to deploy. Follow Vercel's CLI instructions to link the project.
5. Once deployed, open your Vercel Web Dashboard, find the project, and navigate to **Settings -> Environment Variables**. Add the following variables:
   - `TELEGRAM_BOT_TOKEN` = *(Your Bot HTTP API Token from `@BotFather`)*
   - `TELEGRAM_CHAT_ID` = *(Your ID number from `@userinfobot`)*
6. Re-deploy or trigger a production update for the environment variables to take effect.
7. Note down your live URL (e.g. `https://car-scanner-satyam.vercel.app`).

---

### Step 3: Re-Generate Your QR Stickers with the Live URL

Now that you have your live URL:
1. Run:
   ```bash
   ./deploy.sh
   ```
2. Type **`4`** (Re-generate QR Codes).
3. Type in your live URL and press Enter.
4. The script will rebuild your customized vector and raster images inside the `assets/` folder.

---

## 🖨️ Physical Sticker Printing Guide

### 1. Recommended Print Materials
- **Vinyl Sticker (Preferred)**: Ask the printer for a **polypropylene (PP) or vinyl sticker with UV-lamination**. Paper stickers will degrade in rain.
- **Glass Decal (Static Cling)**: If you want to stick it from the *inside* of the windshield looking *out*, request a **reverse-printed static cling decal**.

### 2. Physical Sizes
- **Target Print Size**: 3 inches x 4 inches (7.6 cm x 10 cm). This is large enough to scan from 4-5 feet away but small enough to not block your rear vision.
- **SVG Format**: Provide `assets/sticker_design.svg` to the print shop. Vector graphics can scale to any size without becoming pixelated or losing scan fidelity.
- **PNG Format**: Provide `assets/sticker_design.png` if they require standard image raster prints. It is encoded at high 300 DPI.
