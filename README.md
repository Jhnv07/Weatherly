# 🌦️ Weatherly — Real-Time Weather Dashboard

**Weatherly** is a modern, responsive web application that provides real-time weather updates for any city worldwide. Built using **Flask** for the backend and **React with Tailwind CSS** for the frontend, it fetches data from the [OpenWeatherMap API](https://openweathermap.org/api) to show weather metrics like temperature, humidity, wind speed, and more.

---

## 📋 Table of Contents

1. [Features](#features)
2. [Folder Structure](#folder-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

---

## 🌟 Features

* Get real-time weather info for any city
* Displays temperature, feels-like temp, humidity, wind speed, and weather condition
* Beautiful and responsive UI
* Weather logs saved for future reference (backend feature)

---

## 🗂 Folder Structure

```
weatherly/
├── backend/
│   ├── app.py
│   ├── get_weather.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── tailwind.config.js
│   └── ...
│
├── .gitignore
├── README.md
└── weather_log.txt
```

---

## 🛠️ Installation

### Prerequisites:

* Python 3.11+
* Node.js + npm
* Flask
* Vite (optional for dev experience)

### Backend Setup:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend Setup:

```bash
cd frontend
npm install
npm run dev   # to start Vite dev server
```

> Make sure your Flask API is running before starting the frontend.

---

## 🚀 Usage

1. Start the Flask backend:

   ```bash
   python app.py
   ```

2. In a separate terminal, start the frontend React app:

   ```bash
   npm run dev
   ```

3. Visit `http://localhost:5173` (or your local Vite port)

4. Enter any city name and hit submit to get the latest weather data

---

## 🤝 Contributing

Contributions are welcome! Here’s how you can help:

* 🐛 Report bugs via GitHub Issues
* 🌐 Add support for more cities/languages
* 🎨 Improve UI/UX or suggest color themes
* 📦 Refactor or modularize backend code

To contribute:

1. Fork the repo
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push (`git push origin feature-xyz`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — you're free to use, share, and modify it with attribution. See the [LICENSE](LICENSE) file for more details.
