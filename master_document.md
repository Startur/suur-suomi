# **🚀 Automated News & Media Platform - Master Document**  
_Last updated: 2025-03-08_

## **📌 High-Level Concept & Vision**
### **Project Overview**
The Automated News & Media Platform is a **censorship-resistant content platform** that fetches news articles, enhances them using AI, and distributes them across multiple channels. The platform is designed to:  

✔ **Automate news aggregation** from various sources  
✔ **Ensure content integrity & immutability** using **BSV blockchain**  
✔ **Enable AI-driven content enhancement** for unique article generation  
✔ **Support multi-channel publishing** (web, social, APIs, email)  
✔ **Use blockchain-based monetization** via micropayments and licensing  

Unlike traditional media platforms, this system **stores articles permanently on BSV** for censorship resistance, while also allowing users to **earn revenue via micropayments**.

---

## **📂 Project Architecture**
```
/NEWS_PLATFORM
│── /news-dashboard        # Frontend dashboard for monitoring and management
│── /node_modules          # Frontend dependencies
│── /Specs                 # Specification and documentation files
│── /venv                  # Python virtual environment
│── .env                   # Environment variables
│── ai_rewriter.py         # AI-powered content rewriting
│── batch_rewrite.log      # Logs for batch article rewriting
│── batch_rewrite.py       # Automates AI rewriting for multiple articles
│── database.py            # PostgreSQL connection setup
│── db_setup.py            # Database initialization script
│── extract_article.py     # Extracts full content from URLs
│── fastapi.log            # FastAPI server logs
│── main.py                # Entry point for backend services
│── master_document.md     # This file
│── models.py              # SQLAlchemy database models
│── package-lock.json      # Frontend dependency lock file
│── package.json           # Frontend dependency list
│── README.md              # General project information
│── scraper.py             # Fetches RSS feeds and extracts articles
│── select_articles.py     # Filters and selects relevant articles
│── test_ai.py             # AI model testing script
```

---

## **🛢 Database Schema (PostgreSQL)**
📌 **Database Locations:**
- **Development:** Local PostgreSQL database (`localhost`).
- **Production:** Confirmed as **AWS RDS or DigitalOcean Managed Databases**.
- **Blockchain Storage:** Article hashes stored on **BSV blockchain** for verification.
- **Backup Strategy:** Automated **daily backups to S3 storage**.

The platform uses **PostgreSQL** for structured data storage. Below is the full schema with all tables.

### **🔹 `articles` Table (Stores News Articles)**
```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rewrite_status TEXT CHECK (rewrite_status IN ('not_selected', 'pending', 'completed')) DEFAULT 'not_selected',  -- Track AI processing
    bsv_txid TEXT UNIQUE,  -- Blockchain transaction ID for censorship resistance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **🔹 `users` Table (Manages System Users)**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'editor', 'reader')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **🔹 `transactions` Table (Tracks Payments via BSV)**
```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    article_id INTEGER REFERENCES articles(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    bsv_txid TEXT UNIQUE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'confirmed', 'failed')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **🔹 `api_keys` Table (For External API Access)**
```sql
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    owner VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## **🔑 Database Users & Access Roles**
📌 **Database Access Information:**
- **Local Database:** Accessible via `localhost` using PostgreSQL.
- **Production Database:** Will require **IAM-based access control** and **SSL connections**.
- **Blockchain Verification:** Article hashes can be verified via their **BSV transaction ID (TXID)**.

### **List of Database Users**
| Username     | Role     | Permissions |
|-------------|---------|-------------|
| `admin_user`  | `SUPERUSER` | Full access |
| `editor_user` | `EDITOR` | Can modify articles, but no DB admin rights |
| `reader_user` | `READER` | Read-only access |

### **User Privileges**
- **`admin_user`**: Full control (create, update, delete tables, manage users).  
- **`editor_user`**: Can insert and update articles but **cannot delete** or manage users.  
- **`reader_user`**: Read-only access to published articles.  

---

## **🛠 Technology Stack**
### **Backend**
- **FastAPI** – Lightweight, fast, and scalable API framework  
- **PostgreSQL** – Structured database for managing articles  
- **SQLAlchemy** – ORM for efficient data operations  
- **BeautifulSoup & Requests** – Web scraping for article extraction  
- **BSV (Bitcoin SV)** – Blockchain layer for **censorship resistance** and **micropayments**  

### **Frontend**
- **React.js** – JavaScript-based frontend for the user interface  
- **Vite** – Frontend development bundler for fast performance  
- **Axios** – Handles API requests  
- **TailwindCSS / Material UI** – UI styling  

### **Blockchain Integration (BSV)**
- **Direct On-Chain Storage** – Articles stored permanently on BSV  
- **Micropayments** – Users pay per article or tip using BSV  
- **Smart Contracts** – Automates content licensing and revenue distribution  

### **Infrastructure**
- **Docker (Planned)** – For containerization and easy deployment  
- **AWS / VPS Hosting (Planned)** – Scalable cloud hosting  
- **GitHub** – Version control  

---

## **🔄 Data Flow & Process**
1️⃣ **Fetch articles from RSS feeds (`scraper.py`)**  
2️⃣ **Extract full content from article URLs (`extract_article.py`)**  
3️⃣ **Select articles for rewriting (`select_articles.py`)**
4  **AI-enhanced rewriting of content (`ai_rewriter.py`)**  
5 **Store structured articles in PostgreSQL (`models.py`)**  
6 **Publish full article on BSV (`blockchain.py`)**  
7  **Expose API for frontend & third-party integrations (`main.py`)**  
8 **Fetch and display content in React frontend (`services/api.js`)**  
9 **Allow users to pay per article or tip using BSV micropayments**  

---

## **🛡️ Blockchain Integration for Censorship Resistance (Using BSV)**
### **Why Use BSV?**
✔ **Censorship Resistance** – Articles are permanently stored on-chain  
✔ **Scalability** – Handles high transaction volumes with ultra-low fees  
✔ **Direct On-Chain Storage** – No need for IPFS or third-party hosting  
✔ **Built-in Monetization** – Supports micropayments, tipping, and licensing  

### **How Blockchain is Used in the Platform**
1️⃣ **Full Article Storage On-Chain**  
   - **Articles are stored as BSV transactions**, making them **permanent**.  
   - Each article gets a **BSV transaction ID (TXID)**, which serves as a permanent link.  
   - Readers, publishers, and developers can verify articles via the TXID.  

2️⃣ **On-Chain Proof of Publication**  
   - Each article’s **hash and metadata** are stored on **BSV** before publication.  
   - Prevents stealth edits by maintaining an immutable record of all changes.  

3️⃣ **Micropayments & Monetization**  
   - Users can **pay-per-article** using **BSV micropayments** (fractions of a cent).  
   - Alternative revenue models: **tipping, premium subscriptions, and smart contract licensing**.  
   - Payments are **automated via smart contracts** for instant, transparent revenue distribution.  

4️⃣ **Smart Contract-Based Content Licensing**  
   - **AI-enhanced articles can be licensed via smart contracts**.  
   - Media outlets and third parties can **pay automatically for syndicated content**.  

5️⃣ **Decentralized Identity for Journalists (Planned Upgrade)**  
   - Verified contributors can **cryptographically sign articles** to prove authorship.  
   - Prevents impersonation and deepfake-generated fake news.  

---

## **⚙️ Setup & Installation**
### **1️⃣ Install Backend Dependencies**
```bash
pip install -r requirements.txt
```

### **2️⃣ Install BSV Blockchain Dependencies**
```bash
pip install bsv
```

### **3️⃣ Run FastAPI Backend**
```bash
uvicorn main:app --reload --port 8000
```

### **4️⃣ Start PostgreSQL**
```bash
sudo systemctl start postgresql
```

### **5️⃣ Install & Run Frontend**
```bash
cd news-dashboard
npm start
```

### **6️⃣ Environment Variables (`.env` file)**
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
VITE_API_BASE_URL=http://localhost:8000
BSV_NODE_URL=https://bsv.network
BSV_WALLET_PRIVATE_KEY=your_private_key_here
OPENAI_API_KEY=your_openai_key_here
DB_NAME=news_platform
DB_USER=news_admin
DB_PASSWORD=your_db_password_here
DB_HOST=localhost
```

### **PostgreSQL Setup for macOS**

On macOS, PostgreSQL is installed via **Homebrew**, follow these steps to manage the PostgreSQL service:

1. **Check if PostgreSQL is Installed via Homebrew**:
   If you installed PostgreSQL using Homebrew, use the following command to list services:
   ```zsh
   brew services list
   ```

2. **Start PostgreSQL Using Homebrew**:
   To start PostgreSQL, run:
   ```zsh
   brew services start postgresql
   ```

3. **Check PostgreSQL Status**:
   To confirm that PostgreSQL is running, use:
   ```zsh
   brew services list
   ```

4. **Access PostgreSQL**:
   Once PostgreSQL is running, you can connect to it using:
   ```zsh
   psql postgres
   ```

5. **Install PostgreSQL via Homebrew (if needed)**:
   If you haven't installed PostgreSQL yet, use the following command to install it:
   ```zsh
   brew install postgresql
   ```

After installing, start PostgreSQL using:
   ```zsh
   brew services start postgresql
   ```

This ensures PostgreSQL is properly set up and running on macOS using Homebrew.

**Login directly to News Platform database**
psql -U news_admin -d news_platform

---

## **💰 Monetization Strategy**
- **BSV Micropayments** for reading AI-enhanced content  
- **Crypto tipping system** for content creators  
- **BSV-based smart contract licensing** for media syndication  
- **Subscription-based access** to exclusive AI-generated reports  
  - Users who subscribe **still see ads, but fewer of them**.  
  - BSV micropayments will be **integrated for pay-per-article access**.  

---

## **🚧 Current Issues & Fixes**
| Issue | Status | Notes |
|-------|--------|-------|
| Scraper syntax error | 🔴 **Open** | Investigating |
| Full article not extracted | 🟡 **In Progress** | Adjusting BeautifulSoup parsing |
| AI rewrite performance slow | 🟡 **Planned** | Considering caching |
| BSV smart contract integration | 🟡 **Planned** | Need to finalize payment flow |

---

## **📅 To-Do List**
✅ **Basic article extraction**  
✅ **Database setup**  
✅ **Install React frontend**  
✅ **Blockchain research completed**  
🔲 Fix syntax issues in scraper  
🔲 Connect frontend with backend API  
🔲 Implement BSV integration  
🔲 Deploy smart contract for article payments  
🔲 Implement AI integration with ChatGPT-4o API.  
🔲 Finalize database schema for rewritten articles.  
🔲 Develop API endpoints to serve rewritten content.  
🔲 Plan frontend integration with AI-rewritten articles.  

---

## **📌 Next Steps**
🔹 Implement AI rewriting module with **ChatGPT-4o API**.  
🔹 Finalize API & database schema.  
🔹 Complete React UI integration.  
🔹 Deploy BSV-powered smart contracts.  

---

This **master document** ensures your project remains **structured, scalable, and censorship-resistant**. Store it in **GitHub** and update as needed.  

### Shell Usage
From now on, all instructions will be provided in **zsh**.  

Would you like help drafting the **BSV smart contract logic** for handling payments and licensing? 🚀
