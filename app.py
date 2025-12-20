import streamlit as st
import streamlit.components.v1 as components
import random
import sys
import json
import os
import datetime
from datetime import timedelta
from collections import defaultdict

# =====================================================
# 1. CONFIGURACIÓN DE PÁGINA (SIEMPRE PRIMERO)
# =====================================================
st.set_page_config(
    page_title="Portal Sagrado Noche Profunda",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. GESTIÓN DE ESTADO E INICIALIZACIÓN
# =====================================================
def init_session_state():
    defaults = {
        "login": False, "current_view": "menu", "sub_view": None,
        "biblia_subview": "menu", "biblia_vdia_res": None, "biblia_vdia_date": None, "biblia_vdia_stored": None,
        "finanzas_subview": "menu", "finanzas_result": None,
        "notas_subview": "menu", "notas_result": None,
        "libros_subview": "menu", "libros_result": None, "libros_imagen": None,
        "frases_subview": "menu", "frases_result": None,
        "personalidades_subview": "menu",
        "ideas_subview": "menu", "ideas_history": [], "selected_project_id": None,
        "tarot_subview": "menu", "tarot_result": None, "tarot_reading_type": None,
        "astro_subview": "menu", "astro_result": None,
        "nume_subview": "menu", "nume_result": None, "oculto_subview": "menu",
        "profesional_subview": "menu", "profesional_pregunta": None, "profesional_respuesta": None,
        "first_load_done": False
    }
    for key, value in defaults.items():
        if key not in st.session_state: st.session_state[key] = value

init_session_state()

# =====================================================
# 3. CACHÉ DE ESTILOS Y ASSETS (OPTIMIZACIÓN VISUAL)
# =====================================================
@st.cache_data
def get_main_css():
    return """
<style>
    .stApp, p, span, div, h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    label, .stSelectbox label, .stTextInput label, .stTextArea label, .stNumberInput label {
        color: #ffda89 !important; font-weight: bold !important; font-size: 1.1rem !important; text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }
    textarea, input, .stNumberInput input {
        background-color: rgba(10, 10, 25, 0.9) !important; color: #ffffff !important;
        border: 1px solid rgba(147, 51, 234, 0.5) !important; border-radius: 15px !important;
    }
    .stTextInput > div > div, .stTextArea > div > div, .stSelectbox > div > div, .stNumberInput > div > div { 
        background: rgba(10, 10, 25, 0.85) !important; color: white !important;
    }
    ul[data-testid="stSelectboxVirtualDropdown"] li { background: #020617 !important; color: white !important; }
    ::placeholder { color: rgba(255, 255, 255, 0.6) !important; }
    .stChatInputContainer {
        position: fixed !important; bottom: 180px !important; left: 0 !important; right: 0 !important;
        z-index: 1001 !important; background: rgba(2, 6, 23, 0.98) !important; padding: 15px !important;
        border-top: 1px solid rgba(147, 51, 234, 0.5) !important; backdrop-filter: blur(10px) !important;
    }
    .stChatInput, .stChatInput > div {
        background-color: rgba(255, 255, 255, 0.95) !important; border: 2px solid rgba(147, 51, 234, 0.8) !important;
        border-radius: 25px !important; color: #1a1a2e !important;
    }
    .stChatInput textarea, .stChatInput input { color: #1a1a2e !important; -webkit-text-fill-color: #1a1a2e !important; }
    #MainMenu, footer, header, .stDeployButton {display: none !important;}
    .stApp { background: radial-gradient(circle at 50% 50%, #020617 0%, #01020a 50%, #000000 100%) !important; background-attachment: fixed; }
    .block-container { padding-top: 15vh !important; padding-bottom: 280px !important; max-width: 1000px !important; }
    .stButton button {
        background: linear-gradient(135deg, #ffdd92 0%, #d4af37 100%) !important;
        color: #3d2b00 !important; border-radius: 50px !important; padding: 10px 25px !important; font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(255, 218, 137, 0.4) !important; border: none !important;
        width: 100% !important; transition: transform 0.2s !important; position: relative; z-index: 10;
    }
    .stButton button:hover { transform: scale(1.02) !important; box-shadow: 0 6px 20px rgba(255, 218, 137, 0.6) !important; }
    @keyframes floatIcon { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-6px); } }
    .magic-card {
        display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; 
        padding: 15px 8px; background: linear-gradient(135deg, rgba(147,51,234,0.15) 0%, rgba(16,185,129,0.1) 100%);
        border: 1px solid rgba(147,51,234,0.4); border-radius: 25px; min-height: 120px;
        aspect-ratio: 1 / 1; backdrop-filter: blur(5px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); transition: all 0.3s ease;
    }
    .magic-card:hover { transform: translateY(-8px) scale(1.02); border-color: rgba(255, 218, 137, 0.8); }
    .card-icon { font-size: 4.2rem; filter: drop-shadow(0 0 12px currentColor); animation: floatIcon 3s ease-in-out infinite; }
    .card-label { font-size: 1.05rem; font-weight: 700; color: #fff; text-transform: uppercase; text-shadow: 0 2px 5px rgba(0,0,0,0.5); }
    .tarot-icon { color: #d8b4fe; } .ideas-icon { color: #93c5fd; } .biblia-icon { color: #fde047; }
    .finanzas-icon { color: #86efac; } .notas-icon { color: #c4b5fd; } .libros-icon { color: #67e8f9; }
    .frases-icon { color: #fdba74; } .personalidades-icon { color: #fca5a5; } .profesional-icon { color: #e9d5ff; }
    .oculto-icon { color: #a78bfa; }
    .result-card {
        padding: 25px; background: linear-gradient(135deg, rgba(15, 15, 30, 0.95) 0%, rgba(20, 20, 45, 0.90) 100%);
        backdrop-filter: blur(15px); border: 1px solid rgba(255, 218, 137, 0.3); border-radius: 20px; 
        margin-top: 20px; text-align: center; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    .result-card h2 { color: #ffda89 !important; font-size: 1.8rem; text-shadow: 0 2px 4px rgba(0,0,0,0.8); }
    .result-card p, .result-card div { font-size: 1.15rem; line-height: 1.6; color: #ffffff !important; text-shadow: 0 1px 2px rgba(0,0,0,0.9); }
    .result-card strong { color: #ffda89 !important; font-weight: 700; display: block; margin-bottom: 5px; font-size: 1.2rem; }
    .title-glow { font-size: 5.5rem; font-weight: 900; text-align: center; color: #ffffff !important; text-shadow: 0 0 30px #ffda89; margin: 30px 0 20px 0; }
    .subtitle-text { color: #d8c9ff !important; text-align: center; font-size: 1.2rem; margin-bottom: 30px; }
    .top-banner { position: fixed; top: 0; left: 0; width: 100%; height: 60px; background: rgba(2,6,23,0.95); display: flex; align-items: center; justify-content: center; color: #ffda89 !important; z-index: 999; border-bottom: 1px solid rgba(255,218,137,0.3); }
    .bottom-footer { position: fixed; bottom: 0; left: 0; width: 100%; padding: 10px; text-align: center; color: rgba(216,201,255,0.6) !important; font-size: 0.8rem; background: rgba(2,6,23,0.95); border-top: 1px solid rgba(147,51,234,0.2); z-index: 998; }
    .star { position: fixed; background: white; border-radius: 50%; z-index: 1; opacity: 0; animation: twinkle var(--duration) ease-in-out infinite; }
    @keyframes twinkle { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }
    .shooting-star { 
        position: fixed; width: 3px; height: 3px; background: white; border-radius: 50%; z-index: 2; 
        box-shadow: 0 0 15px 3px rgba(255, 255, 255, 0.9), 0 0 5px 1px rgba(147, 197, 253, 0.5); 
        animation: shoot var(--shoot-duration) cubic-bezier(0.25, 0.46, 0.45, 0.94) var(--shoot-delay) infinite; 
        opacity: 0; 
    }
    .shooting-star::after { 
        content: ''; position: absolute; top: 50%; left: 50%; width: 120px; height: 2px; 
        background: linear-gradient(to right, rgba(255, 255, 255, 0.95), rgba(147, 197, 253, 0.6) 40%, rgba(147, 197, 253, 0.2) 70%, transparent); 
        transform: translate(-120px, -50%); border-radius: 50%; filter: blur(0.5px);
    }
    @keyframes shoot { 
        0% { opacity: 0; transform: translateX(0) translateY(0) rotate(-45deg) scale(0.5); } 
        5% { opacity: 1; transform: translateX(20px) translateY(20px) rotate(-45deg) scale(1); } 
        85% { opacity: 1; } 
        100% { opacity: 0; transform: translateX(400px) translateY(400px) rotate(-45deg) scale(0.8); } 
    }
    
    .spotify-bottom-fixed {
        position: fixed !important;
        bottom: 60px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 999999 !important;
        width: 300px !important;
        box-shadow: 0 8px 32px rgba(147, 51, 234, 0.6) !important;
        border-radius: 12px !important;
        background: rgba(2, 6, 23, 0.95) !important;
        padding: 5px !important;
        pointer-events: auto !important;
    }
    
    .spotify-bottom-fixed iframe {
        border-radius: 12px !important;
    }
    
    .spotify-bottom-fixed:hover {
        transform: translateX(-50%) translateY(-5px) !important;
        box-shadow: 0 12px 40px rgba(147, 51, 234, 0.8) !important;
    }
    
    @media (max-width: 768px) {
        .spotify-bottom-fixed {
            width: 280px !important;
            bottom: 60px !important;
        }
        .title-glow { font-size: 3.5rem !important; } 
        .card-icon { font-size: 3rem; } 
    }
</style>
"""

@st.cache_data
def generar_fondo_estelar_cached():
    stars_html = "".join([f'<div class="star" style="top:{random.randint(0,100)}%; left:{random.randint(0,100)}%; width:{random.uniform(1,2.5)}px; height:{random.uniform(1,2.5)}px; --duration:{random.uniform(2,8)}s;"></div>' for _ in range(50)])
    shooting_html = "".join([f'<div class="shooting-star" style="top:{random.randint(0,50)}%; left:{random.randint(0,80)}%; --shoot-duration:{random.uniform(1.5,3)}s; --shoot-delay:{random.uniform(0,10)}s;"></div>' for _ in range(10)])
    return stars_html + shooting_html

# Inyectamos CSS y Fondo
st.markdown(get_main_css(), unsafe_allow_html=True)
st.markdown(generar_fondo_estelar_cached(), unsafe_allow_html=True)

# =====================================================
# 4. DEFINICIÓN DE CLASES (MODELO)
# =====================================================
class LocalFinanzasHandler:
    def __init__(self):
        self.DATA_FOLDER = "data"
        self.FINANZAS_FILE = os.path.join(self.DATA_FOLDER, "finanzas.json")
        self.CATEGORIAS = {
            "🍔 comida": ["comida", "restaurante", "supermercado", "almuerzo", "cena"],
            "🚗 transporte": ["uber", "taxi", "gasolina", "bus", "metro", "transporte"],
            "🏠 hogar": ["renta", "luz", "agua", "gas", "internet", "servicios"],
            "🎉 entretenimiento": ["cine", "concierto", "salida", "fiesta", "netflix"],
            "👕 ropa": ["ropa", "zapatos", "accesorios", "moda"],
            "💊 salud": ["doctor", "medicina", "farmacia", "gym", "terapia"],
            "📚 educación": ["curso", "libro", "universidad", "clase"],
            "🎁 regalos": ["regalo", "cumpleaños"],
            "💰 ahorro": ["ahorro", "inversión"],
            "📱 tecnología": ["celular", "computadora", "app"],
            "✈️ viajes": ["hotel", "vuelo", "viaje"],
            "🐕 mascotas": ["veterinario", "comida perro", "gato"],
            "💅 personal": ["peluquería", "spa", "cosmético"],
            "📄 otros": []
        }
        os.makedirs(self.DATA_FOLDER, exist_ok=True)

    def _cargar_finanzas(self):
        if not os.path.exists(self.FINANZAS_FILE):
            return {"gastos": [], "ingresos": [], "presupuestos": {}}
        try:
            with open(self.FINANZAS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list): return {"gastos": data, "ingresos": [], "presupuestos": {}}
                return data
        except:
            return {"gastos": [], "ingresos": [], "presupuestos": {}}

    def _guardar_finanzas(self, data):
        with open(self.FINANZAS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _detectar_categoria(self, descripcion):
        desc_lower = descripcion.lower()
        for categoria, palabras in self.CATEGORIAS.items():
            for palabra in palabras:
                if palabra in desc_lower: return categoria
        return "📄 otros"

    def _verificar_presupuesto(self, data, categoria, monto_nuevo):
        if categoria not in data["presupuestos"]: return ""
        mes_actual = datetime.datetime.now().strftime("%Y-%m")
        gasto_mes = sum(g["monto"] for g in data["gastos"] if g["categoria"] == categoria and g["fecha"].startswith(mes_actual))
        presupuesto = data["presupuestos"][categoria]
        porcentaje = (gasto_mes / presupuesto) * 100
        if porcentaje >= 100: return f"\n⚠️ *ALERTA:* Ya gastaste ${gasto_mes} de ${presupuesto} ({porcentaje:.0f}%) en {categoria}"
        elif porcentaje >= 80: return f"\n⚠️ Llevas ${gasto_mes} de ${presupuesto} ({porcentaje:.0f}%) en {categoria}"
        return ""

    def agregar_gasto(self, monto, categoria, descripcion):
        data = self._cargar_finanzas()
        if not categoria or categoria.lower() in ["auto", "automático", ""]:
            categoria = self._detectar_categoria(descripcion)
        nuevo = {
            "id": len(data["gastos"]) + 1,
            "monto": float(monto),
            "categoria": categoria.lower().strip(),
            "descripcion": descripcion,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d"),
            "hora": datetime.datetime.now().strftime("%H:%M")
        }
        data["gastos"].append(nuevo)
        self._guardar_finanzas(data)
        alerta = self._verificar_presupuesto(data, categoria, float(monto))
        return f"✨ *Gasto agregado exitosamente*\n\n💰 Monto: ${monto}\n🏷️ Categoría: {categoria}\n📝 Descripción: {descripcion}\n📅 Fecha: {nuevo['fecha']}\n{alerta}"

    def listar_gastos(self):
        data = self._cargar_finanzas()
        gastos = data["gastos"]
        if not gastos: return "Aún no tienes gastos registrados, amor 🥺"
        texto = "📘 *Todos tus gastos registrados:* \n\n"
        total = 0
        for g in reversed(gastos[-15:]):
            texto += f"**#{g['id']}** ${g['monto']} — {g['categoria']} — {g['descripcion']} ({g['fecha']})\n"
            total += g["monto"]
        texto += f"\n💰 *Total gastado:* ${total}"
        return texto

    def gastos_de_hoy(self):
        hoy = datetime.datetime.now().strftime("%Y-%m-%d")
        data = self._cargar_finanzas()
        filtrados = [g for g in data["gastos"] if g["fecha"] == hoy]
        if not filtrados: return "Hoy no tienes gastos registrados ✨"
        texto = "📅 *Gastos de hoy:* \n\n"
        total = 0
        for g in filtrados:
            texto += f"• ${g['monto']} — {g['categoria']} — {g['descripcion']}\n"
            total += g["monto"]
        texto += f"\n💰 *Total gastado hoy:* ${total}"
        return texto

    def buscar_gastos(self, palabra):
        data = self._cargar_finanzas()
        palabra_lower = palabra.lower()
        resultados = [g for g in data["gastos"] if palabra_lower in g["descripcion"].lower() or palabra_lower in g["categoria"].lower()]
        if not resultados: return f"No encontré gastos con '{palabra}', amor 💛"
        texto = f"🔍 *RESULTADOS PARA: {palabra}* 🔍\n\n"
        total = 0
        for g in reversed(resultados[-10:]):
            texto += f"**#{g['id']}** ${g['monto']} — {g['categoria']} — {g['descripcion']} ({g['fecha']})\n"
            total += g["monto"]
        texto += f"\n📊 *Total encontrado:* ${total}\n🔢 *{len(resultados)} resultados*"
        return texto
    
    def gastos_por_categoria(self, categoria):
        data = self._cargar_finanzas()
        filtrados = [g for g in data["gastos"] if categoria.lower() in g["categoria"].lower()]
        if not filtrados: return f"No tienes gastos en la categoría '{categoria}', amor 💛"
        texto = f"🏷️ *Gastos en categoría '{categoria}':*\n\n"
        total = 0
        for g in reversed(filtrados[-10:]):
            texto += f"**#{g['id']}** ${g['monto']} — {g['descripcion']} ({g['fecha']})\n"
            total += g["monto"]
        texto += f"\n💰 *Total en {categoria}:* ${total}"
        return texto

    def borrar_gasto(self, gasto_id):
        try:
            data = self._cargar_finanzas()
            gasto = next((g for g in data["gastos"] if g["id"] == int(gasto_id)), None)
            if not gasto: return "El ID no es válido 🥺"
            data["gastos"] = [g for g in data["gastos"] if g["id"] != int(gasto_id)]
            self._guardar_finanzas(data)
            return f"🗑️ Gasto eliminado:\n${gasto['monto']} — {gasto['categoria']} — {gasto['descripcion']}"
        except: return "Error eliminando gasto."

    def agregar_ingreso(self, monto, descripcion):
        data = self._cargar_finanzas()
        nuevo = {
            "id": len(data["ingresos"]) + 1,
            "monto": float(monto),
            "descripcion": descripcion,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d"),
            "hora": datetime.datetime.now().strftime("%H:%M")
        }
        data["ingresos"].append(nuevo)
        self._guardar_finanzas(data)
        return f"✨ *Ingreso agregado exitosamente*\n\n💵 Monto: ${monto}\n📝 Descripción: {descripcion}\n📅 Fecha: {nuevo['fecha']}"

    def listar_ingresos(self):
        data = self._cargar_finanzas()
        ingresos = data["ingresos"]
        if not ingresos: return "Aún no tienes ingresos registrados, amor 🥺"
        texto = "💵 *Todos tus ingresos registrados:* \n\n"
        total = 0
        for ing in reversed(ingresos[-15:]):
            texto += f"**#{ing['id']}** ${ing['monto']} — {ing['descripcion']} ({ing['fecha']})\n"
            total += ing["monto"]
        texto += f"\n💰 *Total de ingresos:* ${total}"
        return texto

    def borrar_ingreso(self, indice):
        try:
            data = self._cargar_finanzas()
            ing = next((i for i in data["ingresos"] if i["id"] == int(indice)), None)
            if not ing: return "El ID no es válido 🥺"
            data["ingresos"] = [i for i in data["ingresos"] if i["id"] != int(indice)]
            self._guardar_finanzas(data)
            return f"🗑️ Ingreso eliminado:\n${ing['monto']} — {ing['descripcion']}"
        except: return "Error eliminando ingreso."

    def establecer_presupuesto(self, categoria, monto):
        data = self._cargar_finanzas()
        data["presupuestos"][categoria.lower().strip()] = float(monto)
        self._guardar_finanzas(data)
        return f"✅ *Presupuesto establecido*\n\n🏷️ {categoria}\n💰 ${monto}/mes"

    def ver_presupuestos(self):
        data = self._cargar_finanzas()
        if not data["presupuestos"]: return "No tienes presupuestos establecidos aún, amor 💛"
        mes_actual = datetime.datetime.now().strftime("%Y-%m")
        texto = "📊 *PRESUPUESTOS DEL MES* 📊\n\n"
        for categoria, presupuesto in data["presupuestos"].items():
            gasto_mes = sum(g["monto"] for g in data["gastos"] if g["categoria"] == categoria and g["fecha"].startswith(mes_actual))
            porcentaje = (gasto_mes / presupuesto) * 100
            restante = presupuesto - gasto_mes
            emoji = "🔴" if porcentaje >= 100 else "🟡" if porcentaje >= 80 else "🟢"
            texto += f"{emoji} *{categoria}*\n💰 ${gasto_mes} / ${presupuesto}\n📊 {porcentaje:.0f}% usado\n"
            if restante > 0: texto += f"✅ Quedan ${restante}\n\n"
            else: texto += f"❌ Excedido por ${abs(restante)}\n\n"
        return texto

    def resumen_mensual(self):
        data = self._cargar_finanzas()
        mes_actual = datetime.datetime.now().strftime("%Y-%m")
        mes_nombre = datetime.datetime.now().strftime("%B %Y")
        gastos_mes = [g for g in data["gastos"] if g["fecha"].startswith(mes_actual)]
        ingresos_mes = [i for i in data["ingresos"] if i["fecha"].startswith(mes_actual)]
        if not gastos_mes and not ingresos_mes: return f"No hay movimientos en {mes_nombre}, amor 💛"
        texto = f"📊 *RESUMEN DE {mes_nombre.upper()}* 📊\n\n"
        total_ingresos = sum(i["monto"] for i in ingresos_mes)
        texto += f"💵 *Ingresos:* ${total_ingresos}\n"
        total_gastos = sum(g["monto"] for g in gastos_mes)
        texto += f"💸 *Gastos:* ${total_gastos}\n"
        balance = total_ingresos - total_gastos
        if balance >= 0: texto += f"✅ *Balance:* +${balance}\n\n"
        else: texto += f"❌ *Balance:* -${abs(balance)}\n\n"
        gastos_por_cat = defaultdict(float)
        for gasto in gastos_mes: gastos_por_cat[gasto["categoria"]] += gasto["monto"]
        if gastos_por_cat:
            texto += "📋 *Top Categorías:*\n"
            for cat, total in sorted(gastos_por_cat.items(), key=lambda x: x[1], reverse=True)[:5]:
                porcentaje = (total / total_gastos * 100) if total_gastos > 0 else 0
                texto += f"{cat}: ${total} ({porcentaje:.0f}%)\n"
        if total_ingresos > 0:
            tasa_ahorro = (balance / total_ingresos) * 100
            texto += f"\n💰 *Tasa de ahorro:* {tasa_ahorro:.0f}%"
        return texto

    def comparar_meses(self):
        data = self._cargar_finanzas()
        mes_actual = datetime.datetime.now().strftime("%Y-%m")
        mes_nombre_actual = datetime.datetime.now().strftime("%B")
        primer_dia = datetime.datetime.now().replace(day=1)
        mes_anterior = (primer_dia - timedelta(days=1)).strftime("%Y-%m")
        mes_nombre_anterior = (primer_dia - timedelta(days=1)).strftime("%B")
        gastos_actual = sum(g["monto"] for g in data["gastos"] if g["fecha"].startswith(mes_actual))
        gastos_anterior = sum(g["monto"] for g in data["gastos"] if g["fecha"].startswith(mes_anterior))
        texto = f"📊 *COMPARATIVA MENSUAL* 📊\n\n📅 {mes_nombre_anterior}: ${gastos_anterior}\n📅 {mes_nombre_actual}: ${gastos_actual}\n\n"
        if gastos_anterior > 0:
            diferencia = gastos_actual - gastos_anterior
            porcentaje = (diferencia / gastos_anterior) * 100
            if diferencia > 0: texto += f"📈 Gastaste ${abs(diferencia)} MÁS ({porcentaje:.0f}%)"
            elif diferencia < 0: texto += f"📉 Gastaste ${abs(diferencia)} MENOS ({abs(porcentaje):.0f}%)"
            else: texto += "➡️ Gasto similar"
        return texto

    def ver_categorias(self):
        texto = "🏷 *CATEGORÍAS DISPONIBLES* 🏷\n\n"
        for categoria in self.CATEGORIAS.keys(): texto += f"{categoria}\n"
        return texto
    
    def exportar_a_csv(self):
        import csv
        from io import StringIO
        
        data = self._cargar_finanzas()
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['GASTOS'])
        writer.writerow(['ID', 'Monto', 'Categoría', 'Descripción', 'Fecha', 'Hora'])
        
        for gasto in data.get('gastos', []):
            writer.writerow([
                gasto.get('id', ''),
                gasto.get('monto', ''),
                gasto.get('categoria', ''),
                gasto.get('descripcion', ''),
                gasto.get('fecha', ''),
                gasto.get('hora', '')
            ])
        
        writer.writerow([])
        writer.writerow(['INGRESOS'])
        writer.writerow(['ID', 'Monto', 'Fuente', 'Fecha'])
        
        for ingreso in data.get('ingresos', []):
            writer.writerow([
                ingreso.get('id', ''),
                ingreso.get('monto', ''),
                ingreso.get('fuente', ''),
                ingreso.get('fecha', '')
            ])
        
        writer.writerow([])
        writer.writerow(['PRESUPUESTOS'])
        writer.writerow(['Categoría', 'Presupuesto'])
        
        for categoria, presupuesto in data.get('presupuestos', {}).items():
            writer.writerow([categoria, presupuesto])
        
        csv_string = output.getvalue()
        output.close()
        return csv_string
    
    def estadisticas_avanzadas(self):
        data = self._cargar_finanzas()
        if not data.get('gastos'): return None
        
        hoy = datetime.datetime.now()
        mes_actual = hoy.strftime("%Y-%m")
        dia_actual = hoy.day
        gastos_mes = [g for g in data['gastos'] if g['fecha'].startswith(mes_actual)]
        if not gastos_mes: return None
        
        total_mes = sum(g['monto'] for g in gastos_mes)
        promedio_diario = total_mes / dia_actual if dia_actual > 0 else 0
        dias_mes = 30
        proyeccion_mes = promedio_diario * dias_mes
        
        gastos_por_cat = {}
        for g in gastos_mes:
            cat = g.get('categoria', '📄 otros')
            gastos_por_cat[cat] = gastos_por_cat.get(cat, 0) + g['monto']
        
        top_categorias = sorted(gastos_por_cat.items(), key=lambda x: x[1], reverse=True)[:3]
        
        primer_dia = hoy.replace(day=1)
        mes_anterior = (primer_dia - timedelta(days=1)).strftime("%Y-%m")
        gastos_mes_ant = [g for g in data['gastos'] if g['fecha'].startswith(mes_anterior)]
        total_mes_anterior = sum(g['monto'] for g in gastos_mes_ant)
        
        diferencia = total_mes - total_mes_anterior
        porcentaje_cambio = (diferencia / total_mes_anterior * 100) if total_mes_anterior > 0 else 0
        ingresos_mes = sum(i['monto'] for i in data.get('ingresos', []) if i['fecha'].startswith(mes_actual))
        balance = ingresos_mes - total_mes
        
        return {
            'total_mes': total_mes,
            'promedio_diario': promedio_diario,
            'proyeccion_mes': proyeccion_mes,
            'top_categorias': top_categorias,
            'total_mes_anterior': total_mes_anterior,
            'diferencia': diferencia,
            'porcentaje_cambio': porcentaje_cambio,
            'ingresos_mes': ingresos_mes,
            'balance': balance,
            'num_gastos': len(gastos_mes),
            'gasto_promedio': total_mes / len(gastos_mes) if gastos_mes else 0,
            'dia_actual': dia_actual
        }


class LocalNotasHandler:
    def __init__(self):
        self.DATA_FOLDER = "data"
        self.NOTAS_FILE = os.path.join(self.DATA_FOLDER, "notas.json")
        self.CATEGORIAS = [
            "💼 Trabajo",
            "❤️ Personal",
            "💡 Ideas",
            "⏰ Recordatorios",
            "🛒 Compras",
            "📚 Estudio",
            "🎯 Metas",
            "📄 Otros"
        ]
        os.makedirs(self.DATA_FOLDER, exist_ok=True)

    def _cargar_notas(self):
        if not os.path.exists(self.NOTAS_FILE):
            return []
        try:
            with open(self.NOTAS_FILE, "r", encoding="utf-8") as f:
                notas = json.load(f)
                if notas and isinstance(notas[0], str):
                    notas_nuevas = []
                    for i, texto in enumerate(notas, 1):
                        notas_nuevas.append({
                            "id": i,
                            "texto": texto,
                            "categoria": "📄 Otros",
                            "fecha_creacion": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "importante": False,
                            "recordatorio": None
                        })
                    self._guardar_notas(notas_nuevas)
                    return notas_nuevas
                return notas
        except:
            return []

    def _guardar_notas(self, notas):
        try:
            with open(self.NOTAS_FILE, "w", encoding="utf-8") as f:
                json.dump(notas, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False

    def agregar_nota(self, texto, categoria="📄 Otros", importante=False, recordatorio=None):
        if not texto or texto.strip() == "":
            return "❌ No puedes agregar una nota vacía."
        notas = self._cargar_notas()
        nueva_nota = {
            "id": len(notas) + 1,
            "texto": texto.strip(),
            "categoria": categoria,
            "fecha_creacion": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "importante": importante,
            "recordatorio": recordatorio
        }
        notas.append(nueva_nota)
        if self._guardar_notas(notas):
            mensaje = f"✅ Nota guardada en {categoria}"
            if importante: mensaje += " ⭐"
            if recordatorio: mensaje += f"\n⏰ Recordatorio: {recordatorio}"
            return mensaje
        return "❌ Error al guardar la nota."

    def ver_notas(self, filtro=None):
        notas = self._cargar_notas()
        if not notas: return "📭 No tienes notas guardadas."
        notas_filtradas = notas
        titulo = "📘 *Tus notas:*"
        if filtro == "importantes":
            notas_filtradas = [n for n in notas if n.get("importante", False)]
            titulo = "⭐ *Notas importantes:*"
        elif filtro and filtro.startswith("categoria:"):
            cat = filtro.replace("categoria:", "")
            notas_filtradas = [n for n in notas if n.get("categoria", "").lower() == cat.lower()]
            titulo = f"📂 *Notas en {cat}:*"
        elif filtro == "hoy":
            hoy = datetime.datetime.now().strftime("%Y-%m-%d")
            notas_filtradas = [n for n in notas if n.get("fecha_creacion", "").startswith(hoy)]
            titulo = "📅 *Notas de hoy:*"
        elif filtro == "semana":
            hace_semana = (datetime.datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            notas_filtradas = [n for n in notas if n.get("fecha_creacion", "") >= hace_semana]
            titulo = "📅 *Notas de esta semana:*"
        elif filtro == "mes":
            mes_actual = datetime.datetime.now().strftime("%Y-%m")
            notas_filtradas = [n for n in notas if n.get("fecha_creacion", "").startswith(mes_actual)]
            titulo = "📅 *Notas de este mes:*"
        if not notas_filtradas: return f"📭 No hay notas con ese filtro."
        notas_filtradas.sort(key=lambda x: (not x.get("importante", False), x.get("fecha_creacion", "")), reverse=True)
        texto = f"{titulo}\n\n"
        for nota in notas_filtradas:
            estrella = "⭐ " if nota.get("importante", False) else ""
            categoria = nota.get("categoria", "📄 Otros")
            nota_texto = nota.get("texto", "")
            nota_id = nota.get("id", "?")
            fecha = nota.get("fecha_creacion", "")
            nota_preview = nota_texto[:80] + "..." if len(nota_texto) > 80 else nota_texto
            texto += f"{estrella}**#{nota_id}** {categoria}\n{nota_preview}\n_📅 {fecha}_\n\n"
        return texto

    def ver_notas_por_categoria(self):
        notas = self._cargar_notas()
        if not notas: return "📭 No tienes notas guardadas."
        por_categoria = {}
        for nota in notas:
            cat = nota.get("categoria", "📄 Otros")
            if cat not in por_categoria: por_categoria[cat] = []
            por_categoria[cat].append(nota)
        texto = "📊 *NOTAS POR CATEGORÍA* 📊\n\n"
        for cat, lista in sorted(por_categoria.items()):
            importantes = sum(1 for n in lista if n.get("importante", False))
            texto += f"{cat}: {len(lista)} notas"
            if importantes > 0: texto += f" ({importantes} ⭐)"
            texto += "\n"
        texto += f"\n📂 Total: {len(notas)} notas"
        return texto

    def editar_nota(self, nota_id, nuevo_texto=None, nueva_categoria=None, nuevo_importante=None):
        notas = self._cargar_notas()
        nota = next((n for n in notas if n["id"] == int(nota_id)), None)
        if not nota: return f"❌ No encontré la nota #{nota_id}."
        if nuevo_texto: nota["texto"] = nuevo_texto
        if nueva_categoria: nota["categoria"] = nueva_categoria
        if nuevo_importante is not None: nota["importante"] = nuevo_importante
        if self._guardar_notas(notas):
            estrella = "⭐" if nota["importante"] else ""
            return f"✅ Nota #{nota_id} actualizada {estrella}\n\n{nota['categoria']}\n{nota['texto']}"
        return "❌ Error al actualizar la nota."

    def ver_nota_completa(self, nota_id):
        notas = self._cargar_notas()
        nota = next((n for n in notas if n["id"] == int(nota_id)), None)
        if not nota: return f"❌ No encontré la nota #{nota_id}."
        estrella = "⭐ " if nota.get("importante", False) else ""
        texto = f"{estrella}**NOTA #{nota['id']}**\n\n"
        texto += f"📂 Categoría: {nota.get('categoria', 'Otros')}\n"
        texto += f"📅 Creada: {nota.get('fecha_creacion', 'N/A')}\n"
        if nota.get("recordatorio"): texto += f"⏰ Recordatorio: {nota['recordatorio']}\n"
        texto += f"\n📝 Contenido:\n{nota['texto']}"
        return texto

    def marcar_importante(self, nota_id, importante=True):
        notas = self._cargar_notas()
        nota = next((n for n in notas if n["id"] == int(nota_id)), None)
        if not nota: return f"❌ No encontré la nota #{nota_id}."
        nota["importante"] = importante
        if self._guardar_notas(notas):
            return f"⭐ Nota #{nota_id} marcada como importante" if importante else f"✅ Nota #{nota_id} desmarcada como importante"
        return "❌ Error al actualizar la nota."

    def agregar_recordatorio(self, nota_id, fecha_hora):
        notas = self._cargar_notas()
        nota = next((n for n in notas if n["id"] == int(nota_id)), None)
        if not nota: return f"❌ No encontré la nota #{nota_id}."
        nota["recordatorio"] = fecha_hora
        if self._guardar_notas(notas):
            return f"⏰ Recordatorio agregado\n\n📝 Nota #{nota_id}\n⏰ {fecha_hora}"
        return "❌ Error al agregar recordatorio."

    def ver_recordatorios(self):
        notas = self._cargar_notas()
        con_recordatorio = [n for n in notas if n.get("recordatorio")]
        if not con_recordatorio: return "📭 No tienes recordatorios pendientes."
        con_recordatorio.sort(key=lambda x: x["recordatorio"])
        texto = "⏰ *RECORDATORIOS PENDIENTES* ⏰\n\n"
        for nota in con_recordatorio:
            texto += f"**#{nota['id']}** - {nota['recordatorio']}\n"
            nota_preview = nota['texto'][:60] + "..." if len(nota['texto']) > 60 else nota['texto']
            texto += f"📝 {nota_preview}\n\n"
        return texto

    def borrar_nota(self, nota_id):
        notas = self._cargar_notas()
        nota = next((n for n in notas if n["id"] == int(nota_id)), None)
        if not nota: return f"❌ No encontré la nota #{nota_id}."
        notas = [n for n in notas if n["id"] != int(nota_id)]
        if self._guardar_notas(notas):
            nota_preview = nota['texto'][:100] + "..." if len(nota['texto']) > 100 else nota['texto']
            return f"🗑️ Nota #{nota_id} eliminada:\n\n{nota_preview}"
        return "❌ Error al eliminar la nota."

    def buscar_nota(self, palabra_clave):
        notas = self._cargar_notas()
        if not notas: return "📭 No tienes notas guardadas."
        palabra_clave = palabra_clave.lower()
        encontradas = []
        for nota in notas:
            if palabra_clave in nota['texto'].lower():
                nota_preview = nota['texto'][:80] + "..." if len(nota['texto']) > 80 else nota['texto']
                estrella = "⭐ " if nota.get("importante", False) else ""
                encontradas.append(f"{estrella}**#{nota['id']}** {nota['categoria']}\n{nota_preview}")
        if not encontradas: return f"🔍 No encontré notas con '{palabra_clave}'."
        resultado = f"🔍 *Notas con '{palabra_clave}':*\n\n"
        resultado += "\n\n".join(encontradas)
        return resultado

    def ver_categorias(self):
        texto = "📂 *CATEGORÍAS DISPONIBLES* 📂\n\n"
        for cat in self.CATEGORIAS: texto += f"{cat}\n"
        return texto

    def estadisticas_notas(self):
        notas = self._cargar_notas()
        if not notas: return "📭 No tienes notas guardadas."
        total = len(notas)
        importantes = sum(1 for n in notas if n.get("importante", False))
        con_recordatorio = sum(1 for n in notas if n.get("recordatorio"))
        por_categoria = {}
        for nota in notas:
            cat = nota.get("categoria", "📄 Otros")
            por_categoria[cat] = por_categoria.get(cat, 0) + 1
        cat_top = max(por_categoria.items(), key=lambda x: x[1]) if por_categoria else ("N/A", 0)
        texto = "📊 *ESTADÍSTICAS DE NOTAS* 📊\n\n"
        texto += f"📂 Total: {total}\n"
        texto += f"⭐ Importantes: {importantes}\n"
        texto += f"⏰ Con recordatorio: {con_recordatorio}\n"
        texto += f"🏆 Categoría más usada: {cat_top[0]} ({cat_top[1]})\n"
        return texto
    
    def buscar_notas(self, query):
        if not query or query.strip() == "":
            return self._cargar_notas()
        
        notas = self._cargar_notas()
        query_lower = query.lower().strip()
        resultados = [n for n in notas if query_lower in n.get('texto', '').lower()]
        return resultados

class LocalLibrosHandler:
    def __init__(self):
        self.GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes?q="
        self.OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        self.openai_client = None
        self.openai_enabled = False
        self._inicializar_openai()
        
        # ✅ CORRECCIÓN: Inicializar datos de libros y book club
        self.__init_libros_data()
        self.__init_bookclub_data()

    def _inicializar_openai(self):
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)
            self.openai_enabled = True
        except:
            self.openai_enabled = False

    def buscar_libro(self, query):
        try:
            import requests
            response = requests.get(f"{self.GOOGLE_BOOKS_URL}{query}", timeout=5)
            data = response.json()
            if "items" not in data: return "No encontré resultados para ese libro 📚"
            libro = data["items"][0]["volumeInfo"]
            titulo = libro.get("title", "Sin título")
            autores = ", ".join(libro.get("authors", ["Autor desconocido"]))
            descripcion = libro.get("description", "Sin descripción disponible")[:200]
            return f"📖 *{titulo}*\n👤 {autores}\n\n{descripcion}..."
        except:
            return "Error al buscar el libro. Intenta de nuevo 💛"

    def _generar_imagen(self, prompt):
        if not self.openai_enabled: return None
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            return response.data[0].url
        except Exception as e:
            print(f"Error generando imagen: {e}")
            return None

    def imagen_de_libro(self, titulo):
        prompt = (
            f"Create an aesthetic illustration inspired by the book '{titulo}'. "
            f"Focus on atmosphere, symbolism, and mood. No text, no people. "
            f"Dreamy lighting, soft textures, cinematic digital art style."
        )
        return self._generar_imagen(prompt)

    def fanart_libro(self, titulo):
        prompt = (
            f"Fantasy fanart inspired by the book '{titulo}'. "
            f"Focus on scenery, atmosphere, and symbolic elements. No characters or text. "
            f"High-quality digital art with dramatic lighting."
        )
        return self._generar_imagen(prompt)

    def estetica_libro(self, titulo):
        prompt = (
            f"Aesthetic moodboard inspired by '{titulo}'. "
            f"Show textures, objects, colors, and atmosphere that represent the book's vibe. "
            f"No people, no text. Soft, dreamy aesthetic."
        )
        return self._generar_imagen(prompt)

    def imagen_genero(self, genero):
        prompt = (
            f"Atmospheric artwork representing the literary genre '{genero}'. "
            f"Use symbolic objects, lighting, and mood. No text, no people. "
            f"Cinematic and artistic style."
        )
        return self._generar_imagen(prompt)

    def imagen_autor(self, nombre):
        prompt = (
            f"Conceptual artwork inspired by the writing style of author '{nombre}'. "
            f"Abstract scenery with symbolic textures and atmospheric elements. "
            f"No people, no text. Artistic and evocative."
        )
        return self._generar_imagen(prompt)
    
    def __init_libros_data(self):
        self.DATA_FOLDER = "data"
        self.LIBROS_FILE = os.path.join(self.DATA_FOLDER, "libros_guardados.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
    
    def _cargar_libros(self):
        if not hasattr(self, 'LIBROS_FILE'):
            self.__init_libros_data()
        if not os.path.exists(self.LIBROS_FILE):
            return []
        try:
            with open(self.LIBROS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def _guardar_libros(self, libros):
        if not hasattr(self, 'LIBROS_FILE'):
            self.__init_libros_data()
        with open(self.LIBROS_FILE, "w", encoding="utf-8") as f:
            json.dump(libros, f, indent=2, ensure_ascii=False)
    
    def agregar_resena(self, libro_titulo, rating, texto_resena):
        if not hasattr(self, 'LIBROS_FILE'):
            self.__init_libros_data()
        
        libros = self._cargar_libros()
        libro_existente = next((l for l in libros if l['titulo'].lower() == libro_titulo.lower()), None)
        
        if libro_existente:
            libro_existente['rating'] = rating
            libro_existente['resena'] = texto_resena
            libro_existente['fecha_resena'] = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            nuevo_libro = {
                'id': len(libros) + 1,
                'titulo': libro_titulo,
                'rating': rating,
                'resena': texto_resena,
                'fecha_resena': datetime.datetime.now().strftime("%Y-%m-%d")
            }
            libros.append(nuevo_libro)
        
        self._guardar_libros(libros)
        return True, "Reseña guardada correctamente ⭐"
    
    def ver_libros_con_resenas(self):
        if not hasattr(self, 'LIBROS_FILE'):
            self.__init_libros_data()
        return self._cargar_libros()
    
    def eliminar_resena(self, libro_id):
        if not hasattr(self, 'LIBROS_FILE'):
            self.__init_libros_data()
        libros = self._cargar_libros()
        libros = [l for l in libros if l['id'] != libro_id]
        self._guardar_libros(libros)
        return True
    
    def __init_bookclub_data(self):
        self.DATA_FOLDER = "data"
        self.BOOKCLUB_FILE = os.path.join(self.DATA_FOLDER, "book_club.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
    
    def _cargar_bookclub(self):
        if not hasattr(self, 'BOOKCLUB_FILE'):
            self.__init_bookclub_data()
        if not os.path.exists(self.BOOKCLUB_FILE):
            return {
                'libro_actual': None,
                'reuniones': [],
                'miembros': [],
                'discusiones': []
            }
        try:
            with open(self.BOOKCLUB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {
                'libro_actual': None,
                'reuniones': [],
                'miembros': [],
                'discusiones': []
            }
    
    def _guardar_bookclub(self, data):
        if not hasattr(self, 'BOOKCLUB_FILE'):
            self.__init_bookclub_data()
        with open(self.BOOKCLUB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def establecer_libro_actual(self, titulo, autor=""):
        data = self._cargar_bookclub()
        data['libro_actual'] = {
            'titulo': titulo,
            'autor': autor,
            'fecha_inicio': datetime.datetime.now().strftime("%Y-%m-%d")
        }
        self._guardar_bookclub(data)
        return True, f"Libro actual: {titulo}"
    
    def agregar_reunion(self, fecha, tema, notas=""):
        data = self._cargar_bookclub()
        nueva_reunion = {
            'id': len(data['reuniones']) + 1,
            'fecha': fecha,
            'tema': tema,
            'notas': notas,
            'libro': data['libro_actual']['titulo'] if data['libro_actual'] else "Sin libro",
            'fecha_creacion': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        data['reuniones'].append(nueva_reunion)
        self._guardar_bookclub(data)
        return True, "Reunión agregada"
    
    def agregar_miembro(self, nombre, email=""):
        data = self._cargar_bookclub()
        existe = any(m['nombre'].lower() == nombre.lower() for m in data['miembros'])
        if existe:
            return False, "Este miembro ya existe"
        
        nuevo_miembro = {
            'id': len(data['miembros']) + 1,
            'nombre': nombre,
            'email': email,
            'fecha_union': datetime.datetime.now().strftime("%Y-%m-%d")
        }
        data['miembros'].append(nuevo_miembro)
        self._guardar_bookclub(data)
        return True, f"Miembro {nombre} agregado"
    
    def agregar_discusion(self, pregunta, respuesta=""):
        data = self._cargar_bookclub()
        nueva_discusion = {
            'id': len(data['discusiones']) + 1,
            'pregunta': pregunta,
            'respuesta': respuesta,
            'libro': data['libro_actual']['titulo'] if data['libro_actual'] else "Sin libro",
            'fecha': datetime.datetime.now().strftime("%Y-%m-%d")
        }
        data['discusiones'].append(nueva_discusion)
        self._guardar_bookclub(data)
        return True, "Pregunta de discusión agregada"
    
    def ver_bookclub(self):
        return self._cargar_bookclub()
    
    def eliminar_reunion(self, reunion_id):
        data = self._cargar_bookclub()
        data['reuniones'] = [r for r in data['reuniones'] if r['id'] != reunion_id]
        self._guardar_bookclub(data)
        return True


class LocalFrasesHandler:
    def __init__(self):
        self.DATA_FOLDER = "data"
        self.FAVORITAS_FILE = os.path.join(self.DATA_FOLDER, "frases_favoritas.json")
        self.JOURNAL_FILE = os.path.join(self.DATA_FOLDER, "journal_gratitud.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
        
        self.OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        self.openai_client = None
        self.openai_enabled = False
        self._inicializar_openai()
        
        self.CATEGORIAS_FRASES = {
            "💪 Motivación": [
                "Confía en el proceso, incluso cuando no entiendas el camino.",
                "Eres más fuerte de lo que crees.",
                "Cada día es una nueva oportunidad para empezar de nuevo.",
            ],
            "💛 Amor Propio": [
                "Te mereces todo lo bonito que estás esperando.",
                "Eres suficiente, exactamente como eres.",
            ],
            "🌸 Paz": [
                "Lo que es para ti, encuentra su camino.",
                "Suelta lo que no puedes controlar y confía.",
            ],
        }

    def _inicializar_openai(self):
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)
            self.openai_enabled = True
        except:
            self.openai_enabled = False

    def _cargar_favoritas(self):
        if not os.path.exists(self.FAVORITAS_FILE): return []
        try:
            with open(self.FAVORITAS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []

    def _guardar_favoritas(self, favoritas):
        with open(self.FAVORITAS_FILE, "w", encoding="utf-8") as f:
            json.dump(favoritas, f, indent=2, ensure_ascii=False)

    def frase_del_dia(self):
        hoy = datetime.datetime.now().strftime("%Y-%m-%d")
        random.seed(hoy)
        categoria = random.choice(list(self.CATEGORIAS_FRASES.keys()))
        frase = random.choice(self.CATEGORIAS_FRASES[categoria])
        random.seed()
        return f"✨ *FRASE DEL DÍA* ✨\n_{hoy}_\n\n{categoria}\n\n_{frase}_"

    def agregar_favorita(self, frase):
        favoritas = self._cargar_favoritas()
        nueva = {
            "id": len(favoritas) + 1,
            "frase": frase,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        favoritas.append(nueva)
        self._guardar_favoritas(favoritas)
        return "⭐ Frase guardada en favoritas 💛"

    def ver_favoritas(self):
        favoritas = self._cargar_favoritas()
        if not favoritas: return "📭 No tienes frases favoritas guardadas aún 💛"
        texto = "⭐ *TUS FRASES FAVORITAS* ⭐\n\n"
        for fav in reversed(favoritas[-10:]):
            texto += f"**#{fav['id']}**\n_{fav['frase']}_\n\n"
        return texto


class GestorPersonalidades:
    PERSONALIDADES = {
        "bestie": "Habla como una mejor amiga amorosa, tierna, cercana, con emojis.",
        "formal": "Habla de forma clara, profesional y estructurada. No uses emojis.",
        "espiritual": "Habla como una guía espiritual. Usa un tono suave, canalizado.",
    }
    
    def __init__(self):
        self._personalidad_actual = "bestie"
    
    @property
    def personalidad_actual(self):
        return self._personalidad_actual
    
    @personalidad_actual.setter
    def personalidad_actual(self, nombre):
        nombre = nombre.lower().strip()
        if nombre in self.PERSONALIDADES:
            self._personalidad_actual = nombre
        else:
            raise ValueError(f"Personalidad '{nombre}' no existe")
    
    def obtener_instruccion(self):
        return self.PERSONALIDADES[self._personalidad_actual]


class RobustBibliaHandler:
    def __init__(self):
        self.BIBLIA_FILE = "data/es_rvr.json"
        self.FAVORITOS_FILE = "data/favoritos_biblia.json"
        self.JOURNAL_FILE = "data/journal_biblico.json"
        self.books = []
        self.valid_data = False
        os.makedirs("data", exist_ok=True)

        try:
            with open(self.BIBLIA_FILE, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            if isinstance(data, dict) and "books" in data:
                self.books = data["books"]
            elif isinstance(data, list):
                self.books = data
            self.books = [b for b in self.books if isinstance(b, dict)]
            if self.books:
                self.valid_data = True
        except Exception as e:
            st.error(f"❌ Error cargando la Biblia: {str(e)}")

    def _get_verse_text(self, capitulo, idx):
        try:
            if isinstance(capitulo, list):
                if 0 <= idx < len(capitulo):
                    return capitulo[idx]
            elif isinstance(capitulo, dict):
                verses = capitulo.get("verses", [])
                if 0 <= idx < len(verses):
                    v = verses[idx]
                    return v.get("text", str(v)) if isinstance(v, dict) else str(v)
        except Exception as e:
            print(f"Error extrayendo verso: {e}")
        return None

    def versiculo_del_dia(self):
        if not self.valid_data: return "⚠️ Datos no cargados."
        libro = random.choice(self.books)
        chapters = libro.get("chapters", [])
        if not chapters or not isinstance(chapters, list):
            return "⚠️ Libro sin capítulos."
        cap_idx = random.randint(0, len(chapters) - 1)
        capitulo = chapters[cap_idx]
        num_versiculos = 0
        if isinstance(capitulo, list):
            num_versiculos = len(capitulo)
        elif isinstance(capitulo, dict):
            num_versiculos = len(capitulo.get("verses", []))
        if num_versiculos == 0: return "⚠️ Capítulo vacío."
        ver_idx = random.randint(0, num_versiculos - 1)
        texto = self._get_verse_text(capitulo, ver_idx)
        if not texto: return "⚠️ Error al leer texto."
        return f"📖 **{libro.get('name')} {cap_idx + 1}:{ver_idx + 1}**\n\n_{texto}_"

    def buscar_versiculo_completo(self, ref):
        if not self.valid_data: return "❌ Datos no cargados."
        if ":" not in ref: return "⚠️ Formato inválido (Ej: Juan 3:16)"
        try:
            libro_input, resto = ref.rsplit(" ", 1)
            cap_num, ver_num = map(int, resto.split(":"))
        except:
            return "⚠️ Verifica los números del capítulo y versículo."
        libro_obj = next((l for l in self.books if l.get("name", "").lower() == libro_input.lower()), None)
        if not libro_obj: return f"❌ No encontré el libro '{libro_input}'"
        chapters = libro_obj.get("chapters", [])
        if cap_num < 1 or cap_num > len(chapters):
            return f"❌ {libro_input} solo tiene {len(chapters)} capítulos."
        capitulo = chapters[cap_num - 1]
        max_versos = 0
        if isinstance(capitulo, list):
            max_versos = len(capitulo)
        elif isinstance(capitulo, dict):
            max_versos = len(capitulo.get("verses", []))
        if ver_num < 1 or ver_num > max_versos:
            return f"❌ El capítulo {cap_num} solo tiene {max_versos} versículos."
        texto = self._get_verse_text(capitulo, ver_num - 1)
        if texto:
            return f"📖 **{libro_obj.get('name')} {cap_num}:{ver_num}**\n\n_{texto}_"
        return "❌ Error recuperando el texto."
    
    def _cargar_favoritos(self):
        if not os.path.exists(self.FAVORITOS_FILE): return []
        try:
            with open(self.FAVORITOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    
    def _guardar_favoritos(self, favoritos):
        with open(self.FAVORITOS_FILE, "w", encoding="utf-8") as f:
            json.dump(favoritos, f, indent=2, ensure_ascii=False)
    
    def agregar_favorito(self, referencia, texto):
        favoritos = self._cargar_favoritos()
        existe = any(f['referencia'].lower() == referencia.lower() for f in favoritos)
        if existe: return False, "Este versículo ya está en favoritos"
        nuevo = {
            "id": len(favoritos) + 1,
            "referencia": referencia,
            "texto": texto,
            "fecha_agregado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        favoritos.append(nuevo)
        self._guardar_favoritos(favoritos)
        return True, "✅ Versículo agregado a favoritos"
    
    def ver_favoritos(self):
        return self._cargar_favoritos()
    
    def eliminar_favorito(self, fav_id):
        favoritos = self._cargar_favoritos()
        favoritos = [f for f in favoritos if f['id'] != fav_id]
        self._guardar_favoritos(favoritos)
        return True
    
    def _cargar_journal(self):
        if not os.path.exists(self.JOURNAL_FILE): return []
        try:
            with open(self.JOURNAL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    
    def _guardar_journal(self, journal):
        with open(self.JOURNAL_FILE, "w", encoding="utf-8") as f:
            json.dump(journal, f, indent=2, ensure_ascii=False)
    
    def ver_journal_biblico(self):
        journal = self._cargar_journal()
        if not journal: return "📭 Aún no tienes entradas en tu journal bíblico"
        texto = "📖 **TU JOURNAL BÍBLICO** 📖\n\n"
        for entrada in reversed(journal[-10:]):
            texto += f"**{entrada['fecha']}**\n"
            texto += f"📖 {entrada['referencia']}\n"
            texto += f"_{entrada['reflexion']}_\n\n"
        texto += f"💛 Total de entradas: {len(journal)}"
        return texto
    
    def generar_devocional_personalizado(self, situacion):
        versiculo = self.versiculo_del_dia()
        respuesta = f"""
🙏 **DEVOCIONAL PERSONALIZADO** 🙏

**Tu situación:**
_{situacion}_

━━━━━━━━━━━━━━━━━━━━━

{versiculo}

━━━━━━━━━━━━━━━━━━━━━

💫 **Reflexión:**

Este versículo te recuerda que Dios está contigo en cada situación.

💛 La Palabra de Dios es lámpara a tus pies y luz a tu camino.
"""
        journal = self._cargar_journal()
        entrada = {
            "id": len(journal) + 1,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "referencia": versiculo.split("\n")[0],
            "reflexion": situacion,
            "versiculo_completo": versiculo
        }
        journal.append(entrada)
        self._guardar_journal(journal)
        return respuesta


class TarotHandler:
    def __init__(self, openai_api_key):
        self.OPENAI_API_KEY = openai_api_key
        self.MAZO_TAROT = {
            "El Loco": {"derecha": "nuevos comienzos, espontaneidad", "invertida": "imprudencia, caos"},
            "El Mago": {"derecha": "manifestación, enfoque", "invertida": "manipulación"},
        }
    
    def _seleccionar_carta(self):
        carta_nombre = random.choice(list(self.MAZO_TAROT.keys()))
        invertida = random.choice([True, False])
        carta_info = self.MAZO_TAROT[carta_nombre]
        significado = carta_info["invertida"] if invertida else carta_info["derecha"]
        return {"nombre": carta_nombre, "invertida": invertida, "significado": significado}
    
    def energia_del_dia(self):
        carta = self._seleccionar_carta()
        return f"✨ **ENERGÍA DEL DÍA**\n\n🃏 **{carta['nombre']}** {'(Invertida)' if carta['invertida'] else ''}\n\n_{carta['significado']}_"


class AstrologiaHandler:
    def __init__(self):
        self.SIGNOS_ZODIACALES = {
            "aries": {"fechas": "21 marzo - 19 abril", "elemento": "Fuego", "simbolo": "♈ El Carnero"},
        }
    
    def horoscopo_del_dia(self, signo):
        signo = signo.lower().strip()
        if signo not in self.SIGNOS_ZODIACALES:
            return "❌ Signo no válido"
        info = self.SIGNOS_ZODIACALES[signo]
        return f"🌟 **HORÓSCOPO**\n\n**{signo.upper()}** {info['simbolo']}\n{info['fechas']}"


class NumerologiaHandler:
    def __init__(self):
        self.NUMEROS_BASE = {
            1: {"nombre": "El Líder", "energia": "Independencia, iniciativa"},
        }
    
    def numerologia_del_dia(self):
        hoy = datetime.datetime.now()
        suma = (hoy.day + hoy.month + hoy.year) % 9 + 1
        info = self.NUMEROS_BASE.get(suma, {"nombre": "Especial", "energia": "Energía única"})
        return f"🔢✨ **NUMEROLOGÍA DEL DÍA**\n\n**Número:** {suma} - *{info['nombre']}*\n\n{info['energia']}"


class IdeasHandler:
    def __init__(self, openai_api_key):
        self.OPENAI_API_KEY = openai_api_key
        self.DATA_FOLDER = "data"
        self.PROYECTOS_FILE = os.path.join(self.DATA_FOLDER, "proyectos_ideas.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
    
    def _cargar_proyectos(self):
        if not os.path.exists(self.PROYECTOS_FILE): return []
        try:
            with open(self.PROYECTOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    
    def listar_proyectos(self):
        return self._cargar_proyectos()


class ProfesionalHandler:
    def __init__(self, openai_api_key):
        self.OPENAI_API_KEY = openai_api_key
        self.PREGUNTAS_COMUNES = [
            "Cuéntame sobre ti",
            "¿Por qué quieres trabajar aquí?",
        ]
    
    def obtener_pregunta_entrevista(self):
        pregunta = random.choice(self.PREGUNTAS_COMUNES)
        return f"💬 **PREGUNTA DE PRÁCTICA**\n\n_{pregunta}_"


# =====================================================
# 5. INICIALIZACIÓN DE HANDLERS
# =====================================================
@st.cache_resource(ttl=300)
def get_handlers():
    fin = LocalFinanzasHandler()
    not_h = LocalNotasHandler()
    lib = LocalLibrosHandler()
    fra = LocalFrasesHandler()
    pers = GestorPersonalidades()
    bib = RobustBibliaHandler()
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    tarot = TarotHandler(OPENAI_API_KEY)
    astro = AstrologiaHandler()
    nume = NumerologiaHandler()
    ideas = IdeasHandler(OPENAI_API_KEY)
    profesional = ProfesionalHandler(OPENAI_API_KEY)
    return fin, not_h, lib, fra, pers, bib, ideas, tarot, astro, nume, profesional

finanzas_handler, notas_handler, libros_handler, frases_handler, personalidades_handler, biblia_handler, ideas_handler, tarot, astrologia, numerologia, profesional_handler = get_handlers()
biblia = biblia_handler


# =====================================================
# FUNCIONES DE UTILIDAD
# =====================================================
def crear_backup_datos():
    import zipfile
    from io import BytesIO
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_backup = f"portal_backup_{timestamp}.zip"
    zip_buffer = BytesIO()
    try:
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            data_folder = "data"
            if os.path.exists(data_folder):
                for archivo in os.listdir(data_folder):
                    if archivo.endswith('.json'):
                        ruta_completa = os.path.join(data_folder, archivo)
                        zip_file.write(ruta_completa, archivo)
        zip_buffer.seek(0)
        return zip_buffer, nombre_backup, True
    except Exception as e:
        return None, str(e), False


# =====================================================
# 6. NAVEGACIÓN PRINCIPAL
# =====================================================
CONTRASENA = "portal1058*"
st.markdown('<div class="top-banner">✨ Tu refugio de magia, intuición y energía ✨</div>', unsafe_allow_html=True)

if not st.session_state.login:
    st.markdown("<div class='title-glow'>Bienvenida<br>al Portal</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2: password = st.text_input("Clave", type="password", label_visibility="collapsed", placeholder="🔑 Clave sagrada...")
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3.5, 2, 3.5])
    with c2:
        if st.button("✨ Entrar al Reino", key="btn_login", use_container_width=True):
            if password == CONTRASENA: 
                st.session_state.login = True
                st.rerun()
            elif password: 
                st.error("❌ Clave incorrecta")
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

else:
    # SPOTIFY FLOTANTE
    st.markdown("""
        <div class="spotify-bottom-fixed">
            <iframe 
                style="border-radius:12px" 
                src="https://open.spotify.com/embed/playlist/37i9dQZF1DXcNb6Ba0LuVc?utm_source=generator&theme=0" 
                width="100%" 
                height="152" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy">
            </iframe>
        </div>
    """, unsafe_allow_html=True)
    
    def mostrar_breadcrumbs():
        view = st.session_state.current_view
        if view == "menu": return
        st.caption(f"🏠 Inicio → {view.title()}")
        st.markdown("<br>", unsafe_allow_html=True)
    
    # --- MENÚ PRINCIPAL ---
    if st.session_state.current_view == "menu":
        st.markdown("<div class='title-glow'>💜 Acceso Concedido</div>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle-text'>Bienvenida, Sacerdotisa.</p>", unsafe_allow_html=True)
        opciones = [("🌙", "Lo Oculto", "lo_oculto", "oculto-icon"), ("💡", "Ideas", "ideas", "ideas-icon"), 
                    ("📖", "Biblia", "biblia", "biblia-icon"), ("💰", "Finanzas", "finanzas", "finanzas-icon"), 
                    ("📝", "Notas", "notas", "notas-icon"), ("📚", "Libros", "libros", "libros-icon"),
                    ("💬", "Frases", "frases", "frases-icon"), ("👤", "Personas", "personalidades", "personalidades-icon"), 
                    ("💼", "Pro", "profesional", "profesional-icon")]
        rows = [opciones[i:i+3] for i in range(0, len(opciones), 3)]
        for row in rows:
            cols = st.columns(3, gap="small")
            for idx, (icon, label, key, css) in enumerate(row):
                with cols[idx]:
                    st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                    if st.button(f"Abrir {label}", key=f"btn_menu_{key}", use_container_width=True):
                        st.session_state.current_view = key
                        st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("💾 Crear Backup", key="btn_backup", use_container_width=True):
                zip_buffer, nombre, exito = crear_backup_datos()
                if exito:
                    st.download_button(
                        label="📥 Descargar Backup",
                        data=zip_buffer,
                        file_name=nombre,
                        mime="application/zip",
                        use_container_width=True,
                        key="btn_download_backup"
                    )
                    st.success("✅ Backup creado correctamente")
                else:
                    st.error(f"❌ Error al crear backup: {nombre}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("🚪 Cerrar Sesión", key="btn_logout", use_container_width=True):
                st.session_state.login = False
                st.session_state.current_view = "menu"
                st.rerun()

    # --- MÓDULO BIBLIA ---
    elif st.session_state.current_view == "biblia":
        mostrar_breadcrumbs()
        st.markdown("<div class='title-glow'>📖 Biblia</div>", unsafe_allow_html=True)
        
        if st.session_state.biblia_subview == "menu":
            st.markdown("<p class='subtitle-text'>Tu refugio de luz y palabra sagrada.</p>", unsafe_allow_html=True)
            opciones_biblia = [
                ("🌅", "Versículo del Día", "vdia", "biblia-icon"),
                ("🔍", "Buscar Versículo", "buscar", "libros-icon"),
                ("📿", "Devocional", "devocional", "frases-icon"),
                ("📔", "Mi Diario", "journal", "notas-icon"),
                ("⭐", "Favoritos", "favoritos", "tarot-icon")
            ]
            rows_biblia = [opciones_biblia[i:i+3] for i in range(0, len(opciones_biblia), 3)]
            for row in rows_biblia:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    with cols[idx]:
                        st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                        if st.button(f"Abrir {label}", key=f"btn_biblia_{sub_key}", use_container_width=True):
                            st.session_state.biblia_subview = sub_key
                            st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏠 Menú Principal", key="btn_biblia_home", use_container_width=True):
                st.session_state.current_view = "menu"
                st.rerun()
        
        elif st.session_state.biblia_subview == "vdia":
            st.markdown("### 🌅 Versículo del Día")
            resultado = biblia.versiculo_del_dia()
            st.markdown(f'<div class="result-card">{resultado}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_biblia_volver_vdia"):
                st.session_state.biblia_subview = "menu"
                st.rerun()
        
        elif st.session_state.biblia_subview == "buscar":
            st.markdown("### 🔍 Buscar Versículo")
            referencia = st.text_input("Escribe la referencia:", placeholder="Ej: Juan 3:16", key="input_biblia_ref")
            if st.button("📖 Buscar", use_container_width=True, key="btn_buscar_versiculo"):
                if referencia:
                    resultado = biblia.buscar_versiculo_completo(referencia)
                    st.markdown(f'<div class="result-card">{resultado}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Escribe una referencia primero")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_biblia_volver_buscar"):
                st.session_state.biblia_subview = "menu"
                st.rerun()
        
        else:
            st.info("✨ Módulo en desarrollo")
            if st.button("🔙 Volver", key="btn_biblia_volver_default"):
                st.session_state.biblia_subview = "menu"
                st.rerun()

    # --- RESTO DE MÓDULOS (placeholder simple) ---
    else:
        mostrar_breadcrumbs()
        st.markdown(f"<div class='title-glow'>{st.session_state.current_view.title()}</div>", unsafe_allow_html=True)
        st.info(f"✨ Módulo {st.session_state.current_view} funcionando correctamente")
        if st.button("🔙 Menú Principal", key="btn_default_home"): 
            st.session_state.current_view = "menu"
            st.rerun()

st.markdown('<div class="bottom-footer">🌙 Que la luz de tu intuición te guíe en este viaje sagrado 🌙</div>', unsafe_allow_html=True)

