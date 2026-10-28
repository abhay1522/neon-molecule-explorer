"""Theme, sidebar, footer and 3D viewer helpers."""
import json
import streamlit as st
import streamlit.components.v1 as components

# ===================== EDIT YOUR DETAILS HERE =====================
DEV_NAME = "Abhay Raj"
DEV_ROLE = "B.Tech CSE (AI/ML) – Section C"
DEV_COLLEGE = "SRM Institute of Science and Technology, Tiruchirappalli"
DEV_REG_NO = "RA2611026050168"
DEV_EMAIL = ""          # e.g. "yourname@gmail.com" (leave empty to hide the contact box)
LAB_SUBTITLE = "SRM Institute of Science and Technology, Tiruchirappalli"
# ==================================================================

MAGENTA, BLUE, GREEN = "#ff2bd6", "#00d4ff", "#39ff14"

NAV = [
    "🏠 Home", "📖 Theory", "🧬 Molecular Visualization",
    "📊 Molecular Properties Report", "📈 Structure–Property Analysis",
    "📝 Assessment", "📄 Final Project Report",
]
OBJECTIVES = ["SMILES notation", "Molecular representation", "2D visualization",
              "3D visualization", "Molecular descriptors", "Structure-property relationships"]


def apply_theme():
    st.markdown(f"""
    <style>
    .stApp {{ background: radial-gradient(circle at 15% 0%, #0c1030 0%, #05060a 55%); }}
    [data-testid="stSidebar"] {{ background:#080a14; border-right:1px solid {BLUE}66;
        box-shadow: 0 0 18px {BLUE}33; }}
    h1 {{ color:{GREEN} !important; text-shadow:0 0 14px {GREEN}88; }}
    h2, h3 {{ color:{BLUE} !important; text-shadow:0 0 8px {BLUE}66; }}
    hr {{ border-color:{MAGENTA}55 !important; }}
    .stButton > button, .stDownloadButton > button {{
        background:#0b0f1a; color:{GREEN}; border:1px solid {GREEN};
        border-radius:10px; box-shadow:0 0 10px {GREEN}55; transition:all .2s; }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        background:{GREEN}; color:#000; box-shadow:0 0 20px {GREEN}; border-color:{GREEN}; }}
    [data-testid="stMetricValue"] {{ color:{MAGENTA}; text-shadow:0 0 10px {MAGENTA}88; }}
    [data-testid="stMetricLabel"] {{ color:{BLUE}; }}
    div[data-baseweb="input"], div[data-baseweb="select"] > div, textarea {{
        border:1px solid {BLUE}77 !important; border-radius:10px !important; }}
    [data-testid="stAlert"] {{ border-radius:12px; border:1px solid {BLUE}55; }}
    code {{ color:{GREEN} !important; }}
    .center {{ text-align:center; }}
    .neon-sub {{ color:{BLUE}; font-weight:700; font-size:1.5rem; text-shadow:0 0 10px {BLUE}; }}
    .neon-card {{ border:1px solid {MAGENTA}88; border-radius:14px; padding:16px 20px; margin:8px 0;
        background:#0b0f1a; box-shadow:0 0 14px {MAGENTA}33; }}
    .svgbox {{ background:#fff; border-radius:14px; padding:6px; border:2px solid {BLUE};
        box-shadow:0 0 18px {BLUE}99; }}
    .footer {{ color:#8aa0b8; padding:10px 0; }}
    </style>""", unsafe_allow_html=True)


def init_state():
    st.session_state.setdefault("smiles", "CCO")
    st.session_state.setdefault("valid_smiles", "CCO")
    st.session_state.setdefault("student_name", DEV_NAME.upper())
    st.session_state.setdefault("reg_no", DEV_REG_NO)


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🧪 Virtual Lab")
        page = st.radio("Navigation", NAV, key="nav")
        st.divider()
        st.markdown("### 🧑‍🎓 Student Information")
        st.text_input("Student Name", key="student_name")
        st.text_input("Registration Number", key="reg_no")
        st.markdown("### 🎓 Learning Objectives")
        st.write("Students can learn:")
        st.markdown("\n".join(f"- {o}" for o in OBJECTIVES))
    return page


def page_header(icon, title):
    st.markdown(f"# {icon} {title}")


def footer():
    st.divider()
    st.markdown("<div class='footer'>🧪 Cheminformatics Virtual Laboratory | "
                "Developed using Python, Streamlit and RDKit</div>", unsafe_allow_html=True)


def show_svg(svg, height=380):
    components.html(f"<div style='background:#fff;border-radius:14px;padding:6px;border:2px solid {BLUE};"
                    f"box-shadow:0 0 18px {BLUE}99;text-align:center'>{svg}</div>", height=height)


STYLES = {
    "Ball and Stick": "{stick:{radius:0.15}, sphere:{scale:0.3}}",
    "Stick": "{stick:{radius:0.2}}",
    "Space Filling": "{sphere:{}}",
    "Line": "{line:{}}",
}

_VIEWER = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.0.4/3Dmol-min.js"></script>
<div id="v" style="width:100%;height:420px;position:relative;border:2px solid __GREEN__;
 border-radius:14px;box-shadow:0 0 18px __GREEN__88;"></div>
<script>
 const v = $3Dmol.createViewer("v", {backgroundColor:"black"});
 v.addModel(__MOL__, "sdf");
 v.setStyle({}, __STYLE__);
 v.zoomTo(); v.render();
 if (__SPIN__) v.spin("y", 1);
</script>"""


def show_3d(molblock, style="Ball and Stick", spin=True):
    html = (_VIEWER.replace("__GREEN__", GREEN).replace("__MOL__", json.dumps(molblock))
            .replace("__STYLE__", STYLES[style]).replace("__SPIN__", "true" if spin else "false"))
    components.html(html, height=440)
