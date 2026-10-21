<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flappy Bird Retro 3D/2D</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        body { font-family: 'Press Start 2P', monospace; user-select: none; margin: 0; overflow: hidden; background: #4ec0ca; }
        .pixel-box { image-rendering: pixelated; }
    </style>
</head>
<body class="flex items-center justify-center h-screen w-screen">

    <!-- MÀN HÌNH CHÍNH (START SCREEN) -->
    <div id="start-screen" class="absolute inset-0 z-50 flex flex-col items-center justify-center bg-sky-400">
        <div class="text-center bg-white/90 p-8 rounded-2xl shadow-2xl border-4 border-yellow-500 max-w-md mx-4">
            <h1 class="text-3xl font-black text-yellow-600 mb-4 animate-bounce">FLAPPY BIRD</h1>
            <div class="my-4 flex justify-center">
                <!-- Icon chim mẫu -->
                <div class="w-16 h-12 bg-yellow-400 border-4 border-black relative rounded-lg flex items-center justify-center shadow-md">
                    <div class="absolute right-[-8px] top-3 w-4 h-4 bg-red-500 border-2 border-black"></div>
                    <div class="absolute right-2 top-2 w-3 h-3 bg-white border border-black rounded-full flex items-center justify-center">
                        <div class="w-1 h-1 bg-black rounded-full"></div>
                    </div>
                </div>
            </div>
            <p class="text-xs text-gray-600 mb-6 leading-relaxed">Nhấn phím Cách (Space) hoặc bấm nút bên dưới để bay qua các ống nước!</p>
            <button onclick="startGame()" class="w-full py-4 bg-yellow-400 hover:bg-yellow-500 text-black font-black text-sm rounded-xl shadow-lg border-2 border-black active:scale-95 transition">
                🚀 BẮT ĐẦU CHƠI
            </button>
        </div>
    </div>

    <!-- CANVAS GAME CHÍNH -->
    <div class="relative shadow-2xl rounded-xl overflow-hidden border-4 border-black">
        <canvas id="gameCanvas" width="400" height="600" class="block"></canvas>
    </div>

    <!-- SCRIPT LOGIC GAME & ÂM THANH -->
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Biến trạng thái game
        let gameStarted = false;
        let gameOver = false;
        let score = 0;
        let highScore = 0;

        // Chú chim
        let bird = {
            x: 80,
            y: 250,
            width: 34,
            height: 24,
            gravity: 0.5,
            lift: -8,
            velocity: 0
        };

        // Ống nước
        let pipes = [];
        let pipeWidth = 60;
        let pipeGap = 160;
        let pipeSpeed = 3;
        let frameCount = 0;

        // Web Audio API Tổng hợp âm thanh nền và tiếng nhảy
        let audioCtx = null;
        function initAudio() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }

        function playSound(type) {
            if (!audioCtx) return;
            let osc = audioCtx.createOscillator();
            let gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            let now = audioCtx.currentTime;

            if (type === 'flap') {
                osc.frequency.setValueAtTime(300, now);
                osc.frequency.exponentialRampToValueAtTime(600, now + 0.1);
                gain.gain.setValueAtTime(0.1, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.1);
                osc.start(now); osc.stop(now + 0.1);
            } else if (type === 'score') {
                osc.frequency.setValueAtTime(587.33, now); // D5
                osc.frequency.setValueAtTime(880, now + 0.1); // A5
                gain.gain.setValueAtTime(0.15, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
                osc.start(now); osc.stop(now + 0.2);
            } else if (type === 'hit') {
                osc.frequency.setValueAtTime(150, now);
                osc.frequency.linearRampToValueAtTime(50, now + 0.2);
                gain.gain.setValueAtTime(0.2, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
                osc.start(now); osc.stop(now + 0.2);
            }
        }

        function startGame() {
            initAudio();
            document.getElementById('start-screen').style.display = 'none';
            gameStarted = true;
            resetGame();
        }

        function resetGame() {
            bird.y = 250;
            bird.velocity = 0;
            pipes = [];
            score = 0;
            frameCount = 0;
            gameOver = false;
        }

        // Điều khiển phím và chuột
        window.addEventListener('keydown', e => {
            if (e.code === 'Space' && gameStarted) {
                if (gameOver) {
                    resetGame();
                } else {
                    bird.velocity = bird.lift;
                    playSound('flap');
                }
            }
        });

        canvas.addEventListener('click', () => {
            if (gameStarted) {
                if (gameOver) {
                    resetGame();
                } else {
                    bird.velocity = bird.lift;
                    playSound('flap');
                }
            }
        });

        // Tạo ống nước
        function addPipe() {
            let minHeight = 50;
            let maxHeight = canvas.height - pipeGap - 100;
            let height = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
            pipes.push({
                x: canvas.width,
                top: height,
                bottom: canvas.height - height - pipeGap,
                passed: false
            });
        }

        // Vẽ hình nền trời mây và khung cảnh
        function drawBackground() {
            // Màu nền trời
            ctx.fillStyle = "#4ec0ca";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Mây trôi trang trí
            ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
            ctx.beginPath();
            ctx.arc(100, 100, 30, 0, Math.PI * 2);
            ctx.arc(130, 90, 40, 0, Math.PI * 2);
            ctx.arc(160, 100, 30, 0, Math.PI * 2);
            ctx.fill();

            ctx.beginPath();
            ctx.arc(300, 180, 25, 0, Math.PI * 2);
            ctx.arc(325, 170, 35, 0, Math.PI * 2);
            ctx.arc(350, 180, 25, 0, Math.PI * 2);
            ctx.fill();

            // Đất nền bên dưới
            ctx.fillStyle = "#ded895";
            ctx.fillRect(0, canvas.height - 50, canvas.width, 50);
            ctx.fillStyle = "#73bf2e";
            ctx.fillRect(0, canvas.height - 50, canvas.width, 15);
        }

        // Vẽ ống nước pixel chuẩn ảnh mẫu
        function drawPipes() {
            pipes.forEach(pipe => {
                // Ống trên
                ctx.fillStyle = "#73bf2e";
                ctx.fillRect(pipe.x, 0, pipeWidth, pipe.top);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 2;
                ctx.strokeRect(pipe.x, 0, pipeWidth, pipe.top);
                // Viền đầu ống trên
                ctx.fillRect(pipe.x - 4, pipe.top - 24, pipeWidth + 8, 24);
                ctx.strokeRect(pipe.x - 4, pipe.top - 24, pipeWidth + 8, 24);

                // Ống dưới
                ctx.fillRect(pipe.x, canvas.height - pipe.bottom, pipeWidth, pipe.bottom);
                ctx.strokeRect(pipe.x, canvas.height - pipe.bottom, pipeWidth, pipe.bottom);
                // Viền đầu ống dưới
                ctx.fillRect(pipe.x - 4, canvas.height - pipe.bottom, pipeWidth + 8, 24);
                ctx.strokeRect(pipe.x - 4, canvas.height - pipe.bottom, pipeWidth + 8, 24);
            });
        }

        // Vẽ chú chim vàng cute
        function drawBird() {
            ctx.save();
            ctx.translate(bird.x + bird.width / 2, bird.y + bird.height / 2);
            let rot = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, (bird.velocity / 10)));
            ctx.rotate(rot);

            // Thân chim
            ctx.fillStyle = "#f8e71c";
            ctx.fillRect(-bird.width / 2, -bird.height / 2, bird.width, bird.height);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 2;
            ctx.strokeRect(-bird.width / 2, -bird.height / 2, bird.width, bird.height);

            // Cánh chim
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(-bird.width / 4, 0, 12, 8);
            ctx.strokeRect(-bird.width / 4, 0, 12, 8);

            // Mỏ chim
            ctx.fillStyle = "#f5a623";
            ctx.fillRect(bird.width / 2 - 4, -4, 10, 10);
            ctx.strokeRect(bird.width / 2 - 4, -4, 10, 10);

            // Mắt chim
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(4, -10, 10, 10);
            ctx.fillStyle = "#000000";
            ctx.fillRect(10, -8, 4, 4);

            ctx.restore();
        }

        // Vòng lặp cập nhật game chính
        function update() {
            if (!gameStarted) return;

            if (!gameOver) {
                frameCount++;
                if (frameCount % 100 === 0) {
                    addPipe();
                }

                // Cập nhật vị trí chim
                bird.velocity += bird.gravity;
                bird.y += bird.velocity;

                // Kiểm tra chạm đất hoặc bay quá cao
                if (bird.y + bird.height >= canvas.height - 50 || bird.y <= 0) {
                    gameOver = true;
                    playSound('hit');
                }

                // Cập nhật ống nước
                pipes.forEach(pipe => {
                    pipe.x -= pipeSpeed;

                    // Tính điểm khi vượt qua ống
                    if (!pipe.passed && pipe.x + pipeWidth < bird.x) {
                        score++;
                        pipe.passed = true;
                        playSound('score');
                        if (score > highScore) highScore = score;
                    }

                    // Kiểm tra va chạm ống nước
                    if (
                        bird.x < pipe.x + pipeWidth &&
                        bird.x + bird.width > pipe.x &&
                        (bird.y < pipe.top || bird.y + bird.height > canvas.height - pipe.bottom)
                    ) {
                        gameOver = true;
                        playSound('hit');
                    }
                });

                // Xóa ống đã đi qua màn hình
                pipes = pipes.filter(pipe => pipe.x + pipeWidth > 0);
            }
        }

        // Render giao diện đồ họa
        function draw() {
            drawBackground();
            drawPipes();
            drawBird();

            // Hiển thị Điểm số trên màn hình
            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 24px 'Press Start 2P', monospace";
            ctx.textAlign = "center";
            ctx.shadowColor = "black";
            ctx.shadowBlur = 4;
            ctx.fillText(score, canvas.width / 2, 60);
            ctx.shadowBlur = 0;

            // Màn hình Game Over
            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#ffffff";
                ctx.font = "20px 'Press Start 2P', monospace";
                ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 40);

                ctx.font = "12px 'Press Start 2P', monospace";
                ctx.fillText(`Điểm: ${score} | Kỷ Lục: ${highScore}`, canvas.width / 2, canvas.height / 2);
                ctx.fillText("Nhấn Màn Hình hoặc Phím Cách để chơi lại", canvas.width / 2, canvas.height / 2 + 50);
            }
        }

        // Vòng lặp game chạy liên tục
        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
