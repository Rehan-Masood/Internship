const socket = io();
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const leaderboardList = document.getElementById('leaderboardList');
const activityFeed = document.getElementById('activityFeed');
const levelDisplay = document.getElementById('levelDisplay');
const gameOverOverlay = document.getElementById('gameOverOverlay');

let myId = null;
let players = {};
let coin = {};
let walls = [];
let particles = [];

socket.on('connect', () => {
    socket.emit('join_game', { username: 'Pilot_' + Math.floor(Math.random() * 900 + 100) });
});

socket.on('init_state', (data) => {
    myId = data.my_id;
    players = data.players;
    coin = data.coin;
    walls = data.walls;
    levelDisplay.innerText = `LEVEL ${data.level}`;
    logFeed('System connected to Neon Arena.');
    render();
});

socket.on('state_update', (data) => {
    if (players[data.id]) {
        particles.push({
            x: players[data.id].x,
            y: players[data.id].y,
            color: players[data.id].color,
            alpha: 0.6,
            radius: 6
        });
        players[data.id].x = data.x;
        players[data.id].y = data.y;
    }
});

socket.on('level_up', (data) => {
    walls = data.walls;
    levelDisplay.innerText = `LEVEL ${data.level}`;
    logFeed(`🚀 ${data.player} TRIGGERED LEVEL ${data.level}! Hardness increased!`);
});

socket.on('game_over', () => {
    gameOverOverlay.style.display = 'flex';
    logFeed('❌ Critical collision! System offline.');
});

socket.on('player_respawned', (data) => {
    if (players[data.id]) {
        players[data.id].x = data.x;
        players[data.id].y = data.y;
    }
});

socket.on('coin_spawned', (data) => {
    coin = data.coin;
    if (players[data.collector_id]) {
        players[data.collector_id].score = data.score;
    }
    updateLeaderboard();
});

function respawnPlayer() {
    gameOverOverlay.style.display = 'none';
    socket.emit('respawn_player');
}

window.addEventListener('keydown', (e) => {
    let direction = null;
    if (e.key === 'ArrowUp' || e.key === 'w') direction = 'up';
    if (e.key === 'ArrowDown' || e.key === 's') direction = 'down';
    if (e.key === 'ArrowLeft' || e.key === 'a') direction = 'left';
    if (e.key === 'ArrowRight' || e.key === 'd') direction = 'right';
    
    if (direction) socket.emit('move_player', { direction });
});

function logFeed(msg) {
    const item = document.createElement('div');
    item.className = 'feed-item';
    item.innerText = msg;
    activityFeed.prepend(item);
}

function updateLeaderboard() {
    leaderboardList.innerHTML = '';
    const sorted = Object.entries(players).sort((a, b) => b[1].score - a[1].score);

    sorted.forEach(([id, p]) => {
        const item = document.createElement('div');
        item.className = 'leader-row';
        const isMe = id === myId ? ' (You)' : '';
        item.innerHTML = `
            <div>${p.name}${isMe}</div>
            <div style="color: var(--neon-gold); font-weight: 700;">${p.score}</div>
        `;
        leaderboardList.appendChild(item);
    });
}

function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Render Particle Trails
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.fill();
        ctx.globalAlpha = 1.0;
        p.alpha -= 0.04;
        if (p.alpha <= 0) particles.splice(i, 1);
    }

    // Render Neon Walls
    walls.forEach(w => {
        ctx.shadowBlur = 15;
        ctx.shadowColor = w.color;
        ctx.fillStyle = w.color;
        ctx.fillRect(w.x, w.y, w.w, w.h);
        ctx.shadowBlur = 0;
    });

    // Render Gold Power Core
    if (coin.x) {
        ctx.shadowBlur = 20;
        ctx.shadowColor = '#ffb700';
        ctx.beginPath();
        ctx.arc(coin.x, coin.y, 10, 0, Math.PI * 2);
        ctx.fillStyle = '#ffb700';
        ctx.fill();
        ctx.shadowBlur = 0;
    }

    // Render Players
    for (let id in players) {
        const p = players[id];
        ctx.shadowBlur = 15;
        ctx.shadowColor = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 14, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
        ctx.shadowBlur = 0;
    }

    requestAnimationFrame(render);
}