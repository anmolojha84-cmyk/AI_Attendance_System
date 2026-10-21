import io
import socket
import qrcode
import streamlit as st
import streamlit.components.v1 as components

def apply_custom_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F6 100%);
    color: #0F172A;
}
</style>

<!-- PWA Meta Tags & Web App Manifest Injection -->
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="AI Attendance">
<meta name="theme-color" content="#1E3A8A">

<script>
if (!document.querySelector('link[rel="manifest"]')) {
    const manifest = {
      "name": "AI Smart Attendance System",
      "short_name": "AI Attendance",
      "start_url": window.location.href,
      "display": "standalone",
      "orientation": "portrait",
      "background_color": "#F8FAFC",
      "theme_color": "#1E3A8A",
      "icons": [
        {
          "src": "https://img.icons8.com/color/192/graduation-cap.png",
          "sizes": "192x192",
          "type": "image/png"
        },
        {
          "src": "https://img.icons8.com/color/512/graduation-cap.png",
          "sizes": "512x512",
          "type": "image/png"
        }
      ]
    };
    const blob = new Blob([JSON.stringify(manifest)], {type: 'application/json'});
    const manifestURL = URL.createObjectURL(blob);
    const link = document.createElement('link');
    link.rel = 'manifest';
    link.href = manifestURL;
    document.head.appendChild(link);
}
</script>
<style>

.hero-card {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 55%, #2563EB 100%);
    color: white;
    padding: 26px 24px;
    border-radius: 20px;
    margin-bottom: 22px;
    box-shadow: 0 12px 28px -6px rgba(30, 58, 138, 0.35);
    position: relative;
    overflow: hidden;
}

.hero-title {
    font-size: clamp(22px, 3.5vw, 34px);
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
    color: #FFFFFF !important;
}

.hero-sub {
    font-size: clamp(13px, 1.8vw, 16px);
    color: #BFDBFE !important;
    margin-top: 6px;
    font-weight: 500;
}

.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.2);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34D399;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 10px;
}

.metric-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.04);
    transition: all 0.2s ease;
    margin-bottom: 12px;
}

.metric-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(15, 23, 42, 0.08);
}

.metric-number {
    font-size: clamp(24px, 2.5vw, 32px);
    font-weight: 800;
    line-height: 1.1;
    margin-top: 4px;
}

.metric-title {
    font-size: 12px;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

.glass-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    margin-bottom: 20px;
}

.phone-banner {
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
    color: white;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 14px 0 20px 0;
    box-shadow: 0 8px 24px -4px rgba(49, 46, 129, 0.35);
}

.success-banner {
    background: linear-gradient(135deg, #065F46 0%, #059669 100%);
    color: white;
    border-radius: 14px;
    padding: 16px 20px;
    margin: 12px 0px;
    box-shadow: 0 6px 16px rgba(5, 150, 105, 0.3);
}

.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}

@media (max-width: 768px) {
    .hero-card {
        padding: 18px 16px;
        border-radius: 14px;
    }
    .glass-card {
        padding: 16px;
        border-radius: 14px;
    }
    .metric-box {
        padding: 12px 14px;
    }
    .metric-number {
        font-size: 22px;
    }
    .stButton > button {
        width: 100% !important;
        min-height: 48px !important;
        font-size: 15px !important;
    }
}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

@st.cache_data(ttl=3600)
def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1E3A8A", back_color="#FFFFFF")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def play_browser_voice(text):
    clean = text.replace('"', '').replace("'", "")
    js = f"""
    <script>
    if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance("{clean}");
        msg.rate = 1.0;
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """
    components.html(js, height=0, width=0)
