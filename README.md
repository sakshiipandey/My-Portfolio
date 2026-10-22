# 👩‍💻 Sakshi Pandey | Portfolio

Welcome to my personal portfolio! I am a Computer Science Engineering student and a Data Science & Machine Learning enthusiast passionate about Artificial Intelligence, Deep Learning, and data-driven solutions.

## 🌐 Live Website

🔗 **Portfolio:** https://my-portfolio-pwna.onrender.com/



## ✨ Portfolio Features

- Personal introduction and profile
- Project showcase
- Resume access
- GitHub and LinkedIn links
- Admin login and project management dashboard
- Responsive user interface


## 📂 Project Structure

```text
My-Portfolio/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── README.md
├── templates/
│   ├── index.html
│   ├── admin_login.html
│   └── admin_dashboard.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    ├── images/
    │   └── profile.jpeg
    └── documents/
        └── resume.pdf
```

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/sakshiipandey/My-Portfolio.git
cd My-Portfolio
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Configure the following environment variables before running the application:

- `SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD_HASH`

Generate a password hash with Werkzeug:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YOUR_PASSWORD'))"
```

Use the generated hash as `ADMIN_PASSWORD_HASH`. Keep your password and secret keys private.

### 4. Run the application

```bash
python app.py
```

Open http://127.0.0.1:5000/ in your browser.

## 🔗 Connect With Me

- **GitHub:** https://github.com/sakshiipandey
- **LinkedIn:** https://linkedin.com/in/sakshi-pandey-a6077735b
- **Email:** 16sakshy@gmail.com

## 📌 Repository

🔗 **GitHub Repository:** https://github.com/sakshiipandey/My-Portfolio

---

⭐ Thank you for visiting my portfolio!

**Made with ❤️ by Sakshi Pandey**
