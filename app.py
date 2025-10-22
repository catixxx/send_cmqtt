import paho.mqtt.client as paho
import time
import streamlit as st
import json

# Configuración general de la página
st.set_page_config(
    page_title="Panel de Control MQTT",
    page_icon="💡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🎨 Estilos personalizados (rosas y morados)
st.markdown("""
    <style>
        body {
            background-color: #0e0b16;
            color: #f0f2f6;
        }
        .main {
            background-color: #1a103d;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0px 0px 25px rgba(255, 0, 255, 0.1);
        }
        h1 {
            color: #f8f9fa;
            text-align: center;
            font-size: 2.5em;
        }
        .stButton>button {
            color: white;
            border: none;
            border-radius: 12px;
            height: 50px;
            width: 100%;
            font-size: 1.2em;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        /* Botón rosa (ON) */
        div[data-testid="stButton"] button:first-child {
            background-color: #e91e63;
            box-shadow: 0 0 15px rgba(233, 30, 99, 0.4);
        }
        div[data-testid="stButton"] button:first-child:hover {
            background-color: #ff4081;
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255, 64, 129, 0.6);
        }
        /* Botón morado (OFF) */
        div[data-testid="stButton"] button:nth-child(2) {
            background-color: #7b1fa2;
            box-shadow: 0 0 15px rgba(123, 31, 162, 0.4);
        }
        div[data-testid="stButton"] button:nth-child(2):hover {
            background-color: #9c27b0;
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(156, 39, 176, 0.6);
        }
        /* Slider y texto */
        .stSlider label {
            color: #ce93d8;
            font-weight: bold;
        }
        .stMarkdown h3, .stMarkdown h2 {
            color: #f8bbd0;
        }
    </style>
""", unsafe_allow_html=True)

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
    if st.button('🌸 Encender dispositivo'):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("✨ Dispositivo encendido")

with col2:
    if st.button('💜 Apagar dispositivo'):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.error("💤 Dispositivo apagado")

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
    st.success(f"🚀 Valor analógico enviado: `{values}`")

st.markdown("---")
st.caption("Diseño en rosa 💖 y morado 💜 con Streamlit + MQTT")
