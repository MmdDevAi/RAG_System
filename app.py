import os
import glob
import base64
import html
import requests
import streamlit as st

# ۰. ساخت خودکار کانفیگ تم تیره نیتیو Streamlit
os.makedirs(".streamlit", exist_ok=True)
config_path = os.path.join(".streamlit", "config.toml")
with open(config_path, "w", encoding="utf-8") as f:
    f.write(
        '[theme]\n'
        'base="dark"\n'
        'primaryColor="#2FA6A0"\n'
        'backgroundColor="#0B1521"\n'
        'secondaryBackgroundColor="#101E2E"\n'
        'textColor="#E2E8F0"\n'
    )

# ۱. تنظیمات صفحه
st.set_page_config(
    page_title="سامانه هوشمند پرسش و پاسخ | Persian RAG",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ۲. استایل CSS پیشرفته (با رفع کامل باگ دکمه‌ها، اسلایدرها و سوییچ‌ها در حالت فعال)
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Vazirmatn:wght@300;400;500;600;700;800&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Vazirmatn', sans-serif !important;
    background-color: #0B1521 !important;
    color: #E2E8F0 !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}
footer {
    visibility: hidden;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 6rem !important;
    max-width: 1180px !important;
}

div[data-testid="stBottom"],
div[data-testid="stBottom"] > div {
    background-color: #0B1521 !important;
    background: linear-gradient(180deg, rgba(11,21,33,0) 0%, #0B1521 35%) !important;
}

/* ================= استایل سایدبار و رفع باگ کنترلرها ================= */
section[data-testid="stSidebar"] {
    background-color: #0D1826 !important;
    border-left: 1px solid rgba(47, 166, 160, 0.22) !important;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Vazirmatn', sans-serif !important;
}

/* رفع باگ برعکس پر شدن اسلایدر در حالت RTL */
div[data-testid="stSlider"] > div[data-baseweb="slider"] {
    direction: ltr !important;
    padding-top: 6px !important;
}
div[data-testid="stThumbValue"],
div[data-testid="stTickBarMin"],
div[data-testid="stTickBarMax"] {
    font-family: 'JetBrains Mono', monospace !important;
    direction: ltr !important;
}

/* رفع قطعی بیرون زدن دایره Toggle در حالت RTL */
label[data-baseweb="checkbox"] {
    direction: rtl !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    background: rgba(16, 30, 46, 0.65) !important;
    border: 1px solid rgba(47, 166, 160, 0.25) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    margin: 6px 0 !important;
}
label[data-baseweb="checkbox"] > *:first-child,
label[data-baseweb="checkbox"] > *:first-child * {
    direction: ltr !important;
    box-sizing: border-box !important;
    box-shadow: none !important;
    outline: none !important;
}
/* کادر ورودی لینک در سایدبار */
div[data-baseweb="input"] {
    background-color: #08101A !important;
    border: 1px solid rgba(47, 166, 160, 0.35) !important;
    border-radius: 8px !important;
}
div[data-baseweb="input"] input {
    font-family: 'JetBrains Mono', monospace !important;
    direction: ltr !important;
    text-align: left !important;
    color: #2FA6A0 !important;
    font-size: 0.8rem !important;
}

/* عنوان بخش‌های سایدبار */
.sidebar-section-header {
    background: linear-gradient(90deg, rgba(16, 30, 46, 0.3) 0%, rgba(47, 166, 160, 0.14) 100%);
    border-right: 3px solid #2FA6A0;
    border-radius: 6px;
    padding: 6px 10px;
    margin: 16px 0 8px 0;
    color: #F8FAFC;
    font-weight: 700;
    font-size: 0.86rem;
    direction: rtl;
    text-align: right;
}

/* ================= استایل دکمه‌ها (بدون کادر زشت در حالت کلیک/فعال) ================= */


/* دکمه‌های عادی (سوالات نمونه) */
button[kind="secondary"] {
    width: 100% !important;
    background: rgba(16, 30, 46, 0.75) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(47, 166, 160, 0.28) !important;
    border-right: 3px solid #2FA6A0 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    text-align: right !important;
    direction: rtl !important;
    font-family: 'Vazirmatn', sans-serif !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
    outline: none !important;
}
button[kind="secondary"] p {
    text-align: right !important;
    direction: rtl !important;
    margin: 0 !important;
    line-height: 1.5 !important;
}
button[kind="secondary"]:hover {
    background: rgba(47, 166, 160, 0.16) !important;
    border-color: #2FA6A0 !important;
    border-right-color: #C9A24B !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}
button[kind="secondary"]:focus,
button[kind="secondary"]:focus-visible,
button[kind="secondary"]:active {
    background: rgba(47, 166, 160, 0.25) !important;
    border-color: #C9A24B !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 0 2px rgba(201, 162, 75, 0.25) !important;
    outline: none !important;
}

/* دکمه اصلی در سایدبار (پاکسازی و اکشن‌ها) */
button[kind="primary"] {
    width: 100% !important;
    background: rgba(193, 91, 69, 0.18) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(193, 91, 69, 0.55) !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
    font-family: 'Vazirmatn', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
    outline: none !important;
}
button[kind="primary"]:hover {
    background: #C15B45 !important;
    border-color: #C15B45 !important;
    color: #FFFFFF !important;
}
button[kind="primary"]:focus,
button[kind="primary"]:active {
    background: #A84A36 !important;
    box-shadow: none !important;
    outline: none !important;
}

/* دکمه دانلود PDF */
div[data-testid="stDownloadButton"] button {
    width: 100% !important;
    background: rgba(201, 162, 75, 0.16) !important;
    color: #C9A24B !important;
    border: 1px solid rgba(201, 162, 75, 0.5) !important;
    border-radius: 10px !important;
    font-family: 'Vazirmatn', sans-serif !important;
    font-weight: 600 !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background: #C9A24B !important;
    color: #0B1521 !important;
}

/* ================= استایل تب‌ها (Tabs) ================= */
div[data-baseweb="tab-list"] {
    direction: rtl !important;
    gap: 10px !important;
    background-color: #0E1B2A !important;
    padding: 6px 10px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(47, 166, 160, 0.2) !important;
    margin-bottom: 16px !important;
}
button[data-baseweb="tab"] {
    font-family: 'Vazirmatn', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: rgba(47, 166, 160, 0.2) !important;
    color: #2FA6A0 !important;
}

/* ================= هدر و کارت‌های متریک ================= */
.hero-banner {
    background: radial-gradient(circle at top right, rgba(47, 166, 160, 0.18), rgba(16, 30, 46, 0.92) 65%), #101E2E;
    border: 1px solid rgba(47, 166, 160, 0.32);
    border-right: 5px solid #2FA6A0;
    border-radius: 16px;
    padding: 20px 26px;
    margin-bottom: 16px;
    direction: rtl;
    text-align: right;
}
.hero-title {
    color: #F8FAFC;
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0 0 6px 0;
}
.hero-subtitle {
    color: #94A3B8;
    font-size: 0.9rem;
    margin: 0;
}
.telemetry-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 18px;
    direction: rtl;
}
@media (max-width: 768px) {
    .telemetry-grid { grid-template-columns: repeat(2, 1fr); }
}
.telemetry-card {
    background: rgba(16, 30, 46, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-top: 2px solid #2FA6A0;
    border-radius: 12px;
    padding: 10px 14px;
    text-align: right;
}
.telemetry-card.gold { border-top-color: #C9A24B; }
.telemetry-card.ruby { border-top-color: #C15B45; }
.telemetry-label { color: #94A3B8; font-size: 0.76rem; margin-bottom: 3px; }
.telemetry-value {
    font-family: 'JetBrains Mono', 'Vazirmatn', monospace;
    color: #F8FAFC;
    font-size: 0.92rem;
    font-weight: 600;
    direction: ltr;
    text-align: right;
}
.status-dot {
    display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-left: 6px;
}
.status-dot.online { background-color: #2FA6A0; box-shadow: 0 0 8px #2FA6A0; }
.status-dot.offline { background-color: #C15B45; box-shadow: 0 0 8px #C15B45; }

/* ================= پیام‌های چت و کارت‌های اسناد ================= */
div[data-testid="stChatMessage"] {
    background-color: #101E2E !important;
    border: 1px solid rgba(148, 163, 184, 0.14) !important;
    border-right: 4px solid #2FA6A0 !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    margin-bottom: 12px !important;
    direction: rtl !important;
}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li {
    direction: rtl !important;
    text-align: right !important;
    unicode-bidi: plaintext !important;
    line-height: 1.85 !important;
    font-size: 0.95rem !important;
}

div[data-testid="stExpander"] {
    background-color: #0D1826 !important;
    border: 1px solid rgba(201, 162, 75, 0.28) !important;
    border-radius: 10px !important;
    margin-top: 10px !important;
    direction: rtl !important;
}
div[data-testid="stExpander"] summary {
    direction: rtl !important;
    text-align: right !important;
    color: #C9A24B !important;
    font-weight: 600 !important;
}

.doc-card {
    background: linear-gradient(145deg, #0E1B2A 0%, #0B1521 100%);
    border: 1px solid rgba(47, 166, 160, 0.22);
    border-right: 3px solid #C9A24B;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
    direction: rtl;
    text-align: right;
}
.doc-top {
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 8px; padding-bottom: 8px; margin-bottom: 8px;
    border-bottom: 1px dashed rgba(148, 163, 184, 0.18);
}
.doc-rank-title { color: #F8FAFC; font-weight: 700; font-size: 0.88rem; }
.badges-wrap { display: flex; gap: 6px; flex-wrap: wrap; direction: ltr; }
.pill {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.73rem; padding: 2px 8px; border-radius: 6px; font-weight: 600;
}
.pill-rerank { background: rgba(201, 162, 75, 0.16); color: #C9A24B; border: 1px solid rgba(201, 162, 75, 0.45); }
.pill-hybrid { background: rgba(47, 166, 160, 0.16); color: #2FA6A0; border: 1px solid rgba(47, 166, 160, 0.45); }
.pill-rank { background: rgba(148, 163, 184, 0.12); color: #CBD5E1; border: 1px solid rgba(148, 163, 184, 0.25); }
.score-bar-bg { width: 100%; height: 4px; background: rgba(148, 163, 184, 0.12); border-radius: 4px; margin-bottom: 10px; overflow: hidden; }
.score-bar-fill { height: 100%; background: linear-gradient(90deg, #2FA6A0, #C9A24B); border-radius: 4px; }
.doc-body { color: #CBD5E1; font-size: 0.87rem; line-height: 1.8; direction: rtl; text-align: right; unicode-bidi: plaintext; }

/* کارت‌های معرفی فصول سند مرجع */
.chapter-card {
    background: rgba(16, 30, 46, 0.7);
    border: 1px solid rgba(47, 166, 160, 0.2);
    border-right: 3px solid #2FA6A0;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
    direction: rtl;
    text-align: right;
}
.chapter-title { color: #C9A24B; font-weight: 700; font-size: 0.92rem; margin-bottom: 4px; }
.chapter-desc { color: #CBD5E1; font-size: 0.84rem; line-height: 1.6; }

div[data-testid="stChatInput"] {
    background-color: #101E2E !important;
    border: 1px solid rgba(47, 166, 160, 0.4) !important;
    border-radius: 14px !important;
    padding: 2px 6px !important;
}
div[data-testid="stChatInput"] textarea {
    direction: rtl !important; text-align: right !important;
    font-family: 'Vazirmatn', sans-serif !important; color: #F8FAFC !important;
    padding-right: 12px !important; padding-left: 42px !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ۳. لیست ۱۰ سوال نمونه استاندارد در دسته‌بندی‌های مختلف
SAMPLE_QUESTIONS = [
    ("🔹 تعریفی", "مکانیزم خودتوجهی (Self-Attention) در معماری ترنسفورمر چیست و چه وظیفه‌ای دارد؟"),
    ("🔹 تعریفی", "مفهوم امبدینگ (Embedding) در پردازش زبان طبیعی چیست و چگونه کلمات را به بردار تبدیل می‌کند؟"),
    ("🔸 مفهومی", "پدیده توهم (Hallucination) در مدل‌های زبانی بزرگ چیست و سیستم RAG چگونه از آن جلوگیری می‌کند؟"),
    ("🔸 مفهومی", "چرا در سیستم‌های بازیابی اطلاعات، جستجوی معنایی (Dense) به تنهایی کافی نیست و به جستجوی ترکیبی نیاز داریم؟"),
    ("⚖️ مقایسه‌ای", "معماری ترنسفورمر (Transformer) چه برتری‌هایی نسبت به شبکه‌های عصبی بازگشتی (RNN) دارد؟"),
    ("⚖️ مقایسه‌ای", "تفاوت پرامپت‌نویسی بدون نمونه (Zero-Shot) و چندنمونه‌ای (Few-Shot) در هدایت مدل‌های زبانی چیست؟"),
    ("⚙️ جزئیات فنی", "پارامتر دمای مدل (Temperature) چه تاثیری بر فرآیند تولید متن و میزان خلاقیت یا دقت مدل دارد؟"),
    ("⚙️ جزئیات فنی", "پایگاه داده‌های برداری و کتابخانه FAISS چگونه جستجوی شباهت را در ابعاد بالا تسریع می‌کنند؟"),
    ("🎯 بازرتبه‌بندی", "نقش مدل‌های Cross-Encoder در مرحله بازرتبه‌بندی (Reranking) چیست و چه تفاوتی با Bi-Encoder دارند؟"),
    ("🛡️ تست ضدتوهم", "بر اساس متن مرجع، هزینه راه‌اندازی سرور ابری در سال ۲۰۲۶ چقدر است؟ (تست سوال خارج از متن)")
]

# سرفصل‌های سند مرجع برای نمایش در تب مطالعه منبع
REFERENCE_CHAPTERS = [
    ("فصل ۱: مقدمه‌ای بر هوش مصنوعی و یادگیری ماشین", "تعاریف پایه، سیر تحول مدل‌های آماری به یادگیری عمیق و کاربردهای پردازش زبان طبیعی."),
    ("فصل ۲: معماری ترنسفورمر (Transformer) و انقلاب NLP", "بررسی محدودیت‌های RNN/LSTM، معرفی مکانیزم Self-Attention و پردازش موازی توکن‌ها."),
    ("فصل ۳: مدل‌های زبانی بزرگ (LLMs) و نحوه آموزش آن‌ها", "مراحل Pre-training، تنظیم ظریف (Fine-Tuning) و هم‌راستاسازی با بازخورد انسانی (RLHF)."),
    ("فصل ۴: بازنمایی برداری متون و امبدینگ‌ها (Embeddings)", "انتقال کلمات و جملات به فضای برداری چندبعدی و سنجش شباهت کسینوسی (Cosine Similarity)."),
    ("فصل ۵: پایگاه داده‌های برداری و الگوریتم‌های جستجو", "ساختار ایندکس‌های برداری، کتابخانه FAISS و الگوریتم گراف سلسله‌مراتبی HNSW."),
    ("فصل ۶: مهندسی پرامپت و کنترل خروجی مدل", "تکنیک‌های Zero-Shot، Few-Shot، زنجیره افکار (CoT) و نقش پارامترهایی نظیر Temperature و Top-P."),
    ("فصل ۷: چالش توهم (Hallucination) و ضرورت معماری RAG", "دلایل تولید اطلاعات نادرست در LLMها و چگونگی تزریق دانش مستند با بازیابی اطلاعات."),
    ("فصل ۸: استراتژی‌های قطعه‌بندی متون (Chunking) و پیش‌پردازش فارسی", "انتخاب اندازه بهینه چانک، همپوشانی (Overlap) و استانداردسازی نویسه‌ها و نیم‌فاصله‌ها در زبان فارسی."),
    ("فصل ۹: جستجوی ترکیبی (Hybrid Search) و بازرتبه‌بندی (Reranking)", "ترکیب الگوریتم کلیدواژه‌ای BM25 با جستجوی Dense از طریق RRF و پالایش نهایی با Cross-Encoder."),
    ("فصل ۱۰: ارزیابی پایپ‌لاین‌های RAG", "بررسی متریک‌های بازیابی (Hit@K و MRR) و سنجش وفاداری پاسخ مدل به متن مرجع (Faithfulness).")
]

# ۴. مقداردهی اولیه حافظه موقت (Session State)
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "سلام! سامانه پرسش و پاسخ هوشمند آماده است. می‌توانید یکی از ۱۰ سوال نمونه بالای صفحه را کلیک کنید یا سوال خودتان را در کادر پایین بنویسید.",
            "sources": [],
            "latency": None
        }
    ]
if "last_latency" not in st.session_state:
    st.session_state["last_latency"] = None
if "pending_query" not in st.session_state:
    st.session_state["pending_query"] = None

# جستجوی خودکار فایل PDF در پوشه پروژه
pdf_files = glob.glob("*.pdf")
local_pdf_path = pdf_files[0] if pdf_files else None

# ۵. سایدبار تنظیمات
with st.sidebar:
    st.markdown("### 🎛️ مرکز کنترل پایپ‌لاین")

    st.markdown('<div class="sidebar-section-header">🔗 سرور پردازش گرافیکی (Colab)</div>', unsafe_allow_html=True)
    colab_url = st.text_input(
        "آدرس تونل Cloudflare",
        value="https://extends-theta-reviewed-enter.trycloudflare.com",
        placeholder="https://xxxx.trycloudflare.com"
    )

    st.markdown('<div class="sidebar-section-header">📄 سند مرجع پایگاه دانش</div>', unsafe_allow_html=True)
    st.caption("منبع: مبانی هوش مصنوعی و مدل‌های زبانی (۱۰ فصل)")
    if local_pdf_path:
        with open(local_pdf_path, "rb") as f:
            st.download_button(
                label=f"📥 دانلود فایل PDF مرجع ({os.path.basename(local_pdf_path)})",
                data=f.read(),
                file_name=os.path.basename(local_pdf_path),
                mime="application/pdf"
            )
    else:
        st.caption("💡 برای فعال شدن دانلود مستقیم، فایل PDF مرجع را کنار app.py قرار دهید یا از تب «📖 مطالعه سند مرجع» مشاهده کنید.")

    st.markdown('<div class="sidebar-section-header">🔍 ۱. جستجوی ترکیبی (Hybrid RRF)</div>', unsafe_allow_html=True)
    hybrid_alpha = st.slider(
        "وزن Dense در برابر BM25 (Alpha)",
        min_value=0.0, max_value=1.0, value=0.6, step=0.1
    )
    top_k_retrieval = st.slider(
        "تعداد کاندیدهای اولیه (Top-K)",
        min_value=3, max_value=20, value=10, step=1
    )

    st.markdown('<div class="sidebar-section-header">🎯 ۲. بازرتبه‌بند (Cross-Encoder)</div>', unsafe_allow_html=True)
    use_reranker = st.toggle("فعال‌سازی bge-reranker-v2-m3", value=True)
    top_n_context = st.slider(
        "تعداد اسناد ارسالی به مدل (Top-N)",
        min_value=1, max_value=5, value=3, step=1
    )

    st.markdown('<div class="sidebar-section-header">🧠 ۳. مدل زبانی (Qwen-2.5-7B)</div>', unsafe_allow_html=True)
    temperature = st.slider(
        "دمای تولید پاسخ (Temperature)",
        min_value=0.0, max_value=1.0, value=0.1, step=0.05
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ پاکسازی تاریخچه گفت‌وگو", type="primary"):
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "تاریخچه گفت‌وگو پاک شد. یک سوال نمونه انتخاب کنید یا پرسش جدید خود را بنویسید.",
                "sources": [],
                "latency": None
            }
        ]
        st.session_state["last_latency"] = None
        st.rerun()

# ۶. هدر اصلی و کارت‌های وضعیت
is_connected = bool(colab_url.strip())
dot_class = "status-dot online" if is_connected else "status-dot offline"
conn_label = "Online (T4 GPU)" if is_connected else "Disconnected"
bm25_w = round(1.0 - hybrid_alpha, 1)
rerank_label = f"Active (Top-{top_n_context})" if use_reranker else f"Bypassed (Top-{top_n_context})"
rerank_card_class = "telemetry-card gold" if use_reranker else "telemetry-card ruby"
latency_str = f"{st.session_state['last_latency']} s" if st.session_state["last_latency"] else "Ready"

header_html = (
    '<div class="hero-banner">'
    '<div class="hero-title">💠 سامانه پرسش و پاسخ هوشمند فارسی (End-to-End RAG)</div>'
    '<div class="hero-subtitle">مبتنی بر پایگاه دانش «مبانی هوش مصنوعی و مدل‌های زبانی» | جستجوی ترکیبی (BM25 + Dense)، بازرتبه‌بندی Cross-Encoder و مدل Qwen-2.5-7B</div>'
    '</div>'
    '<div class="telemetry-grid">'
    f'<div class="telemetry-card"><div class="telemetry-label">وضعیت بک‌اند</div><div class="telemetry-value"><span class="{dot_class}"></span>{conn_label}</div></div>'
    f'<div class="telemetry-card"><div class="telemetry-label">وزن جستجوی ترکیبی</div><div class="telemetry-value">Dense {hybrid_alpha} | BM25 {bm25_w}</div></div>'
    f'<div class="{rerank_card_class}"><div class="telemetry-label">وضعیت Reranker</div><div class="telemetry-value">{rerank_label}</div></div>'
    f'<div class="telemetry-card gold"><div class="telemetry-label">زمان آخرین پاسخ</div><div class="telemetry-value">{latency_str}</div></div>'
    '</div>'
)
st.markdown(header_html, unsafe_allow_html=True)


# ۷. توابع ارتباط با بک‌اند و رندر کارت اسناد
def query_colab_backend(base_url, query, alpha, top_k, rerank, top_n, temp):
    if not base_url.strip():
        return "⚠️ لطفاً ابتدا لینک سرور Google Colab را در کادر بالای سایدبار وارد کنید.", [], None

    endpoint = base_url.strip().rstrip("/") + "/ask"
    payload = {
        "query": query,
        "alpha": alpha,
        "top_k": top_k,
        "rerank": rerank,
        "top_n": top_n,
        "temperature": temp
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("answer", ""), data.get("sources", []), data.get("latency", None)
    except requests.exceptions.RequestException as e:
        return (
            f"❌ خطا در ارتباط با سرور Google Colab:\nمطمئن شوید سلول آخر در کولب در حال اجراست و لینک منقضی نشده است.\n\n{e}",
            [],
            None
        )


def render_sources(sources, latency):
    if not sources:
        return

    exp_title = f"📚 اسناد مرجع بازیابی‌شده ({len(sources)} قطعه متنی)"
    if latency:
        exp_title += f"  |  ⏱️ زمان پردازش: {latency} ثانیه"

    with st.expander(exp_title):
        cards_html = ""
        for idx, doc in enumerate(sources, start=1):
            doc_id = html.escape(str(doc.get("id", f"CHUNK-{idx}")))
            raw_title = html.escape(str(doc.get("title", "سند مرجع")))
            doc_text = html.escape(str(doc.get("text", ""))).replace("\n", "<br>")

            h_score = doc.get("hybrid_score")
            r_score = doc.get("rerank_score")

            badges = f'<span class="pill pill-rank">{raw_title}</span>'
            if h_score is not None:
                badges += f'<span class="pill pill-hybrid">Hybrid: {float(h_score):.3f}</span>'
            if r_score is not None:
                badges += f'<span class="pill pill-rerank">Rerank: {float(r_score):.3f}</span>'

            primary_score = float(r_score) if r_score is not None else (float(h_score) if h_score is not None else 0.5)
            bar_pct = max(12, min(100, int(primary_score * 100))) if primary_score <= 1.0 else 85

            cards_html += (
                '<div class="doc-card">'
                '<div class="doc-top">'
                f'<span class="doc-rank-title">📄 رتبه #{idx} — شناسه: {doc_id}</span>'
                f'<div class="badges-wrap">{badges}</div>'
                '</div>'
                f'<div class="score-bar-bg"><div class="score-bar-fill" style="width: {bar_pct}%;"></div></div>'
                f'<div class="doc-body">{doc_text}</div>'
                '</div>'
            )

        st.markdown(cards_html, unsafe_allow_html=True)


# ۸. تب‌بندی اصلی صفحه (تب چت + تب مطالعه PDF مرجع)
tab_chat, tab_pdf = st.tabs([
    "💬 گفت‌وگو و تست هوشمند (RAG Playground)",
    "📖 مطالعه سند مرجع و سرفصل‌های پایگاه دانش (PDF)"
])

with tab_chat:
    # بخش سوالات نمونه آماده (با قابلیت کلیک مستقیم)
    with st.expander("💡 بانک سوالات نمونه (برای تست سریع روی هر سوال کلیک کنید)", expanded=(len(st.session_state["messages"]) <= 1)):
        col_right, col_left = st.columns(2)
        for idx, (category, q_text) in enumerate(SAMPLE_QUESTIONS):
            target_col = col_right if idx % 2 == 0 else col_left
            with target_col:
                if st.button(f"{category} | {q_text}", key=f"sample_q_{idx}", type="secondary"):
                    st.session_state["pending_query"] = q_text
                    # نمایش تاریخچه پیام‌ها
    for msg in st.session_state["messages"]:
        avatar_icon = "🧑‍💻" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar_icon):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                render_sources(msg["sources"], msg.get("latency"))

with tab_pdf:
    st.markdown("#### 📖 سند مرجع پایپ‌لاین: «مبانی هوش مصنوعی و مدل‌های زبانی»")
    st.caption("تمامی پاسخ‌های سیستم مستقیماً از محتوای این سند مرجع استخراج و مستندسازی می‌شوند.")

    # اگر فایل PDF در پوشه پروژه باشد یا کاربر آپلود کند، مستقیم نمایش داده می‌شود
    uploaded_pdf = None
    if not local_pdf_path:
        uploaded_pdf = st.file_uploader(
            "فایل PDF مرجع را برای نمایش مستقیم در صفحه انتخاب کنید (یا فایل PDF را کنار app.py در پوشه پروژه قرار دهید):",
            type=["pdf"]
        )

    pdf_bytes = None
    if local_pdf_path:
        with open(local_pdf_path, "rb") as f:
            pdf_bytes = f.read()
    elif uploaded_pdf is not None:
        pdf_bytes = uploaded_pdf.read()

    if pdf_bytes:
        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_iframe = (
            f'<iframe src="data:application/pdf;base64,{b64_pdf}" '
            'width="100%" height="650px" style="border: 1px solid rgba(47,166,160,0.4); border-radius: 12px;"></iframe>'
        )
        st.markdown(pdf_iframe, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("##### 🗂️ فهرست سرفصل‌های موجود در پایگاه دانش (۱۰ فصل):")
    ch_col1, ch_col2 = st.columns(2)
    for i, (ch_title, ch_desc) in enumerate(REFERENCE_CHAPTERS):
        target = ch_col1 if i % 2 == 0 else ch_col2
        with target:
            st.markdown(
                f'<div class="chapter-card">'
                f'<div class="chapter-title">{ch_title}</div>'
                f'<div class="chapter-desc">{ch_desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ۹. دریافت سوال (چه از کادر چت پایین صفحه، چه از کلیک روی سوالات نمونه)
chat_box_query = st.chat_input("سوال خود را درباره اسناد مرجع بنویسید...")
active_query = chat_box_query or st.session_state.get("pending_query")

if active_query:
    st.session_state["pending_query"] = None
    st.session_state["messages"].append({"role": "user", "content": active_query})

    with tab_chat:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(active_query)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("در حال جستجوی ترکیبی، بازرتبه‌بندی و تولید پاسخ در GPU کولب..."):
                answer, retrieved_docs, elapsed = query_colab_backend(
                    base_url=colab_url,
                    query=active_query,
                    alpha=hybrid_alpha,
                    top_k=top_k_retrieval,
                    rerank=use_reranker,
                    top_n=top_n_context,
                    temp=temperature
                )
            if elapsed is not None:
                st.session_state["last_latency"] = elapsed
            st.markdown(answer)
            render_sources(retrieved_docs, elapsed)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": answer,
        "sources": retrieved_docs,
        "latency": elapsed
    })
    st.rerun()