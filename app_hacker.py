import time
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS CSS CYBERPUNK
# ==========================================
st.set_page_config(
    page_title="CYBERNET // TERMINAL HACKER", page_icon="💻", layout="centered"
)


def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


# Estilos CSS de Consola Terminal Hacker
st.markdown(
    """
    <style>
    /* Fondo principal y fuente de consola */
    .stApp {
        background-color: #050505 !important;
        color: #00ff41 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Contenedor principal con efecto neón verde */
    .main .block-container {
        max-width: 850px !important;
        padding-top: 2rem !important;
        background: #0a0a0a !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.35) !important;
    }

    /* Títulos estilo hacker */
    .hacker-title {
        font-family: 'Courier New', monospace;
        color: #00ff41;
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
        letter-spacing: 3px;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.8);
        margin-bottom: 10px;
    }

    /* Caja de Estado / Consola */
    .terminal-box {
        background: #000000;
        border-left: 4px solid #00ff41;
        padding: 15px;
        border-radius: 5px;
        font-size: 15px;
        color: #00ff41;
        margin-bottom: 20px;
        box-shadow: inset 0 0 10px rgba(0, 255, 65, 0.2);
    }

    /* Tarjetas de Métricas */
    .stat-box {
        background: #0f0f0f;
        border: 1px solid #00ff41;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
    }
    .stat-label { font-size: 12px; color: #888; text-transform: uppercase; }
    .stat-val { font-size: 24px; font-weight: bold; color: #00ff41; }

    /* Personalización de Inputs de Texto */
    div[data-baseweb="input"] {
        background-color: #000000 !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
    }

    div[data-baseweb="input"] input {
        color: #00ff41 !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Personalización de Botones */
    div.stButton > button {
        background-color: #000000 !important;
        color: #00ff41 !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        border: 1px solid #00ff41 !important;
        width: 100% !important;
        border-radius: 5px !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:hover {
        background-color: #00ff41 !important;
        color: #000000 !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.8) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. BASE DE NIVELES Y ACERT IJOS
# ==========================================
LEVELS = [
    {
        "node": "NODO 01 // PUERTA DE ACCESO DE RED",
        "prompt": (
            "Decodifica la secuencia binaria del puerto principal para ingresar"
            " al servidor:\n\n**¿Cuál es el valor decimal del número binario"
            " `1011`?**"
        ),
        "answer": "11",
        "hint": "Recuerda las potencias de 2: (1*8) + (0*4) + (1*2) + (1*1).",
    },
    {
        "node": "NODO 02 // CORTAFUEGOS LOGICO",
        "prompt": (
            "El sistema requiere evaluar la siguiente expresión lógica de"
            " seguridad:\n\n**Si (A = True) y (B = False), ¿cuál es el resultado"
            " de `(A AND NOT B)`? (Responde True o False)**"
        ),
        "answer": "true",
        "hint": "NOT B invierte el valor de False a True. True AND True es...",
    },
    {
        "node": "NODO 03 // SECUENCIA ENCRIPTADA",
        "prompt": (
            "Completa la secuencia criptográfica del protocolo SSH para evitar"
            " la desconexión:\n\n**2, 4, 8, 16, 32, [ ? ]**"
        ),
        "answer": "64",
        "hint": "Cada número en la secuencia se multiplica por 2.",
    },
    {
        "node": "NODO 04 // CLAVE CAESAR",
        "prompt": (
            "Un fragmento de memoria está cifrado con desplazamiento ROT1"
            " (avanzar 1 letra adelante en el abecedario):\n\n**Si la palabra"
            " cifrada es `HAL`, ¿cuál es la palabra original si retrocedes 1"
            " letra?**"
        ),
        "answer": "gdk",
        "hint": (
            "Aplica la resta a cada letra en el abecedario: H->G, A->D... no,"
            " la letra antes de H es G, antes de A es Z o descender... la"
            " respuesta es GDK o IBM según la variante. (Pista: La respuesta"
            " exacta para H-1, A-1, L-1 es GDK / IBM)."
        ),
        "correct_answers": ["gdk", "ibm"],
    },
    {
        "node": "NODO 05 // NÚCLEO CENTRAL Y CLAVE FINAL",
        "prompt": (
            "Para sobreescribir la base de datos raíz de la corporación,"
            " responde la contraseña maestra de 5 letras:\n\n**'Tengo claves"
            " pero no puertas, espacio pero no habitaciones, te permito"
            " entrar pero no salir. ¿Qué soy?'**"
        ),
        "answer": "teclado",
        "hint": "Es el periférico que estás usando en este momento.",
    },
]

# ==========================================
# 3. ESTADO DE SESIÓN (SESSION STATE)
# ==========================================
if "current_level" not in st.session_state:
    st.session_state.current_level = 0
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "game_status" not in st.session_state:
    st.session_state.game_status = "PLAYING"  # PLAYING, WIN, GAMEOVER
if "logs" not in st.session_state:
    st.session_state.logs = [
        "[SYSTEM] Conexión establecida a la IP 192.168.1.104...",
        "[SYSTEM] Iniciando exploit de consola...",
    ]


def restart_game():
    st.session_state.current_level = 0
    st.session_state.lives = 3
    st.session_state.game_status = "PLAYING"
    st.session_state.logs = [
        "[SYSTEM] Conexión reiniciada...",
        "[SYSTEM] Intento de intrusión v2.0 iniciado.",
    ]


# ==========================================
# 4. INTERFAZ DE USUARIO Y LÓGICA
# ==========================================
st.markdown(
    '<div class="hacker-title">💻 CYBERNET // HACKER TERMINAL 🟢</div>',
    unsafe_allow_html=True,
)

# Panel de Estadísticas / Barra Superior
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f'<div class="stat-box"><div class="stat-label">Nivel de Acceso</div><div'
        f' class="stat-val">{st.session_state.current_level + 1} / 5</div></div>',
        unsafe_allow_html=True,
    )

with c2:
    heart_icons = "❤️ " * st.session_state.lives
    st.markdown(
        f'<div class="stat-box"><div class="stat-label">Integridad de'
        f' Sistema</div><div class="stat-val" style="color: #ef4444;'
        f' font-size:18px;">{heart_icons if st.session_state.lives > 0 else "0 (BLOQUEADO)"}</div></div>',
        unsafe_allow_html=True,
    )

with c3:
    status_color = (
        "#00ff41"
        if st.session_state.game_status == "PLAYING"
        else (
            "#3b82f6"
            if st.session_state.game_status == "WIN"
            else "#ef4444"
        )
    )
    st.markdown(
        f'<div class="stat-box"><div class="stat-label">Estado</div><div'
        f' class="stat-val" style="color: {status_color}; font-size:'
        f' 16px;">{st.session_state.game_status}</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# Visualización de la Consola / Logs de eventos
log_text = "<br>".join(st.session_state.logs[-4:])
st.markdown(
    f'<div class="terminal-box">{log_text}</div>', unsafe_allow_html=True
)

# Lógica según estado del juego
if st.session_state.game_status == "PLAYING":
    lvl_data = LEVELS[st.session_state.current_level]

    st.markdown(f"### 🔒 {lvl_data['node']}")
    st.markdown(lvl_data["prompt"])

    # Pista desplegable
    with st.expander("🔑 Desplegar rastreador de pista (Hint)"):
        st.info(lvl_data["hint"])

    # Formulario de entrada de clave
    with st.form(key=f"form_lvl_{st.session_state.current_level}"):
        user_answer = st.text_input(
            "Introduce el código de acceso / comando:",
            placeholder="Escribe tu respuesta...",
        )
        submit_button = st.form_submit_button("⚡ EJECUTAR EXPLOIT")

    if submit_button:
        clean_ans = user_answer.strip().lower()

        # Validación de respuesta
        valid_answers = (
            lvl_data.get("correct_answers", [lvl_data["answer"]])
            if "correct_answers" in lvl_data
            else [lvl_data["answer"]]
        )

        if clean_ans in valid_answers:
            st.session_state.logs.append(
                f"[SUCCESS] {lvl_data['node']} vulnerado correctamente."
            )

            if st.session_state.current_level + 1 < len(LEVELS):
                st.session_state.current_level += 1
                st.success(" Acceso concedido. Avanzando al siguiente nodo...")
            else:
                st.session_state.game_status = "WIN"
                st.session_state.logs.append(
                    "[CRITICAL] ¡ACCESO RAÍZ CONSEGUIDO! SERVIDOR CONTROLADO."
                )

            time.sleep(0.5)
            safe_rerun()
        else:
            st.session_state.lives -= 1
            st.session_state.logs.append(
                f"[WARNING] Código incorrecto. Detección de intrusos activada. Vidas"
                f" restantes: {st.session_state.lives}"
            )

            if st.session_state.lives <= 0:
                st.session_state.game_status = "GAMEOVER"
                st.session_state.logs.append(
                    "[ERROR] CONEXIÓN RECHAZADA. DIRECCIÓN IP RASTREADA Y BLOQUEADA."
                )

            st.error("❌ Código erróneo. Integridad de sistema reducida.")
            time.sleep(0.5)
            safe_rerun()

elif st.session_state.game_status == "WIN":
    st.balloons()
    st.success("🏆 **¡MISIÓN CUMPLIDA!** Has vulnerado exitosamente los 5 nodos.")
    st.markdown(
        "```text\n"
        "   ______   ______ _____ _______ ______  _____ \n"
        "  / ___/ \\ / / __ / ___// ___/  / / __ \\/ ___/ \n"
        " / /__/ /\\  / /_/ / /__/ /__/  / / /_/ / /__   \n"
        " \\___/_/  \\/_.___/\\___/\\___/  /_/\\____/\\___/   \n"
        " SYSTEM COMPROMISED - ALL DATA EXTRACTED\n"
        "```"
    )

    if st.button("🔄 REINICIAR CONEXIÓN", use_container_width=True):
        restart_game()
        safe_rerun()

elif st.session_state.game_status == "GAMEOVER":
    st.error("☠️ **GAME OVER:** El sistema de seguridad te ha localizado.")
    st.markdown(
        "```text\n"
        "   ______ ___    __  ___  ______   _    ______  ____ \n"
        "  / ____//   |  /  |/  / / ____/  | |  / / __ \\/ __ \\\n"
        " / / __ / /| | / /|_/ / / __/     | | / / /_/ / /_/ /\n"
        "/ /_/ // ___ |/ /  / / / /___     | |/ / ____/ _, _/ \n"
        "\\____//_/  |_/_/  /_/ /_____/     |___/_/   /_/ |_|  \n"
        " ACCESS DENIED - SYSTEM LOCKED\n"
        "```"
    )

    if st.button("🔄 REINTENTAR ACCESO", use_container_width=True):
        restart_game()
        safe_rerun()