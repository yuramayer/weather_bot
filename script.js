function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    html.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
}

window.onload = () => {
    const saved = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", saved);

    fetchWeather();

    document.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "visible") {
            fetchWeather();
        }
    });
};

function interpretWeatherCode(code) {
    if ([0, 1].includes(code)) return { emoji: "☀️", label: "Солнечно" };
    if ([2, 3].includes(code)) return { emoji: "☁️", label: "Облачно" };
    if ([51, 61, 63, 65, 80, 81, 82].includes(code)) return { emoji: "🌧️", label: "Дождь" };
    return { emoji: "❓", label: "Неизвестно" };
}

function fetchWeather() {
    // показать лоадер
    document.getElementById("emoji").textContent = "⏳";
    document.getElementById("label").textContent = "Обновляем погоду...";

    // загружаем погоду
    fetch("https://api.open-meteo.com/v1/forecast?latitude=55.75&longitude=37.61&current_weather=true")
        .then(res => res.json())
        .then(data => {
            const code = data.current_weather.weathercode;
            const { emoji, label } = interpretWeatherCode(code);

            // через 5 сек обновим экран
            setTimeout(() => {
                document.getElementById("emoji").textContent = emoji;
                document.getElementById("label").textContent = `${label} в Москве`;
            }, 1500);
        })
        .catch(err => {
            setTimeout(() => {
                document.getElementById("emoji").textContent = "❌";
                document.getElementById("label").textContent = "Ошибка загрузки";
            }, 1500);
            console.error(err);
        });
}
