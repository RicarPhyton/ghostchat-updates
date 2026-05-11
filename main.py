# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:24:23 2026

@author: Ricar
"""
import customtkinter as ctk
from PIL import Image
import json
import os
import time
import socket
import threading
import urllib.request
import subprocess
import sys
import shutil


ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_CLAVES = "claves.json"
ARCHIVO_SESION = "sesion.json"
ARCHIVO_CHATS = "chats.json"
ARCHIVO_SOLICITUDES = "solicitudes.json"
ARCHIVO_AMIGOS = "amigos.json"
ARCHIVO_GRUPOS = "grupos.json"
ARCHIVO_GHOSTPLUS = "ghostplus.json"
ARCHIVO_MENSAJES_GRUPOS = "mensajes_grupos.json"
ARCHIVO_VOZ_GRUPOS = "voz_grupos.json"
ARCHIVO_MENSAJES_PRIVADOS = "mensajes_privados.json"
ARCHIVO_LLAMADAS_PRIVADAS = "llamadas_privadas.json"

HOST = "127.0.0.1"
PORT = 5050
cliente_socket = None

VERSION_ACTUAL = "0.1"

URL_VERSION = "https://raw.githubusercontent.com/RicarPhyton/ghostchat-updates/refs/heads/main/version.json"
URL_MAIN = "https://raw.githubusercontent.com/RicarPhyton/ghostchat-updates/refs/heads/main/main.py"

CLAVES_INICIALES = [
    "KOLQAVQ5","SFZ035AF","FYZVV6WX","FRKHD947","RFY7PE49",
    "HXFUT2U0","CVDHOMMF","VD0MGY3U","H0S9L7HS","EAIQE11K",
    "H2VF5R6F","JJ4SQGPH","EY0LZV76","N1QEIAIS","Z6DLJP1Z",
    "PA0G02TV","PFLNV0UY","12DS1HM6","SBM3SCTJ","UMNFBDXY",
    "8NGCLGL3","CVH5FRY7","HB3V0C59","73PL83Y6","GN7SBG3U",

    "EKTHCQB4","WHU3GAV7","G91MPKJ0","OYFW72UB","DTN51QK3",
    "8MWZZWQ0","ZGYVK2B9","0G4131YC","NQRVGLGB","HFOW7POB",
    "F2PT1BHZ","F9LS20IN","DGAZ06DX","ET2ZABKM","EKUU3H0E",
    "MBT3LVLY","X29A9660","645S6NWP","X4JXDRFN","XL3FEDQP",
    "UQXMF62","78OKP796","7XOY4J53","8XZF7HP2","WCRYKTE4",

    "WCLWXF8U","70E0P5QF","00Q33P48","MUHTKQ92","U45DZT1Y",
    "FV479GX1","R57DS016","HKOHGALL","QYFP6PXL","VXLJ5VTH",
    "X8YAVBPK","P3R8HGKQ","60S465CM","WGRC76WA","SMRBAP7T",
    "ND5WEJZQ","FRSVRC99","JMT05DVN","MEHYKSWJ","7XMOG6PM",
    "9CL1Y7B7","60G067BQ","0I5NO7WH","PL83RZWR","GRF0DFCZ",

    "OVB9ISNA","V1RKHLYP","TOPAT5KW","R1YRZUXF","LRNV5Q7T",
    "PGEHBT9H","C78ZXJHV","J5ZBXESO","8HK6Z59P","JDBP921F",
    "62VWNZ60","GONWBDPW","269J3I8M","DIGE8XHV","9NB0MWYO",
    "T85XFV30","4WASCC6PW","MNZS5TDP","PZMWEB1E","JNH20ATZ",
    "QY4SA98W","181S96JP","FXYZ302N","X1XDNQ3R","GZVN8C3K"
]

CLAVES_GHOSTPLUS = [
    "PLUS-7KQ2A9", "PLUS-M4X8P1", "PLUS-R9T6B3", "PLUS-Z2N5L8",
    "PLUS-A8C1Q7", "PLUS-H6V3D9", "PLUS-P1W9X4", "PLUS-Y7B2M6",
    "PLUS-C5R8T2", "PLUS-L3Q9K1"
]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("GhostChat v0.2")
app.geometry("900x560")
app.minsize(650, 520)
app.resizable(True, True)


def activar_pantalla_completa(event=None):
    app.attributes("-fullscreen", True)


def salir_pantalla_completa(event=None):
    app.attributes("-fullscreen", False)


app.bind("<F11>", activar_pantalla_completa)
app.bind("<Escape>", salir_pantalla_completa)


def limpiar_ventana():
    for widget in app.winfo_children():
        widget.destroy()


def cargar_json(archivo, defecto):
    if not os.path.exists(archivo):
        return defecto

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return defecto


def guardar_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def cargar_usuarios():
    return cargar_json(ARCHIVO_USUARIOS, {})


def guardar_usuarios(datos):
    guardar_json(ARCHIVO_USUARIOS, datos)


def cargar_claves():
    if not os.path.exists(ARCHIVO_CLAVES):
        claves = {clave: True for clave in CLAVES_INICIALES}
        guardar_json(ARCHIVO_CLAVES, claves)
        return claves

    return cargar_json(ARCHIVO_CLAVES, {})


def guardar_claves(datos):
    guardar_json(ARCHIVO_CLAVES, datos)


def cargar_amigos():
    return cargar_json(ARCHIVO_AMIGOS, {})


def guardar_amigos(datos):
    guardar_json(ARCHIVO_AMIGOS, datos)


def cargar_grupos():
    return cargar_json(ARCHIVO_GRUPOS, [])


def guardar_grupos(datos):
    guardar_json(ARCHIVO_GRUPOS, datos)


def cargar_ghostplus():
    if not os.path.exists(ARCHIVO_GHOSTPLUS):
        datos = {
            "claves": {clave: True for clave in CLAVES_GHOSTPLUS},
            "miembros": []
        }
        guardar_json(ARCHIVO_GHOSTPLUS, datos)
        return datos

    return cargar_json(
        ARCHIVO_GHOSTPLUS,
        {
            "claves": {clave: True for clave in CLAVES_GHOSTPLUS},
            "miembros": []
        }
    )


def guardar_ghostplus(datos):
    guardar_json(ARCHIVO_GHOSTPLUS, datos)
    
def asegurar_grupo_ghostplus():
    usuario_actual = cargar_sesion()
    grupos = cargar_grupos()
    datos_plus = cargar_ghostplus()

    grupo_existente = None

    for grupo in grupos:
        if grupo.get("id") == "ghostplus":
            grupo_existente = grupo
            break

    if grupo_existente is None:
        grupo_existente = {
            "id": "ghostplus",
            "nombre": "GhostPlus",
            "creador": "GhostChat",
            "miembros": [],
            "fecha": time.time(),
            "especial": True
        }
        grupos.append(grupo_existente)

    for miembro in datos_plus.get("miembros", []):
        if miembro not in grupo_existente["miembros"]:
            grupo_existente["miembros"].append(miembro)

    guardar_grupos(grupos)
    return grupo_existente


def cargar_mensajes_grupos():
    return cargar_json(ARCHIVO_MENSAJES_GRUPOS, {})


def guardar_mensajes_grupos(datos):
    guardar_json(ARCHIVO_MENSAJES_GRUPOS, datos)


def cargar_voz_grupos():
    return cargar_json(ARCHIVO_VOZ_GRUPOS, {})


def guardar_voz_grupos(datos):
    guardar_json(ARCHIVO_VOZ_GRUPOS, datos)
    
def cargar_mensajes_privados():
    return cargar_json(ARCHIVO_MENSAJES_PRIVADOS, {})


def guardar_mensajes_privados(datos):
    guardar_json(ARCHIVO_MENSAJES_PRIVADOS, datos)


def cargar_llamadas_privadas():
    return cargar_json(ARCHIVO_LLAMADAS_PRIVADAS, {})


def guardar_llamadas_privadas(datos):
    guardar_json(ARCHIVO_LLAMADAS_PRIVADAS, datos)


def guardar_sesion(usuario):
    guardar_json(ARCHIVO_SESION, {"usuario": usuario})


def cargar_sesion():
    datos = cargar_json(ARCHIVO_SESION, {})
    return datos.get("usuario")


def cerrar_sesion():
    if os.path.exists(ARCHIVO_SESION):
        os.remove(ARCHIVO_SESION)

    mostrar_login()


def usuario_es_ghostplus():
    usuario_actual = cargar_sesion()
    datos = cargar_ghostplus()
    return usuario_actual in datos.get("miembros", [])


def crear_panel():
    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    panel = ctk.CTkFrame(
        contenedor,
        fg_color="transparent",
        width=460,
        height=520
    )
    panel.place(relx=0.5, rely=0.5, anchor="center")
    panel.pack_propagate(False)

    return panel


def poner_logo(parent, size=105):
    try:
        imagen = Image.open("ghost_logo.png")
        logo = ctk.CTkImage(
            light_image=imagen,
            dark_image=imagen,
            size=(size, size)
        )

        label = ctk.CTkLabel(parent, image=logo, text="")
        label.image = logo
        label.pack(pady=(0, 14))

    except Exception as e:
        print("Error cargando ghost_logo.png:", e)

        label = ctk.CTkLabel(
            parent,
            text="👻",
            font=("Arial", 80)
        )
        label.pack(pady=(0, 14))


def poner_banner(parent, size=420):
    try:
        imagen = Image.open("ghost_banner.png")

        ancho, alto = imagen.size
        nuevo_ancho = size
        nuevo_alto = int((alto / ancho) * nuevo_ancho)

        banner = ctk.CTkImage(
            light_image=imagen,
            dark_image=imagen,
            size=(nuevo_ancho, nuevo_alto)
        )

        parent.banner_img = banner

        label = ctk.CTkLabel(
            parent,
            image=parent.banner_img,
            text=""
        )

        label.pack(pady=(0, 25))

    except Exception as e:
        print("Error cargando ghost_banner.png:", e)

        label = ctk.CTkLabel(
            parent,
            text="GhostChat",
            font=("Arial", 44, "bold")
        )

        label.pack(pady=(0, 25))

def conectar_servidor():
    global cliente_socket

    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((HOST, PORT))

        print("Conectado al servidor GhostChat")

        hilo = threading.Thread(target=escuchar_servidor, daemon=True)
        hilo.start()

    except Exception as e:
        print("No se pudo conectar al servidor:", e)


def escuchar_servidor():
    global cliente_socket

    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode("utf-8")

            if mensaje:
                print("Mensaje recibido:", mensaje)

        except:
            break


def enviar_servidor(mensaje):
    global cliente_socket

    try:
        if cliente_socket:
            cliente_socket.send(mensaje.encode("utf-8"))

    except Exception as e:
        print("Error enviando:", e)

def comprobar_actualizacion_automatica():
    try:
        with urllib.request.urlopen(URL_VERSION, timeout=5) as respuesta:
            datos = json.loads(respuesta.read().decode("utf-8"))

        version_online = datos.get("version", VERSION_APP)

        if version_online != VERSION_APP:
            subprocess.Popen([sys.executable, "updater.py"])
            app.destroy()
            return True

    except Exception as e:
        print("No se pudo comprobar actualización:", e)

    return False

def crear_id_chat_privado(usuario1, usuario2):
    nombres = sorted([usuario1, usuario2])
    return f"privado_{nombres[0]}_{nombres[1]}"


def asegurar_chats():
    usuario_actual = cargar_sesion()

    if not usuario_actual:
        return

    amigos = cargar_amigos()
    lista_amigos = amigos.get(usuario_actual, [])

    chats = cargar_json(ARCHIVO_CHATS, [])

    ids_existentes = [chat.get("id") for chat in chats]

    for amigo in lista_amigos:
        chat_id = crear_id_chat_privado(usuario_actual, amigo)

        if chat_id not in ids_existentes:
            chats.append({
                "id": chat_id,
                "tipo": "privado",
                "usuarios": [usuario_actual, amigo],
                "nombre": amigo,
                "ultimo_texto": "Chat creado",
                "no_leidos": 0,
                "ultimo_mensaje": 0
            })

    guardar_json(ARCHIVO_CHATS, chats)


def contar_no_leidos():
    asegurar_chats()
    chats = cargar_json(ARCHIVO_CHATS, [])

    return sum(chat.get("no_leidos", 0) for chat in chats)


def contar_solicitudes_pendientes():
    usuario_actual = cargar_sesion()
    solicitudes = cargar_json(ARCHIVO_SOLICITUDES, [])

    return sum(
        1 for solicitud in solicitudes
        if solicitud.get("para") == usuario_actual
        and solicitud.get("estado") == "pendiente"
    )


def contar_no_leidos_grupo(grupo_id):
    usuario_actual = cargar_sesion()
    mensajes_grupos = cargar_mensajes_grupos()
    mensajes = mensajes_grupos.get(grupo_id, [])

    total = 0

    for msg in mensajes:
        if msg.get("usuario") != usuario_actual:
            leido_por = msg.get("leido_por", {})

            if not leido_por.get(usuario_actual, False):
                total += 1

    return total


def contar_no_leidos_grupos():
    usuario_actual = cargar_sesion()
    grupos = cargar_grupos()
    mensajes_grupos = cargar_mensajes_grupos()

    total = 0

    for grupo in grupos:
        grupo_id = grupo.get("id")

        if usuario_actual in grupo.get("miembros", []):
            mensajes = mensajes_grupos.get(grupo_id, [])

            for msg in mensajes:
                if msg.get("usuario") != usuario_actual:
                    leido_por = msg.get("leido_por", {})

                    if not leido_por.get(usuario_actual, False):
                        total += 1

    return total


def ordenar_chats(chats):
    return sorted(
        chats,
        key=lambda chat: chat.get("ultimo_mensaje", 0),
        reverse=True
    )


def mostrar_bandeja():
    limpiar_ventana()
    asegurar_chats()

    usuario_actual = cargar_sesion()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=lambda: mostrar_app(cargar_sesion())
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.18, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Bandeja de entrada",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 20))

    lista = ctk.CTkFrame(contenedor, fg_color="transparent")
    lista.pack(fill="x", padx=45, pady=(260, 30))

    amigos = cargar_amigos()
    lista_amigos = amigos.get(usuario_actual, [])

    chats = cargar_json(ARCHIVO_CHATS, [])

    chats_usuario = []

    for chat in chats:
        if chat.get("tipo") == "privado" and usuario_actual in chat.get("usuarios", []):
            chats_usuario.append(chat)

    chats_usuario = ordenar_chats(chats_usuario)

    if not chats_usuario:
        vacio = ctk.CTkLabel(
            lista,
            text="Todavía no tienes chats con amigos",
            font=("Arial", 18, "bold"),
            text_color="#9ca3af"
        )
        vacio.pack(pady=40)
        return

    for chat in chats_usuario:
        usuarios_chat = chat.get("usuarios", [])
        otro_usuario = ""

        for u in usuarios_chat:
            if u != usuario_actual:
                otro_usuario = u
                break

        chat["nombre"] = otro_usuario if otro_usuario else chat.get("nombre", "Chat")

        crear_tarjeta_chat(lista, chat)


def crear_tarjeta_chat(parent, chat):
    frame = ctk.CTkFrame(
        parent,
        height=95,
        fg_color="#2b2f36",
        corner_radius=20
    )
    frame.pack(fill="x", pady=10)
    frame.pack_propagate(False)
    frame.grid_columnconfigure(0, weight=1)

    nombre = ctk.CTkLabel(
        frame,
        text=chat.get("nombre", "Chat"),
        font=("Arial", 18, "bold"),
        text_color="white",
        anchor="w"
    )
    nombre.grid(row=0, column=0, sticky="w", padx=20, pady=(14, 2))

    ultimo = ctk.CTkLabel(
        frame,
        text=chat.get("ultimo_texto", ""),
        font=("Arial", 14),
        text_color="#cfcfcf",
        anchor="w"
    )
    ultimo.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 14))

    no_leidos = chat.get("no_leidos", 0)

    if no_leidos > 0:
        circulo = ctk.CTkLabel(
            frame,
            text=str(no_leidos),
            fg_color="#ff3333",
            text_color="white",
            width=28,
            height=28,
            corner_radius=14,
            font=("Arial", 13, "bold")
        )
        circulo.grid(row=0, column=1, rowspan=2, padx=20)

    for widget in (frame, nombre, ultimo):
        widget.bind("<Button-1>", lambda e, c=chat: abrir_chat(c))


def abrir_chat(chat):
    chats = cargar_json(ARCHIVO_CHATS, [])

    for c in chats:
        if c.get("id") == chat.get("id"):
            c["no_leidos"] = 0
            c["ultimo_mensaje"] = time.time()
            chat = c
            break

    guardar_json(ARCHIVO_CHATS, chats)
    mostrar_chat(chat)


def mostrar_chat(chat):
    limpiar_ventana()

    usuario_actual = cargar_sesion()
    chat_id = chat.get("id")
    usuarios_chat = chat.get("usuarios", [])

    otro_usuario = chat.get("nombre", "Chat")

    for u in usuarios_chat:
        if u != usuario_actual:
            otro_usuario = u
            break

    contenedor = ctk.CTkFrame(app, fg_color="#111111")
    contenedor.pack(expand=True, fill="both")

    barra = ctk.CTkFrame(contenedor, height=60, fg_color="#202329")
    barra.pack(fill="x")

    volver = ctk.CTkButton(
        barra,
        text="←",
        width=40,
        command=mostrar_bandeja
    )
    volver.pack(side="left", padx=10)

    info = ctk.CTkFrame(barra, fg_color="transparent")
    info.pack(side="left", padx=(5, 10))

    nombre = ctk.CTkLabel(
        info,
        text=otro_usuario,
        font=("Arial", 18, "bold"),
        text_color="white"
    )
    nombre.pack(anchor="w")

    estado = ctk.CTkLabel(
        info,
        text="en este chat",
        font=("Arial", 12),
        text_color="#4CAF50"
    )
    estado.pack(anchor="w")

    boton_llamada = ctk.CTkButton(
        barra,
        text="📞 Llamar",
        width=110,
        height=36,
        corner_radius=18,
        fg_color="#4EA8FF",
        hover_color="#2f6fa3",
        command=lambda: mostrar_llamada_privada(chat)
    )
    boton_llamada.pack(side="right", padx=12)

    chat_frame = ctk.CTkScrollableFrame(contenedor, fg_color="#111111")
    chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

    mensajes_privados = cargar_mensajes_privados()
    mensajes = mensajes_privados.get(chat_id, [])

    if not mensajes:
        vacio = ctk.CTkLabel(
            chat_frame,
            text="Todavía no hay mensajes en este chat",
            font=("Arial", 16),
            text_color="#9ca3af"
        )
        vacio.pack(pady=30)

    for msg in mensajes:
        es_mio = msg.get("usuario") == usuario_actual

        frame_msg = ctk.CTkFrame(chat_frame, fg_color="transparent")
        frame_msg.pack(fill="x", pady=4)

        burbuja = ctk.CTkLabel(
            frame_msg,
            text=msg.get("texto", ""),
            fg_color="#0084ff" if es_mio else "#2b2f36",
            text_color="white",
            corner_radius=15,
            padx=12,
            pady=8,
            wraplength=520,
            justify="left"
        )
        burbuja.pack(anchor="e" if es_mio else "w", padx=10)

    input_frame = ctk.CTkFrame(contenedor, height=60, fg_color="#202329")
    input_frame.pack(fill="x")

    entrada = ctk.CTkEntry(
        input_frame,
        placeholder_text="Escribe un mensaje...",
        height=40
    )
    entrada.pack(side="left", fill="x", expand=True, padx=10, pady=10)

    def enviar():
        texto = entrada.get().strip()

        if texto == "":
            return

        mensajes_privados = cargar_mensajes_privados()
        mensajes_privados.setdefault(chat_id, [])

        mensajes_privados[chat_id].append({
            "usuario": usuario_actual,
            "texto": texto,
            "fecha": time.time()
        })

        guardar_mensajes_privados(mensajes_privados)

        chats = cargar_json(ARCHIVO_CHATS, [])

        for c in chats:
            if c.get("id") == chat_id:
                c["ultimo_texto"] = texto
                c["ultimo_mensaje"] = time.time()
                break

        guardar_json(ARCHIVO_CHATS, chats)

        entrada.delete(0, "end")
        mostrar_chat(chat)

    boton_enviar = ctk.CTkButton(
        input_frame,
        text="➤",
        width=50,
        command=enviar
    )
    boton_enviar.pack(side="right", padx=10)

    entrada.bind("<Return>", lambda e: enviar())


def mostrar_llamada_privada(chat):
    limpiar_ventana()

    usuario_actual = cargar_sesion()
    chat_id = chat.get("id")
    usuarios_chat = chat.get("usuarios", [])

    otro_usuario = chat.get("nombre", "Chat")

    for u in usuarios_chat:
        if u != usuario_actual:
            otro_usuario = u
            break

    llamadas = cargar_llamadas_privadas()
    llamadas.setdefault(chat_id, [])

    contenedor = ctk.CTkFrame(app, fg_color="#111111")
    contenedor.pack(expand=True, fill="both")

    barra = ctk.CTkFrame(contenedor, height=65, fg_color="#202329")
    barra.pack(fill="x")

    volver = ctk.CTkButton(
        barra,
        text="←",
        width=45,
        command=lambda: mostrar_chat(chat)
    )
    volver.pack(side="left", padx=10)

    titulo = ctk.CTkLabel(
        barra,
        text=f"Llamada con {otro_usuario}",
        font=("Arial", 20, "bold"),
        text_color="white"
    )
    titulo.pack(side="left", padx=10)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    titulo_llamada = ctk.CTkLabel(
        panel,
        text="Llamada privada",
        font=("Arial", 42, "bold"),
        text_color="#4EA8FF"
    )
    titulo_llamada.pack(pady=(0, 20))

    usuarios_en_llamada = llamadas.get(chat_id, [])

    def entrar_llamada():
        llamadas = cargar_llamadas_privadas()
        llamadas.setdefault(chat_id, [])

        if usuario_actual not in llamadas[chat_id]:
            llamadas[chat_id].append(usuario_actual)

        guardar_llamadas_privadas(llamadas)
        mostrar_llamada_privada(chat)

    def salir_llamada():
        llamadas = cargar_llamadas_privadas()
        llamadas.setdefault(chat_id, [])

        if usuario_actual in llamadas[chat_id]:
            llamadas[chat_id].remove(usuario_actual)

        guardar_llamadas_privadas(llamadas)
        mostrar_llamada_privada(chat)

    if usuario_actual in usuarios_en_llamada:
        estado = ctk.CTkLabel(
            panel,
            text="Estás dentro de la llamada",
            font=("Arial", 17, "bold"),
            text_color="#4CAF50"
        )
        estado.pack(pady=10)

        boton = ctk.CTkButton(
            panel,
            text="Colgar",
            width=280,
            height=46,
            corner_radius=20,
            fg_color="#8A2BE2",
            hover_color="#6f22b8",
            command=salir_llamada
        )
        boton.pack(pady=12)

    else:
        estado = ctk.CTkLabel(
            panel,
            text="No estás en llamada",
            font=("Arial", 17, "bold"),
            text_color="#b8b8b8"
        )
        estado.pack(pady=10)

        boton = ctk.CTkButton(
            panel,
            text="Entrar a llamada",
            width=280,
            height=46,
            corner_radius=20,
            fg_color="#4EA8FF",
            hover_color="#2f6fa3",
            command=entrar_llamada
        )
        boton.pack(pady=12)

    lista_titulo = ctk.CTkLabel(
        panel,
        text="Usuarios en llamada:",
        font=("Arial", 18, "bold"),
        text_color="white"
    )
    lista_titulo.pack(pady=(25, 8))

    if not usuarios_en_llamada:
        nadie = ctk.CTkLabel(
            panel,
            text="Nadie está en la llamada",
            font=("Arial", 15),
            text_color="#9ca3af"
        )
        nadie.pack()
    else:
        for usuario in usuarios_en_llamada:
            nombre = ctk.CTkLabel(
                panel,
                text=f"📞 {usuario}",
                font=("Arial", 16),
                text_color="white"
            )
            nombre.pack(pady=3)

def mostrar_añadir_amigos():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=mostrar_amigos
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Añadir amigos",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 30))

    entrada_usuario = ctk.CTkEntry(
        panel,
        placeholder_text="Nombre de usuario",
        width=360,
        height=45,
        font=("Arial", 15)
    )
    entrada_usuario.pack(pady=10)

    mensaje = ctk.CTkLabel(panel, text="", font=("Arial", 14))
    mensaje.pack(pady=10)

    def enviar_solicitud():
        usuario_actual = cargar_sesion()
        usuario_destino = entrada_usuario.get().strip()

        usuarios = cargar_usuarios()
        solicitudes = cargar_json(ARCHIVO_SOLICITUDES, [])

        if usuario_destino == "":
            mensaje.configure(text="Escribe un nombre de usuario")
            return

        if usuario_destino == usuario_actual:
            mensaje.configure(text="No puedes enviarte solicitud a ti mismo")
            return

        if usuario_destino not in usuarios:
            mensaje.configure(text="Ese usuario no existe")
            return

        for solicitud in solicitudes:
            if (
                solicitud.get("de") == usuario_actual
                and solicitud.get("para") == usuario_destino
                and solicitud.get("estado") == "pendiente"
            ):
                mensaje.configure(text="Ya enviaste una solicitud a ese usuario")
                return

        solicitudes.append({
            "de": usuario_actual,
            "para": usuario_destino,
            "estado": "pendiente",
            "fecha": time.time()
        })

        guardar_json(ARCHIVO_SOLICITUDES, solicitudes)

        mensaje.configure(text="Solicitud enviada correctamente")
        entrada_usuario.delete(0, "end")

    boton_enviar = ctk.CTkButton(
        panel,
        text="Enviar solicitud",
        command=enviar_solicitud,
        width=320,
        height=46,
        corner_radius=20,
        font=("Arial", 15, "bold")
    )
    boton_enviar.pack(pady=10)


def mostrar_solicitudes_pendientes():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=mostrar_amigos
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.20, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Solicitudes pendientes",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 20))

    lista = ctk.CTkFrame(contenedor, fg_color="transparent")
    lista.pack(fill="x", padx=45, pady=(260, 30))

    usuario_actual = cargar_sesion()
    solicitudes = cargar_json(ARCHIVO_SOLICITUDES, [])

    pendientes = [
        s for s in solicitudes
        if s.get("para") == usuario_actual
        and s.get("estado") == "pendiente"
    ]

    if not pendientes:
        vacio = ctk.CTkLabel(
            lista,
            text="No tienes solicitudes pendientes",
            font=("Arial", 18, "bold"),
            text_color="#9ca3af"
        )
        vacio.pack(pady=40)
        return

    def aceptar_solicitud(solicitud):
        solicitud["estado"] = "aceptada"

        usuario_solicitante = solicitud.get("de")
        amigos = cargar_amigos()

        amigos.setdefault(usuario_actual, [])
        amigos.setdefault(usuario_solicitante, [])

        if usuario_solicitante not in amigos[usuario_actual]:
            amigos[usuario_actual].append(usuario_solicitante)

        if usuario_actual not in amigos[usuario_solicitante]:
            amigos[usuario_solicitante].append(usuario_actual)

        guardar_amigos(amigos)
        guardar_json(ARCHIVO_SOLICITUDES, solicitudes)

        mostrar_solicitudes_pendientes()

    def rechazar_solicitud(solicitud):
        solicitud["estado"] = "rechazada"

        guardar_json(ARCHIVO_SOLICITUDES, solicitudes)

        mostrar_solicitudes_pendientes()

    for solicitud in pendientes:
        fila = ctk.CTkFrame(
            lista,
            height=85,
            fg_color="#2b2f36",
            corner_radius=20
        )
        fila.pack(fill="x", pady=10)
        fila.pack_propagate(False)
        fila.grid_columnconfigure(0, weight=1)

        nombre = ctk.CTkLabel(
            fila,
            text=solicitud.get("de", "Usuario"),
            font=("Arial", 20, "bold"),
            text_color="white",
            anchor="w"
        )
        nombre.grid(row=0, column=0, sticky="w", padx=22, pady=25)

        aceptar = ctk.CTkButton(
            fila,
            text="Aceptar",
            width=120,
            height=38,
            corner_radius=18,
            fg_color="#4EA8FF",
            hover_color="#2f6fa3",
            font=("Arial", 14, "bold"),
            command=lambda s=solicitud: aceptar_solicitud(s)
        )
        aceptar.grid(row=0, column=1, padx=(10, 8), pady=20)

        rechazar = ctk.CTkButton(
            fila,
            text="Rechazar",
            width=120,
            height=38,
            corner_radius=18,
            fg_color="#8A2BE2",
            hover_color="#6f22b8",
            font=("Arial", 14, "bold"),
            command=lambda s=solicitud: rechazar_solicitud(s)
        )
        rechazar.grid(row=0, column=2, padx=(8, 22), pady=20)


def mostrar_gestionar_amigos():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=mostrar_amigos
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.20, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Gestionar amigos",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 20))

    lista = ctk.CTkFrame(contenedor, fg_color="transparent")
    lista.pack(fill="x", padx=45, pady=(260, 30))

    usuario_actual = cargar_sesion()
    amigos = cargar_amigos()
    lista_amigos = amigos.get(usuario_actual, [])

    if not lista_amigos:
        vacio = ctk.CTkLabel(
            lista,
            text="Todavía no tienes amigos añadidos",
            font=("Arial", 18, "bold"),
            text_color="#9ca3af"
        )
        vacio.pack(pady=40)
        return

    def eliminar_amigo(nombre):
        amigos.setdefault(usuario_actual, [])
        amigos[usuario_actual] = [
            amigo for amigo in amigos[usuario_actual]
            if amigo != nombre
        ]

        amigos.setdefault(nombre, [])
        amigos[nombre] = [
            amigo for amigo in amigos[nombre]
            if amigo != usuario_actual
        ]

        guardar_amigos(amigos)

        mostrar_gestionar_amigos()

    for amigo in lista_amigos:
        fila = ctk.CTkFrame(
            lista,
            height=85,
            fg_color="#2b2f36",
            corner_radius=20
        )
        fila.pack(fill="x", pady=10)
        fila.pack_propagate(False)
        fila.grid_columnconfigure(0, weight=1)

        nombre = ctk.CTkLabel(
            fila,
            text=amigo,
            font=("Arial", 20, "bold"),
            text_color="white",
            anchor="w"
        )
        nombre.grid(row=0, column=0, sticky="w", padx=22, pady=25)

        eliminar = ctk.CTkButton(
            fila,
            text="Eliminar",
            width=120,
            height=38,
            corner_radius=18,
            fg_color="#4EA8FF",
            hover_color="#2f6fa3",
            font=("Arial", 14, "bold"),
            command=lambda n=amigo: eliminar_amigo(n)
        )
        eliminar.grid(row=0, column=1, padx=(10, 22), pady=20)


def mostrar_amigos():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=lambda: mostrar_app(cargar_sesion())
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Amigos",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 35))

    botones = ctk.CTkFrame(panel, fg_color="transparent")
    botones.pack()

    def boton_amigos(icono, texto, color, comando=None, notificacion=0):
        caja = ctk.CTkFrame(
            botones,
            width=190,
            height=135,
            corner_radius=22,
            fg_color="#2b2f36"
        )
        caja.pack(side="left", padx=14)
        caja.pack_propagate(False)

        icon = ctk.CTkLabel(
            caja,
            text=icono,
            font=("Arial", 36, "bold"),
            text_color=color
        )
        icon.pack(pady=(22, 8))

        label = ctk.CTkLabel(
            caja,
            text=texto,
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        label.pack()

        if notificacion > 0:
            circulo = ctk.CTkLabel(
                caja,
                text=str(notificacion),
                fg_color="#ff3333",
                text_color="white",
                width=26,
                height=26,
                corner_radius=13,
                font=("Arial", 12, "bold")
            )
            circulo.place(relx=1, rely=0, x=-12, y=10, anchor="ne")

        def ejecutar(event=None):
            if comando:
                comando()
            else:
                print("Abriendo:", texto)

        for widget in (caja, icon, label):
            widget.bind("<Button-1>", ejecutar)

    boton_amigos(
        "➕",
        "Añadir amigos",
        "#00CFFF",
        mostrar_añadir_amigos
    )

    boton_amigos(
        "📨",
        "Solicitudes pendientes",
        "#4EA8FF",
        comando=mostrar_solicitudes_pendientes,
        notificacion=contar_solicitudes_pendientes()
    )

    boton_amigos(
        "🛡",
        "Gestionar amigos",
        "#B36BFF",
        comando=mostrar_gestionar_amigos
    )


def mostrar_crear_grupo():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=mostrar_grupos
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Crear grupo",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 30))

    entrada_nombre = ctk.CTkEntry(
        panel,
        placeholder_text="Nombre del grupo",
        width=360,
        height=45,
        font=("Arial", 15)
    )
    entrada_nombre.pack(pady=10)

    mensaje = ctk.CTkLabel(panel, text="", font=("Arial", 14))
    mensaje.pack(pady=10)

    def crear_grupo():
        usuario_actual = cargar_sesion()
        nombre_grupo = entrada_nombre.get().strip()

        if nombre_grupo == "":
            mensaje.configure(text="Escribe un nombre para el grupo")
            return

        grupos = cargar_grupos()

        for grupo in grupos:
            if grupo.get("nombre", "").lower() == nombre_grupo.lower():
                mensaje.configure(text="Ya existe un grupo con ese nombre")
                return

        nuevo_grupo = {
            "id": str(int(time.time() * 1000)),
            "nombre": nombre_grupo,
            "creador": usuario_actual,
            "miembros": [usuario_actual],
            "fecha": time.time()
        }

        grupos.append(nuevo_grupo)
        guardar_grupos(grupos)

        mensaje.configure(text="Grupo creado correctamente")
        entrada_nombre.delete(0, "end")

    boton_crear = ctk.CTkButton(
        panel,
        text="Crear grupo",
        command=crear_grupo,
        width=320,
        height=46,
        corner_radius=20,
        fg_color="#00CFFF",
        hover_color="#2f6fa3",
        font=("Arial", 15, "bold")
    )
    boton_crear.pack(pady=10)


def mostrar_unirse_grupo():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=mostrar_grupos
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.20, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Unirse a grupo",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 20))

    lista = ctk.CTkFrame(contenedor, fg_color="transparent")
    lista.pack(fill="x", padx=45, pady=(260, 30))

    usuario_actual = cargar_sesion()
    grupos = cargar_grupos()

    grupos_disponibles = [
    grupo for grupo in grupos
    if usuario_actual not in grupo.get("miembros", [])
    and grupo.get("id") != "ghostplus"
]

    if not grupos_disponibles:
        vacio = ctk.CTkLabel(
            lista,
            text="No hay grupos disponibles para unirse",
            font=("Arial", 18, "bold"),
            text_color="#9ca3af"
        )
        vacio.pack(pady=40)
        return

    def unirse(grupo):
        if usuario_actual not in grupo["miembros"]:
            grupo["miembros"].append(usuario_actual)

        guardar_grupos(grupos)

        mostrar_unirse_grupo()

    for grupo in grupos_disponibles:
        fila = ctk.CTkFrame(
            lista,
            height=85,
            fg_color="#2b2f36",
            corner_radius=20
        )
        fila.pack(fill="x", pady=10)
        fila.pack_propagate(False)
        fila.grid_columnconfigure(0, weight=1)

        nombre = ctk.CTkLabel(
            fila,
            text=grupo.get("nombre", "Grupo"),
            font=("Arial", 20, "bold"),
            text_color="white",
            anchor="w"
        )
        nombre.grid(row=0, column=0, sticky="w", padx=22, pady=25)

        boton_unirse = ctk.CTkButton(
            fila,
            text="Unirse",
            width=120,
            height=38,
            corner_radius=18,
            fg_color="#4EA8FF",
            hover_color="#2f6fa3",
            font=("Arial", 14, "bold"),
            command=lambda g=grupo: unirse(g)
        )
        boton_unirse.grid(row=0, column=1, padx=(10, 22), pady=20)


def mostrar_grupo_chat(grupo):
    limpiar_ventana()

    usuario_actual = cargar_sesion()
    grupo_id = grupo.get("id")
    nombre_grupo = grupo.get("nombre", "Grupo")

    contenedor = ctk.CTkFrame(app, fg_color="#111111")
    contenedor.pack(expand=True, fill="both")

    barra = ctk.CTkFrame(contenedor, height=65, fg_color="#202329")
    barra.pack(fill="x")

    volver = ctk.CTkButton(
        barra,
        text="←",
        width=45,
        command=mostrar_mis_grupos
    )
    volver.pack(side="left", padx=10)

    titulo = ctk.CTkLabel(
        barra,
        text=nombre_grupo,
        font=("Arial", 20, "bold"),
        text_color="white"
    )
    titulo.pack(side="left", padx=10)

    boton_voz = ctk.CTkButton(
        barra,
        text="🎙 Canal de voz",
        width=150,
        height=36,
        corner_radius=18,
        fg_color="#8A2BE2",
        hover_color="#6f22b8",
        command=lambda: mostrar_canal_voz(grupo)
    )
    boton_voz.pack(side="right", padx=12)

    zona_mensajes = ctk.CTkScrollableFrame(
        contenedor,
        fg_color="#111111"
    )
    zona_mensajes.pack(fill="both", expand=True, padx=12, pady=12)

    mensajes_grupos = cargar_mensajes_grupos()
    mensajes = mensajes_grupos.get(grupo_id, [])

    for msg in mensajes:
        msg.setdefault("leido_por", {})
        msg["leido_por"][usuario_actual] = True

    guardar_mensajes_grupos(mensajes_grupos)

    if not mensajes:
        vacio = ctk.CTkLabel(
            zona_mensajes,
            text="Todavía no hay mensajes en este grupo",
            font=("Arial", 16),
            text_color="#9ca3af"
        )
        vacio.pack(pady=30)

    for msg in mensajes:
        es_mio = msg.get("usuario") == usuario_actual

        fila = ctk.CTkFrame(
            zona_mensajes,
            fg_color="transparent"
        )
        fila.pack(fill="x", pady=5)

        texto = f'{msg.get("usuario", "Usuario")}: {msg.get("texto", "")}'

        burbuja = ctk.CTkLabel(
            fila,
            text=texto,
            fg_color="#0084ff" if es_mio else "#2b2f36",
            text_color="white",
            corner_radius=15,
            padx=12,
            pady=8,
            wraplength=520,
            justify="left"
        )
        burbuja.pack(anchor="e" if es_mio else "w", padx=10)

    zona_escribir = ctk.CTkFrame(
        contenedor,
        height=65,
        fg_color="#202329"
    )
    zona_escribir.pack(fill="x")

    entrada = ctk.CTkEntry(
        zona_escribir,
        placeholder_text="Escribe un mensaje...",
        height=42,
        font=("Arial", 15)
    )
    entrada.pack(side="left", fill="x", expand=True, padx=12, pady=10)

    def enviar_mensaje():
        texto = entrada.get().strip()

        if texto == "":
            return

        mensajes_grupos = cargar_mensajes_grupos()
        mensajes_grupos.setdefault(grupo_id, [])

        mensajes_grupos[grupo_id].append({
            "usuario": usuario_actual,
            "texto": texto,
            "fecha": time.time(),
            "leido_por": {
                usuario_actual: True
            }
        })

        guardar_mensajes_grupos(mensajes_grupos)

        entrada.delete(0, "end")

        mostrar_grupo_chat(grupo)

    boton_enviar = ctk.CTkButton(
        zona_escribir,
        text="➤",
        width=55,
        height=42,
        command=enviar_mensaje
    )
    boton_enviar.pack(side="right", padx=12)

    entrada.bind("<Return>", lambda e: enviar_mensaje())


def mostrar_canal_voz(grupo):
    limpiar_ventana()

    usuario_actual = cargar_sesion()
    grupo_id = grupo.get("id")
    nombre_grupo = grupo.get("nombre", "Grupo")

    voz = cargar_voz_grupos()
    voz.setdefault(grupo_id, [])

    contenedor = ctk.CTkFrame(app, fg_color="#111111")
    contenedor.pack(expand=True, fill="both")

    barra = ctk.CTkFrame(contenedor, height=65, fg_color="#202329")
    barra.pack(fill="x")

    volver = ctk.CTkButton(
        barra,
        text="←",
        width=45,
        command=lambda: mostrar_grupo_chat(grupo)
    )
    volver.pack(side="left", padx=10)

    titulo = ctk.CTkLabel(
        barra,
        text=f"Canal de voz · {nombre_grupo}",
        font=("Arial", 20, "bold"),
        text_color="white"
    )
    titulo.pack(side="left", padx=10)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    texto = ctk.CTkLabel(
        panel,
        text="Canal de voz",
        font=("Arial", 42, "bold"),
        text_color="#8A2BE2"
    )
    texto.pack(pady=(0, 20))

    def entrar_voz():
        voz = cargar_voz_grupos()
        voz.setdefault(grupo_id, [])

        if usuario_actual not in voz[grupo_id]:
            voz[grupo_id].append(usuario_actual)

        guardar_voz_grupos(voz)

        mostrar_canal_voz(grupo)

    def salir_voz():
        voz = cargar_voz_grupos()
        voz.setdefault(grupo_id, [])

        if usuario_actual in voz[grupo_id]:
            voz[grupo_id].remove(usuario_actual)

        guardar_voz_grupos(voz)

        mostrar_canal_voz(grupo)

    usuarios_en_voz = voz.get(grupo_id, [])

    if usuario_actual in usuarios_en_voz:
        estado = ctk.CTkLabel(
            panel,
            text="Estás dentro del canal de voz",
            font=("Arial", 17, "bold"),
            text_color="#4CAF50"
        )
        estado.pack(pady=10)

        boton = ctk.CTkButton(
            panel,
            text="Salir del canal",
            width=280,
            height=46,
            corner_radius=20,
            fg_color="#8A2BE2",
            hover_color="#6f22b8",
            command=salir_voz
        )
        boton.pack(pady=12)

    else:
        estado = ctk.CTkLabel(
            panel,
            text="No estás dentro del canal",
            font=("Arial", 17, "bold"),
            text_color="#b8b8b8"
        )
        estado.pack(pady=10)

        boton = ctk.CTkButton(
            panel,
            text="Entrar al canal",
            width=280,
            height=46,
            corner_radius=20,
            fg_color="#4EA8FF",
            hover_color="#2f6fa3",
            command=entrar_voz
        )
        boton.pack(pady=12)

    lista_titulo = ctk.CTkLabel(
        panel,
        text="Usuarios en llamada:",
        font=("Arial", 18, "bold"),
        text_color="white"
    )
    lista_titulo.pack(pady=(25, 8))

    if not usuarios_en_voz:
        nadie = ctk.CTkLabel(
            panel,
            text="Nadie está en el canal",
            font=("Arial", 15),
            text_color="#9ca3af"
        )
        nadie.pack()

    else:
        for usuario in usuarios_en_voz:
            nombre = ctk.CTkLabel(
                panel,
                text=f"🎙 {usuario}",
                font=("Arial", 16),
                text_color="white"
            )
            nombre.pack(pady=3)


def mostrar_mis_grupos():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=mostrar_grupos
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.20, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Mis grupos",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 20))

    lista = ctk.CTkFrame(contenedor, fg_color="transparent")
    lista.pack(fill="x", padx=45, pady=(260, 30))

    usuario_actual = cargar_sesion()
    grupos = cargar_grupos()

    mis_grupos = [
        grupo for grupo in grupos
        if usuario_actual in grupo.get("miembros", [])
    ]

    if not mis_grupos:
        vacio = ctk.CTkLabel(
            lista,
            text="Todavía no estás en ningún grupo",
            font=("Arial", 18, "bold"),
            text_color="#9ca3af"
        )
        vacio.pack(pady=40)
        return

    def salir_grupo(grupo):
        if usuario_actual in grupo["miembros"]:
            grupo["miembros"].remove(usuario_actual)

        guardar_grupos(grupos)

        mostrar_mis_grupos()

    for grupo in mis_grupos:
        fila = ctk.CTkFrame(
            lista,
            height=85,
            fg_color="#2b2f36",
            corner_radius=20
        )
        fila.pack(fill="x", pady=10)
        fila.pack_propagate(False)
        fila.grid_columnconfigure(0, weight=1)

        nombre = ctk.CTkLabel(
            fila,
            text=grupo.get("nombre", "Grupo"),
            font=("Arial", 20, "bold"),
            text_color="white",
            anchor="w"
        )
        nombre.grid(row=0, column=0, sticky="w", padx=22, pady=25)

        miembros = ctk.CTkLabel(
            fila,
            text=f'{len(grupo.get("miembros", []))} miembros',
            font=("Arial", 13),
            text_color="#b8b8b8"
        )
        miembros.grid(row=1, column=0, sticky="w", padx=22, pady=(0, 14))

        no_leidos = contar_no_leidos_grupo(grupo.get("id"))

        if no_leidos > 0:
            circulo = ctk.CTkLabel(
                fila,
                text=str(no_leidos),
                fg_color="#ff3333",
                text_color="white",
                width=28,
                height=28,
                corner_radius=14,
                font=("Arial", 12, "bold")
            )
            circulo.place(relx=0.63, rely=0.5, anchor="center")

        abrir = ctk.CTkButton(
            fila,
            text="Entrar",
            width=120,
            height=38,
            corner_radius=18,
            fg_color="#4EA8FF",
            hover_color="#2f6fa3",
            font=("Arial", 14, "bold"),
            command=lambda g=grupo: mostrar_grupo_chat(g)
        )
        abrir.grid(row=0, column=1, rowspan=2, padx=(10, 8))

        salir = ctk.CTkButton(
            fila,
            text="Salir",
            width=120,
            height=38,
            corner_radius=18,
            fg_color="#8A2BE2",
            hover_color="#6f22b8",
            font=("Arial", 14, "bold"),
            command=lambda g=grupo: salir_grupo(g)
        )
        salir.grid(row=0, column=2, rowspan=2, padx=(8, 22))


def mostrar_grupo_ghostplus():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="#111111")
    contenedor.pack(expand=True, fill="both")

    barra = ctk.CTkFrame(contenedor, height=65, fg_color="#202329")
    barra.pack(fill="x")

    volver = ctk.CTkButton(
        barra,
        text="←",
        width=45,
        command=mostrar_ghostplus
    )
    volver.pack(side="left", padx=10)

    titulo = ctk.CTkLabel(
        barra,
        text="GhostPlus",
        font=("Arial", 20, "bold"),
        text_color="#FFD700"
    )
    titulo.pack(side="left", padx=10)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    texto = ctk.CTkLabel(
        panel,
        text="Bienvenido a GhostPlus 👻",
        font=("Arial", 40, "bold"),
        text_color="#FFD700"
    )
    texto.pack(pady=20)

    subtexto = ctk.CTkLabel(
        panel,
        text="Aquí estarán los mensajes y canales especiales.",
        font=("Arial", 17),
        text_color="white"
    )
    subtexto.pack(pady=10)


def mostrar_ghostplus():
    usuario_actual = cargar_sesion()
    datos = cargar_ghostplus()

    grupo_ghostplus = asegurar_grupo_ghostplus()

    if usuario_actual in datos.get("miembros", []):
        mostrar_grupo_chat(grupo_ghostplus)
        return

    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=mostrar_grupos
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    try:
        img = Image.open("ghost_plus_logo.png")
        logo = ctk.CTkImage(light_image=img, dark_image=img, size=(95, 95))
        logo_label = ctk.CTkLabel(panel, image=logo, text="")
        logo_label.image = logo
        logo_label.pack(pady=(0, 14))
    except:
        poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="GhostPlus",
        font=("Arial", 42, "bold"),
        text_color="#FFD700"
    )
    titulo.pack(pady=(0, 18))

    texto = ctk.CTkLabel(
        panel,
        text="Introduce una clave GhostPlus para entrar al grupo especial.",
        font=("Arial", 16),
        text_color="white"
    )
    texto.pack(pady=(0, 18))

    entrada_clave = ctk.CTkEntry(
        panel,
        placeholder_text="Clave GhostPlus",
        show="*",
        width=360,
        height=45,
        font=("Arial", 15)
    )
    entrada_clave.pack(pady=10)

    mostrar_var = ctk.BooleanVar()

    def toggle_clave():
        entrada_clave.configure(show="" if mostrar_var.get() else "*")

    check = ctk.CTkCheckBox(
        panel,
        text="Mostrar contraseña",
        variable=mostrar_var,
        command=toggle_clave,
        font=("Arial", 14)
    )
    check.pack(pady=(0, 10))

    mensaje = ctk.CTkLabel(panel, text="", font=("Arial", 14))
    mensaje.pack(pady=10)

    def activar_ghostplus():
        clave = entrada_clave.get().strip().upper()
        datos = cargar_ghostplus()

        if clave == "":
            mensaje.configure(text="Escribe una clave GhostPlus")
            return

        if clave not in datos["claves"]:
            mensaje.configure(text="Clave GhostPlus incorrecta")
            return

        if datos["claves"][clave] is False:
            mensaje.configure(text="Esta clave GhostPlus ya fue usada")
            return

        datos["claves"][clave] = False

        if usuario_actual not in datos["miembros"]:
            datos["miembros"].append(usuario_actual)

        guardar_ghostplus(datos)

        grupo = asegurar_grupo_ghostplus()

        mensaje.configure(text="GhostPlus activado correctamente")

        app.after(700, lambda: mostrar_grupo_chat(grupo))

    boton_activar = ctk.CTkButton(
        panel,
        text="Activar GhostPlus",
        command=activar_ghostplus,
        width=320,
        height=46,
        corner_radius=20,
        fg_color="#FFD700",
        hover_color="#c9a600",
        text_color="black",
        font=("Arial", 15, "bold")
    )
    boton_activar.pack(pady=10)

  



def mostrar_grupos():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=lambda: mostrar_app(cargar_sesion())
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Grupos",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 35))

    botones = ctk.CTkFrame(panel, fg_color="transparent")
    botones.pack()

    def boton_grupo(icono, texto, color, comando=None, imagen=None, notificacion=0):
        caja = ctk.CTkFrame(
            botones,
            width=190,
            height=135,
            corner_radius=22,
            fg_color="#2b2f36"
        )
        caja.pack(side="left", padx=14)
        caja.pack_propagate(False)

        if imagen:
            try:
                img = Image.open(imagen)
                icono_img = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(42, 42)
                )
                icon = ctk.CTkLabel(caja, image=icono_img, text="")
                icon.image = icono_img
            except:
                icon = ctk.CTkLabel(caja, text="❌", font=("Arial", 36))
        else:
            icon = ctk.CTkLabel(
                caja,
                text=icono,
                font=("Arial", 36, "bold"),
                text_color=color
            )

        icon.pack(pady=(22, 8))

        label = ctk.CTkLabel(
            caja,
            text=texto,
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        label.pack()

        if notificacion > 0:
            circulo = ctk.CTkLabel(
                caja,
                text=str(notificacion),
                fg_color="#ff3333",
                text_color="white",
                width=26,
                height=26,
                corner_radius=13,
                font=("Arial", 12, "bold")
            )
            circulo.place(relx=1, rely=0, x=-12, y=10, anchor="ne")

        def ejecutar(event=None):
            if comando:
                comando()

        for widget in (caja, icon, label):
            widget.bind("<Button-1>", ejecutar)

    boton_grupo(
        "➕",
        "Crear grupo",
        "#00CFFF",
        comando=mostrar_crear_grupo
    )

    boton_grupo(
        "🔎",
        "Unirse a grupo",
        "#4EA8FF",
        comando=mostrar_unirse_grupo
    )

    boton_grupo(
        "👥",
        "Mis grupos",
        "#8A2BE2",
        comando=mostrar_mis_grupos,
        notificacion=contar_no_leidos_grupos()
    )

    boton_grupo(
        "",
        "GhostPlus",
        "#FFD700",
        comando=mostrar_ghostplus,
        imagen="ghost_plus_logo.png",
        notificacion=contar_no_leidos_grupo("ghostplus") if usuario_es_ghostplus() else 0
    )

def mostrar_preferencias():
    limpiar_ventana()

    usuario_actual = cargar_sesion()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold"),
        command=lambda: mostrar_app(cargar_sesion())
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    poner_logo(panel, 95)

    titulo = ctk.CTkLabel(
        panel,
        text="Preferencias",
        font=("Arial", 42, "bold"),
        text_color="white"
    )
    titulo.pack(pady=(0, 25))

    usuario_label = ctk.CTkLabel(
        panel,
        text=f"Usuario: {usuario_actual}",
        font=("Arial", 17),
        text_color="#cfcfcf"
    )
    usuario_label.pack(pady=(0, 10))

    version = ctk.CTkLabel(
        panel,
        text="GhostChat v0.1",
        font=("Arial", 15),
        text_color="#9ca3af"
    )
    version.pack(pady=(0, 25))

    boton_cerrar = ctk.CTkButton(
        panel,
        text="Cerrar sesión",
        width=320,
        height=46,
        corner_radius=20,
        fg_color="#8A2BE2",
        hover_color="#6f22b8",
        font=("Arial", 15, "bold"),
        command=cerrar_sesion
    )
    boton_cerrar.pack(pady=10)

def mostrar_app(usuario):
    limpiar_ventana()
    asegurar_chats()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    panel = ctk.CTkFrame(contenedor, fg_color="transparent")
    panel.place(relx=0.5, rely=0.5, anchor="center")

    poner_banner(panel, 420)

    botones = ctk.CTkFrame(panel, fg_color="transparent")
    botones.pack()

    def boton_inicio(parent, icono, texto, color, comando=None, notificacion=0):
        caja = ctk.CTkFrame(
            parent,
            width=155,
            height=130,
            corner_radius=22,
            fg_color="#2b2f36"
        )
        caja.pack(side="left", padx=14)
        caja.pack_propagate(False)

        icon = ctk.CTkLabel(
            caja,
            text=icono,
            font=("Arial", 34, "bold"),
            text_color=color
        )
        icon.pack(pady=(22, 8))

        label = ctk.CTkLabel(
            caja,
            text=texto,
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        label.pack()

        if notificacion > 0:
            circulo = ctk.CTkLabel(
                caja,
                text=str(notificacion),
                fg_color="#ff3333",
                text_color="white",
                width=26,
                height=26,
                corner_radius=13,
                font=("Arial", 12, "bold")
            )
            circulo.place(relx=1, rely=0, x=-12, y=10, anchor="ne")

        def ejecutar(event=None):
            if comando:
                comando()
            else:
                print("Abriendo:", texto)

        for widget in (caja, icon, label):
            widget.bind("<Button-1>", ejecutar)

    boton_inicio(
        botones,
        "📥",
        "Bandeja",
        "#00CFFF",
        comando=mostrar_bandeja,
        notificacion=contar_no_leidos()
    )

    boton_inicio(
        botones,
        "👤",
        "Amigos",
        "#4EA8FF",
        comando=mostrar_amigos,
        notificacion=contar_solicitudes_pendientes()
    )

    boton_inicio(
        botones,
        "👥",
        "Grupos",
        "#8A2BE2",
        comando=mostrar_grupos,
        notificacion=contar_no_leidos_grupos()
    )

    boton_inicio(
    botones,
    "⚙",
    "Preferencias",
    "#B36BFF",
    comando=mostrar_preferencias
)


def mostrar_login():
    limpiar_ventana()

    panel = crear_panel()

    poner_logo(panel, 110)

    titulo = ctk.CTkLabel(
        panel,
        text="Iniciar sesión",
        font=("Arial", 36, "bold")
    )
    titulo.pack(pady=(0, 24))

    entrada_usuario = ctk.CTkEntry(
        panel,
        placeholder_text="Nombre de usuario",
        width=360,
        height=44,
        font=("Arial", 15)
    )
    entrada_usuario.pack(pady=9)

    entrada_password = ctk.CTkEntry(
        panel,
        placeholder_text="Contraseña",
        show="*",
        width=360,
        height=44,
        font=("Arial", 15)
    )
    entrada_password.pack(pady=9)

    mostrar_var = ctk.BooleanVar()

    def toggle_password():
        entrada_password.configure(show="" if mostrar_var.get() else "*")

    check = ctk.CTkCheckBox(
        panel,
        text="Mostrar contraseña",
        variable=mostrar_var,
        command=toggle_password,
        font=("Arial", 14)
    )
    check.pack(pady=(6, 12))

    mensaje = ctk.CTkLabel(panel, text="", font=("Arial", 14))
    mensaje.pack(pady=(0, 8))

    def iniciar_sesion():
        usuario = entrada_usuario.get().strip()
        password = entrada_password.get()

        usuarios = cargar_usuarios()

        if usuario == "" or password == "":
            mensaje.configure(text="Rellena todos los campos")
            return

        if usuario in usuarios and usuarios[usuario] == password:
            guardar_sesion(usuario)
            mostrar_app(usuario)

        else:
            mensaje.configure(text="Usuario o contraseña incorrectos")

    boton_login = ctk.CTkButton(
        panel,
        text="Iniciar sesión",
        command=iniciar_sesion,
        width=320,
        height=46,
        font=("Arial", 15, "bold")
    )
    boton_login.pack(pady=(8, 20))

    frame_registro = ctk.CTkFrame(panel, fg_color="transparent")
    frame_registro.pack(pady=(0, 5))

    texto = ctk.CTkLabel(
        frame_registro,
        text="¿No tienes cuenta?",
        font=("Arial", 13)
    )
    texto.pack(side="left")

    link = ctk.CTkLabel(
        frame_registro,
        text=" Crear una",
        text_color="#4EA8FF",
        font=("Arial", 13, "bold"),
        cursor="hand2"
    )
    link.pack(side="left")

    link.bind("<Button-1>", lambda e: mostrar_registro())


def mostrar_registro():
    limpiar_ventana()

    contenedor = ctk.CTkFrame(app, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")

    boton_volver = ctk.CTkButton(
        contenedor,
        text="← Volver",
        command=mostrar_login,
        width=120,
        height=40,
        corner_radius=20,
        fg_color="#2f6fa3",
        hover_color="#3b82c4",
        font=("Arial", 14, "bold")
    )
    boton_volver.place(x=20, y=20)

    panel = ctk.CTkFrame(
        contenedor,
        fg_color="transparent",
        width=460,
        height=520
    )
    panel.place(relx=0.5, rely=0.5, anchor="center")
    panel.pack_propagate(False)

    poner_logo(panel, 100)

    titulo = ctk.CTkLabel(
        panel,
        text="Crear cuenta",
        font=("Arial", 34, "bold")
    )
    titulo.pack(pady=(0, 18))

    entrada_usuario = ctk.CTkEntry(
        panel,
        placeholder_text="Nombre de usuario",
        width=360,
        height=42,
        font=("Arial", 15)
    )
    entrada_usuario.pack(pady=6)

    entrada_password1 = ctk.CTkEntry(
        panel,
        placeholder_text="Contraseña",
        show="*",
        width=360,
        height=42,
        font=("Arial", 15)
    )
    entrada_password1.pack(pady=6)

    entrada_password2 = ctk.CTkEntry(
        panel,
        placeholder_text="Repetir contraseña",
        show="*",
        width=360,
        height=42,
        font=("Arial", 15)
    )
    entrada_password2.pack(pady=6)

    entrada_clave = ctk.CTkEntry(
        panel,
        placeholder_text="Clave de único uso",
        show="*",
        width=360,
        height=42,
        font=("Arial", 15)
    )
    entrada_clave.pack(pady=6)

    mostrar_var = ctk.BooleanVar()

    def toggle_passwords():
        valor = "" if mostrar_var.get() else "*"

        entrada_password1.configure(show=valor)
        entrada_password2.configure(show=valor)
        entrada_clave.configure(show=valor)

    check = ctk.CTkCheckBox(
        panel,
        text="Mostrar contraseñas",
        variable=mostrar_var,
        command=toggle_passwords,
        font=("Arial", 14)
    )
    check.pack(pady=(6, 8))

    mensaje = ctk.CTkLabel(panel, text="", font=("Arial", 14))
    mensaje.pack(pady=(0, 6))

    def crear_cuenta():
        usuario = entrada_usuario.get().strip()
        pass1 = entrada_password1.get()
        pass2 = entrada_password2.get()
        clave = entrada_clave.get().strip().upper()

        usuarios = cargar_usuarios()
        claves = cargar_claves()

        if usuario == "" or pass1 == "" or pass2 == "" or clave == "":
            mensaje.configure(text="Rellena todos los campos")
            return

        if usuario in usuarios:
            mensaje.configure(text="Ese usuario ya existe")
            return

        if pass1 != pass2:
            mensaje.configure(text="Las contraseñas no coinciden")
            return

        if clave not in claves:
            mensaje.configure(text="Clave incorrecta")
            return

        if claves[clave] is False:
            mensaje.configure(text="Clave ya usada")
            return

        usuarios[usuario] = pass1
        claves[clave] = False

        guardar_usuarios(usuarios)
        guardar_claves(claves)

        mensaje.configure(text="Cuenta creada correctamente")

        app.after(900, mostrar_login)

    boton_crear = ctk.CTkButton(
        panel,
        text="Crear cuenta",
        command=crear_cuenta,
        width=320,
        height=46,
        font=("Arial", 15, "bold")
    )
    boton_crear.pack(pady=5)


def comprobar_actualizaciones():
    try:
        with urllib.request.urlopen(URL_VERSION) as respuesta:
            datos = json.loads(respuesta.read().decode())

        version_nueva = datos.get("version")

        if version_nueva != VERSION_ACTUAL:
            print("Nueva actualización encontrada")

            urllib.request.urlretrieve(URL_MAIN, "main_nuevo.py")

            os.replace("main_nuevo.py", "main.py")

            print("GhostChat actualizado")

            os.execv(sys.executable, ['python'] + sys.argv)

    except Exception as e:
        print("Error buscando actualización:", e)

usuario_guardado = cargar_sesion()

if not comprobar_actualizacion_automatica():

    if usuario_guardado:
        mostrar_app(usuario_guardado)
    else:
        mostrar_login()

    conectar_servidor()

comprobar_actualizaciones()

app.mainloop()

