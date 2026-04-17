import os
import subprocess
import sys
import tempfile
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk


class AplicacionCotizacion:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Cotización")
        self.raiz.configure(bg="#efefef")
        self.raiz.geometry("1100x860")
        self.raiz.minsize(980, 760)

        self.columnas = ["Cantidad", "Productos", "Valor Unitario", "Total"]
        self.filas = []
        self.entradas_encabezado = []
        self.bloqueado = False
        self.max_columnas_renderizadas = 0

        self.var_neto = tk.StringVar(value="$0")
        self.var_iva = tk.StringVar(value="$0")
        self.var_total = tk.StringVar(value="$0")

        self.var_nombre_ejecutivo = tk.StringVar(value="EMMA OLIVEROS")
        self.var_cargo_ejecutivo = tk.StringVar(value="Ejecutiva de ventas")
        self.var_telefono = tk.StringVar(value="9918-63590")
        self.var_correo = tk.StringVar(value="EMMAOLIVEROS23@GMAIL.COM")
        self.var_senores = tk.StringVar(value="COMUNIDAD RIVAS VICUÑA 1214 - QTA NORMAL")
        self.var_atencion = tk.StringVar(value="SR ROBERTO ARMIJO")
        self.var_copias_impresion = tk.IntVar(value=1)
        self.var_orientacion_impresion = tk.StringVar(value="Vertical")

        self.menu_impresion = None
        self.logo_principal = None
        self.imagen_extintor = None

        self._construir_interfaz()
        self.agregar_fila()
        self._aplicar_estado_edicion()

    def _construir_interfaz(self):
        self.marco_principal = tk.Frame(self.raiz, bg="#efefef", padx=28, pady=18)
        self.marco_principal.pack(fill="both", expand=True)

        self.marco_superior = tk.Frame(self.marco_principal, bg="#efefef")
        self.marco_superior.pack(fill="x")
        self.marco_superior.grid_columnconfigure(0, weight=3)
        self.marco_superior.grid_columnconfigure(1, weight=1)

        self._crear_bloque_encabezado_izquierdo(self.marco_superior)
        self._crear_bloque_logo_derecho(self.marco_superior)

        self._crear_bloque_destinatario()
        self._crear_tabla_y_totales()
        self._crear_bloque_pie()

    def _crear_bloque_encabezado_izquierdo(self, padre: tk.Frame):
        marco_izquierdo = tk.Frame(padre, bg="#efefef")
        marco_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

        tk.Label(
            marco_izquierdo,
            text="EQUIPOS CONTRA INCENDIO GREIG HERMANOS LIMITADA",
            font=("Arial", 17, "bold"),
            bg="#efefef",
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        ttk.Separator(marco_izquierdo, orient="horizontal").pack(fill="x", pady=(0, 12))

        for texto in [
            "EXTINTORES NUEVOS  |  RECARGA DE EXTINTORES",
            "GABINETES RED HUMEDA MANTENCIÓN DE CARRETES",
            "EMPRESA CERTIFICADA DECRETO 44",
        ]:
            tk.Label(
                marco_izquierdo,
                text=texto,
                font=("Arial", 12 if "EMPRESA" not in texto else 16, "bold"),
                fg="#b71818",
                bg="#efefef",
                anchor="w",
            ).pack(fill="x", pady=(0, 5))
            ttk.Separator(marco_izquierdo, orient="horizontal").pack(fill="x", pady=(0, 8))

        marco_cotizacion = tk.Frame(marco_izquierdo, bg="#efefef")
        marco_cotizacion.pack(fill="x", pady=(10, 0))

        tk.Frame(marco_cotizacion, bg="#b71818", height=4).pack(side="left", fill="x", expand=True, padx=(0, 14))
        tk.Label(
            marco_cotizacion,
            text="COTIZACIÓN",
            font=("Arial", 30, "bold"),
            fg="#b71818",
            bg="#efefef",
        ).pack(side="left")
        tk.Frame(marco_cotizacion, bg="#b71818", height=4).pack(side="left", fill="x", expand=True, padx=(14, 0))

        tk.Label(
            marco_izquierdo,
            textvariable=self.var_telefono,
            font=("Arial", 22, "bold"),
            fg="#b71818",
            bg="#efefef",
        ).pack(pady=(8, 0))

    def _crear_bloque_logo_derecho(self, padre: tk.Frame):
        marco_derecho = tk.Frame(padre, bg="#efefef")
        marco_derecho.grid(row=0, column=1, sticky="nsew")

        panel_marca = tk.Frame(
            marco_derecho,
            bg="#ffffff",
            bd=1,
            relief="solid",
            width=330,
            height=390,
        )
        panel_marca.pack(fill="both", expand=True)
        panel_marca.pack_propagate(False)

        ruta_logo = Path(__file__).parent / "assets" / "logogermania.png"
        if ruta_logo.exists():
            # El logo se reduce para dejar espacio suficiente al extintor dentro del mismo panel.
            self.logo_principal = tk.PhotoImage(file=str(ruta_logo)).subsample(2, 2)
            tk.Label(panel_marca, image=self.logo_principal, bg="#ffffff").pack(pady=(28, 14))
        else:
            tk.Label(
                panel_marca,
                text="GERMANIA",
                font=("Arial", 24, "bold"),
                fg="#b71818",
                bg="#ffffff",
            ).pack(pady=(28, 14))

        ruta_extintor = Path(__file__).parent / "assets" / "PQS10KGDEFINITIVO.png"
        if ruta_extintor.exists():
            # Se usa una escala mayor en el extintor para que se vea completo y proporcionado.
            self.imagen_extintor = tk.PhotoImage(file=str(ruta_extintor)).subsample(3, 3)
            tk.Label(panel_marca, image=self.imagen_extintor, bg="#ffffff").pack(pady=(0, 16))
        else:
            tk.Label(
                panel_marca,
                text="Imagen extintor no disponible",
                font=("Arial", 11),
                fg="#666666",
                bg="#ffffff",
            ).pack(pady=(0, 20))

    def _crear_bloque_destinatario(self):
        marco_destinatario = tk.Frame(self.marco_principal, bg="#efefef")
        marco_destinatario.pack(fill="x", pady=(20, 10))

        tk.Label(
            marco_destinatario,
            text="SEÑORES,",
            font=("Arial", 15, "bold"),
            bg="#efefef",
            anchor="w",
        ).pack(fill="x")

        self.entrada_senores = tk.Entry(
            marco_destinatario,
            textvariable=self.var_senores,
            font=("Arial", 16, "bold"),
            relief="flat",
            bg="#efefef",
            justify="left",
        )
        self.entrada_senores.pack(fill="x", pady=(8, 8))

        marco_atencion = tk.Frame(marco_destinatario, bg="#efefef")
        marco_atencion.pack(fill="x")

        tk.Label(
            marco_atencion,
            text="ATT:",
            font=("Arial", 14, "bold"),
            bg="#efefef",
        ).pack(side="left")

        self.entrada_atencion = tk.Entry(
            marco_atencion,
            textvariable=self.var_atencion,
            font=("Arial", 14, "bold"),
            relief="flat",
            bg="#efefef",
            justify="left",
        )
        self.entrada_atencion.pack(side="left", fill="x", expand=True, padx=(8, 0))

        tk.Label(
            marco_destinatario,
            text="PRESENTE",
            font=("Arial", 14),
            bg="#efefef",
            anchor="w",
        ).pack(fill="x", pady=(8, 12))

        tk.Label(
            marco_destinatario,
            text="Estimados señores, tenemos el agrado en cotizar lo siguiente:",
            font=("Arial", 14, "bold"),
            bg="#efefef",
            anchor="w",
        ).pack(fill="x")

    def _crear_tabla_y_totales(self):
        self.marco_tabla = tk.Frame(self.marco_principal, bg="#efefef")
        self.marco_tabla.pack(fill="x", pady=(10, 0))

        marco_totales = tk.Frame(self.marco_principal, bg="#efefef")
        marco_totales.pack(fill="x")

        self._crear_fila_total_resumen(marco_totales, "NETO", self.var_neto)
        self._crear_fila_total_resumen(marco_totales, "IVA (19%)", self.var_iva)
        self._crear_fila_total_resumen(marco_totales, "TOTAL", self.var_total, es_total=True)

        marco_botones_tabla = tk.Frame(self.marco_principal, bg="#efefef")
        marco_botones_tabla.pack(fill="x", pady=(14, 10))

        self.boton_agregar_fila = ttk.Button(marco_botones_tabla, text="Agregar fila", command=self.agregar_fila)
        self.boton_agregar_fila.pack(side="left", padx=(0, 8))

        self.boton_eliminar_fila = ttk.Button(marco_botones_tabla, text="Eliminar fila", command=self.eliminar_fila)
        self.boton_eliminar_fila.pack(side="left", padx=(0, 12))

        self.boton_agregar_columna = ttk.Button(marco_botones_tabla, text="Agregar columna", command=self.agregar_columna)
        self.boton_agregar_columna.pack(side="left", padx=(0, 8))

        self.boton_eliminar_columna = ttk.Button(marco_botones_tabla, text="Eliminar columna", command=self.eliminar_columna)
        self.boton_eliminar_columna.pack(side="left")

        self.boton_guardar = ttk.Button(marco_botones_tabla, text="Guardar", command=self.guardar_cotizacion)
        self.boton_guardar.pack(side="right", padx=(8, 0))

        self.boton_editar = ttk.Button(marco_botones_tabla, text="Editar", command=self.editar_cotizacion)
        self.boton_editar.pack(side="right")

        self.boton_imprimir = ttk.Button(marco_botones_tabla, text="Imprimir", command=self.abrir_menu_impresion)
        self.boton_imprimir.pack(side="right", padx=(0, 8))

    def _crear_fila_total_resumen(
        self,
        padre: tk.Frame,
        etiqueta: str,
        variable: tk.StringVar,
        es_total: bool = False,
    ):
        fila = tk.Frame(padre, bg="#efefef")
        fila.pack(fill="x")

        tk.Label(fila, text="", bg="#efefef").pack(side="left", fill="x", expand=True)

        fondo = "#d31b1b" if es_total else "#efefef"
        color_texto = "white" if es_total else "#111111"
        ancho_etiqueta = 14

        tk.Label(
            fila,
            text=etiqueta,
            width=ancho_etiqueta,
            anchor="e",
            bg=fondo,
            fg=color_texto,
            font=("Arial", 13, "bold"),
            padx=10,
            pady=7,
        ).pack(side="left")

        tk.Label(
            fila,
            textvariable=variable,
            width=14,
            anchor="e",
            bg=fondo,
            fg=color_texto,
            font=("Arial", 16, "bold"),
            padx=12,
            pady=7,
        ).pack(side="left")

    def _crear_bloque_pie(self):
        marco_pie = tk.Frame(self.marco_principal, bg="#efefef")
        marco_pie.pack(fill="x", pady=(12, 0))
        marco_pie.grid_columnconfigure(0, weight=1)
        marco_pie.grid_columnconfigure(1, weight=1)

        marco_izquierdo = tk.Frame(marco_pie, bg="#efefef")
        marco_izquierdo.grid(row=0, column=0, sticky="nw")

        tk.Label(
            marco_izquierdo,
            text="PLAZO DE ENTREGA: INMEDIATA",
            font=("Arial", 15, "bold"),
            bg="#efefef",
        ).pack(anchor="w")
        tk.Label(
            marco_izquierdo,
            text="FORMA DE PAGO: A CONVENIR",
            font=("Arial", 15, "bold"),
            bg="#efefef",
        ).pack(anchor="w", pady=(8, 12))

        # El logo del pie se elimina para evitar que aparezca duplicado en la cotización.

        marco_derecho = tk.Frame(marco_pie, bg="#efefef")
        marco_derecho.grid(row=0, column=1, sticky="ne")

        tk.Label(
            marco_derecho,
            text="Se despide atentamente.",
            font=("Arial", 11),
            bg="#efefef",
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        self.entrada_nombre_ejecutivo = tk.Entry(
            marco_derecho,
            textvariable=self.var_nombre_ejecutivo,
            font=("Arial", 16, "bold"),
            relief="flat",
            bg="#efefef",
            justify="left",
        )
        self.entrada_nombre_ejecutivo.pack(fill="x")

        self.entrada_cargo_ejecutivo = tk.Entry(
            marco_derecho,
            textvariable=self.var_cargo_ejecutivo,
            font=("Arial", 13),
            relief="flat",
            bg="#efefef",
            justify="left",
        )
        self.entrada_cargo_ejecutivo.pack(fill="x", pady=(2, 12))

        tk.Entry(
            marco_derecho,
            textvariable=self.var_telefono,
            font=("Arial", 13, "bold"),
            relief="flat",
            bg="#efefef",
            justify="left",
        ).pack(fill="x", pady=(0, 6))

        tk.Entry(
            marco_derecho,
            textvariable=self.var_correo,
            font=("Arial", 13, "bold"),
            relief="flat",
            bg="#efefef",
            justify="left",
        ).pack(fill="x")

    def agregar_fila(self):
        if self.bloqueado:
            return

        nuevas_celdas = []
        for indice_columna, _ in enumerate(self.columnas):
            entrada = tk.Entry(self.marco_tabla, font=("Arial", 15), relief="solid", bd=1)
            if indice_columna == 0:
                entrada.insert(0, "1")
                entrada.configure(justify="center")
            elif indice_columna == 2:
                entrada.insert(0, "0")
                entrada.configure(justify="right")
            elif indice_columna == len(self.columnas) - 1:
                entrada.insert(0, "$0")
                entrada.configure(justify="right")
            else:
                entrada.configure(justify="left")
            entrada.bind("<KeyRelease>", self._actualizar_calculos_automaticos)
            nuevas_celdas.append(entrada)

        self.filas.append(nuevas_celdas)
        self._renderizar_tabla()
        self._actualizar_calculos_automaticos()

    def eliminar_fila(self):
        if self.bloqueado:
            return
        if len(self.filas) <= 1:
            return
        fila = self.filas.pop()
        for celda in fila:
            celda.destroy()
        self._renderizar_tabla()
        self._actualizar_calculos_automaticos()

    def agregar_columna(self):
        if self.bloqueado:
            return

        nombre = f"Columna {len(self.columnas) - 3}" if len(self.columnas) > 3 else "Columna 1"
        self.columnas.insert(-1, nombre)

        for fila in self.filas:
            entrada = tk.Entry(self.marco_tabla, font=("Arial", 15), relief="solid", bd=1)
            entrada.bind("<KeyRelease>", self._actualizar_calculos_automaticos)
            fila.insert(-1, entrada)

        self._renderizar_tabla()

    def eliminar_columna(self):
        if self.bloqueado:
            return
        if len(self.columnas) <= 4:
            return

        indice = len(self.columnas) - 2
        self.columnas.pop(indice)

        for fila in self.filas:
            celda = fila.pop(indice)
            celda.destroy()

        self._renderizar_tabla()
        self._actualizar_calculos_automaticos()

    def _renderizar_tabla(self):
        for widget in self.marco_tabla.grid_slaves():
            widget.grid_forget()

        for indice_columna in range(self.max_columnas_renderizadas + 2):
            self.marco_tabla.grid_columnconfigure(indice_columna, weight=0, minsize=0)

        self.entradas_encabezado = []
        for indice_columna, titulo in enumerate(self.columnas):
            encabezado = tk.Entry(
                self.marco_tabla,
                font=("Arial", 14, "bold"),
                relief="solid",
                bd=1,
                bg="#d31b1b",
                fg="white",
                justify="center",
            )
            encabezado.insert(0, titulo.upper())
            encabezado.bind(
                "<FocusOut>",
                lambda evento, i=indice_columna: self._actualizar_nombre_columna(i, evento),
            )
            encabezado.configure(state="readonly" if self.bloqueado else "normal")
            encabezado.grid(row=0, column=indice_columna, sticky="nsew", ipady=7)
            self.entradas_encabezado.append(encabezado)

        for indice_fila, fila in enumerate(self.filas, start=1):
            for indice_columna, celda in enumerate(fila):
                if indice_columna == len(self.columnas) - 1:
                    celda.configure(state="readonly", fg="#a51818", font=("Arial", 16, "bold"))
                else:
                    celda.configure(state="readonly" if self.bloqueado else "normal")
                    if indice_columna == 0:
                        celda.configure(justify="center")
                    elif indice_columna >= 2:
                        celda.configure(justify="right")
                celda.grid(row=indice_fila, column=indice_columna, sticky="nsew", ipady=10)

        for indice_columna in range(len(self.columnas)):
            ancho_columna = self._obtener_ancho_columna(indice_columna)
            self.marco_tabla.grid_columnconfigure(indice_columna, weight=0, minsize=ancho_columna)

        self.marco_tabla.grid_columnconfigure(len(self.columnas), weight=1, minsize=0)
        self.max_columnas_renderizadas = max(self.max_columnas_renderizadas, len(self.columnas))

    def _obtener_ancho_columna(self, indice_columna: int) -> int:
        anchos_base = [140, 420, 190, 190]
        if indice_columna < len(anchos_base):
            return anchos_base[indice_columna]
        return 170

    def _actualizar_nombre_columna(self, indice_columna: int, evento):
        self.columnas[indice_columna] = evento.widget.get().strip() or self.columnas[indice_columna]

    def guardar_cotizacion(self):
        self.bloqueado = True
        self._aplicar_estado_edicion()

    def editar_cotizacion(self):
        self.bloqueado = False
        self._aplicar_estado_edicion()

    def _aplicar_estado_edicion(self):
        # Este método concentra el estado editable de toda la pantalla para evitar
        # inconsistencias entre los botones y los campos de datos al guardar/editar.
        estado_controles = "disabled" if self.bloqueado else "normal"
        self.boton_agregar_fila.configure(state=estado_controles)
        self.boton_eliminar_fila.configure(state=estado_controles)
        self.boton_agregar_columna.configure(state=estado_controles)
        self.boton_eliminar_columna.configure(state=estado_controles)

        self.boton_guardar.configure(state="disabled" if self.bloqueado else "normal")
        self.boton_editar.configure(state="normal" if self.bloqueado else "disabled")

        self.entrada_nombre_ejecutivo.configure(state="readonly" if self.bloqueado else "normal")
        self.entrada_cargo_ejecutivo.configure(state="readonly" if self.bloqueado else "normal")
        self.entrada_senores.configure(state="readonly" if self.bloqueado else "normal")
        self.entrada_atencion.configure(state="readonly" if self.bloqueado else "normal")

        self._renderizar_tabla()

    def abrir_menu_impresion(self):
        if self.menu_impresion and self.menu_impresion.winfo_exists():
            self.menu_impresion.lift()
            self.menu_impresion.focus_force()
            return

        self.menu_impresion = tk.Toplevel(self.raiz)
        self.menu_impresion.title("Imprimir")
        self.menu_impresion.configure(bg="#ececec")
        self.menu_impresion.geometry("1040x640")
        self.menu_impresion.minsize(960, 580)
        self.menu_impresion.transient(self.raiz)
        self.menu_impresion.grab_set()

        marco_lateral = tk.Frame(self.menu_impresion, bg="#ececec", width=320, padx=18, pady=16)
        marco_lateral.pack(side="left", fill="y")
        marco_lateral.pack_propagate(False)

        tk.Label(
            marco_lateral,
            text="Imprimir",
            font=("Arial", 20, "bold"),
            bg="#ececec",
            anchor="w",
        ).pack(fill="x", pady=(0, 14))

        boton_imprimir_menu = ttk.Button(
            marco_lateral,
            text="Imprimir",
            command=self._imprimir_desde_menu,
        )
        boton_imprimir_menu.pack(fill="x", ipady=8, pady=(0, 14))

        tk.Label(
            marco_lateral,
            text="Copias:",
            font=("Arial", 10, "bold"),
            bg="#ececec",
            anchor="w",
        ).pack(fill="x")
        control_copias = tk.Spinbox(
            marco_lateral,
            from_=1,
            to=999,
            textvariable=self.var_copias_impresion,
            font=("Arial", 10),
            width=8,
        )
        control_copias.pack(anchor="w", pady=(4, 10))

        tk.Label(
            marco_lateral,
            text="Orientación:",
            font=("Arial", 10, "bold"),
            bg="#ececec",
            anchor="w",
        ).pack(fill="x")
        combo_orientacion = ttk.Combobox(
            marco_lateral,
            textvariable=self.var_orientacion_impresion,
            values=["Vertical", "Horizontal"],
            state="readonly",
        )
        combo_orientacion.pack(fill="x", pady=(4, 14))
        combo_orientacion.bind("<<ComboboxSelected>>", lambda _: self._actualizar_vista_previa_impresion())

        tk.Label(
            marco_lateral,
            text="Vista previa",
            font=("Arial", 10, "bold"),
            bg="#ececec",
            anchor="w",
        ).pack(fill="x", pady=(2, 6))

        tk.Label(
            marco_lateral,
            text=(
                "Este panel replica un flujo de impresión tipo Office: "
                "configuras y luego envías con el botón Imprimir."
            ),
            justify="left",
            wraplength=280,
            bg="#ececec",
            fg="#3f3f3f",
            font=("Arial", 9),
        ).pack(fill="x")

        marco_vista = tk.Frame(self.menu_impresion, bg="#dcdcdc", padx=18, pady=16)
        marco_vista.pack(side="left", fill="both", expand=True)

        self.texto_vista_previa = tk.Text(
            marco_vista,
            font=("Times New Roman", 12),
            bg="white",
            relief="solid",
            bd=1,
            wrap="word",
            padx=24,
            pady=18,
        )
        self.texto_vista_previa.pack(fill="both", expand=True)
        self.texto_vista_previa.configure(state="disabled")

        self._actualizar_vista_previa_impresion()

    def _obtener_texto_vista_previa(self) -> str:
        lineas = [
            "COTIZACIÓN",
            "",
            f"Señores: {self.var_senores.get()}",
            f"Atención: {self.var_atencion.get()}",
            "",
            "DETALLE",
            "-" * 82,
        ]

        encabezado = " | ".join(self.columnas)
        lineas.append(encabezado)
        lineas.append("-" * 82)

        for fila in self.filas:
            valores = [celda.get().strip() for celda in fila]
            lineas.append(" | ".join(valores))

        lineas.extend(
            [
                "-" * 82,
                f"Neto: {self.var_neto.get()}",
                f"IVA: {self.var_iva.get()}",
                f"Total: {self.var_total.get()}",
                "",
                f"Ejecutivo: {self.var_nombre_ejecutivo.get()}",
                f"Cargo: {self.var_cargo_ejecutivo.get()}",
            ]
        )
        return "\n".join(lineas)

    def _actualizar_vista_previa_impresion(self):
        if not hasattr(self, "texto_vista_previa"):
            return

        orientacion = self.var_orientacion_impresion.get().strip().lower()
        ancho = 130 if orientacion == "horizontal" else 95

        contenido = self._obtener_texto_vista_previa()
        contenido = "\n".join(
            linea if len(linea) <= ancho else f"{linea[:ancho]}..."
            for linea in contenido.splitlines()
        )

        self.texto_vista_previa.configure(state="normal")
        self.texto_vista_previa.delete("1.0", tk.END)
        self.texto_vista_previa.insert(
            "1.0",
            f"Orientación: {self.var_orientacion_impresion.get()}\n\n{contenido}",
        )
        self.texto_vista_previa.configure(state="disabled")

    def _imprimir_desde_menu(self):
        try:
            copias = max(1, int(self.var_copias_impresion.get()))
        except (TypeError, ValueError):
            messagebox.showerror("Impresión", "Ingrese una cantidad de copias válida.")
            return

        try:
            ruta_temporal = self._generar_archivo_impresion()
            self._enviar_a_impresora(ruta_temporal, copias)
            if self.menu_impresion and self.menu_impresion.winfo_exists():
                self.menu_impresion.destroy()
            messagebox.showinfo("Impresión", "Se envió el documento a impresión.")
        except Exception as error:
            messagebox.showerror("Error de impresión", f"No se pudo imprimir: {error}")

    def _generar_archivo_impresion(self) -> str:
        # Se crea un archivo temporal PostScript con el contenido visible de la ventana.
        # El comando de impresión toma este archivo como fuente para mantener el diseño actual.
        archivo = tempfile.NamedTemporaryFile(delete=False, suffix=".ps")
        archivo.close()
        self.raiz.update_idletasks()
        self.raiz.postscript(file=archivo.name, colormode="color")
        return archivo.name

    def _enviar_a_impresora(self, ruta_archivo: str, copias: int):
        if sys.platform.startswith("win"):
            # En Windows se envía una impresión por cada copia solicitada.
            for _ in range(copias):
                os.startfile(ruta_archivo, "print")
            return

        comando = ["lpr", "-#", str(copias), ruta_archivo]
        proceso = subprocess.run(
            comando,
            check=False,
            capture_output=True,
            text=True,
        )
        if proceso.returncode != 0:
            mensaje_error = proceso.stderr.strip() or "No fue posible invocar el comando de impresión."
            raise RuntimeError(mensaje_error)

    def _actualizar_calculos_automaticos(self, *_):
        total_neto = 0

        for fila in self.filas:
            if len(fila) < 4:
                continue

            cantidad = self._texto_a_numero(fila[0].get())
            valor_unitario = self._texto_a_numero(fila[2].get())
            total_fila = int(cantidad * valor_unitario)

            total_neto += total_fila
            fila[-1].configure(state="normal")
            fila[-1].delete(0, tk.END)
            fila[-1].insert(0, self._formatear_moneda(total_fila))
            fila[-1].configure(state="readonly")

        iva = int(total_neto * 0.19)
        total = total_neto + iva

        self.var_neto.set(self._formatear_moneda(total_neto))
        self.var_iva.set(self._formatear_moneda(iva))
        self.var_total.set(self._formatear_moneda(total))

    def _texto_a_numero(self, texto: str) -> float:
        texto_limpio = texto.replace("$", "").replace(".", "").replace(",", ".").strip()
        if not texto_limpio:
            return 0
        try:
            return float(texto_limpio)
        except ValueError:
            return 0

    def _formatear_moneda(self, valor: int) -> str:
        return f"${valor:,.0f}".replace(",", ".")


def main():
    raiz = tk.Tk()
    AplicacionCotizacion(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
