# AI Content Empire (ACE) - Documentation

Welcome to the AI Content Empire (ACE) platform! ACE is an autonomous pipeline designed to generate, manage, and distribute content for AI Influencers across various social platforms, complete with automated monetization and fan interaction capabilities.

---

## 🚀 1. Installation

### Prerequisites
- Python 3.10+
- A [Supabase](https://supabase.com/) account (for the database and revenue dashboard).
- A [Hugging Face](https://huggingface.co/) account with an API token (for Nova and Pixel AI model generation).

### Setup Instructions

1. **Clone the repository:**
   Ensure you are in the root directory of the ACE project (`/root/x-auto-ai/ai-content-empire/`).

2. **Install Dependencies:**
   Run the following command to install all required Python packages (including the Web UI requirements):
   ```bash
   pip install -r web_ui/requirements.txt
   pip install python-telegram-bot tweepy supabase pyyaml
   ```

3. **Configure Environment Variables / Config:**
   Open (or create) the `config/config.yaml` file. You need to provide your API keys for the system to function.
   ```yaml
   # config/config.yaml
   supabase_url: "YOUR_SUPABASE_PROJECT_URL"
   supabase_anon_key: "YOUR_SUPABASE_ANON_KEY"
   huggingface_api_key: "YOUR_HF_TOKEN"
   ```

---

## ⚙️ 2. Running the Platform

There are two primary ways to interact with the ACE platform: the interactive **Web UI Dashboard** (recommended for day-to-day management) and the **Autonomous Headless Pipeline** (for scheduled daily execution).

### Option A: The Web UI (Control Center)
The Web UI is the command center for your empire. Use it to create new influencers, view analytics, and monitor the content queue.

To start the UI, run:
```bash
streamlit run web_ui/app.py
```
*The dashboard will start locally (usually on `http://localhost:8501`).*

### Option B: The Autonomous Pipeline
To run a single cycle of the automated pipeline (which scans trends, creates content, applies character personas, and distributes it via `Echo`), run:
```bash
python main.py
```
*Tip: In a production environment, you would schedule `main.py` to run daily via a Cron job.*

---

## 🎮 3. Using the Platform

### Creating a New AI Influencer
1. Open the **Web UI** and navigate to the **🎭 Character Studio** tab.
2. Fill out the form with the character's Name, Style, Personality Traits, and Visual Identity prompts.
3. Toggle **"Allow NSFW Content"** if this influencer will generate uncensored material (This routes generation to specific uncensored LLM/SDXL models).
4. Click **Save Character**. This automatically creates their "Character Bible" JSON file in `content/character_bibles/`.

### Setting Up Social Media Accounts (The Guided Wizard)
Fully automated bot creation of social accounts often results in immediate bans. Use our guided flow instead:
1. In the Web UI, go to the **🔗 Account Setup** tab.
2. Select your newly created influencer.
3. Follow the step-by-step instructions (Step 1: Email, Step 2: Twitter, Step 3: TikTok) using an anti-detect browser or mobile device.
4. Input the successfully created handles into the form and click **Save** to link them to the character's profile.

### Generating the Linktree (Bio Link)
Every influencer needs a landing page for their bio. ACE generates a custom HTML page tailored to the influencer's style.
1. Run the generator script:
   ```bash
   python platforms/linktree_generator.py
   ```
2. The generated `index.html` file will be saved in `platforms/static_sites/<character_name>/`. You can deploy this via free hosting (Vercel, Netlify, GitHub Pages).

### Managing Affiliate Links (Monetization)
1. Open `revenue/affiliate_manager.py`.
2. Update the `self.local_library` dictionary with your actual affiliate links (Amazon Associates, Clickbank, VPNs, etc.), categorized by niche.
3. When `Echo` responds to fans, it will automatically weave these links into conversations when relevant (e.g., if a fan asks about fitness, Echo will drop a GymShark link).

---

## 🤖 4. Platform Automation (Echo Agent)

The `Echo` agent handles distribution and interaction.

### Telegram Automation
Telegram is highly automatable.
1. Talk to `@BotFather` on Telegram to create a Bot and get a Token.
2. Create a channel for your influencer and make the Bot an Admin.
3. Update `platforms/telegram_bot.py` with your Token and Channel ID. ACE will now autonomously push content and premium teasers to Telegram.

### Twitter (X) Automation
`Echo` is pre-configured with `tweepy`.
1. Inside `agents/echo.py`, locate the `publish_content` function.
2. Uncomment the Tweepy block and insert your Twitter Developer API keys to enable fully automated tweeting.

### Paywalls (OnlyFans / Patreon)
Because OnlyFans lacks a public API, ACE cannot post there autonomously.
- **Workflow:** ACE generates the content and queues it. You act as the human-in-the-loop to manually upload to OnlyFans.
- **Cross-Promotion:** `Echo`'s logic is designed to take your Paywall links and automatically post them as teasers onto your automated platforms (Twitter/Telegram) to drive traffic.
