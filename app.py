import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración general de la página
st.set_page_config(
    page_title="Panel de Control MQTT",
    page_icon="💡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #f0f2f6;
        }
        .main {
            background-color: #1c1e26;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.05);
        }
        h1 {
            color: #f8f9fa;
            text-align: center;
            font-size: 2.5em;
        }
        .stButton>button {
            background-color: #00c853;
            color: white;
            border: none;
            border-radius: 10px;
            height: 50px;
            width: 100%;
            font-size: 1.2em;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #00e676;
            transform: scale(1.05);
        }
        .off-button>button {
            background-color: #d50000 !important;
        }
        .off-button>button:hover {
            background-color: #ff1744 !important;
        }
        .stSlider label {
            color: #90caf9;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Información del sistema
st.markdown(f"### 🧠 Versión de Python: `{platform.python_version()}`")

# Variables globales
values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")

def on_message(client, userdata, message):
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(f"📩 Mensaje recibido: `{message_received}`")

# Conexión MQTT
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# INTERFAZ PRINCIPAL
st.title("💡 Panel de Control MQTT")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button('🔛 Encender dispositivo'):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("✅ Dispositivo encendido")

with col2:
    if st.button('🔴 Apagar dispositivo', key='off', help="Apaga el dispositivo actual", type='primary'):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.error("🚫 Dispositivo apagado")

st.markdown("---")

# Slider para valores analógicos
st.markdown("### ⚙️ Control analógico")
values = st.slider('Selecciona un valor para enviar', 0.0, 100.0, 50.0)
st.write(f"Valor seleccionado: `{values}`")

if st.button('📤 Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    st.success(f"📡 Valor analógico enviado: `{values}`")

st.markdown("---")
st.caption("Desarrollado con 💚 usando Streamlit y MQTT")
