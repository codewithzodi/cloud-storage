# ☁️ ZOD CLOUD - Simple Cloud File Storage

ZOD CLOUD is a modern, easy-to-use cloud file storage web app built with Flask. Effortlessly upload, download, list, rename, and delete files from your browser. Download all your files as a ZIP archive with a single click!

---

## 🚀 Features

- **Upload Files** (with file type and size restrictions)
- **Download Files** (individually or all as ZIP)
- **List Files** (see all files in your cloud storage)
- **Rename Files** (directly from the web UI)
- **Delete Files** (with confirmation)
- **Modern, Responsive UI**
- **Secure** (filename sanitization, allowed types, size limits)
- **CORS Enabled** (for easy frontend expansion)

---

## 🖥️ Screenshots

> _Add your screenshots here!_

---

## 🛠️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   - Go to [http://localhost:5000](http://localhost:5000)

---

## 📂 File Storage
- All uploaded files are stored in the `cloud_storage/` directory (created automatically).
- Maximum file size: **50MB**
- Allowed file types: `txt`, `pdf`, `png`, `jpg`, `jpeg`, `gif`, `zip`, `csv`, `docx`, `xlsx`

---

## 🧩 API Endpoints

| Endpoint            | Method | Description                        |
|---------------------|--------|------------------------------------|
| `/upload`           | POST   | Upload a file                      |
| `/download_file`    | GET    | Download a specific file           |
| `/download_all`     | GET    | Download all files as a ZIP        |
| `/list`             | GET    | List all files                     |
| `/delete/<filename>`| DELETE | Delete a file                      |
| `/rename`           | POST   | Rename a file                      |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

MIT License 