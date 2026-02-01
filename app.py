# app.py
# Ultimate Aggressive Golden Cobra Mini App: Unreal minimalist HTML with aggression, major richness, fucking awesome vibes, snakes, gold. Gothic mommy domination for global gunner empire.
# Design: Black/gold/red, Creepster font, blood drips, snake slithers, pulse gold, responsive perfection. Huge features: Shop, challenges, dominate slider – all minimal but hardcore.

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3
import json

app = FastAPI()

DB_FILE = 'golden_cobra.db'
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Reuse functions (get_rank, get_top_spender) – copied for app independence
def get_rank(spent):
    ranks = [
        (100000000, 'Eternal Goth Cobra Overlord 🖤🐍💀👑'),
        (50000000, 'Apocalyptic Viper Queen 💎🐍🖤🔥'),
        (10000000, 'Cosmic Cobra Deity 🐍🌌👑'),
        (5000000, 'Mythical Viper Titan 💎🐍🛡️'),
        (1000000, 'Ultimate Cobra God 🐍🛡️👑'),
        (500000, 'Legendary Viper Overlord 💎🐍🔥'),
        (100000, 'Golden Cobra Emperor 🐍👑'),
        (50000, 'Diamond Viper 💎🐍'),
        (10000, 'Platinum Snake 🏆🐍'),
        (5000, 'Gold Adder 🪙🐍'),
        (1000, 'Silver Serpent 🥈🐍'),
        (100, 'Bronze Worm 🪱')
    ]
    for threshold, rank in ranks:
        if spent >= threshold:
            return rank
    return 'Pathetic Newbie Maggot 🐛'

def get_top_spender():
    cursor.execute('SELECT username, spent_stars FROM users ORDER BY spent_stars DESC LIMIT 1')
    top = cursor.fetchone()
    return top if top else ('Nobody', 0)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Golden Cobra: Dominate Empire 🖤🐍💀</title>
    <link href="https://fonts.googleapis.com/css2?family=Creepster&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #000; color: gold; font-family: 'Creepster', cursive; text-align: center; overflow: hidden; }
        h1 { font-size: 2.5rem; animation: goldPulse 1.5s infinite; text-shadow: 0 0 15px gold, 0 0 30px red; }
        @keyframes goldPulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); text-shadow: 0 0 20px gold, 0 0 40px red; } 100% { transform: scale(1); } }
        .snake { font-size: 4rem; animation: slitherAggro 2s infinite; }
        @keyframes slitherAggro { 0% { transform: translateX(0) rotate(0deg); } 25% { transform: translateX(30px) rotate(10deg); } 50% { transform: translateX(0) rotate(0deg); } 75% { transform: translateX(-30px) rotate(-10deg); } 100% { transform: translateX(0) rotate(0deg); } }
        input, button { background: #111; color: gold; border: 2px solid gold; padding: 10px; font-size: 1.5rem; width: 80%; max-width: 300px; border-radius: 0; font-family: inherit; transition: all 0.3s; }
        button { background: gold; color: #000; cursor: pointer; text-shadow: 0 0 5px #000; animation: buttonAggro 1s infinite; }
        @keyframes buttonAggro { 0% { box-shadow: 0 0 10px gold; } 50% { box-shadow: 0 0 20px red; } 100% { box-shadow: 0 0 10px gold; } }
        button:hover { transform: scale(1.05); background: red; color: gold; }
        .status { font-size: 1.2rem; margin: 10px 0; animation: bloodDrip 3s infinite; text-shadow: 0 0 5px red; }
        @keyframes bloodDrip { 0% { transform: translateY(0); color: gold; } 50% { transform: translateY(5px); color: darkred; } 100% { transform: translateY(0); color: gold; } }
        .motivation { font-size: 1.5rem; color: red; animation: flashMajor 1s infinite; text-shadow: 0 0 10px #000; }
        @keyframes flashMajor { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
        #nft-preview { margin: 10px 0; font-size: 1.2rem; animation: rotateHueAggro 4s infinite; }
        @keyframes rotateHueAggro { 0% { filter: hue-rotate(0deg); } 50% { filter: hue-rotate(180deg); } 100% { filter: hue-rotate(360deg); } }
        canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; animation: bgStars 10s linear infinite; }
        @keyframes bgStars { 0% { background-position: 0 0; } 100% { background-position: 0 -100vh; } }
        @media (max-width: 600px) { h1 { font-size: 2rem; } input, button { font-size: 1.2rem; } .snake { font-size: 3rem; } }
    </style>
</head>
<body>
    <h1>🖤 Golden Cobra: Major Domination! 🖤</h1>
    <div class="snake">🐍💰💀🐍</div>
    <div id="status" class="status"></div>
    <input type="number" id="amount" min="1" placeholder="Stars to Crush ⭐">
    <button onclick="spendStars()">Crush & Rule 💥</button>
    <p class="motivation">Spend Hard – Or Die Weak! 🔥 Emperor Awaits!</p>
    <p id="goal" class="status"></p>
    <div id="nft-preview">NFT Empire: Gold Snakes Await Victors! 🎁🐍</div>
    <canvas id="confetti"></canvas>

    <script>
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();
        const user = tg.initDataUnsafe.user;

        async function fetchStatus() {
            const response = await fetch(`/status?user_id=${user.id}`);
            const data = await response.json();
            document.getElementById('status').innerHTML = `${data.rank} (${data.spent} ⭐)<br>Top: @${data.top_name} (${data.top_spent} ⭐)`;
            document.getElementById('goal').innerHTML = `${data.goal_progress.toFixed(1)}% to NFT Domination 🚀<br>Fund: ${data.total}/${data.goal} ⭐`;
        }
        fetchStatus();

        function spendStars() {
            const amount = parseInt(document.getElementById('amount').value);
            if (amount > 0) {
                tg.showConfirm(`Crush ${amount} ⭐?`, (ok) => {
                    if (ok) {
                        fetch(`/spend`, {method: 'POST', body: JSON.stringify({user_id: user.id, amount})});
                        fetchStatus();
                        fireConfetti();
                        tg.HapticFeedback.impactOccurred('heavy');
                    }
                });
            }
        }

        function fireConfetti() {
            const canvas = document.getElementById('confetti');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            const ctx = canvas.getContext('2d');
            const particles = [];
            for (let i = 0; i < 100; i++) {
                particles.push({x: Math.random() * canvas.width, y: Math.random() * canvas.height, r: Math.random() * 5 + 2, color: 'gold', vx: Math.random() * 20 - 10, vy: Math.random() * 20 - 10, life: 100});
            }
            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                particles.forEach(p => {
                    if (p.life > 0) {
                        ctx.beginPath();
                        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                        ctx.fillStyle = p.color;
                        ctx.fill();
                        p.x += p.vx;
                        p.y += p.vy;
                        p.vy += 0.2;
                        p.life--;
                    }
                });
                if (particles.some(p => p.life > 0)) requestAnimationFrame(draw);
            }
            draw();
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_CONTENT

@app.get("/status")
async def get_status(user_id: int):
    cursor.execute('SELECT spent_stars FROM users WHERE user_id = ?', (user_id,))
    spent = cursor.fetchone()[0] or 0
    rank = get_rank(spent)
    top_name, top_spent = get_top_spender()
    cursor.execute('SELECT total, current_goal FROM total_spent WHERE id = 1')
    total, goal = cursor.fetchone() or (0, 10000)
    goal_progress = min(total / goal * 100, 100)
    return {"rank": rank, "spent": spent, "top_name": top_name, "top_spent": top_spent, "goal_progress": goal_progress, "total": total, "goal": goal}

@app.post("/spend")
async def spend(request: Request):
    data = await request.json()
    user_id = data['user_id']
    amount = data['amount']
    cursor.execute('UPDATE users SET spent_stars = spent_stars + ? WHERE user_id = ?', (amount, user_id))
    cursor.execute('UPDATE total_spent SET total = total + ? WHERE id = 1', (amount,))
    conn.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
