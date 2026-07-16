from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# HTML + CSS + JavaScript (все в одном файле)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Аналитический дашборд: крах рынка?</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(145deg, #1a1a2e, #16213e);
            color: #e0e0e0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .dashboard {
            max-width: 1200px;
            width: 100%;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 32px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.08);
        }
        h1 {
            text-align: center;
            font-weight: 300;
            letter-spacing: 1px;
            margin-bottom: 10px;
            font-size: 2.2rem;
            background: linear-gradient(90deg, #f7971e, #ffd200);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            opacity: 0.7;
            margin-bottom: 30px;
            font-style: italic;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
        }
        .card {
            background: rgba(0,0,0,0.3);
            border-radius: 24px;
            padding: 20px 25px;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            transition: 0.2s;
        }
        .card:hover {
            border-color: rgba(255,215,0,0.2);
        }
        .card h3 {
            font-weight: 300;
            margin-bottom: 15px;
            color: #f0e6a0;
            border-bottom: 1px solid rgba(255,215,0,0.15);
            padding-bottom: 8px;
        }
        .slider-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .slider-group label {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            opacity: 0.8;
        }
        input[type=range] {
            width: 100%;
            height: 6px;
            -webkit-appearance: none;
            background: linear-gradient(90deg, #ff6b6b, #feca57);
            border-radius: 10px;
            outline: none;
        }
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: white;
            cursor: pointer;
            box-shadow: 0 0 10px #feca57;
        }
        .value-badge {
            background: #2d2d44;
            padding: 4px 12px;
            border-radius: 30px;
            font-size: 0.9rem;
        }
        .btn {
            background: rgba(255,215,0,0.12);
            border: 1px solid #feca57;
            color: #feca57;
            padding: 10px 20px;
            border-radius: 40px;
            cursor: pointer;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: 0.15s;
            width: 100%;
            margin-top: 10px;
            font-size: 1rem;
        }
        .btn:hover {
            background: #feca57;
            color: #1a1a2e;
            box-shadow: 0 0 25px #feca57aa;
        }
        .btn-danger {
            background: rgba(255,80,80,0.15);
            border-color: #ff6b6b;
            color: #ff6b6b;
        }
        .btn-danger:hover {
            background: #ff6b6b;
            color: #1a1a2e;
            box-shadow: 0 0 25px #ff6b6baa;
        }
        .quote-box {
            background: rgba(255,215,0,0.05);
            border-left: 4px solid #feca57;
            padding: 14px 18px;
            border-radius: 12px;
            margin: 15px 0;
            font-style: italic;
            min-height: 70px;
        }
        .flex-row {
            display: flex;
            justify-content: space-between;
            gap: 15px;
            flex-wrap: wrap;
        }
        .chart-container {
            position: relative;
            height: 200px;
            margin-top: 10px;
        }
        .full-width {
            grid-column: 1 / -1;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            text-align: center;
        }
        .stat-item {
            background: rgba(0,0,0,0.2);
            border-radius: 16px;
            padding: 8px;
        }
        .stat-number {
            font-size: 1.8rem;
            font-weight: 600;
            color: #feca57;
        }
        .stat-label {
            font-size: 0.7rem;
            opacity: 0.6;
            text-transform: uppercase;
        }
        @media (max-width: 800px) {
            .grid { grid-template-columns: 1fr; }
            .full-width { grid-column: 1; }
        }
        .badge-buffett {
            background: #2d4059;
            border-radius: 30px;
            padding: 2px 14px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>📉 Crash-O-Meter</h1>
        <div class="subtitle">Мнения аналитиков: от «всё рухнет» до «вечный рост»</div>

        <div class="grid">
            <!-- Левая колонка: управление -->
            <div class="card">
                <h3>🎚️ Рычаги паники / жадности</h3>
                <div class="slider-group">
                    <label>
                        <span>🔴 Мультипликаторы S&P 500 (Shiller CAPE)</span>
                        <span class="value-badge" id="capeValue">34.2</span>
                    </label>
                    <input type="range" id="capeSlider" min="25" max="45" step="0.1" value="34.2">
                </div>
                <div class="slider-group" style="margin-top: 15px;">
                    <label>
                        <span>🏦 Доля кэша у Баффета (млрд $)</span>
                        <span class="value-badge" id="cashValue">147</span>
                    </label>
                    <input type="range" id="cashSlider" min="100" max="200" step="1" value="147">
                </div>
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button class="btn" id="btnBull">🐂 Бычий сценарий</button>
                    <button class="btn btn-danger" id="btnBear">🐻 Медвежий сценарий</button>
                </div>
                <button class="btn" id="btnRandom" style="background: rgba(100,200,255,0.08); border-color: #4fc3f7; color: #4fc3f7; margin-top: 8px;">
                    🎲 Случайное мнение
                </button>
            </div>

            <!-- Правая колонка: цитаты и индикаторы -->
            <div class="card">
                <h3>💬 Мнение аналитика</h3>
                <div class="quote-box" id="quoteDisplay">
                    «Посмотрите на эти дикие мультиплиплы — сейчас долбанёт!»
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                    <span>📊 Вероятность краха:</span>
                    <span id="crashProb" style="font-weight: 600; color: #ff6b6b;">42%</span>
                </div>
                <div style="background: #2d2d44; height: 6px; border-radius: 10px; margin: 6px 0 12px;">
                    <div id="probBar" style="height: 6px; width: 42%; background: linear-gradient(90deg, #ff6b6b, #feca57); border-radius: 10px;"></div>
                </div>
                <div class="stat-grid">
                    <div class="stat-item"><div class="stat-number" id="statCape">34.2</div><div class="stat-label">CAPE</div></div>
                    <div class="stat-item"><div class="stat-number" id="statCash">147</div><div class="stat-label">Кэш Баффета</div></div>
                    <div class="stat-item"><div class="stat-number" id="statFear">65</div><div class="stat-label">Индекс страха</div></div>
                </div>
            </div>

            <!-- График: динамика краха (имитация) -->
            <div class="card full-width">
                <h3>📈 Индикатор рыночного безумия (последние 12 месяцев)</h3>
                <div class="chart-container">
                    <canvas id="crashChart"></canvas>
                </div>
                <div style="display: flex; justify-content: flex-end; gap: 20px; margin-top: 6px; font-size: 0.7rem; opacity: 0.5;">
                    <span>⬆️ Пузырь</span>
                    <span>⬇️ Крах</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // --- Данные для графика ---
        const ctx = document.getElementById('crashChart').getContext('2d');
        let chartData = [65, 70, 68, 72, 78, 82, 79, 85, 88, 84, 90, 87]; // условный индекс безумия
        const labels = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];

        const crashChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Индекс безумия',
                    data: chartData,
                    borderColor: '#feca57',
                    backgroundColor: 'rgba(254, 202, 87, 0.05)',
                    borderWidth: 3,
                    pointBackgroundColor: '#feca57',
                    tension: 0.2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        ticks: { color: '#aaa' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#aaa' }
                    }
                }
            }
        });

        // --- Элементы управления ---
        const capeSlider = document.getElementById('capeSlider');
        const cashSlider = document.getElementById('cashSlider');
        const capeValue = document.getElementById('capeValue');
        const cashValue = document.getElementById('cashValue');
        const quoteDisplay = document.getElementById('quoteDisplay');
        const crashProb = document.getElementById('crashProb');
        const probBar = document.getElementById('probBar');
        const statCape = document.getElementById('statCape');
        const statCash = document.getElementById('statCash');
        const statFear = document.getElementById('statFear');

        // Функция обновления всего дашборда
        function updateDashboard() {
            const cape = parseFloat(capeSlider.value);
            const cash = parseInt(cashSlider.value);
            capeValue.textContent = cape.toFixed(1);
            cashValue.textContent = cash;

            // Вычисляем вероятность краха (формула фантазийная)
            let baseProb = 30 + (cape - 30) * 1.8 - (cash - 130) * 0.15;
            baseProb = Math.min(95, Math.max(5, baseProb));
            const prob = Math.round(baseProb);
            crashProb.textContent = prob + '%';
            probBar.style.width = prob + '%';
            if (prob > 70) probBar.style.background = 'linear-gradient(90deg, #ff6b6b, #ee5a24)';
            else if (prob > 40) probBar.style.background = 'linear-gradient(90deg, #ff6b6b, #feca57)';
            else probBar.style.background = 'linear-gradient(90deg, #feca57, #4fc3f7)';

            statCape.textContent = cape.toFixed(1);
            statCash.textContent = cash;
            const fearIndex = Math.round(30 + (cape - 25) * 2.2 + (cash - 100) * 0.2);
            statFear.textContent = Math.min(100, Math.max(0, fearIndex));

            // Генерируем цитату в зависимости от вероятности
            let quote = '';
            if (prob > 70) {
                quote = '💀 «Крах неизбежен! Баффет сидит в кэше, мультипликаторы заоблачные. Продавай всё!»';
            } else if (prob > 50) {
                quote = '😰 «Рынок перегрет, но ФРС может смягчить падение. Лучше держать оборону.»';
            } else if (prob > 30) {
                quote = '🤔 «Мнения разделились. Новый глава ФРС — надежда на мягкую посадку.»';
            } else {
                quote = '🚀 «Вечный рост! Печатный станок даже не включали, у рынка есть потенциал +20%!»';
            }
            // Добавляем нюанс от Баффета
            if (cash > 170) quote += ' (Баффет наращивает кэш — тревожный знак)';
            else if (cash < 120) quote += ' (Баффет инвестирует — значит, дно близко)';
            quoteDisplay.textContent = quote;

            // Обновляем график: добавляем новый "месяц" (сдвигаем)
            const newPoint = Math.min(100, Math.max(40, prob + (Math.random() * 10 - 5)));
            chartData.push(Math.round(newPoint));
            if (chartData.length > 12) chartData.shift();
            crashChart.data.datasets[0].data = chartData;
            crashChart.update();
        }

        // События слайдеров
        capeSlider.addEventListener('input', updateDashboard);
        cashSlider.addEventListener('input', updateDashboard);

        // Кнопки сценариев
        document.getElementById('btnBull').addEventListener('click', function() {
            capeSlider.value = '28.5';
            cashSlider.value = '185';
            updateDashboard();
        });
        document.getElementById('btnBear').addEventListener('click', function() {
            capeSlider.value = '42.0';
            cashSlider.value = '110';
            updateDashboard();
        });
        document.getElementById('btnRandom').addEventListener('click', function() {
            capeSlider.value = (25 + Math.random() * 20).toFixed(1);
            cashSlider.value = Math.round(100 + Math.random() * 100);
            updateDashboard();
        });

        // Инициализация
        updateDashboard();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
