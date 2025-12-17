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
    
    /* SPOTIFY: Sin animaciones complejas, opacidad fija */
    .spotify-container { 
        position: fixed; 
        bottom: 50px; 
        left: 50%; 
        transform: translateX(-50%); 
        z-index: 995; 
        border-radius: 12px; 
        overflow: hidden; 
        box-shadow: 0 4px 20px rgba(147, 51, 234, 0.5); 
        width: 300px; 
        opacity: 0.9; 
        transition: all 0.3s ease;
    }
    .spotify-container iframe { 
        pointer-events: all !important; 
        border: none; 
        display: block; 
    }
    .spotify-container:hover { 
        transform: translateX(-50%) translateY(-5px); 
        box-shadow: 0 6px 30px rgba(147, 51, 234, 0.7); 
        opacity: 1; 
    }
    
    @media (max-width: 768px) { 
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
        """Exporta todos los datos financieros a CSV"""
        import csv
        from io import StringIO
        
        data = self._cargar_finanzas()
        
        # Crear CSV en memoria
        output = StringIO()
        
        # Exportar gastos
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
        
        writer.writerow([])  # Línea en blanco
        
        # Exportar ingresos
        writer.writerow(['INGRESOS'])
        writer.writerow(['ID', 'Monto', 'Fuente', 'Fecha'])
        
        for ingreso in data.get('ingresos', []):
            writer.writerow([
                ingreso.get('id', ''),
                ingreso.get('monto', ''),
                ingreso.get('fuente', ''),
                ingreso.get('fecha', '')
            ])
        
        writer.writerow([])  # Línea en blanco
        
        # Exportar presupuestos
        writer.writerow(['PRESUPUESTOS'])
        writer.writerow(['Categoría', 'Presupuesto'])
        
        for categoria, presupuesto in data.get('presupuestos', {}).items():
            writer.writerow([categoria, presupuesto])
        
        csv_string = output.getvalue()
        output.close()
        
        return csv_string
    
    def estadisticas_avanzadas(self):
        """Genera estadísticas avanzadas de finanzas"""
        data = self._cargar_finanzas()
        
        if not data.get('gastos'):
            return None
        
        # Fecha actual
        hoy = datetime.datetime.now()
        mes_actual = hoy.strftime("%Y-%m")
        dia_actual = hoy.day
        
        # Gastos del mes actual
        gastos_mes = [g for g in data['gastos'] if g['fecha'].startswith(mes_actual)]
        
        if not gastos_mes:
            return None
        
        # Total gastado este mes
        total_mes = sum(g['monto'] for g in gastos_mes)
        
        # Promedio diario (basado en días transcurridos)
        promedio_diario = total_mes / dia_actual if dia_actual > 0 else 0
        
        # Proyección del mes (promedio diario × días del mes)
        dias_mes = 30  # Aproximado
        proyeccion_mes = promedio_diario * dias_mes
        
        # Gastos por categoría este mes
        gastos_por_cat = {}
        for g in gastos_mes:
            cat = g.get('categoria', '📄 otros')
            gastos_por_cat[cat] = gastos_por_cat.get(cat, 0) + g['monto']
        
        # Top 3 categorías
        top_categorias = sorted(gastos_por_cat.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Comparación con mes anterior
        primer_dia = hoy.replace(day=1)
        mes_anterior = (primer_dia - timedelta(days=1)).strftime("%Y-%m")
        gastos_mes_ant = [g for g in data['gastos'] if g['fecha'].startswith(mes_anterior)]
        total_mes_anterior = sum(g['monto'] for g in gastos_mes_ant)
        
        # Calcular diferencia y porcentaje
        diferencia = total_mes - total_mes_anterior
        porcentaje_cambio = (diferencia / total_mes_anterior * 100) if total_mes_anterior > 0 else 0
        
        # Ingresos del mes
        ingresos_mes = sum(i['monto'] for i in data.get('ingresos', []) if i['fecha'].startswith(mes_actual))
        
        # Balance (ingresos - gastos)
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
        """Busca notas que contengan la palabra clave"""
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
        """Inicializa archivo de libros guardados"""
        self.DATA_FOLDER = "data"
        self.LIBROS_FILE = os.path.join(self.DATA_FOLDER, "libros_guardados.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
    
    def _cargar_libros(self):
        """Carga libros guardados"""
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
        """Guarda libros"""
        if not hasattr(self, 'LIBROS_FILE'):
            self.__init_libros_data()
        with open(self.LIBROS_FILE, "w", encoding="utf-8") as f:
            json.dump(libros, f, indent=2, ensure_ascii=False)
    
    def agregar_resena(self, libro_titulo, rating, texto_resena):
        """Agrega reseña y rating a un libro"""
        if not hasattr(self, 'LIBROS_FILE'):
            self.__init_libros_data()
        
        libros = self._cargar_libros()
        
        # Buscar si el libro ya existe
        libro_existente = next((l for l in libros if l['titulo'].lower() == libro_titulo.lower()), None)
        
        if libro_existente:
            # Actualizar reseña
            libro_existente['rating'] = rating
            libro_existente['resena'] = texto_resena
            libro_existente['fecha_resena'] = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            # Crear nuevo libro
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
        """Ver todos los libros con reseñas"""
        if not hasattr(self, 'LIBROS_FILE'):
            self.__init_libros_data()
        return self._cargar_libros()
    
    def eliminar_resena(self, libro_id):
        """Elimina una reseña"""
        if not hasattr(self, 'LIBROS_FILE'):
            self.__init_libros_data()
        libros = self._cargar_libros()
        libros = [l for l in libros if l['id'] != libro_id]
        self._guardar_libros(libros)
        return True
    
    # === BOOK CLUB FUNCTIONS ===
    
    def __init_bookclub_data(self):
        """Inicializa archivo de book club"""
        self.DATA_FOLDER = "data"
        self.BOOKCLUB_FILE = os.path.join(self.DATA_FOLDER, "book_club.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
    
    def _cargar_bookclub(self):
        """Carga datos del book club"""
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
        """Guarda datos del book club"""
        if not hasattr(self, 'BOOKCLUB_FILE'):
            self.__init_bookclub_data()
        with open(self.BOOKCLUB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def establecer_libro_actual(self, titulo, autor=""):
        """Establece el libro actual del club"""
        data = self._cargar_bookclub()
        data['libro_actual'] = {
            'titulo': titulo,
            'autor': autor,
            'fecha_inicio': datetime.datetime.now().strftime("%Y-%m-%d")
        }
        self._guardar_bookclub(data)
        return True, f"Libro actual: {titulo}"
    
    def agregar_reunion(self, fecha, tema, notas=""):
        """Agrega una reunión del book club"""
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
        """Agrega un miembro al book club"""
        data = self._cargar_bookclub()
        
        # Verificar si ya existe
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
        """Agrega una pregunta/tema de discusión"""
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
        """Ver información completa del book club"""
        return self._cargar_bookclub()
    
    def eliminar_reunion(self, reunion_id):
        """Elimina una reunión"""
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
                "No estás atrasada, estás justo donde tienes que estar.",
                "Estás aprendiendo, creciendo y sanando. Eso es progreso.",
                "Tu esfuerzo nunca es en vano, aunque aún no veas los resultados.",
            ],
            "💛 Amor Propio": [
                "Te mereces todo lo bonito que estás esperando.",
                "Eres suficiente, exactamente como eres.",
                "Tu valor no disminuye por la incapacidad de alguien de verlo.",
                "Mereces amor, respeto y gentileza, especialmente de ti misma.",
                "No tienes que probarte ante nadie. Eres valiosa por existir.",
            ],
            "🌸 Paz": [
                "Lo que es para ti, encuentra su camino.",
                "Suelta lo que no puedes controlar y confía.",
                "La paz comienza cuando las expectativas terminan.",
                "Está bien no tener todo resuelto ahora mismo.",
                "Respira. Estás a salvo. Todo está bien en este momento.",
            ],
            "✨ Abundancia": [
                "Tu energía atrae. Vibra bonito.",
                "Yo merezco abundancia, paz y amor.",
                "Estoy abierta a recibir todas las bendiciones que el universo tiene para mí.",
                "La abundancia fluye hacia mí desde todas las direcciones.",
                "Hay suficiente para todos, incluyéndome a mí.",
            ],
            "🎯 Productividad": [
                "Hoy elijo enfocarme en lo que sí puedo hacer.",
                "Progreso sobre perfección, siempre.",
                "Cada pequeño paso cuenta. Sigue avanzando.",
                "Tengo todo lo que necesito para lograr mis metas.",
                "Mi disciplina de hoy crea mi libertad de mañana.",
            ],
            "💔 Sanación": [
                "Sanar no es lineal. Está bien tener días difíciles.",
                "Tu dolor es válido y mereces tiempo para procesarlo.",
                "Estás sanando aunque no se sienta así hoy.",
                "No tienes que estar bien todo el tiempo. Date permiso de sentir.",
                "De esta también sales, como de todo lo anterior.",
            ],
            "🦋 Transformación": [
                "Estoy en proceso de convertirme en mi mejor versión.",
                "Los finales son solo nuevos comienzos disfrazados.",
                "Me permito crecer, cambiar y evolucionar.",
                "Confío en los cambios que estoy atravesando.",
                "Todo lo que necesito ya está dentro de mí.",
            ],
            "🌟 Espiritualidad": [
                "Estoy exactamente donde debo estar.",
                "Mi energía crea mi realidad.",
                "Hoy elijo confiar.",
                "Mi corazón se abre a nuevas bendiciones.",
                "Estoy conectada con algo más grande que yo.",
            ]
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

    def _cargar_journal(self):
        if not os.path.exists(self.JOURNAL_FILE): return []
        try:
            with open(self.JOURNAL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []

    def _guardar_journal(self, journal):
        with open(self.JOURNAL_FILE, "w", encoding="utf-8") as f:
            json.dump(journal, f, indent=2, ensure_ascii=False)

    def frase_por_categoria(self, categoria):
        if categoria in self.CATEGORIAS_FRASES:
            return random.choice(self.CATEGORIAS_FRASES[categoria])
        return "✨ Categoría no encontrada"

    def listar_categorias(self):
        texto = "📚 *CATEGORÍAS DISPONIBLES* 📚\n\n"
        for cat in self.CATEGORIAS_FRASES.keys():
            texto += f"{cat}\n"
        return texto

    def frase_del_dia(self):
        hoy = datetime.datetime.now().strftime("%Y-%m-%d")
        random.seed(hoy)
        categoria = random.choice(list(self.CATEGORIAS_FRASES.keys()))
        frase = random.choice(self.CATEGORIAS_FRASES[categoria])
        random.seed()
        return f"✨ *FRASE DEL DÍA* ✨\n_{hoy}_\n\n{categoria}\n\n_{frase}_"

    def generar_frase_personalizada(self, mood="", situacion="", personalidad_handler=None):
        if not self.openai_enabled:
            return "❌ OpenAI no está configurado"
        contexto = ""
        if mood: contexto += f"La persona se siente: {mood}. "
        if situacion: contexto += f"Situación actual: {situacion}."
        if not contexto: contexto = "La persona necesita motivación general."
        
        prompt = f"""Genera una frase motivacional personalizada, profunda y hermosa.

Contexto: {contexto}

La frase debe:
- Ser específica a su situación
- Validar sus emociones
- Dar esperanza y fortaleza
- Ser genuina, no cliché
- Máximo 2-3 oraciones
- Tono cálido, empático, como una mejor amiga

No uses comillas. Solo la frase."""

        instruccion_personalidad = personalidad_handler.obtener_instruccion() if personalidad_handler else ""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"Eres una coach espiritual y motivacional experta. Generas frases profundas, personalizadas y transformadoras. {instruccion_personalidad}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.9
            )
            frase = response.choices[0].message.content.strip()
            return f"✨ *FRASE PARA TI* ✨\n\n_{frase}_\n\n💛"
        except:
            return "❌ Error al generar la frase. Intenta de nuevo 💛"

    def generar_afirmaciones_personalizadas(self, area, cantidad=5, personalidad_handler=None):
        if not self.openai_enabled:
            return "❌ OpenAI no está configurado"
        
        prompt = f"""Genera {cantidad} afirmaciones positivas personalizadas para el área de: {area}

Las afirmaciones deben:
- Estar en primera persona ("Yo soy", "Yo merezco", etc.)
- Ser específicas al área mencionada
- Ser poderosas y transformadoras
- Ser variadas entre sí
- Ser cortas (1 frase cada una)

Formato: Solo las afirmaciones numeradas, sin explicaciones."""

        instruccion_personalidad = personalidad_handler.obtener_instruccion() if personalidad_handler else ""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"Eres experta en crear afirmaciones positivas poderosas y transformadoras. {instruccion_personalidad}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.8
            )
            afirmaciones = response.choices[0].message.content.strip()
            return f"🎯 *AFIRMACIONES PARA: {area.upper()}* 🎯\n\n{afirmaciones}\n\n💛 _Repite la que más resuene contigo_"
        except:
            return "❌ Error al generar afirmaciones. Intenta de nuevo 💛"

    def procesar_gratitud_con_ia(self, gratitud, personalidad_handler=None):
        if not self.openai_enabled:
            return "Qué hermoso que reconozcas esas bendiciones 💛 La gratitud transforma todo."
        
        prompt = f"""La persona escribió en su journal de gratitud:

"{gratitud}"

Responde de forma:
- Validadora y empática
- Profundizando en la gratitud
- Haciendo 1-2 preguntas reflexivas
- Tono cálido, como mejor amiga
- Máximo 100 palabras
- Incluye 1-2 emojis relevantes"""

        instruccion_personalidad = personalidad_handler.obtener_instruccion() if personalidad_handler else ""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"Eres una coach de gratitud y bienestar emocional. Respondes con calidez, validación y preguntas reflexivas que profundizan la gratitud. {instruccion_personalidad}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except:
            return "Qué hermoso que reconozcas esas bendiciones 💛 La gratitud transforma todo."

    def agregar_entrada_journal(self, gratitud, personalidad_handler=None):
        journal = self._cargar_journal()
        respuesta_ia = self.procesar_gratitud_con_ia(gratitud, personalidad_handler)
        entrada = {
            "id": len(journal) + 1,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "gratitud": gratitud,
            "respuesta_ia": respuesta_ia
        }
        journal.append(entrada)
        self._guardar_journal(journal)
        return f"📖 *JOURNAL DE GRATITUD* 📖\n\n_{gratitud}_\n\n💬 {respuesta_ia}\n\n✅ Guardado en tu journal 💛"

    def ver_journal(self, filtro="todos"):
        journal = self._cargar_journal()
        if not journal: return "📭 Aún no tienes entradas en tu journal de gratitud 💛"
        
        if filtro == "hoy":
            hoy = datetime.datetime.now().strftime("%Y-%m-%d")
            journal = [e for e in journal if e["fecha"].startswith(hoy)]
        elif filtro == "semana":
            hace_semana = (datetime.datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            journal = [e for e in journal if e["fecha"] >= hace_semana]
        elif filtro == "mes":
            mes_actual = datetime.datetime.now().strftime("%Y-%m")
            journal = [e for e in journal if e["fecha"].startswith(mes_actual)]
        
        if not journal: return f"📭 No hay entradas en: {filtro}"
        ultimas = journal[-5:]
        texto = f"📖 *JOURNAL DE GRATITUD*\n"
        if filtro != "todos": texto += f"({filtro})\n"
        texto += "\n"
        for entrada in reversed(ultimas):
            texto += f"**{entrada['fecha']}**\n_{entrada['gratitud']}_\n\n"
        texto += f"💛 Total de entradas: {len(journal)}"
        return texto

    def estadisticas_journal(self):
        journal = self._cargar_journal()
        if not journal: return "📭 Aún no tienes entradas en tu journal"
        total = len(journal)
        meses = {}
        for entrada in journal:
            mes = entrada["fecha"][:7]
            meses[mes] = meses.get(mes, 0) + 1
        mes_top = max(meses.items(), key=lambda x: x[1]) if meses else ("N/A", 0)
        primera = journal[0]["fecha"][:10]
        ultima = journal[-1]["fecha"][:10]
        texto = "📊 *ESTADÍSTICAS DE GRATITUD* 📊\n\n"
        texto += f"📖 Total de entradas: {total}\n"
        texto += f"📅 Primera entrada: {primera}\n"
        texto += f"📅 Última entrada: {ultima}\n"
        texto += f"🏆 Mes con más entradas: {mes_top[0]} ({mes_top[1]})\n"
        texto += f"\n💛 La gratitud transforma vidas"
        return texto

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

    def favorita_aleatoria(self):
        favoritas = self._cargar_favoritas()
        if not favoritas: return "📭 No tienes frases favoritas guardadas aún 💛"
        fav = random.choice(favoritas)
        return f"⭐ *TU FRASE FAVORITA* ⭐\n\n_{fav['frase']}_"

    def borrar_favorita(self, fav_id):
        favoritas = self._cargar_favoritas()
        fav = next((f for f in favoritas if f["id"] == int(fav_id)), None)
        if not fav: return f"❌ No encontré la frase #{fav_id}"
        favoritas = [f for f in favoritas if f["id"] != int(fav_id)]
        self._guardar_favoritas(favoritas)
        return f"🗑️ Frase #{fav_id} eliminada"

class GestorPersonalidades:
    PERSONALIDADES = {
        "bestie": (
            "Habla como una mejor amiga amorosa, tierna, cercana, con emojis, "
            "validando emociones y usando frases como 'mi amor', 'bebé', "
            "'mi cielo', 'bestie', 'mi vida'. Sé cálida y suave."
        ),
        "formal": (
            "Habla de forma clara, profesional y estructurada. "
            "No uses emojis. No uses diminutivos. Tono serio y respetuoso."
        ),
        "espiritual": (
            "Habla como una guía espiritual. Usa un tono suave, canalizado, "
            "con mensajes profundos, intuitivos y de luz. "
            "Incluye energía, señales y sabiduría interior."
        ),
        "psicologa": (
            "Habla como una psicóloga empática. "
            "Valida emociones, explica procesos con suavidad, ofrece claridad emocional, "
            "no juzga y no da órdenes. No uses emojis."
        ),
        "honesta": (
            "Habla de forma directa, sincera y sin adornos. "
            "No hieras, pero tampoco suavices demasiado. "
            "Sé práctica, concreta y muy clara."
        ),
        "tecnico": (
            "Habla como una experta en tecnología/análisis de datos. "
            "Explica conceptos complejos con claridad, usa ejemplos técnicos y precisos. "
            "No uses emojis."
        )
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
    
    def listar_personalidades(self):
        return list(self.PERSONALIDADES.keys())
    
    def existe_personalidad(self, nombre):
        return nombre.lower().strip() in self.PERSONALIDADES
    
    def cambiar_personalidad(self, nombre):
        try:
            self.personalidad_actual = nombre
            return f"✨ Personalidad cambiada a *{nombre}*."
        except ValueError:
            disponibles = ", ".join(self.listar_personalidades())
            return f"Personalidad desconocida. Las disponibles son: {disponibles}"
    
    def obtener_personalidad_actual(self):
        return self._personalidad_actual
    
    def texto_menu_personalidades(self):
        return (
            "😎 *Modos disponibles:*\n\n"
            "• Bestie (cálida y amorosa)\n"
            "• Formal (profesional)\n"
            "• Espiritual (guía intuitiva)\n"
            "• Psicóloga (empática y validante)\n"
            "• Honesta (directa y clara)\n"
            "• Técnico (experta en tech)\n\n"
            "💛 La personalidad afecta cómo responden las funciones de IA"
        )
    
    def obtener_descripcion_personalidad(self, nombre):
        nombre = nombre.lower().strip()
        if nombre in self.PERSONALIDADES:
            return self.PERSONALIDADES[nombre]
        return "Personalidad no encontrada."

class RobustBibliaHandler:
    VERSICULOS_DB = {
        "juan 3:16": "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree, no se pierda, mas tenga vida eterna.",
        "salmos 23:1": "Jehová es mi pastor; nada me faltará.",
        "filipenses 4:13": "Todo lo puedo en Cristo que me fortalece.",
        "proverbios 3:5-6": "Confía en Jehová con todo tu corazón, y no te apoyes en tu propia prudencia. Reconócelo en todos tus caminos, y él enderezará tus veredas.",
        "isaías 40:31": "Pero los que esperan en Jehová tendrán nuevas fuerzas; levantarán alas como las águilas; correrán, y no se cansarán; caminarán, y no se fatigarán.",
        "mateo 11:28": "Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar.",
        "romanos 8:28": "Y sabemos que a los que aman a Dios, todas las cosas les ayudan a bien.",
        "josué 1:9": "Mira que te mando que te esfuerces y seas valiente; no temas ni desmayes, porque Jehová tu Dios estará contigo en dondequiera que vayas.",
        "salmos 46:1": "Dios es nuestro amparo y fortaleza, nuestro pronto auxilio en las tribulaciones.",
        "juan 14:27": "La paz os dejo, mi paz os doy; yo no os la doy como el mundo la da. No se turbe vuestro corazón, ni tenga miedo."
    }
    VERSICULOS_POOL_DIARIO = list(VERSICULOS_DB.keys())
    
    def __init__(self):
        self.DATA_FOLDER = "data"
        self.FAVORITOS_FILE = os.path.join(self.DATA_FOLDER, "versiculos_favoritos.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
        
        # Inicializar OpenAI
        self.OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        self.openai_client = None
        self.openai_enabled = False
        self._inicializar_openai()
    
    def _inicializar_openai(self):
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)
            self.openai_enabled = True
        except:
            self.openai_enabled = False
    
    def _enriquecer_versiculo(self, referencia, texto):
        """Enriquece cualquier versículo con reflexión, aplicación y oración usando IA"""
        if not self.openai_enabled:
            return f"""**📖 {referencia}**

"{texto}"

---

💡 La IA no está disponible para enriquecer este versículo, pero medita en estas palabras sagradas.
"""
        
        prompt = f"""Eres una guía espiritual cristiana profunda y compasiva. 

Versículo: {referencia}
Texto: "{texto}"

Genera un devocional enriquecido con:

1. REFLEXIÓN (100-150 palabras):
   - Contexto bíblico e histórico
   - Significado profundo
   - Por qué es relevante hoy
   
2. APLICACIÓN PRÁCTICA (80-100 palabras):
   - Cómo aplicarlo hoy
   - Preguntas reflexivas (1-2)
   - Conexión con la vida diaria
   
3. ORACIÓN (50-70 palabras):
   - Personal y sincera
   - Relacionada directamente con el versículo
   - Que invite a la acción

Formato:
REFLEXION: [texto]
APLICACION: [texto]
ORACION: [texto]

Tono: Cálido, profundo, esperanzador, sin ser religioso en exceso.
"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres una guía espiritual cristiana que crea devocionales profundos, prácticos y transformadores."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.8
            )
            
            contenido = response.choices[0].message.content.strip()
            
            # Parsear respuesta
            partes = {}
            if "REFLEXION:" in contenido:
                partes['reflexion'] = contenido.split("REFLEXION:")[1].split("APLICACION:")[0].strip()
            if "APLICACION:" in contenido:
                partes['aplicacion'] = contenido.split("APLICACION:")[1].split("ORACION:")[0].strip()
            if "ORACION:" in contenido:
                partes['oracion'] = contenido.split("ORACION:")[1].strip()
            
            resultado = f"""**🌅 VERSÍCULO**

📖 **{referencia}**

---

**"{texto}"**

---

**💡 REFLEXIÓN:**

{partes.get('reflexion', 'Medita en este versículo y permite que Dios hable a tu corazón.')}

---

**🎯 APLICACIÓN HOY:**

{partes.get('aplicacion', '¿Cómo puedes vivir este versículo hoy? Reflexiona en oración.')}

---

**✨ ORACIÓN:**

_{partes.get('oracion', 'Señor, ayúdame a vivir tu palabra hoy. Amén.')}_
"""
            return resultado
            
        except Exception as e:
            return f"""**📖 {referencia}**

"{texto}"

---

💡 **REFLEXIÓN:** Medita en este versículo. Dios tiene un mensaje especial para ti en estas palabras.

**🎯 APLICACIÓN:** ¿Cómo puedes aplicar esta verdad en tu vida hoy?

**✨ ORACIÓN:** _Señor, abre mi corazón a tu palabra. Amén._
"""
    
    def _cargar_favoritos(self):
        if not os.path.exists(self.FAVORITOS_FILE):
            return []
        try:
            with open(self.FAVORITOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def _guardar_favoritos(self, favoritos):
        with open(self.FAVORITOS_FILE, "w", encoding="utf-8") as f:
            json.dump(favoritos, f, indent=2, ensure_ascii=False)
    
    def versiculo_del_dia(self):
        hoy = datetime.date.today().isoformat()
        if st.session_state.get("biblia_vdia_date") == hoy and st.session_state.get("biblia_vdia_stored"):
            return st.session_state["biblia_vdia_stored"]
        
        # Seleccionar versículo aleatorio
        random.seed(hoy)
        referencia = random.choice(self.VERSICULOS_POOL_DIARIO)
        random.seed()
        
        texto = self.VERSICULOS_DB[referencia]
        
        # Enriquecer con IA
        resultado = self._enriquecer_versiculo(referencia, texto)
        
        st.session_state["biblia_vdia_date"] = hoy
        st.session_state["biblia_vdia_stored"] = resultado
        return resultado
    
    def buscar_versiculo_completo(self, ref):
        try:
            ref_clean = ref.lower().strip()
            if ref_clean in self.VERSICULOS_DB:
                texto = self.VERSICULOS_DB[ref_clean]
                # Enriquecer con IA
                return self._enriquecer_versiculo(ref_clean, texto)
            return f"🕊️ No encontré ese versículo en la base de datos. Intenta con: {', '.join(list(self.VERSICULOS_DB.keys())[:3])}"
        except:
            return "❌ Error al buscar el versículo."
    
    def generar_devocional_personalizado(self, situacion):
        """Genera un devocional personalizado con IA para una situación específica"""
        if not self.openai_enabled:
            return "La IA no está disponible para generar devocionales personalizados."
        
        prompt = f"""La persona está atravesando esta situación:

"{situacion}"

Genera un devocional cristiano personalizado que incluya:

1. Un versículo bíblico apropiado (con referencia)
2. Reflexión profunda (100 palabras)
3. Aplicación práctica (80 palabras)
4. Oración personalizada (60 palabras)

Formato:
VERSICULO: [referencia] - [texto]
REFLEXION: [texto]
APLICACION: [texto]
ORACION: [texto]

Sé compasivo, esperanzador y profundo.
"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres una guía espiritual cristiana compasiva que ofrece consuelo y dirección bíblica."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.8
            )
            
            contenido = response.choices[0].message.content.strip()
            
            # Parsear
            partes = {}
            if "VERSICULO:" in contenido:
                partes['versiculo'] = contenido.split("VERSICULO:")[1].split("REFLEXION:")[0].strip()
            if "REFLEXION:" in contenido:
                partes['reflexion'] = contenido.split("REFLEXION:")[1].split("APLICACION:")[0].strip()
            if "APLICACION:" in contenido:
                partes['aplicacion'] = contenido.split("APLICACION:")[1].split("ORACION:")[0].strip()
            if "ORACION:" in contenido:
                partes['oracion'] = contenido.split("ORACION:")[1].strip()
            
            resultado = f"""**🙏 DEVOCIONAL PERSONALIZADO**

---

**📖 VERSÍCULO:**

{partes.get('versiculo', 'Confía en Dios en todo tiempo.')}

---

**💡 REFLEXIÓN:**

{partes.get('reflexion', 'Dios está contigo en esta situación.')}

---

**🎯 APLICACIÓN:**

{partes.get('aplicacion', 'Confía y da un paso a la vez.')}

---

**✨ ORACIÓN:**

_{partes.get('oracion', 'Señor, guíame en este momento. Amén.')}_
"""
            return resultado
            
        except:
            return "❌ Error al generar el devocional personalizado."
    
    def ver_journal_biblico(self):
        return "📖 Journal bíblico en desarrollo. Próximamente podrás registrar tus reflexiones diarias."
    
    def agregar_favorito(self, referencia, texto):
        """Agrega un versículo a favoritos"""
        favoritos = self._cargar_favoritos()
        
        existe = any(f['referencia'].lower() == referencia.lower() for f in favoritos)
        if existe:
            return False, "Este versículo ya está en favoritos"
        
        nuevo_favorito = {
            "id": len(favoritos) + 1,
            "referencia": referencia,
            "texto": texto,
            "fecha_agregado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        favoritos.append(nuevo_favorito)
        self._guardar_favoritos(favoritos)
        return True, "Versículo agregado a favoritos ⭐"
    
    def ver_favoritos(self):
        """Ver todos los versículos favoritos"""
        favoritos = self._cargar_favoritos()
        if not favoritos:
            return []
        return favoritos
    
    def eliminar_favorito(self, favorito_id):
        """Elimina un versículo de favoritos"""
        favoritos = self._cargar_favoritos()
        favoritos = [f for f in favoritos if f['id'] != favorito_id]
        self._guardar_favoritos(favoritos)
        return True

# =====================================================
# HANDLER TAROT CON IA
# =====================================================
class TarotHandler:
    def __init__(self, openai_api_key):
        self.OPENAI_API_KEY = openai_api_key
        self.openai_client = None
        self.openai_enabled = False
        self._inicializar_openai()
        
        self.DATA_FOLDER = "data"
        self.TIRADAS_FILE = os.path.join(self.DATA_FOLDER, "historial_tiradas.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
        
        # Mazo de Tarot completo
        self.MAZO_TAROT = {
            "El Loco": {
                "derecha": "nuevos comienzos, espontaneidad, salto de fe, energía fresca",
                "invertida": "imprudencia, caos, falta de dirección"
            },
            "El Mago": {
                "derecha": "manifestación, enfoque, poder personal, decisión clara",
                "invertida": "manipulación, bloqueo creativo, falta de enfoque"
            },
            "La Sacerdotisa": {
                "derecha": "intuición profunda, secretos revelándose, sabiduría silenciosa",
                "invertida": "secretos ocultos, desconexión intuitiva"
            },
            "La Emperatriz": {
                "derecha": "creación, abundancia, autocuidado, florecimiento",
                "invertida": "dependencia, creatividad bloqueada"
            },
            "El Emperador": {
                "derecha": "estructura, orden, liderazgo, estabilidad",
                "invertida": "tiranía, rigidez excesiva, autoritarismo"
            },
            "El Hierofante": {
                "derecha": "tradición, lecciones, guía espiritual",
                "invertida": "dogma, rebelión contra tradiciones"
            },
            "Los Enamorados": {
                "derecha": "decisiones del corazón, conexiones profundas",
                "invertida": "desamor, decisión equivocada, conflicto interno"
            },
            "El Carro": {
                "derecha": "avance, determinación, victoria",
                "invertida": "falta de dirección, pérdida de control"
            },
            "La Fuerza": {
                "derecha": "dominio interior, compasión, coraje tranquilo",
                "invertida": "debilidad, falta de control, inseguridad"
            },
            "El Ermitaño": {
                "derecha": "búsqueda interna, introspección, retiro necesario",
                "invertida": "aislamiento excesivo, soledad dolorosa"
            },
            "La Rueda de la Fortuna": {
                "derecha": "cambios positivos, destino, cierres que abren caminos",
                "invertida": "mala suerte, resistencia al cambio"
            },
            "La Justicia": {
                "derecha": "equilibrio, verdad, resolución justa",
                "invertida": "injusticia, deshonestidad, karma pendiente"
            },
            "El Colgado": {
                "derecha": "nueva perspectiva, pausa necesaria, entrega",
                "invertida": "resistencia, martirio, estancamiento"
            },
            "La Muerte": {
                "derecha": "transformación profunda, cierre necesario, renacimiento",
                "invertida": "resistencia al cambio, estancamiento"
            },
            "La Templanza": {
                "derecha": "armonía, paciencia, integración, sanación",
                "invertida": "desequilibrio, excesos, falta de moderación"
            },
            "El Diablo": {
                "derecha": "apegos, patrones limitantes, tentaciones",
                "invertida": "liberación de cadenas, romper patrones"
            },
            "La Torre": {
                "derecha": "ruptura necesaria, revelación, sacudidas que liberan",
                "invertida": "evitar cambios necesarios, crisis interna"
            },
            "La Estrella": {
                "derecha": "esperanza renovada, guía divina, claridad",
                "invertida": "desesperanza, falta de fe"
            },
            "La Luna": {
                "derecha": "intuición profunda, miedos conscientes, ilusiones",
                "invertida": "confusión extrema, engaños, paranoia"
            },
            "El Sol": {
                "derecha": "vitalidad, éxito radiante, claridad absoluta",
                "invertida": "optimismo bloqueado, éxito retrasado"
            },
            "El Juicio": {
                "derecha": "despertar espiritual, llamado interno, decisiones finales",
                "invertida": "autocrítica destructiva, negación del llamado"
            },
            "El Mundo": {
                "derecha": "cierre perfecto, logro total, expansión",
                "invertida": "incompletitud, falta de cierre"
            }
        }
    
    def _inicializar_openai(self):
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)
            self.openai_enabled = True
        except:
            self.openai_enabled = False
    
    def _seleccionar_carta(self):
        carta_nombre = random.choice(list(self.MAZO_TAROT.keys()))
        invertida = random.choice([True, False])
        carta_info = self.MAZO_TAROT[carta_nombre]
        significado = carta_info["invertida"] if invertida else carta_info["derecha"]
        return {
            "nombre": carta_nombre,
            "invertida": invertida,
            "significado": significado
        }
    
    def tirada_tres_cartas_ia(self, pregunta):
        if not pregunta:
            return "❌ Por favor escribe una pregunta"
        
        pasado = self._seleccionar_carta()
        presente = self._seleccionar_carta()
        futuro = self._seleccionar_carta()
        
        if not self.openai_enabled:
            return f"""
🔮 **TIRADA DE 3 CARTAS**

**Pregunta:** _{pregunta}_

━━━━━━━━━━━━━━━━━━━━━

**📜 PASADO**
🃏 **{pasado['nombre']}** {"(Invertida)" if pasado['invertida'] else ""}
_{pasado['significado']}_

**🌟 PRESENTE**
🃏 **{presente['nombre']}** {"(Invertida)" if presente['invertida'] else ""}
_{presente['significado']}_

**✨ FUTURO**
🃏 **{futuro['nombre']}** {"(Invertida)" if futuro['invertida'] else ""}
_{futuro['significado']}_

━━━━━━━━━━━━━━━━━━━━━

💜 Las cartas han hablado. Confía en tu intuición.
"""
        
        # Generar interpretación con IA
        cartas_texto = f"Pasado: {pasado['nombre']} {'(Invertida)' if pasado['invertida'] else ''}, Presente: {presente['nombre']} {'(Invertida)' if presente['invertida'] else ''}, Futuro: {futuro['nombre']} {'(Invertida)' if futuro['invertida'] else ''}"
        
        prompt = f"""Eres una lectora de tarot experta. Interpreta esta tirada de 3 cartas:

Pregunta: {pregunta}
Cartas: {cartas_texto}

Significados:
- Pasado: {pasado['significado']}
- Presente: {presente['significado']}
- Futuro: {futuro['significado']}

Genera una lectura profunda, personal y esperanzadora. Conecta las 3 cartas en una narrativa coherente. Máximo 200 palabras."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres una lectora de tarot sabia, compasiva y profunda. Ofreces guía esperanzadora."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=350,
                temperature=0.8
            )
            interpretacion = response.choices[0].message.content.strip()
        except:
            interpretacion = "Las cartas revelan un mensaje poderoso. Confía en tu intuición para interpretarlo."
        
        return f"""
🔮 **TIRADA DE 3 CARTAS**

**Pregunta:** _{pregunta}_

━━━━━━━━━━━━━━━━━━━━━

**📜 PASADO**
🃏 **{pasado['nombre']}** {"(Invertida)" if pasado['invertida'] else ""}

**🌟 PRESENTE**
🃏 **{presente['nombre']}** {"(Invertida)" if presente['invertida'] else ""}

**✨ FUTURO**
🃏 **{futuro['nombre']}** {"(Invertida)" if futuro['invertida'] else ""}

━━━━━━━━━━━━━━━━━━━━━

💫 **INTERPRETACIÓN:**

{interpretacion}

━━━━━━━━━━━━━━━━━━━━━

💜 Las cartas son guía, no destino. Tú tienes el poder final.
"""
    
    def energia_del_dia(self):
        carta = self._seleccionar_carta()
        mensajes = [
            "Tu energía hoy se mueve suave pero consciente.",
            "Hay algo alineándose aunque no lo veas aún.",
            "Tu intuición está más fina de lo normal.",
            "Hay una señal escondida en lo cotidiano."
        ]
        
        return f"""
✨ **ENERGÍA DEL DÍA**

🃏 **{carta['nombre']}** {"(Invertida)" if carta['invertida'] else ""}

_{carta['significado']}_

💜 {random.choice(mensajes)}
"""
    
    def tirada_amor_ia(self, pregunta):
        """Tirada de amor con 4 cartas"""
        if not pregunta:
            return "❌ Por favor escribe una pregunta sobre amor"
        
        tu_energia = self._seleccionar_carta()
        su_energia = self._seleccionar_carta()
        conexion = self._seleccionar_carta()
        consejo = self._seleccionar_carta()
        
        if not self.openai_enabled:
            return f"""
💕 **TIRADA DE AMOR**

**Pregunta:** _{pregunta}_

━━━━━━━━━━━━━━━━━━━━━

**💖 TU ENERGÍA**
🃏 **{tu_energia['nombre']}** {"(Invertida)" if tu_energia['invertida'] else ""}

**💗 SU ENERGÍA**
🃏 **{su_energia['nombre']}** {"(Invertida)" if su_energia['invertida'] else ""}

**✨ LA CONEXIÓN**
🃏 **{conexion['nombre']}** {"(Invertida)" if conexion['invertida'] else ""}

**🌟 CONSEJO**
🃏 **{consejo['nombre']}** {"(Invertida)" if consejo['invertida'] else ""}

━━━━━━━━━━━━━━━━━━━━━

💜 Las cartas hablan del amor. Confía en tu corazón.
"""
        
        # Generar interpretación con IA
        cartas_texto = f"Tu energía: {tu_energia['nombre']}, Su energía: {su_energia['nombre']}, Conexión: {conexion['nombre']}, Consejo: {consejo['nombre']}"
        
        prompt = f"""Interpreta esta tirada de amor con 4 cartas:

Pregunta: {pregunta}

Cartas:
- Tu energía: {tu_energia['nombre']} {"(Invertida)" if tu_energia['invertida'] else ""} - {tu_energia['significado']}
- Su energía: {su_energia['nombre']} {"(Invertida)" if su_energia['invertida'] else ""} - {su_energia['significado']}
- La conexión: {conexion['nombre']} {"(Invertida)" if conexion['invertida'] else ""} - {conexion['significado']}
- Consejo: {consejo['nombre']} {"(Invertida)" if consejo['invertida'] else ""} - {consejo['significado']}

Genera una lectura de amor profunda, compasiva y esperanzadora. Máximo 200 palabras."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres una experta en tarot de amor. Ofreces lecturas compasivas, honestas y esperanzadoras sobre relaciones."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=350,
                temperature=0.8
            )
            interpretacion = response.choices[0].message.content.strip()
        except:
            interpretacion = "Las cartas revelan las energías en juego. Confía en tu intuición para interpretar esta conexión."
        
        return f"""
💕 **TIRADA DE AMOR**

**Pregunta:** _{pregunta}_

━━━━━━━━━━━━━━━━━━━━━

**💖 TU ENERGÍA**
🃏 **{tu_energia['nombre']}** {"(Invertida)" if tu_energia['invertida'] else ""}

**💗 SU ENERGÍA**
🃏 **{su_energia['nombre']}** {"(Invertida)" if su_energia['invertida'] else ""}

**✨ LA CONEXIÓN**
🃏 **{conexion['nombre']}** {"(Invertida)" if conexion['invertida'] else ""}

**🌟 CONSEJO**
🃏 **{consejo['nombre']}** {"(Invertida)" if consejo['invertida'] else ""}

━━━━━━━━━━━━━━━━━━━━━

💫 **LECTURA:**

{interpretacion}

━━━━━━━━━━━━━━━━━━━━━

💜 El amor es un viaje, no un destino. Honra tu corazón.
"""
    
    def tirada_trabajo_ia(self, pregunta):
        """Tirada profesional con 4 cartas"""
        if not pregunta:
            return "❌ Por favor escribe una pregunta sobre trabajo"
        
        situacion = self._seleccionar_carta()
        fortalezas = self._seleccionar_carta()
        desafios = self._seleccionar_carta()
        resultado = self._seleccionar_carta()
        
        if not self.openai_enabled:
            return f"""
💼 **TIRADA PROFESIONAL**

**Pregunta:** _{pregunta}_

━━━━━━━━━━━━━━━━━━━━━

**📊 SITUACIÓN ACTUAL**
🃏 **{situacion['nombre']}** {"(Invertida)" if situacion['invertida'] else ""}

**🎯 TUS FORTALEZAS**
🃏 **{fortalezas['nombre']}** {"(Invertida)" if fortalezas['invertida'] else ""}

**⚠️ DESAFÍOS**
🃏 **{desafios['nombre']}** {"(Invertida)" if desafios['invertida'] else ""}

**🚀 RESULTADO/CONSEJO**
🃏 **{resultado['nombre']}** {"(Invertida)" if resultado['invertida'] else ""}

━━━━━━━━━━━━━━━━━━━━━

💜 Las cartas iluminan tu camino profesional.
"""
        
        prompt = f"""Interpreta esta tirada profesional:

Pregunta: {pregunta}

Cartas:
- Situación: {situacion['nombre']} {"(Inv.)" if situacion['invertida'] else ""} - {situacion['significado']}
- Fortalezas: {fortalezas['nombre']} {"(Inv.)" if fortalezas['invertida'] else ""} - {fortalezas['significado']}
- Desafíos: {desafios['nombre']} {"(Inv.)" if desafios['invertida'] else ""} - {desafios['significado']}
- Resultado: {resultado['nombre']} {"(Inv.)" if resultado['invertida'] else ""} - {resultado['significado']}

Genera una lectura profesional clara y práctica. Máximo 200 palabras."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres experta en tarot profesional. Ofreces consejos prácticos y motivadores sobre carrera y trabajo."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=350,
                temperature=0.8
            )
            interpretacion = response.choices[0].message.content.strip()
        except:
            interpretacion = "Las cartas revelan el panorama profesional. Confía en tus habilidades y avanza con propósito."
        
        return f"""
💼 **TIRADA PROFESIONAL**

**Pregunta:** _{pregunta}_

━━━━━━━━━━━━━━━━━━━━━

**📊 SITUACIÓN ACTUAL**
🃏 **{situacion['nombre']}** {"(Invertida)" if situacion['invertida'] else ""}

**🎯 TUS FORTALEZAS**
🃏 **{fortalezas['nombre']}** {"(Invertida)" if fortalezas['invertida'] else ""}

**⚠️ DESAFÍOS**
🃏 **{desafios['nombre']}** {"(Invertida)" if desafios['invertida'] else ""}

**🚀 RESULTADO/CONSEJO**
🃏 **{resultado['nombre']}** {"(Invertida)" if resultado['invertida'] else ""}

━━━━━━━━━━━━━━━━━━━━━

💫 **ANÁLISIS:**

{interpretacion}

━━━━━━━━━━━━━━━━━━━━━

💜 Tu trabajo es tu contribución al mundo. Hónralo.
"""
    
    def tirada_si_no_ia(self, pregunta):
        """Tirada Sí/No con interpretación"""
        if not pregunta:
            return "❌ Por favor escribe una pregunta de sí/no"
        
        carta = self._seleccionar_carta()
        
        # Determinar respuesta según carta
        si_fuerte = ["El Sol", "La Estrella", "El Mundo", "El Mago", "La Emperatriz", "El Emperador"]
        no_fuerte = ["La Torre", "La Muerte", "El Diablo"]
        
        if carta['nombre'] in si_fuerte and not carta['invertida']:
            respuesta = "SÍ"
            emoji = "✅"
        elif carta['nombre'] in no_fuerte or (carta['nombre'] in si_fuerte and carta['invertida']):
            respuesta = "NO"
            emoji = "❌"
        else:
            respuesta = "TAL VEZ / DEPENDE DE TI"
            emoji = "🔄"
        
        if not self.openai_enabled:
            return f"""
🔮 **TIRADA SÍ/NO**

**Pregunta:** _{pregunta}_

━━━━━━━━━━━━━━━━━━━━━

🃏 **{carta['nombre']}** {"(Invertida)" if carta['invertida'] else ""}

{emoji} **{respuesta}**

━━━━━━━━━━━━━━━━━━━━━

_{carta['significado']}_

💜 El tarot es guía, no destino. Tú decides siempre.
"""
        
        prompt = f"""Para la pregunta: {pregunta}

Salió la carta: {carta['nombre']} {"(Invertida)" if carta['invertida'] else ""}
Significado: {carta['significado']}

La respuesta es: {respuesta}

Explica brevemente por qué esta carta sugiere esta respuesta. Máximo 100 palabras. Tono empoderador."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres experta en tarot. Explicas las respuestas sí/no con claridad y empoderamiento."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            interpretacion = response.choices[0].message.content.strip()
        except:
            interpretacion = "Esta carta revela la energía alrededor de tu pregunta. Confía en tu intuición para decidir."
        
        return f"""
🔮 **TIRADA SÍ/NO**

**Pregunta:** _{pregunta}_

━━━━━━━━━━━━━━━━━━━━━

🃏 **{carta['nombre']}** {"(Invertida)" if carta['invertida'] else ""}

{emoji} **{respuesta}**

━━━━━━━━━━━━━━━━━━━━━

💫 **LECTURA:**

{interpretacion}

━━━━━━━━━━━━━━━━━━━━━

💜 El tarot es guía, no destino. Tú tienes el poder final.
"""
    
    def _cargar_historial(self):
        """Carga el historial de tiradas"""
        if not os.path.exists(self.TIRADAS_FILE):
            return []
        try:
            with open(self.TIRADAS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def _guardar_historial(self, historial):
        """Guarda el historial de tiradas"""
        with open(self.TIRADAS_FILE, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=2, ensure_ascii=False)
    
    def guardar_tirada(self, tipo, cartas_info, interpretacion):
        """Guarda una tirada en el historial"""
        historial = self._cargar_historial()
        
        nueva_tirada = {
            "id": len(historial) + 1,
            "tipo": tipo,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "cartas": cartas_info,
            "interpretacion": interpretacion[:500]  # Limitar tamaño
        }
        
        historial.append(nueva_tirada)
        
        # Mantener solo últimas 50 tiradas
        if len(historial) > 50:
            historial = historial[-50:]
        
        self._guardar_historial(historial)
        return True
    
    def ver_historial(self):
        """Ver historial de tiradas"""
        historial = self._cargar_historial()
        if not historial:
            return []
        # Retornar en orden inverso (más recientes primero)
        return list(reversed(historial))


# =====================================================
# HANDLER ASTROLOGÍA
# =====================================================
class AstrologiaHandler:
    def __init__(self):
        self.SIGNOS_ZODIACALES = {
            "aries": {
                "fechas": "21 marzo - 19 abril",
                "elemento": "Fuego",
                "planeta": "Marte",
                "fortalezas": "Valiente, directo, enérgico, pionero",
                "simbolo": "♈ El Carnero"
            },
            "tauro": {
                "fechas": "20 abril - 20 mayo",
                "elemento": "Tierra",
                "planeta": "Venus",
                "fortalezas": "Leal, paciente, confiable, sensual",
                "simbolo": "♉ El Toro"
            },
            "geminis": {
                "fechas": "21 mayo - 20 junio",
                "elemento": "Aire",
                "planeta": "Mercurio",
                "fortalezas": "Adaptable, comunicativo, inteligente",
                "simbolo": "♊ Los Gemelos"
            },
            "cancer": {
                "fechas": "21 junio - 22 julio",
                "elemento": "Agua",
                "planeta": "Luna",
                "fortalezas": "Intuitivo, emocional, protector",
                "simbolo": "♋ El Cangrejo"
            },
            "leo": {
                "fechas": "23 julio - 22 agosto",
                "elemento": "Fuego",
                "planeta": "Sol",
                "fortalezas": "Creativo, carismático, generoso",
                "simbolo": "♌ El León"
            },
            "virgo": {
                "fechas": "23 agosto - 22 septiembre",
                "elemento": "Tierra",
                "planeta": "Mercurio",
                "fortalezas": "Analítico, servicial, perfeccionista",
                "simbolo": "♍ La Virgen"
            },
            "libra": {
                "fechas": "23 septiembre - 22 octubre",
                "elemento": "Aire",
                "planeta": "Venus",
                "fortalezas": "Diplomático, justo, social",
                "simbolo": "♎ La Balanza"
            },
            "escorpio": {
                "fechas": "23 octubre - 21 noviembre",
                "elemento": "Agua",
                "planeta": "Plutón",
                "fortalezas": "Intenso, magnético, transformador",
                "simbolo": "♏ El Escorpión"
            },
            "sagitario": {
                "fechas": "22 noviembre - 21 diciembre",
                "elemento": "Fuego",
                "planeta": "Júpiter",
                "fortalezas": "Optimista, aventurero, filosófico",
                "simbolo": "♐ El Arquero"
            },
            "capricornio": {
                "fechas": "22 diciembre - 19 enero",
                "elemento": "Tierra",
                "planeta": "Saturno",
                "fortalezas": "Ambicioso, disciplinado, responsable",
                "simbolo": "♑ La Cabra"
            },
            "acuario": {
                "fechas": "20 enero - 18 febrero",
                "elemento": "Aire",
                "planeta": "Urano",
                "fortalezas": "Innovador, humanitario, independiente",
                "simbolo": "♒ El Aguador"
            },
            "piscis": {
                "fechas": "19 febrero - 20 marzo",
                "elemento": "Agua",
                "planeta": "Neptuno",
                "fortalezas": "Empático, artístico, intuitivo",
                "simbolo": "♓ Los Peces"
            }
        }
    
    def horoscopo_del_dia(self, signo):
        signo = signo.lower().strip()
        normalizaciones = {
            "geminis": "geminis", "géminis": "geminis",
            "cancer": "cancer", "cáncer": "cancer",
            "escorpio": "escorpio", "escorpion": "escorpio"
        }
        signo = normalizaciones.get(signo, signo)
        
        if signo not in self.SIGNOS_ZODIACALES:
            return "❌ Signo no válido. Elige: Aries, Tauro, Géminis, Cáncer, Leo, Virgo, Libra, Escorpio, Sagitario, Capricornio, Acuario, Piscis"
        
        info = self.SIGNOS_ZODIACALES[signo]
        mensajes = [
            f"Tu {info['elemento'].lower()} interior está activo hoy. Confía en tu intuición.",
            f"Como {info['simbolo']}, hoy brillas con luz propia.",
            f"Tu planeta regente {info['planeta']} te guía hacia nuevas oportunidades.",
            f"Las estrellas te recuerdan tus fortalezas: {info['fortalezas'].split(',')[0]}."
        ]
        
        consejos = [
            "Escucha tu corazón hoy, sabe más de lo que crees.",
            "Algo se alinea a tu favor, mantente atenta.",
            "Tu energía está en punto perfecto para crear.",
            "Las señales están ahí, solo necesitas verlas."
        ]
        
        return f"""
🌟 **HORÓSCOPO DEL DÍA**

**{signo.upper()}** {info['simbolo']}
{info['fechas']}

━━━━━━━━━━━━━━━━━━━━━

💫 {random.choice(mensajes)}

✨ {random.choice(consejos)}

━━━━━━━━━━━━━━━━━━━━━

🔥 **Tu elemento:** {info['elemento']}
🪐 **Tu planeta:** {info['planeta']}

💛 Recuerda tus fortalezas naturales hoy.
"""
    
    def fase_lunar_actual(self):
        hoy = datetime.datetime.now()
        dias_desde_nueva = (hoy.day + hoy.month * 30) % 29.5
        
        if dias_desde_nueva < 1:
            fase = "nueva"
            emoji = "🌑"
            consejo = "Establece intenciones claras. Comienza nuevos proyectos."
        elif dias_desde_nueva < 7:
            fase = "creciente"
            emoji = "🌒"
            consejo = "Toma acción hacia tus metas. Construye momentum."
        elif dias_desde_nueva < 14:
            fase = "cuarto creciente"
            emoji = "🌓"
            consejo = "Supera obstáculos con determinación. Toma decisiones."
        elif dias_desde_nueva < 15:
            fase = "llena"
            emoji = "🌕"
            consejo = "Celebra tus logros. Clarifica tu visión. Libera lo que no sirve."
        elif dias_desde_nueva < 22:
            fase = "menguante"
            emoji = "🌖"
            consejo = "Comparte tu conocimiento. Reflexiona sobre logros."
        else:
            fase = "menguante final"
            emoji = "🌘"
            consejo = "Descansa profundamente. Medita e introspecciona."
        
        return f"""
🌙 **FASE LUNAR ACTUAL**

{emoji} **Luna {fase.title()}**

━━━━━━━━━━━━━━━━━━━━━

**QUÉ HACER EN ESTA FASE:**

{consejo}

━━━━━━━━━━━━━━━━━━━━━

💫 La Luna influye en tus emociones y energía. Fluye con sus ciclos naturales.
"""
    
    def listar_signos(self):
        texto = "🌟 **SIGNOS ZODIACALES** 🌟\n\n"
        for signo, info in self.SIGNOS_ZODIACALES.items():
            texto += f"{info['simbolo']} **{signo.upper()}** - {info['fechas']}\n"
        return texto

# =====================================================
# HANDLER NUMEROLOGÍA
# =====================================================
class NumerologiaHandler:
    def __init__(self):
        self.NUMEROS_BASE = {
            1: {
                "nombre": "El Líder",
                "energia": "Independencia, iniciativa, liderazgo",
                "luz": "Pionero, creativo, valiente",
                "consejo": "Confía en tu visión única. No temas destacar."
            },
            2: {
                "nombre": "El Diplomático",
                "energia": "Cooperación, sensibilidad, intuición",
                "luz": "Empático, pacificador, intuitivo",
                "consejo": "Tu sensibilidad es un don. Pon límites sanos."
            },
            3: {
                "nombre": "El Creativo",
                "energia": "Expresión, creatividad, comunicación",
                "luz": "Artístico, optimista, carismático",
                "consejo": "Tu luz es contagiosa. No la apagues por otros."
            },
            4: {
                "nombre": "El Constructor",
                "energia": "Estabilidad, estructura, trabajo",
                "luz": "Confiable, organizado, práctico",
                "consejo": "Descansa. El mundo no colapsa si te detienes."
            },
            5: {
                "nombre": "El Aventurero",
                "energia": "Libertad, cambio, aventura",
                "luz": "Adaptable, curioso, valiente",
                "consejo": "El cambio es tu naturaleza, pero crea raíces conscientes."
            },
            6: {
                "nombre": "El Sanador",
                "energia": "Amor, servicio, responsabilidad",
                "luz": "Compasivo, protector, consejero",
                "consejo": "Cuídate a ti primero. No puedes dar desde el vacío."
            },
            7: {
                "nombre": "El Místico",
                "energia": "Sabiduría, introspección, espiritualidad",
                "luz": "Sabio, intuitivo, investigador",
                "consejo": "El mundo necesita tu sabiduría. No te escondas."
            },
            8: {
                "nombre": "El Poderoso",
                "energia": "Abundancia, poder, autoridad",
                "luz": "Exitoso, ambicioso, justo",
                "consejo": "El poder es responsabilidad. Úsalo para elevar."
            },
            9: {
                "nombre": "El Humanitario",
                "energia": "Compasión universal, finalización",
                "luz": "Compasivo, sabio, altruista",
                "consejo": "Has vivido mucho internamente. Comparte tu luz."
            },
            11: {
                "nombre": "El Visionario",
                "energia": "Intuición elevada, misión espiritual",
                "luz": "Visionario, inspirador, canal espiritual",
                "consejo": "Tu sensibilidad es extrema. Ground yourself daily."
            },
            22: {
                "nombre": "El Arquitecto Maestro",
                "energia": "Manifestación masiva, construcción de legados",
                "luz": "Constructor de imperios, visionario práctico",
                "consejo": "Construyes imperios. Recuerda vivir mientras lo haces."
            }
        }
        
        self.NUMEROS_ANGELICALES = {
            111: "Portal de manifestación abierto. Tus pensamientos se materializan rápido.",
            222: "Todo se está alineando perfectamente. Confía en el proceso.",
            333: "Los maestros ascendidos están contigo. Estás protegida divinamente.",
            444: "Ángeles rodeándote. Estabilidad y protección.",
            555: "Cambio masivo en camino. Suelta lo viejo.",
            666: "Reequilibra lo material y espiritual.",
            777: "Milagros y bendiciones descendiendo. Sincronicidades activadas.",
            888: "Abundancia infinita fluyendo. Recibe sin culpa.",
            999: "Ciclo completándose. Suelta con amor.",
            1111: "Portal maestro abierto. Deseo masivo manifestándose."
        }
    
    def numerologia_del_dia(self):
        hoy = datetime.datetime.now()
        suma = hoy.day + hoy.month + hoy.year
        
        while suma > 9 and suma not in (11, 22):
            suma = sum(int(x) for x in str(suma))
        
        if suma in self.NUMEROS_BASE:
            info = self.NUMEROS_BASE[suma]
            return f"""
🔢✨ **NUMEROLOGÍA DEL DÍA**

**Número:** {suma} - *{info['nombre']}*

🌟 **Energía del día:**
{info['energia']}

💫 **Tu luz hoy:**
{info['luz']}

💛 **Consejo:**
{info['consejo']}
"""
        return f"🔢 Número del día: **{suma}**"
    
    def calcular_camino_de_vida(self, fecha_str):
        try:
            if "/" in fecha_str:
                dia, mes, anio = fecha_str.split("/")
            elif "-" in fecha_str:
                dia, mes, anio = fecha_str.split("-")
            else:
                return "❌ Formato inválido. Usa: DD/MM/AAAA o DD-MM-AAAA"
            
            suma = int(dia) + int(mes) + int(anio)
            
            while suma > 9 and suma not in (11, 22):
                suma = sum(int(x) for x in str(suma))
            
            if suma in self.NUMEROS_BASE:
                info = self.NUMEROS_BASE[suma]
                return f"""
🔢💫 **TU CAMINO DE VIDA: {suma}**
*{info['nombre']}*

━━━━━━━━━━━━━━━━━━━━━

✨ **ENERGÍA:** {info['energia']}

🌟 **TU LUZ:** {info['luz']}

━━━━━━━━━━━━━━━━━━━━━

💛 **CONSEJO:** {info['consejo']}
"""
            return f"Tu camino de vida es: {suma}"
        except:
            return "❌ Formato inválido. Usa: DD/MM/AAAA o DD-MM-AAAA"
    
    def significado_numero(self, numero_str):
        try:
            numero = int(numero_str)
        except:
            return "Por favor escribe un número válido 💛"
        
        if numero in self.NUMEROS_ANGELICALES:
            return f"""
👼✨ **NÚMERO ANGELICAL: {numero}**

{self.NUMEROS_ANGELICALES[numero]}

💫 Los ángeles te están enviando un mensaje. Presta atención a las señales.
"""
        
        if numero in self.NUMEROS_BASE:
            info = self.NUMEROS_BASE[numero]
            return f"""
🔢✨ **NÚMERO {numero}: {info['nombre']}**

**Energía:** {info['energia']}

**Luz:** {info['luz']}

💛 **Consejo:** {info['consejo']}
"""
        
        # Reducir número
        suma = numero
        while suma > 9 and suma not in (11, 22):
            suma = sum(int(x) for x in str(suma))
        
        if suma in self.NUMEROS_BASE:
            info = self.NUMEROS_BASE[suma]
            return f"""
🔢 **TU NÚMERO {numero}**

Se reduce a: **{suma}** - {info['nombre']}

**Energía:** {info['energia']}

💛 {info['consejo']}
"""
        
        return f"🔢 Número {numero} - Energía especial ✨"


# =====================================================
# HANDLER IDEAS CON IA
# =====================================================
class IdeasHandler:
    def __init__(self, openai_api_key):
        self.OPENAI_API_KEY = openai_api_key
        self.openai_client = None
        self.openai_enabled = False
        self._inicializar_openai()
        
        self.DATA_FOLDER = "data"
        self.PROYECTOS_FILE = os.path.join(self.DATA_FOLDER, "proyectos_ideas.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
    
    def _inicializar_openai(self):
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)
            self.openai_enabled = True
        except:
            self.openai_enabled = False
    
    def _cargar_proyectos(self):
        if not os.path.exists(self.PROYECTOS_FILE):
            return []
        try:
            with open(self.PROYECTOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def _guardar_proyectos(self, proyectos):
        with open(self.PROYECTOS_FILE, "w", encoding="utf-8") as f:
            json.dump(proyectos, f, indent=2, ensure_ascii=False)
    
    def conversar_con_ia(self, mensaje_usuario, contexto=""):
        """Conversa con IA sobre ideas"""
        if not self.openai_enabled:
            return "La IA no está disponible en este momento 💜"
        
        prompt = f"""Eres una amiga cercana que ayuda con ideas y proyectos personales.

Contexto: {contexto if contexto else "Conversación nueva sobre ideas"}

Usuario dice: "{mensaje_usuario}"

Responde de forma:
- Cálida y emocionada
- Natural y conversacional
- Empática y validadora
- Proactiva con sugerencias
- Usa emojis ocasionalmente 💛
- Máximo 150 palabras

Escribe en prosa natural."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres una amiga cercana que ayuda con ideas y proyectos personales. Conversas naturalmente, sin parecer robótica."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.9
            )
            return response.choices[0].message.content.strip()
        except:
            return "Ayy perdón bebé, tuve un problemita técnico 🥺 ¿Me lo repites?"
    
    def generar_imagen_dalle(self, descripcion):
        """Genera imagen con DALL-E 3"""
        if not self.openai_enabled:
            return {'success': False, 'error': 'IA no disponible'}
        
        prompt = f"{descripcion}, high quality, detailed, aesthetic, beautiful composition"
        
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            return {
                'success': True,
                'url': response.data[0].url,
                'prompt': prompt
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def crear_proyecto(self, nombre, descripcion=""):
        """Crea un nuevo proyecto"""
        proyectos = self._cargar_proyectos()
        nuevo_id = len(proyectos) + 1
        
        nuevo_proyecto = {
            "id": nuevo_id,
            "nombre": nombre,
            "descripcion": descripcion,
            "fecha_creacion": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "items": [],
            "total_inspiracion": 0,
            "total_compras": 0,
            "conseguidos": 0
        }
        
        proyectos.append(nuevo_proyecto)
        self._guardar_proyectos(proyectos)
        return nuevo_proyecto
    
    def listar_proyectos(self):
        """Lista todos los proyectos"""
        return self._cargar_proyectos()
    
    def obtener_proyecto(self, proyecto_id):
        """Obtiene un proyecto por ID"""
        proyectos = self._cargar_proyectos()
        try:
            pid = int(proyecto_id)
            return next((p for p in proyectos if p["id"] == pid), None)
        except:
            return None
    
    def agregar_item(self, proyecto_id, tipo, descripcion, **kwargs):
        """Agrega item a un proyecto"""
        proyectos = self._cargar_proyectos()
        try:
            pid = int(proyecto_id)
        except:
            return None
        
        proyecto = next((p for p in proyectos if p["id"] == pid), None)
        if not proyecto:
            return None
        
        nuevo_item = {
            "id": len(proyecto['items']) + 1,
            "tipo": tipo,
            "descripcion": descripcion,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "conseguido": False
        }
        
        for key, value in kwargs.items():
            if value:
                nuevo_item[key] = value
        
        proyecto['items'].append(nuevo_item)
        
        if tipo == 'inspiracion':
            proyecto['total_inspiracion'] += 1
        else:
            proyecto['total_compras'] += 1
        
        self._guardar_proyectos(proyectos)
        return nuevo_item


# =====================================================
# HANDLER PROFESIONAL CON IA
# =====================================================
class ProfesionalHandler:
    def __init__(self, openai_api_key):
        self.OPENAI_API_KEY = openai_api_key
        self.openai_client = None
        self.openai_enabled = False
        self._inicializar_openai()
        
        self.DATA_FOLDER = "data"
        self.VACANTES_FILE = os.path.join(self.DATA_FOLDER, "vacantes.json")
        os.makedirs(self.DATA_FOLDER, exist_ok=True)
        
        self.PREGUNTAS_COMUNES = [
            "Cuéntame sobre ti",
            "¿Por qué quieres trabajar aquí?",
            "¿Cuáles son tus fortalezas?",
            "¿Cuál es tu mayor debilidad?",
            "Cuéntame sobre un desafío que hayas superado",
            "¿Dónde te ves en 5 años?",
            "¿Por qué dejaste tu último trabajo?",
            "¿Cómo manejas la presión?",
            "Cuéntame sobre un error que cometiste",
            "¿Por qué deberíamos contratarte?"
        ]
    
    def _inicializar_openai(self):
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)
            self.openai_enabled = True
        except:
            self.openai_enabled = False
    
    def _cargar_vacantes(self):
        if not os.path.exists(self.VACANTES_FILE):
            return []
        try:
            with open(self.VACANTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def _guardar_vacantes(self, vacantes):
        with open(self.VACANTES_FILE, "w", encoding="utf-8") as f:
            json.dump(vacantes, f, indent=2, ensure_ascii=False)
    
    def generar_correo_profesional(self, tipo, contexto=""):
        """Genera correos profesionales con IA"""
        if not self.openai_enabled:
            return "La IA no está disponible 💜"
        
        prompts = {
            "agradecimiento": f"""Genera un correo profesional de agradecimiento después de una entrevista.
Contexto: {contexto if contexto else "entrevista reciente para un puesto"}

El correo debe:
- Agradecer por el tiempo
- Reafirmar interés en la posición
- Ser conciso (máximo 150 palabras)
- Tono profesional pero cálido

Formato:
Asunto: [línea de asunto]
---
[Cuerpo del correo]""",

            "seguimiento": f"""Genera un correo profesional de seguimiento para una aplicación.
Contexto: {contexto if contexto else "aplicación enviada hace 1-2 semanas"}

El correo debe:
- Recordar brevemente la aplicación
- Reafirmar interés
- Preguntar sobre el estado del proceso
- Ser breve y respetuoso (máximo 120 palabras)

Formato:
Asunto: [línea de asunto]
---
[Cuerpo del correo]""",

            "networking": f"""Genera un mensaje profesional para LinkedIn/networking.
Contexto: {contexto if contexto else "contacto profesional en la industria"}

El mensaje debe:
- Presentarte brevemente
- Explicar por qué te contactas
- Solicitar conexión de forma natural
- Ser conciso (máximo 100 palabras)

[Mensaje]""",

            "feedback": f"""Genera un correo solicitando feedback después de un proceso.
Contexto: {contexto if contexto else "proceso de selección que no avanzó"}

El correo debe:
- Agradecer por la oportunidad
- Solicitar feedback constructivo
- Mantener profesionalismo
- Ser breve (máximo 120 palabras)

Formato:
Asunto: [línea de asunto]
---
[Cuerpo del correo]""",

            "negociacion": f"""Genera un correo profesional para negociar oferta/salario.
Contexto: {contexto if contexto else "oferta recibida, quiero negociar"}

El correo debe:
- Agradecer por la oferta
- Expresar entusiasmo
- Presentar contra-propuesta profesionalmente
- Ser asertivo pero respetuoso (máximo 150 palabras)

Formato:
Asunto: [línea de asunto]
---
[Cuerpo del correo]"""
        }
        
        if tipo not in prompts:
            return "❌ Tipo de correo no válido"
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres una experta en comunicación profesional y recursos humanos. Generas correos profesionales, claros y efectivos en español."},
                    {"role": "user", "content": prompts[tipo]}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            correo = response.choices[0].message.content.strip()
            return f"📧 **CORREO GENERADO**\n\n{correo}\n\n💡 Personalízalo con tus datos antes de enviar 💛"
        except:
            return "❌ Error al generar el correo. Intenta de nuevo 💛"
    
    def obtener_pregunta_entrevista(self):
        """Retorna pregunta aleatoria para practicar"""
        pregunta = random.choice(self.PREGUNTAS_COMUNES)
        return f"""💬 **PREGUNTA DE PRÁCTICA**

_{pregunta}_

💡 Responde usando el método STAR:
• **S**ituación - Contexto
• **T**area - Qué debías lograr
• **A**cción - Qué hiciste
• **R**esultado - Qué lograste

✍️ Escribe tu respuesta y te daré feedback 💛"""
    
    def analizar_respuesta_entrevista(self, pregunta, respuesta):
        """Analiza respuesta y da feedback con IA"""
        if not self.openai_enabled:
            return "La IA no está disponible 💜"
        
        prompt = f"""Eres una coach de entrevistas de trabajo experta.

Pregunta: "{pregunta}"
Respuesta del candidato: "{respuesta}"

Analiza y proporciona:
1. Aspectos positivos (2-3 puntos)
2. Áreas de mejora (2-3 puntos)
3. Sugerencia de mejora (1 párrafo)

Sé constructiva, específica y motivadora. Máximo 200 palabras."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres una coach de entrevistas profesional, empática y constructiva."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=350,
                temperature=0.7
            )
            
            feedback = response.choices[0].message.content.strip()
            return f"📋 **FEEDBACK DE TU RESPUESTA**\n\n{feedback}\n\n💛 ¡Sigue practicando!"
        except:
            return "❌ Error al analizar tu respuesta 💛"
    
    def agregar_vacante(self, empresa, cargo, fecha_aplicacion, contacto="", notas=""):
        """Agrega vacante al seguimiento"""
        vacantes = self._cargar_vacantes()
        
        nueva = {
            "id": len(vacantes) + 1,
            "empresa": empresa,
            "cargo": cargo,
            "fecha_aplicacion": fecha_aplicacion,
            "contacto": contacto,
            "estado": "aplicado",
            "notas": notas,
            "fecha_actualizacion": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        
        vacantes.append(nueva)
        self._guardar_vacantes(vacantes)
        return nueva
    
    def listar_vacantes(self):
        """Lista todas las vacantes"""
        return self._cargar_vacantes()
    
    def actualizar_estado_vacante(self, vacante_id, nuevo_estado, notas=""):
        """Actualiza estado de vacante"""
        vacantes = self._cargar_vacantes()
        estados_validos = ["aplicado", "entrevista", "oferta", "rechazado", "retirado"]
        
        if nuevo_estado.lower() not in estados_validos:
            return None
        
        vacante = next((v for v in vacantes if v["id"] == int(vacante_id)), None)
        if not vacante:
            return None
        
        vacante["estado"] = nuevo_estado.lower()
        vacante["fecha_actualizacion"] = datetime.datetime.now().strftime("%Y-%m-%d")
        if notas:
            vacante["notas"] = notas
        
        self._guardar_vacantes(vacantes)
        return vacante
    
    def borrar_vacante(self, vacante_id):
        """Elimina vacante"""
        vacantes = self._cargar_vacantes()
        vacante = next((v for v in vacantes if v["id"] == int(vacante_id)), None)
        
        if not vacante:
            return None
        
        vacantes = [v for v in vacantes if v["id"] != int(vacante_id)]
        self._guardar_vacantes(vacantes)
        return vacante
    
    def verificar_vacantes_pendientes_seguimiento(self):
        """Verifica vacantes que necesitan seguimiento (7+ días)"""
        vacantes = self._cargar_vacantes()
        pendientes = []
        
        for v in vacantes:
            if v.get('estado') != 'aplicado':
                continue
            
            try:
                fecha_app = datetime.datetime.strptime(v['fecha_aplicacion'], "%Y-%m-%d")
                dias = (datetime.datetime.now() - fecha_app).days
                
                if dias >= 7:
                    pendientes.append({
                        'id': v['id'],
                        'empresa': v['empresa'],
                        'cargo': v['cargo'],
                        'dias': dias
                    })
            except:
                continue
        
        return pendientes
    
    def generar_estadisticas_vacantes(self):
        """Genera estadísticas de vacantes"""
        vacantes = self._cargar_vacantes()
        
        if not vacantes:
            return None
        
        total = len(vacantes)
        
        # Contar por estado
        estados = {
            'aplicado': 0,
            'entrevista': 0,
            'oferta': 0,
            'rechazado': 0,
            'retirado': 0
        }
        
        for v in vacantes:
            estado = v.get('estado', 'aplicado')
            if estado in estados:
                estados[estado] += 1
        
        # Calcular tasa de respuesta (entrevistas + ofertas / total)
        respuestas = estados['entrevista'] + estados['oferta']
        tasa_respuesta = (respuestas / total * 100) if total > 0 else 0
        
        # Calcular tasa de éxito (ofertas / total)
        tasa_exito = (estados['oferta'] / total * 100) if total > 0 else 0
        
        # Empresas más contactadas (top 3)
        empresas = {}
        for v in vacantes:
            emp = v.get('empresa', 'N/A')
            empresas[emp] = empresas.get(emp, 0) + 1
        
        top_empresas = sorted(empresas.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Tiempo promedio por estado (días)
        try:
            dias_totales = []
            for v in vacantes:
                if v.get('fecha_aplicacion'):
                    fecha_app = datetime.datetime.strptime(v['fecha_aplicacion'], "%Y-%m-%d")
                    fecha_actual = datetime.datetime.strptime(v.get('fecha_actualizacion', datetime.datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
                    dias = (fecha_actual - fecha_app).days
                    dias_totales.append(dias)
            
            dias_promedio = sum(dias_totales) / len(dias_totales) if dias_totales else 0
        except:
            dias_promedio = 0
        
        return {
            'total': total,
            'estados': estados,
            'tasa_respuesta': tasa_respuesta,
            'tasa_exito': tasa_exito,
            'top_empresas': top_empresas,
            'dias_promedio': dias_promedio,
            'activas': estados['aplicado'] + estados['entrevista']
        }

    
    def marcar_conseguido(self, proyecto_id, item_id):
        """Marca un item como conseguido"""
        proyectos = self._cargar_proyectos()
        try:
            pid = int(proyecto_id)
            iid = int(item_id)
        except:
            return False
        
        proyecto = next((p for p in proyectos if p["id"] == pid), None)
        if not proyecto:
            return False
        
        item = next((i for i in proyecto['items'] if i["id"] == iid), None)
        if not item:
            return False
        
        item['conseguido'] = True
        item['fecha_conseguido'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        proyecto['conseguidos'] = proyecto.get('conseguidos', 0) + 1
        
        self._guardar_proyectos(proyectos)
        return True
    
    def expandir_idea(self, idea_usuario):
        """Expande una idea con sugerencias de IA"""
        if not self.openai_enabled:
            return "La IA no está disponible 💜"
        
        prompt = f"""El usuario tiene esta idea: "{idea_usuario}"

Ayúdale a expandirla. Genera:
1. 3 variaciones interesantes de la idea
2. 2 preguntas para profundizar
3. 1 sugerencia práctica para empezar

Máximo 200 palabras. Tono amigable y motivador."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres una amiga creativa que ayuda a expandir ideas de proyectos personales."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=350,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except:
            return "No pude procesar la idea 🥺 Intenta de nuevo"


class MockHandler:
    def listar_proyectos(self): return []
    def conversacion_ia(self, m, c=""): return "🔮 El oráculo descansa."
    def conversar_con_ia(self, m, c=""): return "🔮 El oráculo descansa."
    def energia_del_dia(self): return "✨ Energía no disponible"
    def horoscopo_del_dia(self, s): return "✨ Horóscopo no disponible"
    def numerologia_del_dia(self): return "🔢 Nume no disponible"
    def tirada_tres_cartas_ia(self, p): return "🃏 Pasado: El Loco\nPresente: La Fuerza\nFuturo: El Mundo"
    def ver_journal_tarot(self): return "Journal vacío"
    def carta_natal_basica(self, f): return "Carta no disponible"
    def fase_lunar_actual(self): return "Luna no disponible"
    def transitos_actuales(self): return "Tránsitos no disponibles"
    def listar_signos(self): return "Signos no disponibles"
    def compatibilidad_signos(self, a, b): return "Compatibilidad no disponible"
    def calcular_camino_de_vida(self, f): return "Camino no disponible"
    def ano_personal(self, f): return "Año no disponible"
    def significado_numero(self, n): return "Significado no disponible"
    def compatibilidad_numerologica(self, a, b): return "Compatibilidad no disponible"
    def ver_proyecto_detallado(self, i): return "Detalle no disponible"
    def crear_proyecto(self, n, d): pass
    def agregar_item(self, i, t, d): pass
    def eliminar_proyecto(self, i): pass
    def tirada_amor_ia(self, p): return "Tirada amor no disponible"
    def tirada_trabajo_ia(self, p): return "Tirada trabajo no disponible"
    def tirada_si_no_ia(self, p): return "Tirada si/no no disponible"

# =====================================================
# FUNCIONES DE UTILIDAD
# =====================================================
def crear_backup_datos():
    """Crea un backup ZIP de todos los archivos de datos"""
    import zipfile
    from io import BytesIO
    
    # Crear nombre de archivo con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_backup = f"portal_backup_{timestamp}.zip"
    
    # Crear archivo ZIP en memoria
    zip_buffer = BytesIO()
    
    try:
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Agregar todos los archivos JSON de la carpeta data/
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
# FUNCIÓN SPOTIFY PERSISTENTE (VERSIÓN SIMPLE)
# =====================================================
def render_spotify_persistente():
    """Renderiza Spotify flotante en la parte inferior"""
    
    spotify_html = """
    <style>
        #spotify-fixed {
            position: fixed !important;
            bottom: 50px !important;              /* 👈 ARRIBA del footer */
            left: 50% !important;
            transform: translateX(-50%) !important;
            z-index: 999999 !important;
            width: 300px !important;
            box-shadow: 0 4px 20px rgba(147, 51, 234, 0.5) !important;
            border-radius: 12px !important;
            background: rgba(2, 6, 23, 0.98) !important;
            padding: 5px !important;
            pointer-events: auto !important;
        }
        
        #spotify-fixed iframe {
            width: 100% !important;
            height: 152px !important;
            border-radius: 12px !important;
        }
        
        #spotify-fixed:hover {
            transform: translateX(-50%) translateY(-5px) !important;
            box-shadow: 0 6px 30px rgba(147, 51, 234, 0.7) !important;
        }
        
        @media (max-width: 768px) {
            #spotify-fixed {
                width: 250px !important;
                bottom: 50px !important;
            }
        }
    </style>
    
    <div id="spotify-fixed">
        <iframe 
            style="border-radius:12px" 
            src="https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwq3LiO?utm_source=generator&theme=0" 
            width="100%" 
            height="152" 
            frameBorder="0" 
            allowfullscreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy">
        </iframe>
    </div>
    """
    
    components.html(spotify_html, height=180, scrolling=False)
# =====================================================
# 5. INICIALIZACIÓN DE HANDLERS (OPTIMIZADO CON CACHÉ)
# =====================================================
@st.cache_resource
def get_handlers():
    fin = LocalFinanzasHandler()
    not_h = LocalNotasHandler()
    lib = LocalLibrosHandler()
    fra = LocalFrasesHandler()
    pers = GestorPersonalidades()
    bib = RobustBibliaHandler()
    
    # Usar la misma API key que libros y frases
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

    
    # Inicializar handlers de Lo Oculto
    tarot = TarotHandler(OPENAI_API_KEY)
    astro = AstrologiaHandler()
    nume = NumerologiaHandler()
    ideas = IdeasHandler(OPENAI_API_KEY)  # Ideas con IA real
        
    # Inicializar handler Profesional
    profesional = ProfesionalHandler(OPENAI_API_KEY)
    
    return fin, not_h, lib, fra, pers, bib, ideas, tarot, astro, nume, profesional

# Inicializar handlers
finanzas_handler, notas_handler, libros_handler, frases_handler, personalidades_handler, biblia_handler, ideas_handler, tarot, astrologia, numerologia, profesional_handler = get_handlers()
biblia = biblia_handler

# =====================================================
# 6. NAVEGACIÓN PRINCIPAL
# =====================================================
CONTRASENA = "portal123"
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
    # === SPOTIFY FLOTANTE CON TU PLAYLIST ===
    st.markdown("""
        <style>
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
            }
        </style>
        
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
    
    # Función para mostrar breadcrumbs
    def mostrar_breadcrumbs():
        view = st.session_state.current_view
        
        # Nombres amigables
        nombres = {
            "menu": "Inicio",
            "lo_oculto": "Lo Oculto",
            "ideas": "Ideas",
            "biblia": "Biblia",
            "finanzas": "Finanzas",
            "notas": "Notas",
            "libros": "Libros",
            "frases": "Frases",
            "personalidades": "Personas",
            "profesional": "Profesional",
            "tarot": "Tarot",
            "astrologia": "Astrología",
            "numerologia": "Numerología"
        }
        
        if view == "menu":
            return
        
        breadcrumb = f"🏠 Inicio"
        
        # Agregar vista actual
        if view in nombres:
            breadcrumb += f" → {nombres[view]}"
        
        # Agregar subvista si existe
        subview_keys = [
            ("finanzas_subview", view == "finanzas"),
            ("notas_subview", view == "notas"),
            ("libros_subview", view == "libros"),
            ("frases_subview", view == "frases"),
            ("ideas_subview", view == "ideas"),
            ("tarot_subview", view == "tarot"),
            ("astro_subview", view == "astrologia"),
            ("nume_subview", view == "numerologia"),
            ("profesional_subview", view == "profesional"),
            ("biblia_subview", view == "biblia"),
            ("oculto_subview", view == "lo_oculto")
        ]
        
        for key, condition in subview_keys:
            if condition and key in st.session_state and st.session_state[key] != "menu":
                subview = st.session_state[key].replace("_", " ").title()
                breadcrumb += f" → {subview}"
                break
        
        st.caption(breadcrumb)
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
        
        # Botón de Backup
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
        
        # Botón de Cerrar Sesión
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
            st.markdown("<p style='color:#d8c9ff; font-size:0.95rem;'>Ejemplo: Juan 3:16, Salmos 23:1</p>", unsafe_allow_html=True)
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
        
        elif st.session_state.biblia_subview == "devocional":
            st.markdown("### 📿 Devocional Personalizado")
            situacion = st.text_area("¿Qué estás atravesando hoy?", height=100, key="input_devocional")
            if st.button("🙏 Generar Devocional", use_container_width=True, key="btn_generar_devocional"):
                if situacion:
                    resultado = biblia.generar_devocional_personalizado(situacion)
                    st.markdown(f'<div class="result-card">{resultado}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Comparte tu situación primero")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_biblia_volver_devocional"):
                st.session_state.biblia_subview = "menu"
                st.rerun()
        
        elif st.session_state.biblia_subview == "journal":
            st.markdown("### 📔 Mi Diario Bíblico")
            resultado = biblia.ver_journal_biblico()
            st.markdown(f'<div class="result-card" style="text-align:left; max-height:400px; overflow-y:auto;">{resultado}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_biblia_volver_journal"):
                st.session_state.biblia_subview = "menu"
                st.rerun()
        
        elif st.session_state.biblia_subview == "favoritos":
            st.markdown("### ⭐ Versículos Favoritos")
            
            favoritos = biblia.ver_favoritos()
            
            if favoritos:
                st.success(f"✅ Tienes {len(favoritos)} versículo(s) favorito(s)")
                for fav in favoritos:
                    with st.expander(f"📖 {fav['referencia']}", expanded=False):
                        st.markdown(f"**{fav['texto']}**")
                        st.caption(f"Agregado: {fav['fecha_agregado']}")
                        if st.button("🗑️ Eliminar", key=f"btn_eliminar_fav_{fav['id']}"):
                            biblia.eliminar_favorito(fav['id'])
                            st.success("Eliminado de favoritos")
                            st.rerun()
            else:
                st.info("No tienes versículos favoritos aún. ¡Agrega algunos desde Versículo del Día o Buscar!")
            
            # Agregar nuevo favorito manualmente
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### ➕ Agregar Favorito")
            ref_fav = st.text_input("Referencia:", placeholder="Ej: Juan 3:16", key="input_ref_fav")
            texto_fav = st.text_area("Texto del versículo:", height=100, key="input_texto_fav")
            
            if st.button("⭐ Agregar a Favoritos", use_container_width=True, key="btn_agregar_fav"):
                if ref_fav and texto_fav:
                    exito, mensaje = biblia.agregar_favorito(ref_fav, texto_fav)
                    if exito:
                        st.success(mensaje)
                        st.rerun()
                    else:
                        st.warning(mensaje)
                else:
                    st.warning("⚠️ Completa referencia y texto")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_biblia_volver_favoritos"):
                st.session_state.biblia_subview = "menu"
                st.rerun()

    # --- MÓDULO FINANZAS ---
    elif st.session_state.current_view == "finanzas":
        mostrar_breadcrumbs()
        st.markdown("<div class='title-glow'>💰 Finanzas</div>", unsafe_allow_html=True)
        
        if st.session_state.finanzas_subview == "menu":
            st.markdown("<p class='subtitle-text'>Tu centro de control financiero.</p>", unsafe_allow_html=True)
            
            opciones_finanzas = [
                ("💸", "Gastos", "gastos", "finanzas-icon"),
                ("💵", "Ingresos", "ingresos", "ideas-icon"),
                ("📊", "Reportes", "reportes", "libros-icon"),
                ("🎯", "Presupuestos", "presupuestos", "tarot-icon"),
                ("🏷️", "Categorías", "categorias", "frases-icon"),
                ("📈", "Estadísticas", "estadisticas", "biblia-icon")
            ]
            
            rows_finanzas = [opciones_finanzas[i:i+3] for i in range(0, len(opciones_finanzas), 3)]
            for row in rows_finanzas:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    if idx < len(row):
                        with cols[idx]:
                            st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                            if st.button(f"Ver {label}", key=f"btn_finanzas_{sub_key}", use_container_width=True):
                                st.session_state.finanzas_subview = sub_key
                                st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Botón de exportar
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                if st.button("📥 Exportar a CSV", key="btn_exportar_finanzas", use_container_width=True):
                    csv_data = finanzas_handler.exportar_a_csv()
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        label="💾 Descargar CSV",
                        data=csv_data,
                        file_name=f"finanzas_{timestamp}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="btn_download_csv_finanzas"
                    )
            with col3:
                if st.button("🏠 Menú Principal", key="btn_finanzas_home", use_container_width=True):
                    st.session_state.current_view = "menu"
                    st.rerun()
        
        elif st.session_state.finanzas_subview == "gastos":
            st.markdown("### 💸 Gestión de Gastos")
            
            tab1, tab2, tab3, tab4 = st.tabs(["➕ Agregar", "📋 Ver Todos", "🔍 Buscar", "🗑️ Borrar"])
            
            with tab1:
                monto = st.number_input("Monto del gasto:", min_value=0.0, step=0.01, key="input_monto_gasto")
                categoria = st.selectbox("Categoría (auto si dejas vacío):", [""] + list(finanzas_handler.CATEGORIAS.keys()), key="select_categoria_gasto")
                descripcion = st.text_input("Descripción:", placeholder="Ej: Almuerzo en restaurante", key="input_desc_gasto")
                if st.button("💰 Agregar Gasto", use_container_width=True, key="btn_agregar_gasto"):
                    if monto > 0 and descripcion:
                        res = finanzas_handler.agregar_gasto(monto, categoria, descripcion)
                        st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Completa todos los campos")
            
            with tab2:
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📘 Todos", use_container_width=True, key="btn_ver_todos_gastos"):
                        res = finanzas_handler.listar_gastos()
                        st.markdown(f'<div class="result-card" style="text-align:left; max-height:400px; overflow-y:auto;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("📅 Hoy", use_container_width=True, key="btn_gastos_hoy"):
                        res = finanzas_handler.gastos_de_hoy()
                        st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                with col3:
                    if st.button("🏷️ Por Categoría", use_container_width=True, key="btn_gastos_cat"):
                        cat_buscar = st.selectbox("Elige categoría:", list(finanzas_handler.CATEGORIAS.keys()), key="select_cat_buscar")
                        if cat_buscar:
                            res = finanzas_handler.gastos_por_categoria(cat_buscar)
                            st.markdown(f'<div class="result-card" style="text-align:left;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            with tab3:
                palabra = st.text_input("Buscar por palabra clave:", placeholder="Ej: restaurante", key="input_buscar_gasto")
                if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_gasto"):
                    if palabra:
                        res = finanzas_handler.buscar_gastos(palabra)
                        st.markdown(f'<div class="result-card" style="text-align:left;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Escribe una palabra primero")
            
            with tab4:
                id_gasto = st.number_input("ID del gasto a borrar:", min_value=1, step=1, key="input_id_gasto_borrar")
                confirmar_borrar_gasto = st.checkbox("⚠️ Confirmo que quiero eliminar este gasto", key="check_confirmar_borrar_gasto")
                if st.button("🗑️ Confirmar Borrado", use_container_width=True, key="btn_borrar_gasto", disabled=not confirmar_borrar_gasto):
                    res = finanzas_handler.borrar_gasto(id_gasto)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
                if not confirmar_borrar_gasto:
                    st.caption("✋ Marca la casilla para habilitar el botón")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_gastos"):
                st.session_state.finanzas_subview = "menu"
                st.rerun()
        
        elif st.session_state.finanzas_subview == "ingresos":
            st.markdown("### 💵 Gestión de Ingresos")
            
            tab1, tab2, tab3 = st.tabs(["➕ Agregar", "📋 Ver Todos", "🗑️ Borrar"])
            
            with tab1:
                monto_ing = st.number_input("Monto del ingreso:", min_value=0.0, step=0.01, key="input_monto_ingreso")
                desc_ing = st.text_input("Descripción:", placeholder="Ej: Salario mensual", key="input_desc_ingreso")
                if st.button("💵 Agregar Ingreso", use_container_width=True, key="btn_agregar_ingreso"):
                    if monto_ing > 0 and desc_ing:
                        res = finanzas_handler.agregar_ingreso(monto_ing, desc_ing)
                        st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Completa todos los campos")
            
            with tab2:
                if st.button("📘 Ver Todos", use_container_width=True, key="btn_ver_ingresos"):
                    res = finanzas_handler.listar_ingresos()
                    st.markdown(f'<div class="result-card" style="text-align:left; max-height:400px; overflow-y:auto;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            with tab3:
                id_ing = st.number_input("ID del ingreso a borrar:", min_value=1, step=1, key="input_id_ingreso_borrar")
                st.warning("⚠️ Esta acción no se puede deshacer")
                if st.button("🗑️ Confirmar Borrado", use_container_width=True, key="btn_borrar_ingreso"):
                    res = finanzas_handler.borrar_ingreso(id_ing)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_ingresos"):
                st.session_state.finanzas_subview = "menu"
                st.rerun()
        
        elif st.session_state.finanzas_subview == "reportes":
            st.markdown("### 📊 Reportes Financieros")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📅 Resumen Mensual", use_container_width=True, key="btn_resumen_mes"):
                    res = finanzas_handler.resumen_mensual()
                    st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("📈 Comparar Meses", use_container_width=True, key="btn_comparar_meses"):
                    res = finanzas_handler.comparar_meses()
                    st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_reportes"):
                st.session_state.finanzas_subview = "menu"
                st.rerun()
        
        elif st.session_state.finanzas_subview == "presupuestos":
            st.markdown("### 🎯 Gestión de Presupuestos")
            
            tab1, tab2 = st.tabs(["➕ Establecer", "📊 Ver Estado"])
            
            with tab1:
                cat_pres = st.selectbox("Categoría:", list(finanzas_handler.CATEGORIAS.keys()), key="select_cat_presupuesto")
                monto_pres = st.number_input("Presupuesto mensual:", min_value=0.0, step=0.01, key="input_monto_presupuesto")
                if st.button("✅ Establecer Presupuesto", use_container_width=True, key="btn_set_presupuesto"):
                    if monto_pres > 0:
                        res = finanzas_handler.establecer_presupuesto(cat_pres, monto_pres)
                        st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ El monto debe ser mayor a 0")
            
            with tab2:
                if st.button("📊 Ver Presupuestos", use_container_width=True, key="btn_ver_presupuestos"):
                    res = finanzas_handler.ver_presupuestos()
                    st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_presupuestos"):
                st.session_state.finanzas_subview = "menu"
                st.rerun()
        
        elif st.session_state.finanzas_subview == "categorias":
            st.markdown("### 🏷️ Categorías Disponibles")
            res = finanzas_handler.ver_categorias()
            st.markdown(f'<div class="result-card" style="text-align:left;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_categorias"):
                st.session_state.finanzas_subview = "menu"
                st.rerun()
        
        elif st.session_state.finanzas_subview == "estadisticas":
            st.markdown("### 📈 Estadísticas Avanzadas")
            
            stats = finanzas_handler.estadisticas_avanzadas()
            
            if stats:
                # Métricas principales
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Este Mes", f"${stats['total_mes']:.2f}")
                with col2:
                    st.metric("Promedio Diario", f"${stats['promedio_diario']:.2f}")
                with col3:
                    st.metric("Balance", f"${stats['balance']:.2f}",
                             delta=f"${stats['balance']:.2f}" if stats['balance'] >= 0 else None)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Proyección y comparación
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**📊 Proyección del Mes:**")
                    st.metric("Proyección", f"${stats['proyeccion_mes']:.2f}",
                             help=f"Basado en ${stats['promedio_diario']:.2f}/día × 30 días")
                    st.caption(f"Llevamos {stats['dia_actual']} días del mes")
                
                with col2:
                    st.markdown("**📉 Comparación con Mes Anterior:**")
                    cambio_emoji = "📈" if stats['diferencia'] > 0 else "📉" if stats['diferencia'] < 0 else "➡️"
                    st.metric(
                        "Diferencia", 
                        f"${abs(stats['diferencia']):.2f}",
                        delta=f"{stats['porcentaje_cambio']:+.1f}%"
                    )
                    if stats['diferencia'] > 0:
                        st.caption(f"{cambio_emoji} Gastaste MÁS que el mes pasado")
                    elif stats['diferencia'] < 0:
                        st.caption(f"{cambio_emoji} Gastaste MENOS que el mes pasado")
                    else:
                        st.caption(f"{cambio_emoji} Gasto similar al mes pasado")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Top categorías
                st.markdown("**🏆 Top 3 Categorías Este Mes:**")
                for i, (cat, monto) in enumerate(stats['top_categorias'], 1):
                    porcentaje = (monto / stats['total_mes'] * 100) if stats['total_mes'] > 0 else 0
                    st.progress(porcentaje / 100, text=f"{i}. {cat}: ${monto:.2f} ({porcentaje:.1f}%)")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Métricas adicionales
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Ingresos Este Mes", f"${stats['ingresos_mes']:.2f}")
                with col2:
                    st.metric("Número de Gastos", stats['num_gastos'])
                with col3:
                    st.metric("Gasto Promedio", f"${stats['gasto_promedio']:.2f}")
                
                # Recomendaciones
                st.markdown("<br>", unsafe_allow_html=True)
                if stats['balance'] < 0:
                    st.warning(f"⚠️ Estás gastando ${abs(stats['balance']):.2f} más de lo que ingresas")
                elif stats['balance'] > 0:
                    st.success(f"✨ ¡Excelente! Tienes un superávit de ${stats['balance']:.2f}")
                else:
                    st.info("➡️ Tus ingresos y gastos están equilibrados")
                
            else:
                st.info("No hay suficientes datos para generar estadísticas. ¡Agrega algunos gastos!")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_stats_finanzas"):
                st.session_state.finanzas_subview = "menu"
                st.rerun()

    # --- MÓDULO NOTAS ---
    elif st.session_state.current_view == "notas":
        st.markdown("<div class='title-glow'>📝 Notas</div>", unsafe_allow_html=True)
        
        if st.session_state.notas_subview == "menu":
            st.markdown("<p class='subtitle-text'>Tu espacio de pensamientos y recordatorios.</p>", unsafe_allow_html=True)
            
            opciones_notas = [
                ("➕", "Agregar Nota", "agregar", "notas-icon"),
                ("📘", "Ver Notas", "ver", "libros-icon"),
                ("⭐", "Importantes", "importantes", "tarot-icon"),
                ("🔍", "Buscar", "buscar", "ideas-icon"),
                ("📊", "Estadísticas", "stats", "finanzas-icon"),
                ("⏰", "Recordatorios", "recordatorios", "frases-icon")
            ]
            
            rows_notas = [opciones_notas[i:i+3] for i in range(0, len(opciones_notas), 3)]
            for row in rows_notas:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    with cols[idx]:
                        st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                        if st.button(f"Ver {label}", key=f"btn_notas_{sub_key}", use_container_width=True):
                            st.session_state.notas_subview = sub_key
                            st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏠 Menú Principal", key="btn_notas_home", use_container_width=True):
                st.session_state.current_view = "menu"
                st.rerun()
        
        elif st.session_state.notas_subview == "agregar":
            st.markdown("### ➕ Agregar Nueva Nota")
            texto_nota = st.text_area("Contenido de la nota:", height=150, key="input_texto_nota")
            categoria_nota = st.selectbox("Categoría:", notas_handler.CATEGORIAS, key="select_categoria_nota")
            importante = st.checkbox("⭐ Marcar como importante", key="check_importante")
            recordatorio = st.text_input("Recordatorio (opcional):", placeholder="Ej: 2024-12-31 14:00", key="input_recordatorio")
            
            if st.button("✅ Guardar Nota", use_container_width=True, key="btn_guardar_nota"):
                if texto_nota:
                    res = notas_handler.agregar_nota(texto_nota, categoria_nota, importante, recordatorio if recordatorio else None)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Escribe algo en la nota primero")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_agregar_nota"):
                st.session_state.notas_subview = "menu"
                st.rerun()
        
        elif st.session_state.notas_subview == "ver":
            st.markdown("### 📘 Ver Notas")
            
            filtro_opciones = ["Todas", "Hoy", "Esta semana", "Este mes"]
            filtro = st.selectbox("Filtrar por:", filtro_opciones, key="select_filtro_notas")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Ver Notas", use_container_width=True, key="btn_ver_notas_filtradas"):
                    filtro_map = {"Todas": None, "Hoy": "hoy", "Esta semana": "semana", "Este mes": "mes"}
                    res = notas_handler.ver_notas(filtro_map[filtro])
                    st.markdown(f'<div class="result-card" style="text-align:left; max-height:400px; overflow-y:auto;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("📂 Por Categoría", use_container_width=True, key="btn_notas_por_cat"):
                    res = notas_handler.ver_notas_por_categoria()
                    st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🔧 Acciones con Notas")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                id_ver = st.number_input("ID nota:", min_value=1, step=1, key="input_id_ver_completa")
                if st.button("👁️ Ver Completa", key="btn_ver_completa"):
                    res = notas_handler.ver_nota_completa(id_ver)
                    st.markdown(f'<div class="result-card" style="text-align:left;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            with col2:
                id_importancia = st.number_input("ID nota:", min_value=1, step=1, key="input_id_importancia")
                if st.button("⭐ Marcar Importante", key="btn_marcar_importante"):
                    res = notas_handler.marcar_importante(id_importancia, True)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
            
            with col3:
                id_borrar = st.number_input("ID nota:", min_value=1, step=1, key="input_id_borrar_nota")
                confirmar_borrar = st.checkbox("⚠️ Confirmo que quiero eliminar", key="check_confirmar_borrar_nota")
                if st.button("🗑️ Borrar", key="btn_borrar_nota", disabled=not confirmar_borrar):
                    res = notas_handler.borrar_nota(id_borrar)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
                if not confirmar_borrar:
                    st.caption("✋ Marca la casilla para habilitar")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_ver_notas"):
                st.session_state.notas_subview = "menu"
                st.rerun()
        
        elif st.session_state.notas_subview == "importantes":
            st.markdown("### ⭐ Notas Importantes")
            res = notas_handler.ver_notas("importantes")
            st.markdown(f'<div class="result-card" style="text-align:left; max-height:400px; overflow-y:auto;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_importantes"):
                st.session_state.notas_subview = "menu"
                st.rerun()
        
        elif st.session_state.notas_subview == "buscar":
            st.markdown("### 🔍 Buscar Notas")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                palabra_clave = st.text_input("Palabra clave:", placeholder="Ej: reunión", key="input_palabra_clave_nota")
            with col2:
                categoria_filtro = st.selectbox("Categoría:", ["Todas"] + notas_handler.CATEGORIAS, key="select_categoria_filtro")
            
            if palabra_clave or categoria_filtro != "Todas":
                # Buscar por palabra clave primero
                if palabra_clave:
                    resultados = notas_handler.buscar_notas(palabra_clave)
                else:
                    resultados = notas_handler._cargar_notas()
                
                # Filtrar por categoría si no es "Todas"
                if categoria_filtro != "Todas":
                    resultados = [n for n in resultados if n.get('categoria', '') == categoria_filtro]
                
                if resultados:
                    st.success(f"✅ {len(resultados)} nota(s) encontrada(s)")
                    for nota in resultados:
                        with st.expander(f"📝 {nota['texto'][:50]}..." if len(nota['texto']) > 50 else f"📝 {nota['texto']}", expanded=False):
                            st.markdown(f"**Contenido:** {nota['texto']}")
                            st.markdown(f"**Categoría:** {nota.get('categoria', '📄 Otros')}")
                            st.markdown(f"**Fecha:** {nota.get('fecha_creacion', 'N/A')}")
                            if nota.get('importante'):
                                st.markdown("⭐ **Importante**")
                else:
                    if palabra_clave and categoria_filtro != "Todas":
                        st.info(f"No se encontraron notas con '{palabra_clave}' en categoría '{categoria_filtro}'")
                    elif palabra_clave:
                        st.info(f"No se encontraron notas con '{palabra_clave}'")
                    else:
                        st.info(f"No hay notas en la categoría '{categoria_filtro}'")
            else:
                st.info("💡 Escribe una palabra clave y/o selecciona una categoría para buscar")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_buscar_nota"):
                st.session_state.notas_subview = "menu"
                st.rerun()
        
        elif st.session_state.notas_subview == "stats":
            st.markdown("### 📊 Estadísticas de Notas")
            res = notas_handler.estadisticas_notas()
            st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_stats"):
                st.session_state.notas_subview = "menu"
                st.rerun()
        
        elif st.session_state.notas_subview == "recordatorios":
            st.markdown("### ⏰ Recordatorios Pendientes")
            res = notas_handler.ver_recordatorios()
            st.markdown(f'<div class="result-card" style="text-align:left;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_recordatorios"):
                st.session_state.notas_subview = "menu"
                st.rerun()

 # --- MÓDULO LIBROS ---
    elif st.session_state.current_view == "libros":
        st.markdown("<div class='title-glow'>📚 Libros</div>", unsafe_allow_html=True)
        
        if st.session_state.libros_subview == "menu":
            st.markdown("<p class='subtitle-text'>Tu biblioteca personal y generador de arte.</p>", unsafe_allow_html=True)
            
            opciones_libros = [
                ("🔍", "Buscar Libro", "buscar", "libros-icon"),
                ("🎨", "Generar Arte", "arte", "ideas-icon"),
                ("📖", "Info del Libro", "info", "notas-icon"),
                ("⭐", "Mis Reseñas", "resenas", "frases-icon"),
                ("📚", "Book Club", "bookclub", "biblia-icon")
            ]
            
            rows_libros = [opciones_libros[i:i+3] for i in range(0, len(opciones_libros), 3)]
            for row in rows_libros:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    if idx < len(row):
                        with cols[idx]:
                            st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                            if st.button(f"Abrir {label}", key=f"btn_libros_{sub_key}", use_container_width=True):
                                st.session_state.libros_subview = sub_key
                                st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏠 Menú Principal", key="btn_libros_home", use_container_width=True):
                st.session_state.current_view = "menu"
                st.rerun()
        
        elif st.session_state.libros_subview == "buscar":
            st.markdown("### 🔍 Buscar Libro")
            titulo_buscar = st.text_input("Título o autor:", placeholder="Ej: Cien años de soledad", key="input_buscar_libro")
            if st.button("📖 Buscar", use_container_width=True, key="btn_buscar_libro"):
                if titulo_buscar:
                    res = libros_handler.buscar_libro(titulo_buscar)
                    st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Escribe un título primero")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_buscar_libro"):
                st.session_state.libros_subview = "menu"
                st.rerun()
        
        elif st.session_state.libros_subview == "arte":
            st.markdown("### 🎨 Generar Arte Inspirado")
            
            tipo_arte = st.selectbox("Tipo de arte:", [
                "Ilustración del libro",
                "Fanart del libro",
                "Estética del libro",
                "Arte por género",
                "Arte por autor"
            ], key="select_tipo_arte")
            
            if tipo_arte in ["Ilustración del libro", "Fanart del libro", "Estética del libro"]:
                titulo_arte = st.text_input("Título del libro:", key="input_titulo_arte")
            elif tipo_arte == "Arte por género":
                titulo_arte = st.text_input("Género literario:", placeholder="Ej: ciencia ficción", key="input_genero_arte")
            else:
                titulo_arte = st.text_input("Nombre del autor:", key="input_autor_arte")
            
            if st.button("🎨 Generar Imagen", use_container_width=True, key="btn_generar_arte"):
                if titulo_arte:
                    with st.spinner("🎨 Generando arte con DALL-E 3... (puede tardar 30-60 seg)"):
                        if tipo_arte == "Ilustración del libro":
                            url = libros_handler.imagen_de_libro(titulo_arte)
                        elif tipo_arte == "Fanart del libro":
                            url = libros_handler.fanart_libro(titulo_arte)
                        elif tipo_arte == "Estética del libro":
                            url = libros_handler.estetica_libro(titulo_arte)
                        elif tipo_arte == "Arte por género":
                            url = libros_handler.imagen_genero(titulo_arte)
                        else:
                            url = libros_handler.imagen_autor(titulo_arte)
                        
                        if url:
                            st.session_state.libros_imagen = url
                            st.image(url, caption=f"Arte generado para: {titulo_arte}", use_container_width=True)
                        else:
                            st.error("❌ No se pudo generar la imagen. Verifica tu API key de OpenAI.")
                else:
                    st.warning("⚠️ Completa el campo primero")
            
            if st.session_state.get("libros_imagen"):
                st.markdown(f"[🔗 Descargar imagen]({st.session_state.libros_imagen})")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_arte"):
                st.session_state.libros_subview = "menu"
                st.session_state.libros_imagen = None
                st.rerun()
        
        elif st.session_state.libros_subview == "info":
            st.markdown("### 📖 Información del Libro")
            st.info("✨ Usa la opción 'Buscar Libro' para obtener información detallada")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_info"):
                st.session_state.libros_subview = "menu"
                st.rerun()
        
        elif st.session_state.libros_subview == "resenas":
            st.markdown("### ⭐ Mis Reseñas de Libros")
            
            # Ver reseñas existentes
            libros = libros_handler.ver_libros_con_resenas()
            
            if libros:
                st.success(f"✅ Tienes {len(libros)} libro(s) reseñado(s)")
                for libro in libros:
                    with st.expander(f"📚 {libro['titulo']} - {'⭐' * libro['rating']}", expanded=False):
                        st.markdown(f"**Rating:** {'⭐' * libro['rating']} ({libro['rating']}/5)")
                        st.markdown(f"**Reseña:** {libro['resena']}")
                        st.caption(f"Fecha: {libro.get('fecha_resena', 'N/A')}")
                        if st.button("🗑️ Eliminar", key=f"btn_eliminar_resena_{libro['id']}"):
                            libros_handler.eliminar_resena(libro['id'])
                            st.success("Reseña eliminada")
                            st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("No tienes reseñas aún. ¡Agrega la primera!")
            
            # Agregar nueva reseña
            st.markdown("### ➕ Agregar Reseña")
            
            titulo_libro = st.text_input("Título del libro:", key="input_titulo_resena")
            rating = st.select_slider("Rating:", options=[1, 2, 3, 4, 5], value=3, key="slider_rating")
            texto_resena = st.text_area("Tu reseña:", height=120, 
                                        placeholder="¿Qué te pareció este libro?", 
                                        key="input_texto_resena")
            
            if st.button("⭐ Guardar Reseña", use_container_width=True, key="btn_guardar_resena"):
                if titulo_libro and texto_resena:
                    exito, mensaje = libros_handler.agregar_resena(titulo_libro, rating, texto_resena)
                    if exito:
                        st.success(mensaje)
                        st.rerun()
                else:
                    st.warning("⚠️ Completa título y reseña")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_resenas"):
                st.session_state.libros_subview = "menu"
                st.rerun()
        
        elif st.session_state.libros_subview == "bookclub":
            st.markdown("### 📚 Book Club")
            st.markdown("<p style='color:#d8c9ff;'>Tu espacio de lectura consciente - Ritual personal cada jueves</p>", unsafe_allow_html=True)
            
            bookclub = libros_handler.ver_bookclub()
            
            # Libro actual
            st.markdown("### 📖 Libro Actual")
            if bookclub.get('libro_actual'):
                libro = bookclub['libro_actual']
                st.success(f"📚 **{libro['titulo']}**")
                if libro.get('autor'):
                    st.caption(f"Autor: {libro['autor']}")
                st.caption(f"Inicio: {libro.get('fecha_inicio', 'N/A')}")
            else:
                st.info("No hay libro actual. ¡Establece uno!")
            
            # Establecer nuevo libro
            with st.expander("📖 Establecer Nuevo Libro", expanded=False):
                titulo_club = st.text_input("Título del libro:", key="input_titulo_bookclub")
                autor_club = st.text_input("Autor (opcional):", key="input_autor_bookclub")
                if st.button("📚 Establecer como Libro Actual", use_container_width=True, key="btn_establecer_libro"):
                    if titulo_club:
                        exito, mensaje = libros_handler.establecer_libro_actual(titulo_club, autor_club)
                        if exito:
                            st.success(mensaje)
                            st.rerun()
                    else:
                        st.warning("⚠️ Escribe el título del libro")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tabs para diferentes secciones
            tab1, tab2, tab3 = st.tabs(["📅 Check-ins", "🎭 Facetas", "💭 Preguntas"])
            
            with tab1:
                st.markdown("### 📅 Mis Check-ins de Lectura")
                
                reuniones = bookclub.get('reuniones', [])
                if reuniones:
                    # Mostrar últimas 5 reuniones
                    for reunion in sorted(reuniones, key=lambda x: x.get('fecha', ''), reverse=True)[:5]:
                        with st.expander(f"📅 {reunion.get('fecha', 'N/A')} - {reunion.get('tema', 'Sin tema')}", expanded=False):
                            st.markdown(f"**Libro:** {reunion.get('libro', 'N/A')}")
                            st.markdown(f"**Procesando:** {reunion.get('tema', 'N/A')}")
                            if reunion.get('notas'):
                                st.markdown(f"**Reflexiones:** {reunion['notas']}")
                            st.caption(f"Creada: {reunion.get('fecha_creacion', 'N/A')}")
                            if st.button("🗑️ Eliminar", key=f"btn_eliminar_reunion_{reunion['id']}"):
                                libros_handler.eliminar_reunion(reunion['id'])
                                st.success("Check-in eliminado")
                                st.rerun()
                else:
                    st.info("No tienes check-ins registrados aún")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### ✨ Registrar Check-in")
                
                col1, col2 = st.columns(2)
                with col1:
                    fecha_reunion = st.date_input("Fecha de mi check-in:", key="input_fecha_reunion")
                with col2:
                    tema_reunion = st.text_input("¿Qué estoy procesando?", key="input_tema_reunion", 
                                                 placeholder="Ej: Capítulos 1-5: Resistencia al cambio")
                
                notas_reunion = st.text_area("Cómo me sentí / Qué descubrí:", height=100, key="input_notas_reunion",
                                            placeholder="Mis reflexiones, emociones, insights...")
                
                if st.button("✨ Registrar Check-in", use_container_width=True, key="btn_agregar_reunion"):
                    if tema_reunion:
                        fecha_str = fecha_reunion.strftime("%Y-%m-%d")
                        exito, mensaje = libros_handler.agregar_reunion(fecha_str, tema_reunion, notas_reunion)
                        if exito:
                            st.success("Check-in registrado")
                            st.rerun()
                    else:
                        st.warning("⚠️ Escribe qué estás procesando")
            
            with tab2:
                st.markdown("### 🎭 Mis Facetas Lectoras")
                
                miembros = bookclub.get('miembros', [])
                if miembros:
                    st.success(f"✅ {len(miembros)} faceta(s) lectora(s)")
                    for miembro in miembros:
                        with st.expander(f"🎭 {miembro.get('nombre', 'N/A')}", expanded=False):
                            if miembro.get('email'):
                                st.markdown(f"**Intención:** {miembro['email']}")
                            st.caption(f"Creada: {miembro.get('fecha_union', 'N/A')}")
                else:
                    st.info("No tienes facetas registradas aún. ¡Crea tu primera!")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### ✨ Crear Faceta")
                
                col1, col2 = st.columns(2)
                with col1:
                    nombre_miembro = st.text_input("Nombre de esta faceta:", key="input_nombre_miembro",
                                                   placeholder="Ej: La Mística, La Analítica, La Soñadora...")
                with col2:
                    email_miembro = st.text_input("Intención de lectura (opcional):", key="input_email_miembro",
                                                  placeholder="Ej: Busco inspiración, Necesito claridad...")
                
                if st.button("✨ Crear Faceta", use_container_width=True, key="btn_agregar_miembro"):
                    if nombre_miembro:
                        exito, mensaje = libros_handler.agregar_miembro(nombre_miembro, email_miembro)
                        if exito:
                            st.success(f"Faceta '{nombre_miembro}' creada")
                            st.rerun()
                        else:
                            st.warning("Esta faceta ya existe")
                    else:
                        st.warning("⚠️ Dale un nombre a esta faceta")
            
            with tab3:
                st.markdown("### 💭 Preguntas que me Transforman")
                
                discusiones = bookclub.get('discusiones', [])
                if discusiones:
                    # Agrupar por libro
                    discusiones_por_libro = {}
                    for disc in discusiones:
                        libro = disc.get('libro', 'Sin libro')
                        if libro not in discusiones_por_libro:
                            discusiones_por_libro[libro] = []
                        discusiones_por_libro[libro].append(disc)
                    
                    for libro, discs in discusiones_por_libro.items():
                        st.markdown(f"**📖 {libro}** ({len(discs)} pregunta(s))")
                        for disc in discs:
                            with st.expander(f"❓ {disc.get('pregunta', 'N/A')[:80]}...", expanded=False):
                                st.markdown(f"**Pregunta:** {disc['pregunta']}")
                                if disc.get('respuesta'):
                                    st.markdown(f"**Mi Reflexión:** {disc['respuesta']}")
                                st.caption(f"Fecha: {disc.get('fecha', 'N/A')}")
                        st.markdown("<br>", unsafe_allow_html=True)
                else:
                    st.info("No tienes preguntas registradas aún")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### ✨ Registrar Pregunta")
                
                pregunta_disc = st.text_area("¿Qué me está preguntando este libro?", height=80, 
                                             key="input_pregunta_disc",
                                             placeholder="Ej: ¿Qué estoy posponiendo por miedo? ¿Qué parte de mí se resiste?")
                respuesta_disc = st.text_area("Mi reflexión actual (opcional):", height=100,
                                              key="input_respuesta_disc",
                                              placeholder="Puede evolucionar con el tiempo...")
                
                if st.button("✨ Registrar Pregunta", use_container_width=True, key="btn_agregar_discusion"):
                    if pregunta_disc:
                        exito, mensaje = libros_handler.agregar_discusion(pregunta_disc, respuesta_disc)
                        if exito:
                            st.success("Pregunta registrada")
                            st.rerun()
                    else:
                        st.warning("⚠️ Escribe una pregunta")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_bookclub"):
                st.session_state.libros_subview = "menu"
                st.rerun()
        
           # --- MÓDULO FRASES ---
    elif st.session_state.current_view == "frases":
        st.markdown("<div class='title-glow'>💬 Frases</div>", unsafe_allow_html=True)
        
        if st.session_state.frases_subview == "menu":
            st.markdown("<p class='subtitle-text'>Tu dosis diaria de inspiración y motivación.</p>", unsafe_allow_html=True)
            
            opciones_frases = [
                ("🌅", "Frase del Día", "fdia", "frases-icon"),
                ("🎯", "Por Categoría", "categoria", "finanzas-icon"),
                ("✨", "Personalizada", "personalizada", "ideas-icon"),
                ("🎯", "Afirmaciones", "afirmaciones", "tarot-icon"),
                ("📖", "Journal Gratitud", "journal", "notas-icon"),
                ("⭐", "Favoritas", "favoritas", "libros-icon")
            ]
            
            rows_frases = [opciones_frases[i:i+3] for i in range(0, len(opciones_frases), 3)]
            for row in rows_frases:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    with cols[idx]:
                        st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                        if st.button(f"Ver {label}", key=f"btn_frases_{sub_key}", use_container_width=True):
                            st.session_state.frases_subview = sub_key
                            st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏠 Menú Principal", key="btn_frases_home", use_container_width=True):
                st.session_state.current_view = "menu"
                st.rerun()
        
        elif st.session_state.frases_subview == "fdia":
            st.markdown("### 🌅 Frase del Día")
            res = frases_handler.frase_del_dia()
            st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_fdia"):
                st.session_state.frases_subview = "menu"
                st.rerun()
        
        elif st.session_state.frases_subview == "categoria":
            st.markdown("### 🎯 Frase por Categoría")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                cat_frase = st.selectbox("Elige una categoría:", list(frases_handler.CATEGORIAS_FRASES.keys()), key="select_cat_frase")
            with col2:
                if st.button("📚 Ver Categorías", key="btn_ver_cats_frases"):
                    res = frases_handler.listar_categorias()
                    st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            if st.button("✨ Generar Frase", use_container_width=True, key="btn_frase_categoria"):
                if cat_frase:
                    res = frases_handler.frase_por_categoria(cat_frase)
                    st.markdown(f'<div class="result-card">_{res}_</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_categoria"):
                st.session_state.frases_subview = "menu"
                st.rerun()
        
        elif st.session_state.frases_subview == "personalizada":
            st.markdown("### ✨ Frase Personalizada")
            mood = st.text_input("¿Cómo te sientes?", placeholder="Ej: ansiosa, feliz, cansada...", key="input_mood")
            situacion = st.text_area("¿Qué estás atravesando?", height=100, key="input_situacion")
            
            if st.button("💫 Generar Frase", use_container_width=True, key="btn_frase_personalizada"):
                res = frases_handler.generar_frase_personalizada(mood, situacion, personalidades_handler)
                st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_personalizada"):
                st.session_state.frases_subview = "menu"
                st.rerun()
        
        elif st.session_state.frases_subview == "afirmaciones":
            st.markdown("### 🎯 Afirmaciones Personalizadas")
            area_afirm = st.text_input("¿Para qué área?", placeholder="Ej: amor propio, abundancia, trabajo...", key="input_area_afirm")
            cantidad = st.slider("¿Cuántas afirmaciones?", 3, 10, 5, key="slider_cantidad_afirm")
            
            if st.button("✨ Generar Afirmaciones", use_container_width=True, key="btn_generar_afirm"):
                if area_afirm:
                    res = frases_handler.generar_afirmaciones_personalizadas(area_afirm, cantidad, personalidades_handler)
                    st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Escribe el área primero")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_afirmaciones"):
                st.session_state.frases_subview = "menu"
                st.rerun()
        
        elif st.session_state.frases_subview == "journal":
            st.markdown("### 📖 Journal de Gratitud")
            
            tab1, tab2, tab3 = st.tabs(["➕ Nueva Entrada", "📘 Ver Journal", "📊 Estadísticas"])
            
            with tab1:
                gratitud = st.text_area("¿Por qué estás agradecida hoy?", height=150, key="input_gratitud")
                if st.button("💛 Guardar en Journal", use_container_width=True, key="btn_guardar_gratitud"):
                    if gratitud:
                        res = frases_handler.agregar_entrada_journal(gratitud, personalidades_handler)
                        st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Escribe algo primero")
            
            with tab2:
                filtro_journal = st.selectbox("Filtrar por:", ["Todos", "Hoy", "Esta semana", "Este mes"], key="select_filtro_journal")
                if st.button("📖 Ver Entradas", use_container_width=True, key="btn_ver_journal"):
                    filtro_map = {"Todos": "todos", "Hoy": "hoy", "Esta semana": "semana", "Este mes": "mes"}
                    res = frases_handler.ver_journal(filtro_map[filtro_journal])
                    st.markdown(f'<div class="result-card" style="text-align:left; max-height:400px; overflow-y:auto;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            with tab3:
                if st.button("📊 Ver Estadísticas", use_container_width=True, key="btn_stats_journal"):
                    res = frases_handler.estadisticas_journal()
                    st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_journal"):
                st.session_state.frases_subview = "menu"
                st.rerun()
        
        elif st.session_state.frases_subview == "favoritas":
            st.markdown("### ⭐ Frases Favoritas")
            
            tab1, tab2, tab3 = st.tabs(["➕ Agregar", "👁️ Ver Todas", "🗑️ Borrar"])
            
            with tab1:
                frase_nueva = st.text_area("Escribe la frase para guardar:", height=100, key="input_nueva_fav")
                if st.button("⭐ Guardar en Favoritas", use_container_width=True, key="btn_guardar_fav"):
                    if frase_nueva:
                        res = frases_handler.agregar_favorita(frase_nueva)
                        st.success(res)
                    else:
                        st.warning("⚠️ Escribe una frase primero")
            
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Ver Todas", use_container_width=True, key="btn_ver_todas_fav"):
                        res = frases_handler.ver_favoritas()
                        st.markdown(f'<div class="result-card" style="text-align:left; max-height:400px; overflow-y:auto;">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("🎲 Frase Aleatoria", use_container_width=True, key="btn_fav_random"):
                        res = frases_handler.favorita_aleatoria()
                        st.markdown(f'<div class="result-card">{res.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            with tab3:
                id_fav = st.number_input("ID de la frase a borrar:", min_value=1, step=1, key="input_id_fav_borrar")
                st.warning("⚠️ Esta acción no se puede deshacer")
                if st.button("🗑️ Confirmar Borrado", use_container_width=True, key="btn_borrar_fav"):
                    res = frases_handler.borrar_favorita(id_fav)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_volver_favoritas"):
                st.session_state.frases_subview = "menu"
                st.rerun()

    # --- MÓDULO PERSONALIDADES ---
    elif st.session_state.current_view == "personalidades":
        st.markdown("<div class='title-glow'>👤 Personalidades</div>", unsafe_allow_html=True)
        
        if st.session_state.personalidades_subview == "menu":
            st.markdown("<p class='subtitle-text'>Elige cómo quieres que te hable la IA.</p>", unsafe_allow_html=True)
            
            actual = personalidades_handler.obtener_personalidad_actual()
            st.markdown(f"""
            <div class="result-card" style="text-align:center;">
                <h3 style='color:#fbbf24;'>Personalidad Actual</h3>
                <p style='font-size:1.5rem; text-transform:capitalize;'><strong>{actual}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 😎 Selecciona una personalidad")
            
            personalidades_opciones = [
                ("bestie", "💛", "Bestie", "Cálida y amorosa", "frases-icon"),
                ("formal", "💼", "Formal", "Profesional", "profesional-icon"),
                ("espiritual", "🌟", "Espiritual", "Guía intuitiva", "oculto-icon"),
                ("psicologa", "🧠", "Psicóloga", "Empática y validante", "personalidades-icon"),
                ("honesta", "💪", "Honesta", "Directa y clara", "ideas-icon"),
                ("tecnico", "🔧", "Técnico", "Experta en tech", "finanzas-icon")
            ]
            
            rows = [personalidades_opciones[i:i+3] for i in range(0, len(personalidades_opciones), 3)]
            
            for row in rows:
                cols = st.columns(3, gap="small")
                for idx, (key, icon, nombre, desc, css) in enumerate(row):
                    with cols[idx]:
                        st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{nombre}</div><p style="font-size:0.85rem; margin-top:5px;">{desc}</p></div>', unsafe_allow_html=True)
                        if st.button(f"Activar {nombre}", key=f"btn_pers_{key}", use_container_width=True):
                            res = personalidades_handler.cambiar_personalidad(key)
                            st.success(res)
                            st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
            
            with st.expander("ℹ️ ¿Qué hace cada personalidad?"):
                for key, icon, nombre, desc, css in personalidades_opciones:
                    instruccion = personalidades_handler.obtener_descripcion_personalidad(key)
                    st.markdown(f"**{icon} {nombre}**")
                    st.markdown(f"_{instruccion}_")
                    st.markdown("---")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏠 Menú Principal", key="btn_pers_home", use_container_width=True):
                st.session_state.current_view = "menu"
                st.rerun()

    # --- LO OCULTO, IDEAS, ETC ---
    elif st.session_state.current_view == "lo_oculto":
        st.markdown("<div class='title-glow'>🌙 Lo Oculto</div>", unsafe_allow_html=True)
        if st.session_state.oculto_subview == "menu":
            opciones_oculto = [("🔮", "Tarot", "tarot", "tarot-icon"), ("⭐", "Astrología", "astrologia", "libros-icon"), ("🔢", "Numerología", "numerologia", "finanzas-icon")]
            cols = st.columns(3, gap="small")
            for idx, (icon, label, modulo, css) in enumerate(opciones_oculto):
                with cols[idx]:
                    st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                    if st.button(f"Abrir {label}", key=f"btn_oculto_{modulo}", use_container_width=True):
                        st.session_state.current_view = modulo
                        st.session_state.oculto_subview = "menu"
                        st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏠 Menú Principal", key="btn_oculto_home"): 
                st.session_state.current_view = "menu"
                st.rerun()
    
    # --- MÓDULO TAROT ---
    elif st.session_state.current_view == "tarot":
        st.markdown("<div class='title-glow'>🔮 Tarot</div>", unsafe_allow_html=True)
        
        if st.session_state.tarot_subview == "menu":
            st.markdown("<p class='subtitle-text'>Las cartas revelan lo que tu alma ya sabe.</p>", unsafe_allow_html=True)
            
            opciones_tarot = [
                ("✨", "Energía del Día", "energia", "tarot-icon"),
                ("🔮", "Tirada General", "tres_cartas", "libros-icon"),
                ("💕", "Tirada de Amor", "amor", "frases-icon"),
                ("💼", "Tirada de Trabajo", "trabajo", "finanzas-icon"),
                ("❓", "Pregunta Sí/No", "si_no", "ideas-icon"),
                ("📜", "Historial", "historial", "biblia-icon"),
                ("🏠", "Volver", "volver", "notas-icon")
            ]
            
            rows_tarot = [opciones_tarot[i:i+3] for i in range(0, len(opciones_tarot), 3)]
            for row in rows_tarot:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    if idx < len(row):
                        with cols[idx]:
                            st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                            if st.button(f"Abrir {label}" if sub_key != "volver" else label, key=f"btn_tarot_{sub_key}", use_container_width=True):
                                if sub_key == "volver":
                                    st.session_state.current_view = "lo_oculto"
                                    st.session_state.oculto_subview = "menu"
                                else:
                                    st.session_state.tarot_subview = sub_key
                                st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
        
        elif st.session_state.tarot_subview == "energia":
            st.markdown("### ✨ Energía del Día")
            st.markdown("<p style='color:#d8c9ff;'>Una carta para guiar tu jornada</p>", unsafe_allow_html=True)
            resultado = tarot.energia_del_dia()
            st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_tarot_volver_energia", use_container_width=True):
                st.session_state.tarot_subview = "menu"
                st.rerun()
        
        elif st.session_state.tarot_subview == "tres_cartas":
            st.markdown("### 🔮 Tirada General")
            st.markdown("<p style='color:#d8c9ff;'>Pasado, Presente y Futuro con interpretación de IA</p>", unsafe_allow_html=True)
            
            pregunta = st.text_area("¿Qué pregunta le haces a las cartas?", height=100, 
                                   placeholder="Ej: ¿Qué necesito saber sobre mi situación actual?", 
                                   key="input_pregunta_tarot")
            
            if st.button("🔮 Consultar las Cartas", use_container_width=True, key="btn_tirada_tres"):
                if pregunta:
                    with st.spinner("🌙 Las cartas están revelando su mensaje..."):
                        resultado = tarot.tirada_tres_cartas_ia(pregunta)
                    st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Escribe tu pregunta primero")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_tarot_volver_tres", use_container_width=True):
                st.session_state.tarot_subview = "menu"
                st.rerun()
        
        elif st.session_state.tarot_subview == "amor":
            st.markdown("### 💕 Tirada de Amor")
            st.markdown("<p style='color:#d8c9ff;'>Tu energía, su energía, la conexión y el consejo</p>", unsafe_allow_html=True)
            
            pregunta_amor = st.text_area("¿Qué quieres saber sobre el amor?", height=100,
                                        placeholder="Ej: ¿Cómo fluye mi relación con esta persona?",
                                        key="input_pregunta_amor")
            
            if st.button("💕 Consultar sobre Amor", use_container_width=True, key="btn_tirada_amor"):
                if pregunta_amor:
                    with st.spinner("💖 Las cartas están hablando del amor..."):
                        resultado = tarot.tirada_amor_ia(pregunta_amor)
                    st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Escribe tu pregunta primero")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_tarot_volver_amor", use_container_width=True):
                st.session_state.tarot_subview = "menu"
                st.rerun()
        
        elif st.session_state.tarot_subview == "trabajo":
            st.markdown("### 💼 Tirada Profesional")
            st.markdown("<p style='color:#d8c9ff;'>Situación, fortalezas, desafíos y resultado</p>", unsafe_allow_html=True)
            
            pregunta_trabajo = st.text_area("¿Qué quieres saber sobre tu trabajo?", height=100,
                                           placeholder="Ej: ¿Debo aceptar esta oferta laboral?",
                                           key="input_pregunta_trabajo")
            
            if st.button("💼 Consultar sobre Trabajo", use_container_width=True, key="btn_tirada_trabajo"):
                if pregunta_trabajo:
                    with st.spinner("🌟 Las cartas están iluminando tu camino profesional..."):
                        resultado = tarot.tirada_trabajo_ia(pregunta_trabajo)
                    st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Escribe tu pregunta primero")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_tarot_volver_trabajo", use_container_width=True):
                st.session_state.tarot_subview = "menu"
                st.rerun()
        
        elif st.session_state.tarot_subview == "si_no":
            st.markdown("### ❓ Pregunta Sí/No")
            st.markdown("<p style='color:#d8c9ff;'>Una carta, una respuesta clara</p>", unsafe_allow_html=True)
            
            pregunta_sino = st.text_input("Haz tu pregunta de sí o no:", 
                                         placeholder="Ej: ¿Debo tomar esta decisión?",
                                         key="input_pregunta_sino")
            
            if st.button("❓ Consultar Sí/No", use_container_width=True, key="btn_tirada_sino"):
                if pregunta_sino:
                    with st.spinner("✨ Las cartas están decidiendo..."):
                        resultado = tarot.tirada_si_no_ia(pregunta_sino)
                    st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Escribe tu pregunta primero")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_tarot_volver_sino", use_container_width=True):
                st.session_state.tarot_subview = "menu"
                st.rerun()
        
        elif st.session_state.tarot_subview == "historial":
            st.markdown("### 📜 Historial de Tiradas")
            st.markdown("<p style='color:#d8c9ff;'>Tus lecturas pasadas</p>", unsafe_allow_html=True)
            
            historial = tarot.ver_historial()
            
            if historial:
                st.success(f"✅ {len(historial)} tirada(s) guardada(s)")
                
                for tirada in historial[:10]:  # Mostrar últimas 10
                    tipo_emoji = {
                        "energia": "✨",
                        "tres_cartas": "🔮",
                        "amor": "💕",
                        "trabajo": "💼",
                        "si_no": "❓"
                    }
                    emoji = tipo_emoji.get(tirada.get('tipo', ''), "🔮")
                    
                    with st.expander(f"{emoji} {tirada.get('tipo', 'Tirada').title()} - {tirada.get('fecha', 'N/A')}", expanded=False):
                        # Mostrar cartas
                        cartas = tirada.get('cartas', [])
                        if isinstance(cartas, list):
                            st.markdown("**Cartas:**")
                            for carta in cartas:
                                if isinstance(carta, dict):
                                    st.caption(f"🃏 {carta.get('nombre', 'N/A')} {' (Invertida)' if carta.get('invertida') else ''}")
                                else:
                                    st.caption(f"🃏 {carta}")
                        
                        # Mostrar interpretación resumida
                        interp = tirada.get('interpretacion', '')
                        if interp:
                            st.markdown("**Lectura:**")
                            st.markdown(interp[:300] + "..." if len(interp) > 300 else interp)
            else:
                st.info("No tienes tiradas guardadas aún. ¡Haz tu primera lectura! 🔮")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_tarot_volver_historial", use_container_width=True):
                st.session_state.tarot_subview = "menu"
                st.rerun()
    
    # --- MÓDULO ASTROLOGÍA ---
    elif st.session_state.current_view == "astrologia":
        st.markdown("<div class='title-glow'>⭐ Astrología</div>", unsafe_allow_html=True)
        
        if st.session_state.astro_subview == "menu":
            st.markdown("<p class='subtitle-text'>Las estrellas cuentan tu historia.</p>", unsafe_allow_html=True)
            
            opciones_astro = [
                ("🌟", "Horóscopo Diario", "horoscopo", "libros-icon"),
                ("🌙", "Fase Lunar", "luna", "tarot-icon"),
                ("🏠", "Volver", "volver", "ideas-icon")
            ]
            
            rows_astro = [opciones_astro[i:i+3] for i in range(0, len(opciones_astro), 3)]
            for row in rows_astro:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    with cols[idx]:
                        st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                        if st.button(f"Abrir {label}" if sub_key != "volver" else label, key=f"btn_astro_{sub_key}", use_container_width=True):
                            if sub_key == "volver":
                                st.session_state.current_view = "lo_oculto"
                                st.session_state.oculto_subview = "menu"
                            else:
                                st.session_state.astro_subview = sub_key
                            st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
        
        elif st.session_state.astro_subview == "horoscopo":
            st.markdown("### 🌟 Horóscopo del Día")
            
            signos = ["Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo", "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"]
            signo = st.selectbox("Tu signo zodiacal:", signos, key="select_signo_astro")
            
            if st.button("✨ Ver Horóscopo", use_container_width=True, key="btn_horoscopo"):
                resultado = astrologia.horoscopo_del_dia(signo)
                st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_astro_volver_horo"):
                st.session_state.astro_subview = "menu"
                st.rerun()
        
        elif st.session_state.astro_subview == "luna":
            st.markdown("### 🌙 Fase Lunar Actual")
            resultado = astrologia.fase_lunar_actual()
            st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_astro_volver_luna"):
                st.session_state.astro_subview = "menu"
                st.rerun()
    
    # --- MÓDULO NUMEROLOGÍA ---
    elif st.session_state.current_view == "numerologia":
        st.markdown("<div class='title-glow'>🔢 Numerología</div>", unsafe_allow_html=True)
        
        if st.session_state.nume_subview == "menu":
            st.markdown("<p class='subtitle-text'>Los números revelan tu propósito.</p>", unsafe_allow_html=True)
            
            opciones_nume = [
                ("🔢", "Número del Día", "dia", "finanzas-icon"),
                ("✨", "Camino de Vida", "camino", "ideas-icon"),
                ("👼", "Significado", "significado", "tarot-icon"),
                ("🏠", "Volver", "volver", "libros-icon")
            ]
            
            rows_nume = [opciones_nume[i:i+3] for i in range(0, len(opciones_nume), 3)]
            for row in rows_nume:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    with cols[idx]:
                        st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                        if st.button(f"Ver {label}" if sub_key != "volver" else label, key=f"btn_nume_{sub_key}", use_container_width=True):
                            if sub_key == "volver":
                                st.session_state.current_view = "lo_oculto"
                                st.session_state.oculto_subview = "menu"
                            else:
                                st.session_state.nume_subview = sub_key
                            st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
        
        elif st.session_state.nume_subview == "dia":
            st.markdown("### 🔢 Número del Día")
            resultado = numerologia.numerologia_del_dia()
            st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_nume_volver_dia"):
                st.session_state.nume_subview = "menu"
                st.rerun()
        
        elif st.session_state.nume_subview == "camino":
            st.markdown("### ✨ Tu Camino de Vida")
            st.markdown("<p style='color:#d8c9ff;'>Ingresa tu fecha de nacimiento</p>", unsafe_allow_html=True)
            
            fecha = st.text_input("Fecha de nacimiento:", placeholder="DD/MM/AAAA", key="input_fecha_nume")
            
            if st.button("🔢 Calcular", use_container_width=True, key="btn_calcular_camino"):
                if fecha:
                    resultado = numerologia.calcular_camino_de_vida(fecha)
                    st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Ingresa tu fecha de nacimiento")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_nume_volver_camino"):
                st.session_state.nume_subview = "menu"
                st.rerun()
        
        elif st.session_state.nume_subview == "significado":
            st.markdown("### 👼 Significado de un Número")
            st.markdown("<p style='color:#d8c9ff;'>Números angelicales, números base, etc.</p>", unsafe_allow_html=True)
            
            numero = st.text_input("Número a consultar:", placeholder="Ej: 111, 7, 1234", key="input_numero_signif")
            
            if st.button("✨ Ver Significado", use_container_width=True, key="btn_significado"):
                if numero:
                    resultado = numerologia.significado_numero(numero)
                    st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Ingresa un número")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver", key="btn_nume_volver_signif"):
                st.session_state.nume_subview = "menu"
                st.rerun()
    
    # --- MÓDULO IDEAS ---
    elif st.session_state.current_view == "ideas":
        mostrar_breadcrumbs()
        st.markdown("<div class='title-glow'>💡 Ideas</div>", unsafe_allow_html=True)
        
        if st.session_state.ideas_subview == "menu":
            st.markdown("<p class='subtitle-text'>Tu espacio para soñar y crear</p>", unsafe_allow_html=True)
            
            opciones_ideas = [
                ("💬", "Chat con IA", "chat", "frases-icon"),
                ("📂", "Mis Proyectos", "proyectos", "libros-icon"),
                ("✨", "Expandir Idea", "expandir", "ideas-icon"),
                ("🎨", "Generar Imagen", "imagen", "tarot-icon"),
                ("🏠", "Volver", "volver", "notas-icon")
            ]
            
            rows_ideas = [opciones_ideas[i:i+3] for i in range(0, len(opciones_ideas), 3)]
            for row in rows_ideas:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    if idx < len(row):
                        with cols[idx]:
                            st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                            if st.button(f"Abrir {label}" if sub_key != "volver" else label, key=f"btn_ideas_{sub_key}", use_container_width=True):
                                if sub_key == "volver":
                                    st.session_state.current_view = "menu"
                                else:
                                    st.session_state.ideas_subview = sub_key
                                st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
        
        elif st.session_state.ideas_subview == "chat":
            st.markdown("### 💬 Chat con IA")
            st.markdown("<p style='color:#d8c9ff;'>Conversa sobre tus ideas y proyectos</p>", unsafe_allow_html=True)
            
            # Mostrar historial
            if st.session_state.ideas_history:
                st.markdown("**Conversación:**")
                for msg in st.session_state.ideas_history[-5:]:
                    if msg['role'] == 'user':
                        st.markdown(f"**Tú:** {msg['content']}")
                    else:
                        st.markdown(f'<div class="result-card">**IA:** {msg["content"]}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
            
            mensaje = st.text_area("¿Qué idea tienes en mente?", height=100, 
                                  placeholder="Ej: Quiero empezar un proyecto de decoración para mi cuarto...",
                                  key="input_chat_ideas")
            
            if st.button("💬 Enviar", use_container_width=True, key="btn_chat_ideas"):
                if mensaje:
                    # Guardar mensaje del usuario
                    st.session_state.ideas_history.append({'role': 'user', 'content': mensaje})
                    
                    # Generar contexto
                    contexto = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.ideas_history[-3:]])
                    
                    with st.spinner("💭 Conversando con IA... (5-10 seg)"):
                        respuesta = ideas_handler.conversar_con_ia(mensaje, contexto)
                    
                    # Guardar respuesta
                    st.session_state.ideas_history.append({'role': 'assistant', 'content': respuesta})
                    st.rerun()
                else:
                    st.warning("⚠️ Escribe algo primero")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_ideas_volver_chat", use_container_width=True):
                st.session_state.ideas_subview = "menu"
                st.rerun()
        
        elif st.session_state.ideas_subview == "proyectos":
            st.markdown("### 📂 Mis Proyectos")
            
            # Mostrar proyectos existentes
            proyectos = ideas_handler.listar_proyectos()
            
            if proyectos:
                st.markdown(f"**Tienes {len(proyectos)} proyecto(s):**")
                for proyecto in proyectos:
                    with st.expander(f"💡 {proyecto['nombre']}", expanded=False):
                        st.markdown(f"**Creado:** {proyecto['fecha_creacion']}")
                        if proyecto.get('descripcion'):
                            st.markdown(f"**Descripción:** {proyecto['descripcion']}")
                        st.markdown(f"**Items:** {len(proyecto['items'])} ({proyecto.get('conseguidos', 0)} conseguidos)")
                        
                        # Mostrar items
                        if proyecto['items']:
                            st.markdown("---")
                            st.markdown("**Items del proyecto:**")
                            for item in proyecto['items']:
                                icono = "✅" if item.get('conseguido') else "⬜"
                                tipo_emoji = "💡" if item.get('tipo') == 'inspiracion' else "🛒"
                                st.caption(f"{icono} {tipo_emoji} {item.get('descripcion', 'N/A')}")
                        
                        # Agregar nuevo item
                        st.markdown("---")
                        st.markdown("**➕ Agregar Item**")
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            desc_item = st.text_input("Descripción:", key=f"input_item_{proyecto['id']}", 
                                                     placeholder="Ej: Lámpara de lectura")
                        with col2:
                            tipo_item = st.selectbox("Tipo:", ["inspiracion", "compra"], 
                                                    format_func=lambda x: "💡 Inspiración" if x == "inspiracion" else "🛒 Compra",
                                                    key=f"select_tipo_item_{proyecto['id']}")
                        
                        if st.button("➕ Agregar", key=f"btn_agregar_item_{proyecto['id']}"):
                            if desc_item:
                                nuevo_item = ideas_handler.agregar_item(proyecto['id'], tipo_item, desc_item)
                                if nuevo_item:
                                    st.success("✅ Item agregado")
                                    st.rerun()
                            else:
                                st.warning("⚠️ Escribe una descripción")
                
                st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("Aún no tienes proyectos. ¡Crea uno!")
            
            # Crear nuevo proyecto
            st.markdown("### ✨ Crear Nuevo Proyecto")
            nombre_proy = st.text_input("Nombre del proyecto:", placeholder="Ej: Mi Cuarto Nuevo", key="input_nombre_proyecto")
            desc_proy = st.text_area("Descripción (opcional):", height=80, placeholder="Describe tu proyecto...", key="input_desc_proyecto")
            
            if st.button("✨ Crear Proyecto", use_container_width=True, key="btn_crear_proyecto"):
                if nombre_proy:
                    nuevo = ideas_handler.crear_proyecto(nombre_proy, desc_proy)
                    st.success(f"✅ Proyecto '{nuevo['nombre']}' creado!")
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("⚠️ Escribe un nombre para el proyecto")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_ideas_volver_proyectos", use_container_width=True):
                st.session_state.ideas_subview = "menu"
                st.rerun()
        
        elif st.session_state.ideas_subview == "expandir":
            st.markdown("### ✨ Expandir una Idea")
            st.markdown("<p style='color:#d8c9ff;'>La IA te ayudará a desarrollar tu idea</p>", unsafe_allow_html=True)
            
            idea = st.text_area("Cuéntame tu idea:", height=120,
                               placeholder="Ej: Quiero crear un espacio de lectura acogedor en mi casa",
                               key="input_expandir_idea")
            
            if st.button("✨ Expandir con IA", use_container_width=True, key="btn_expandir_idea"):
                if idea:
                    with st.spinner("🌟 Expandiendo tu idea con IA... (10-15 seg)"):
                        resultado = ideas_handler.expandir_idea(idea)
                    st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Escribe una idea primero")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_ideas_volver_expandir", use_container_width=True):
                st.session_state.ideas_subview = "menu"
                st.rerun()
        
        elif st.session_state.ideas_subview == "imagen":
            st.markdown("### 🎨 Generar Imagen con IA")
            st.markdown("<p style='color:#d8c9ff;'>DALL-E 3 creará una imagen basada en tu descripción</p>", unsafe_allow_html=True)
            
            descripcion_img = st.text_area("Describe la imagen que quieres:", height=120,
                                          placeholder="Ej: Un cuarto acogedor con muchas plantas, luz natural y libros",
                                          key="input_desc_imagen")
            
            if st.button("🎨 Generar Imagen", use_container_width=True, key="btn_generar_imagen"):
                if descripcion_img:
                    with st.spinner("🎨 Generando imagen con DALL-E 3... (esto puede tardar ~30 segundos)"):
                        resultado = ideas_handler.generar_imagen_dalle(descripcion_img)
                    
                    if resultado['success']:
                        st.success("✅ ¡Imagen generada!")
                        st.image(resultado['url'], caption=f"Prompt: {resultado['prompt']}", use_container_width=True)
                    else:
                        st.error(f"❌ Error: {resultado.get('error', 'No se pudo generar la imagen')}")
                else:
                    st.warning("⚠️ Describe la imagen que quieres")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_ideas_volver_imagen", use_container_width=True):
                st.session_state.ideas_subview = "menu"
                st.rerun()


    # --- MÓDULO PROFESIONAL ---
    elif st.session_state.current_view == "profesional":
        mostrar_breadcrumbs()
        st.markdown("<div class='title-glow'>💼 Profesional</div>", unsafe_allow_html=True)
        
        if st.session_state.profesional_subview == "menu":
            st.markdown("<p class='subtitle-text'>Herramientas para tu carrera profesional</p>", unsafe_allow_html=True)
            
            opciones_prof = [
                ("📧", "Generar Correos", "correos", "frases-icon"),
                ("💬", "Preparar Entrevistas", "entrevistas", "ideas-icon"),
                ("📊", "Seguir Vacantes", "vacantes", "finanzas-icon"),
                ("📈", "Estadísticas", "estadisticas", "tarot-icon"),
                ("🏠", "Volver", "volver", "notas-icon")
            ]
            
            rows_prof = [opciones_prof[i:i+3] for i in range(0, len(opciones_prof), 3)]
            for row in rows_prof:
                cols = st.columns(3, gap="small")
                for idx, (icon, label, sub_key, css) in enumerate(row):
                    if idx < len(row):
                        with cols[idx]:
                            st.markdown(f'<div class="magic-card"><div class="card-icon {css}">{icon}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                            if st.button(f"Abrir {label}" if sub_key != "volver" else label, key=f"btn_prof_{sub_key}", use_container_width=True):
                                if sub_key == "volver":
                                    st.session_state.current_view = "menu"
                                else:
                                    st.session_state.profesional_subview = sub_key
                                st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
        
        elif st.session_state.profesional_subview == "correos":
            st.markdown("### 📧 Generar Correos Profesionales")
            st.markdown("<p style='color:#d8c9ff;'>IA creará correos profesionales para distintas situaciones</p>", unsafe_allow_html=True)
            
            tipo_correo = st.selectbox(
                "Tipo de correo:",
                ["agradecimiento", "seguimiento", "networking", "feedback", "negociacion"],
                format_func=lambda x: {
                    "agradecimiento": "📧 Agradecimiento post-entrevista",
                    "seguimiento": "📤 Seguimiento de aplicación",
                    "networking": "🤝 Networking / LinkedIn",
                    "feedback": "💬 Solicitar feedback",
                    "negociacion": "💰 Negociar oferta/salario"
                }[x],
                key="select_tipo_correo"
            )
            
            contexto_correo = st.text_area(
                "Contexto adicional (opcional):",
                height=100,
                placeholder="Ej: Entrevista con Google para puesto de PM, hablamos sobre...",
                key="input_contexto_correo"
            )
            
            if st.button("📧 Generar Correo", use_container_width=True, key="btn_generar_correo"):
                with st.spinner("✍️ Generando correo profesional con IA... (5-10 seg)"):
                    resultado = profesional_handler.generar_correo_profesional(tipo_correo, contexto_correo)
                st.markdown(f'<div class="result-card">{resultado.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_prof_volver_correos", use_container_width=True):
                st.session_state.profesional_subview = "menu"
                st.rerun()
        
        elif st.session_state.profesional_subview == "entrevistas":
            st.markdown("### 💬 Preparar Entrevistas")
            st.markdown("<p style='color:#d8c9ff;'>Practica con preguntas comunes y recibe feedback de IA</p>", unsafe_allow_html=True)
            
            if st.button("🎲 Nueva Pregunta Aleatoria", use_container_width=True, key="btn_nueva_pregunta"):
                pregunta = profesional_handler.obtener_pregunta_entrevista()
                st.session_state.profesional_pregunta = pregunta
                st.session_state.profesional_respuesta = None
                st.rerun()
            
            if st.session_state.profesional_pregunta:
                st.markdown(f'<div class="result-card">{st.session_state.profesional_pregunta.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                
                respuesta_usuario = st.text_area(
                    "Tu respuesta:",
                    height=150,
                    placeholder="Escribe tu respuesta usando el método STAR...",
                    key="input_respuesta_entrevista"
                )
                
                if st.button("📋 Recibir Feedback", use_container_width=True, key="btn_feedback_respuesta"):
                    if respuesta_usuario:
                        # Extraer solo la pregunta del texto completo
                        pregunta_limpia = st.session_state.profesional_pregunta.split("\n")[2].strip("_")
                        
                        with st.spinner("🤔 Analizando tu respuesta con IA... (10-15 seg)"):
                            feedback = profesional_handler.analizar_respuesta_entrevista(pregunta_limpia, respuesta_usuario)
                        st.session_state.profesional_respuesta = feedback
                        st.rerun()
                    else:
                        st.warning("⚠️ Escribe tu respuesta primero")
                
                if st.session_state.profesional_respuesta:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f'<div class="result-card">{st.session_state.profesional_respuesta.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_prof_volver_entrevistas", use_container_width=True):
                st.session_state.profesional_subview = "menu"
                st.session_state.profesional_pregunta = None
                st.session_state.profesional_respuesta = None
                st.rerun()
        
        elif st.session_state.profesional_subview == "vacantes":
            st.markdown("### 📊 Seguimiento de Vacantes")
            
            # Verificar vacantes pendientes de seguimiento
            pendientes = profesional_handler.verificar_vacantes_pendientes_seguimiento()
            if pendientes:
                st.warning(f"⏰ **Recordatorio de Seguimiento:** Tienes {len(pendientes)} vacante(s) con 7+ días sin respuesta")
                for p in pendientes[:3]:  # Mostrar máximo 3
                    st.caption(f"• #{p['id']} {p['empresa']} - {p['cargo']} ({p['dias']} días)")
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Mostrar vacantes existentes
            vacantes = profesional_handler.listar_vacantes()
            
            if vacantes:
                st.markdown(f"**Tienes {len(vacantes)} vacante(s) en seguimiento:**")
                
                # Agrupar por estado
                estados = {}
                for v in vacantes:
                    estado = v.get('estado', 'aplicado')
                    if estado not in estados:
                        estados[estado] = []
                    estados[estado].append(v)
                
                emojis_estado = {
                    "aplicado": "📤",
                    "entrevista": "💬",
                    "oferta": "🎉",
                    "rechazado": "❌",
                    "retirado": "🔙"
                }
                
                for estado, lista in estados.items():
                    if lista:
                        st.markdown(f"**{emojis_estado.get(estado, '📋')} {estado.upper()}** ({len(lista)})")
                        for v in lista:
                            with st.expander(f"#{v['id']} - {v['empresa']} - {v['cargo']}", expanded=False):
                                st.markdown(f"**Aplicado:** {v['fecha_aplicacion']}")
                                st.markdown(f"**Estado:** {v['estado']}")
                                if v.get('contacto'):
                                    st.markdown(f"**Contacto:** {v['contacto']}")
                                if v.get('notas'):
                                    st.markdown(f"**Notas:** {v['notas']}")
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    nuevo_estado = st.selectbox(
                                        "Cambiar estado:",
                                        ["aplicado", "entrevista", "oferta", "rechazado", "retirado"],
                                        index=["aplicado", "entrevista", "oferta", "rechazado", "retirado"].index(v['estado']),
                                        key=f"estado_{v['id']}"
                                    )
                                    if st.button("💾 Actualizar", key=f"btn_actualizar_{v['id']}"):
                                        profesional_handler.actualizar_estado_vacante(v['id'], nuevo_estado)
                                        st.success("✅ Actualizado")
                                        st.rerun()
                                with col2:
                                    if st.button("🗑️ Eliminar", key=f"btn_eliminar_{v['id']}"):
                                        profesional_handler.borrar_vacante(v['id'])
                                        st.success("✅ Eliminado")
                                        st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("No tienes vacantes en seguimiento aún.")
            
            # Formulario para agregar nueva vacante
            st.markdown("### ✨ Agregar Nueva Vacante")
            
            col1, col2 = st.columns(2)
            with col1:
                empresa = st.text_input("Empresa:", placeholder="Google", key="input_empresa")
                fecha_app = st.date_input("Fecha de aplicación:", key="input_fecha_app")
            with col2:
                cargo = st.text_input("Cargo:", placeholder="Product Manager", key="input_cargo")
                contacto = st.text_input("Contacto (opcional):", placeholder="Juan Pérez - Recruiter", key="input_contacto")
            
            notas = st.text_area("Notas (opcional):", height=80, placeholder="Detalles de la aplicación...", key="input_notas_vac")
            
            if st.button("✨ Agregar Vacante", use_container_width=True, key="btn_agregar_vacante"):
                if empresa and cargo:
                    fecha_str = fecha_app.strftime("%Y-%m-%d")
                    profesional_handler.agregar_vacante(empresa, cargo, fecha_str, contacto, notas)
                    st.success(f"✅ Vacante agregada: {empresa} - {cargo}")
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("⚠️ Completa al menos Empresa y Cargo")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_prof_volver_vacantes", use_container_width=True):
                st.session_state.profesional_subview = "menu"
                st.rerun()
        
        elif st.session_state.profesional_subview == "estadisticas":
            st.markdown("### 📈 Estadísticas de Búsqueda Laboral")
            
            stats = profesional_handler.generar_estadisticas_vacantes()
            
            if stats:
                # Resumen general
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Aplicaciones", stats['total'])
                with col2:
                    st.metric("Activas", stats['activas'])
                with col3:
                    st.metric("Tasa de Respuesta", f"{stats['tasa_respuesta']:.1f}%")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Distribución por estado
                st.markdown("**📊 Distribución por Estado:**")
                estados = stats['estados']
                for estado, cantidad in estados.items():
                    if cantidad > 0:
                        porcentaje = (cantidad / stats['total'] * 100)
                        emoji = {"aplicado": "📤", "entrevista": "💬", "oferta": "🎉", "rechazado": "❌", "retirado": "🔙"}
                        st.progress(porcentaje / 100, text=f"{emoji.get(estado, '📋')} {estado.capitalize()}: {cantidad} ({porcentaje:.0f}%)")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Métricas adicionales
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Tasa de Éxito", f"{stats['tasa_exito']:.1f}%", 
                             help="Porcentaje de ofertas recibidas")
                with col2:
                    st.metric("Días Promedio", f"{stats['dias_promedio']:.0f}", 
                             help="Tiempo promedio por proceso")
                
                # Top empresas contactadas
                if stats['top_empresas']:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("**🏢 Empresas Más Contactadas:**")
                    for i, (empresa, cantidad) in enumerate(stats['top_empresas'], 1):
                        st.caption(f"{i}. {empresa}: {cantidad} aplicación(es)")
                
                # Mensajes motivacionales
                st.markdown("<br>", unsafe_allow_html=True)
                if stats['tasa_respuesta'] >= 20:
                    st.success("✨ ¡Excelente tasa de respuesta! Sigue así 💪")
                elif stats['tasa_respuesta'] >= 10:
                    st.info("💡 Buena tasa de respuesta. Considera optimizar tu CV o aplicaciones")
                else:
                    st.warning("💪 Sigue aplicando. Cada 'no' te acerca al 'sí' perfecto")
            else:
                st.info("No tienes vacantes registradas aún. ¡Agrega algunas para ver estadísticas!")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Volver al Menú", key="btn_prof_volver_estadisticas", use_container_width=True):
                st.session_state.profesional_subview = "menu"
                st.rerun()

    # DEFAULT
    else:
        st.markdown(f"<div class='title-glow'>{st.session_state.current_view.capitalize()}</div>", unsafe_allow_html=True)
        st.info("✨ Sección en construcción energética")
        if st.button("🔙 Menú Principal", key="btn_default_home"): 
            st.session_state.current_view = "menu"
            st.rerun()
    
    # =====================================================
    # SPOTIFY: Renderizado al final cuando usuario está loggeado
    # =====================================================
      
st.markdown('<div class="bottom-footer">🌙 Que la luz de tu intuición te guíe en este viaje sagrado 🌙</div>', unsafe_allow_html=True)

