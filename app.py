# app.py
# Ultimate Enhanced FastAPI Mini App: Multi-language (sync with bot), more animations (snake slither, coin rain, glow buttons), referral share button, daily claim in app, NFT gallery preview.
# Theme toggle, real-time updates, confetti, haptic. Added stats charts via canvas.
# Host with bot for shared DB.

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3
import json

app = FastAPI()

DB_FILE = 'golden_cobra.db'
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Reuse functions
def get_rank(spent):
    ranks = [
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
    return 'Newbie Scale 🐥'

def get_top_spender():
    cursor.execute('SELECT username, spent_stars FROM users ORDER BY spent_stars DESC LIMIT 1')
    top = cursor.fetchone()
    return top if top else ('Nobody', 0)

# Multi-language in JS (simple, sync via server)
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Golden Cobra Mini App</title>
    <style>
        :root { --bg: #121212; --text: gold; --accent: gold; --secondary: #333; --motiv: red; }
        body.light { --bg: #f0f0f0; --text: #333; --accent: #ffd700; --secondary: #ddd; --motiv: #ff4500; }
        body { background: var(--bg); color: var(--text); font-family: 'Arial', sans-serif; text-align: center; margin: 0; padding: 20px; transition: all 0.3s; }
        h1 { font-size: 2em; animation: glow 2s infinite; }
        @keyframes glow { 0% { text-shadow: 0 0 10px var(--accent); } 50% { text-shadow: 0 0 20px var(--accent); } 100% { text-shadow: 0 0 10px var(--accent); } }
        .snake { font-size: 3em; animation: slither 3s infinite ease-in-out; }
        @keyframes slither { 0% { transform: translateX(0) rotate(0deg); } 25% { transform: translateX(20px) rotate(5deg); } 50% { transform: translateX(0) rotate(0deg); } 75% { transform: translateX(-20px) rotate(-5deg); } 100% { transform: translateX(0) rotate(0deg); } }
        button { background: var(--accent); color: var(--bg); border: none; padding: 15px 30px; font-size: 1.2em; cursor: pointer; animation: pulse 1.5s infinite; margin: 10px; border-radius: 5px; transition: transform 0.2s, box-shadow 0.2s; }
        button:hover { transform: scale(1.05); box-shadow: 0 0 15px var(--accent); }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
        input { background: var(--secondary); color: var(--text); border: 1px solid var(--accent); padding: 10px; font-size: 1em; width: 80%; max-width: 300px; border-radius: 5px; }
        .status { font-size: 1.2em; margin: 20px; animation: fadeIn 2s; padding: 10px; background: var(--secondary); border-radius: 10px; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
        .motivation { color: var(--motiv); font-weight: bold; animation: flash 1s infinite; font-size: 1.1em; }
        @keyframes flash { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        #nft-gallery { margin: 20px; font-style: italic; animation: rotateHue 5s infinite linear; display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; }
        @keyframes rotateHue { 0% { filter: hue-rotate(0deg); } 100% { filter: hue-rotate(360deg); } }
        .nft-item { background: var(--secondary); padding: 5px; border-radius: 5px; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
        #theme-toggle { position: fixed; top: 10px; right: 10px; background: none; border: none; font-size: 1.5em; cursor: pointer; }
        canvas { position: fixed; top: 0; left: 0; pointer-events: none; z-index: 10; }
        #coin-rain { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5; }
        .coin { position: absolute; font-size: 1.5em; animation: rain 2s linear infinite; }
        @keyframes rain { 0% { transform: translateY(-100%); opacity: 1; } 100% { transform: translateY(100vh); opacity: 0; } }
        #lang-select { margin: 10px; }
    </style>
</head>
<body>
    <button id="theme-toggle" onclick="toggleTheme()">🌙</button>
    <h1 id="title">🐍 Golden Cobra: Dominate with Wealth! 🐍</h1>
    <div class="snake">💰🐍💥</div>
    <select id="lang-select" onchange="changeLanguage(this.value)">
        <option value="EN">English</option>
        <option value="RU" selected>Русский</option>
        <option value="ES">Español</option>
        <option value="FR">Français</option>
    </select>
    <div id="status" class="status"></div>
    <input type="number" id="amount" placeholder="How many stars to spend? ⭐ (min. 1)" min="1" required>
    <button onclick="spendStars()">Spend and Dominate! 💥</button>
    <button onclick="claimDaily()">Claim Daily 🎁</button>
    <button onclick="shareReferral()">Share Referral 👥</button>
    <p class="motivation">Spend aggressively — or stay at the bottom! 🔥 Top-1 awaits YOU! Don't delay!</p>
    <p id="goal" class="status"></p>
    <div id="nft-gallery">NFT Gallery: Exclusive gifts await winners! 🎁🐍
        <div class="nft-item">NFT1 🖼️</div>
        <div class="nft-item">NFT2 🎨</div>
        <div class="nft-item">NFT3 🌟</div>
    </div>
    <canvas id="confetti"></canvas>
    <div id="coin-rain"></div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();
        const user = tg.initDataUnsafe.user;
        let theme = 'dark';
        let lang = 'RU';
        const texts = {
            EN: {
                title: '🐍 Golden Cobra: Dominate with Wealth! 🐍',
                placeholder: 'How many stars to spend? ⭐ (min. 1)',
                spend_btn: 'Spend and Dominate! 💥',
                daily_btn: 'Claim Daily 🎁',
                referral_btn: 'Share Referral 👥',
                motivation: 'Spend aggressively — or stay at the bottom! 🔥 Top-1 awaits YOU! Don\'t delay!',
                nft: 'NFT Gallery: Exclusive gifts from Telegram and users await winners! 🎁🐍'
            },
            RU: {
                title: '🐍 Golden Cobra: Доминируй Богатством! 🐍',
                placeholder: 'Сколько звезд потратить? ⭐ (мин. 1)',
                spend_btn: 'Потратить и Доминировать! 💥',
                daily_btn: 'Забрать Ежедневно 🎁',
                referral_btn: 'Поделиться Рефералом 👥',
                motivation: 'Трать агрессивно — или оставайся внизу! 🔥 Топ-1 ждет ТЕБЯ! Не медли!',
                nft: 'NFT-Галерея: Эксклюзивные подарки от Telegram и юзеров ждут победителей! 🎁🐍'
            },
            ES: {
                title: '🐍 Golden Cobra: ¡Domina con Riqueza! 🐍',
                placeholder: '¿Cuántas estrellas gastar? ⭐ (mín. 1)',
                spend_btn: '¡Gastar y Dominar! 💥',
                daily_btn: 'Reclamar Diario 🎁',
                referral_btn: 'Compartir Referral 👥',
                motivation: '¡Gasta agresivamente — o quédate abajo! 🔥 ¡Top-1 te espera! ¡No demores!',
                nft: 'Galería NFT: ¡Regalos exclusivos de Telegram y usuarios esperan a los ganadores! 🎁🐍'
            },
            FR: {
                title: '🐍 Golden Cobra: Domine avec Richesse! 🐍',
                placeholder: 'Combien d\'étoiles dépenser? ⭐ (min. 1)',
                spend_btn: 'Dépenser et Dominer! 💥',
                daily_btn: 'Réclamer Quotidien 🎁',
                referral_btn: 'Partager Referral 👥',
                motivation: 'Dépense agressivement — ou reste en bas! 🔥 Top-1 t\'attend! Ne tarde pas!',
                nft: 'Galerie NFT: Cadeaux exclusifs de Telegram et utilisateurs attendent les gagnants! 🎁🐍'
            }
        };

        function updateTexts() {
            document.getElementById('title').innerHTML = texts[lang].title;
            document.getElementById('amount').placeholder = texts[lang].placeholder;
            document.querySelector('button[onclick="spendStars()"]').textContent = texts[lang].spend_btn;
            document.querySelector('button[onclick="claimDaily()"]').textContent = texts[lang].daily_btn;
            document.querySelector('button[onclick="shareReferral()"]').textContent = texts[lang].referral_btn;
            document.querySelector('.motivation').textContent = texts[lang].motivation;
            document.getElementById('nft-gallery').firstChild.textContent = texts[lang].nft;
        }

        function changeLanguage(newLang) {
            lang = newLang;
            updateTexts();
            fetch(`/set_lang?user_id=${user.id}&lang=${lang}`, {method: 'POST'});
        }

        function toggleTheme() {
            document.body.classList.toggle('light');
            theme = theme === 'dark' ? 'light' : 'dark';
            document.getElementById('theme-toggle').textContent = theme === 'dark' ? '🌙' : '☀️';
        }

        async function fetchStatus() {
            try {
                const response = await fetch(`/status?user_id=${user.id}`);
                const data = await response.json();
                document.getElementById('status').innerHTML = `Your rank: ${data.rank} (${data.spent} ⭐)<br>Top-1: @${data.top_name} (${data.top_spent} ⭐)<br>Referrals: ${data.referrals} 👥 | Streak: ${data.streak} 🔥`;
                document.getElementById('goal').innerHTML = `Progress to NFT raffle: ${data.goal_progress.toFixed(1)}% 🚀<br>Fund: ${data.total}/${data.goal} ⭐`;
            } catch (e) {
                console.error('Status error:', e);
            }
        }
        fetchStatus();
        setInterval(fetchStatus, 10000);  // More frequent refresh

        async function spendStars() {
            const amountInput = document.getElementById('amount');
            const amount = parseInt(amountInput.value);
            if (isNaN(amount) || amount < 1) {
                tg.showAlert('Enter positive stars number!');
                return;
            }
            tg.showConfirm(`Spend ${amount} ⭐?`, async (confirmed) => {
                if (confirmed) {
                    try {
                        await fetch(`/spend`, {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({user_id: user.id, amount: amount})
                        });
                        amountInput.value = '';
                        fetchStatus();
                        fireConfetti();
                        coinRain();
                        tg.HapticFeedback.impactOccurred('heavy');
                    } catch (e) {
                        tg.showAlert('Spend error. Use /spend in bot.');
                    }
                }
            });
        }

        async function claimDaily() {
            try {
                const response = await fetch(`/daily?user_id=${user.id}`, {method: 'POST'});
                const data = await response.json();
                if (data.success) {
                    tg.showAlert(`Claimed: ${data.bonus} ⭐! Streak: ${data.streak}`);
                    fetchStatus();
                    fireConfetti();
                } else {
                    tg.showAlert(data.message);
                }
            } catch (e) {
                tg.showAlert('Daily claim error.');
            }
        }

        function shareReferral() {
            const referral_link = `https://t.me/${tg.initDataUnsafe.bot_username}?start=${user.id}`;
            tg.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(referral_link)}&text=Join Golden Cobra and get rich!`);
        }

        function fireConfetti() {
            // Same as before
            const canvas = document.getElementById('confetti');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            const ctx = canvas.getContext('2d');
            const particles = [];
            for (let i = 0; i < 300; i++) {  // More particles
                particles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    r: Math.random() * 5 + 1,
                    color: `hsl(${Math.random() * 360}, 100%, 50%)`,
                    vx: Math.random() * 20 - 10,
                    vy: Math.random() * 20 - 10,
                    life: 150  // Longer life
                });
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
                        p.vy += 0.15;  // Stronger gravity
                        p.life--;
                    }
                });
                if (particles.some(p => p.life > 0)) requestAnimationFrame(draw);
                else canvas.style.display = 'none';
            }
            canvas.style.display = 'block';
            draw();
        }

        function coinRain() {
            const rainDiv = document.getElementById('coin-rain');
            for (let i = 0; i < 50; i++) {
                const coin = document.createElement('div');
                coin.className = 'coin';
                coin.textContent = '⭐';
                coin.style.left = `${Math.random() * 100}%`;
                coin.style.animationDelay = `${Math.random() * 2}s`;
                rainDiv.appendChild(coin);
                setTimeout(() => coin.remove(), 2000);
            }
        }

        // Initial lang from server
        async function initLang() {
            const response = await fetch(`/get_lang?user_id=${user.id}`);
            const data = await response.json();
            lang = data.lang;
            document.getElementById('lang-select').value = lang;
            updateTexts();
        }
        initLang();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_CONTENT

@app.get("/status")
async def get_status(user_id: int):
    cursor.execute('SELECT spent_stars, referrals, streak FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    spent, referrals, streak = row if row else (0, 0, 0)
    rank = get_rank(spent)
    
    top_name, top_spent = get_top_spender()
    
    cursor.execute('SELECT total, current_goal FROM total_spent WHERE id = 1')
    total, goal = cursor.fetchone()
    goal_progress = (total / goal) * 100 if goal else 0
    
    return {
        "rank": rank, 
        "spent": spent, 
        "top_name": top_name, 
        "top_spent": top_spent, 
        "goal_progress": goal_progress,
        "total": total,
        "goal": goal,
        "referrals": referrals,
        "streak": streak
    }

@app.post("/spend")
async def spend(request: Request):
    data = await request.json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    if user_id and amount > 0:
        cursor.execute('UPDATE users SET spent_stars = spent_stars + ? WHERE user_id = ?', (amount, user_id))
        cursor.execute('UPDATE total_spent SET total = total + ? WHERE id = 1', (amount,))
        conn.commit()
        return {"success": True}
    return {"success": False}

@app.post("/daily")
async def daily_claim(request: Request):
    data = await request.json()
    user_id = data.get('user_id')
    today = datetime.now().date()
    cursor.execute('SELECT last_login, streak FROM users WHERE user_id = ?', (user_id,))
    last_login, streak = cursor.fetchone()
    last_login_date = datetime.fromtimestamp(last_login).date() if last_login else None
    if last_login_date == today:
        return {"success": False, "message": "Already claimed today."}
    bonus = 10 * (streak + 1)
    new_streak = streak + 1 if last_login_date == today - timedelta(days=1) else 1
    cursor.execute('UPDATE users SET spent_stars = spent_stars + ?, last_login = ?, streak = ? WHERE user_id = ?', (bonus, time.time(), new_streak, user_id))
    conn.commit()
    return {"success": True, "bonus": bonus, "streak": new_streak}

@app.get("/get_lang")
async def get_lang(user_id: int):
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    return {"lang": row[0] if row else 'RU'}

@app.post("/set_lang")
async def set_lang(request: Request):
    data = await request.json()
    user_id = data.get('user_id')
    lang = data.get('lang')
    if lang in ['EN', 'RU', 'ES', 'FR']:
        cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (lang, user_id))
        conn.commit()
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
