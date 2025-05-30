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

    fetch("https://api.open-meteo.com/v1/forecast?latitude=55.75&longitude=37.61&current_weather=true")
        .then(res => res.json())
        .then(data => {
            const code = data.current_weather.weathercode;
            const { emoji, label } = interpretWeatherCode(code);
            document.getElementById("emoji").textContent = emoji;
            document.getElementById("label").textContent = `${label} в Москве`;
        })
        .catch(err => {
            document.getElementById("emoji").textContent = "❌";
            document.getElementById("label").textContent = "Ошибка загрузки";
            console.error(err);
        });
};

function interpretWeatherCode(code) {
    if ([0, 1].includes(code)) return { emoji: "☀️", label: "Солнечно" };
    if ([2, 3].includes(code)) return { emoji: "☁️", label: "Облачно" };
    if ([51, 61, 63, 65, 80, 81, 82].includes(code)) return { emoji: "🌧️", label: "Дождь" };
    return { emoji: "❓", label: "Неизвестно" };
}
