import random
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Flappy Bird GIFHUD",
    page_icon="🐦",
    layout="centered"
)

# --- CSS TÙY CHỈNH GIAO DIỆN KUTE (GIFHUD STYLE) ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #70c5ce 0%, #4682b4 100%);
    }
    .stButton>button {
        border-radius: 15px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        background-color: #f1c40f;
        color: #fff;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        background-color: #f39c12;
    }
    .game-card {
        background: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        backdrop-filter: blur(4px);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO TRẠNG THÁI TRÒ CHƠI (SESSION STATE) ---
if "flappy_started" not in st.session_state:
    st.session_state.flappy_started = False
    st.session_state.score = 0
    st.session_state.bird_y = 50        # Vị trí chiều cao của chim (0 - 100)
    st.session_state.game_over = False
    st.session_state.high_score = 0

# Link GIF minh họa chú chim Flappy Bird và chướng ngại vật ống nước
BIRD_GIF = "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif"
PIPE_GIF = "https://media.giphy.com/media/l0HlRnAWXxn0MhOBK/giphy.gif"
DEAD_GIF = "https://media.giphy.com/media/9JcMdbUTGxD3G/giphy.gif"

# --- 1. MÀN HÌNH CHÍNH (START SCREEN) ---
if not st.session_state.flappy_started:
    st.markdown("<h1 style='text-align: center; color: #fff; text-shadow: 2px 2px 4px #000;'>🐦 Flappy Bird GIFHUD 🌆</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #f1f2f6; font-size: 18px;'>Trò chơi né ống nước kinh điển với giao diện GIF động sinh động!</p>", unsafe_allow_html=True)
    
    # Nhúng âm thanh nền qua HTML5 audio
    st.markdown("""
        <audio autoplay loop hidden>
            <source src="https://www.bensound.com/bensound-music/bensound-cute.mp3" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(BIRD_GIF, width=250)
        if st.button("🚀 BẮT ĐẦU BAY", use_container_width=True):
            st.session_state.flappy_started = True
            st.session_state.score = 0
            st.session_state.bird_y = 50
            st.session_state.game_over = False
            st.rerun()

else:
    # --- 2. GIAO DIỆN TRÒ CHƠI CHÍNH ---
    
    # Nhúng âm thanh nền
    st.markdown("""
        <audio autoplay loop hidden>
            <source src="https://www.bensound.com/bensound-music/bensound-cute.mp3" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)

    st.markdown(f"<h2 style='text-align: center; color: white;'>🏆 Điểm Số: {st.session_state.score} | Kỷ Lục: {st.session_state.high_score}</h2>", unsafe_allow_html=True)

    # Khu vực hiển thị trò chơi GIFHUD
    col_l, col_m, col_r = st.columns([1, 3, 1])
    with col_m:
        if not st.session_state.game_over:
            st.markdown(f"""
            <div class="game-card" style="height: 300px; position: relative; overflow: hidden; background: linear-gradient(to bottom, #87CEEB, #E0F6FF);">
                <div style="position: absolute; top: {st.session_state.bird_y}%; left: 30%; transition: top 0.2s ease;">
                    <img src="{BIRD_GIF}" width="60px">
                </div>
                <div style="position: absolute; right: 20%; top: 20%;">
                    <img src="{PIPE_GIF}" width="40px" height="120px">
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="game-card" style="height: 300px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #ff7675;">
                <img src="{DEAD_GIF}" width="100px">
                <h2 style="color: white; margin: 10px 0;">GAME OVER!</h2>
                <p style="color: white;">Điểm của bạn: <b>{st.session_state.score}</b></p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- 3. BẢNG ĐIỀU KHIỂN BAY (FLAP CONTROLS) ---
    if not st.session_state.game_over:
        b1, b2, b3 = st.columns([1, 2, 1])
        with b2:
            if st.button("🦅 NHẤT CÁNH (FLAP UP!)", use_container_width=True):
                # Bay lên
                st.session_state.bird_y = max(10, st.session_state.bird_y - 20)
                st.session_state.score += 1
                if st.session_state.score > st.session_state.high_score:
                    st.session_state.high_score = st.session_state.score
                
                # Tỉ lệ ngẫu nhiên va chạm ống nước (Game Over)
                if random.random() < 0.25:
                    st.session_state.game_over = True
                st.rerun()

            # Tự động rơi xuống nhẹ sau mỗi lượt nếu không bấm kịp
            st.session_state.bird_y = min(85, st.session_state.bird_y + 10)
    else:
        b1, b2, b3 = st.columns([1, 2, 1])
        with b2:
            if st.button("🔄 CHƠI LẠI", use_container_width=True):
                st.session_state.game_over = False
                st.session_state.score = 0
                st.session_state.bird_y = 50
                st.rerun()

    # Nút quay về màn hình chính ở sidebar
    with st.sidebar:
        st.header("⚙️ Tùy Chọn")
        if st.button("🏠 Về Màn Hình Chính"):
            st.session_state.flappy_started = False
            st.session_state.game_over = False
            st.rerun()
