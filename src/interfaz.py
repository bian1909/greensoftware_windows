import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageFont
import os
import sys
from io import BytesIO
# Solución para importación relativa
try:
    from src.proyectoco2 import EnergyMonitor
except ImportError:
    from proyectoco2 import EnergyMonitor


def resource_path(relative_path):
    """Convierte rutas relativas a absolutas para .exe y desarrollo"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", relative_path)


class MonitorApp:
    def __init__(self, root_window):
        self.root = root_window
        self.monitor = EnergyMonitor()
        self.root.title("co2 generado")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.attributes("-alpha", 0.8)  # Usar un solo valor consistente
        self.root.protocol("WM_DELETE_WINDOW", self._al_cerrar)

        # Configura rutas base
        self.font_path = resource_path(os.path.join("fonts", "DS-DIGIB.TTF"))
        self.imagenes_texto = []
        
        self._setup_ui()
        self._set_window_icon()
        self._actualizar()

    def _setup_ui(self):
        """Configura la interfaz sin ImageTk"""
        self.canvas = Canvas(self.root, width=500, height=600, highlightthickness=0, bg='black')
        self.canvas.place(x=0, y=0)
        
        # Carga el fondo con BytesIO
        try:
            bg_path = resource_path(os.path.join("assets", "background.png"))
            self.original_bg = Image.open(bg_path).resize((500, 600))
            
            # Convertir PIL.Image a tk.PhotoImage sin ImageTk
            bio = BytesIO()
            self.original_bg.save(bio, format="PNG")
            self.fondo_img = tk.PhotoImage(data=bio.getvalue())
            self.fondo_label = self.canvas.create_image(0, 0, anchor='nw', image=self.fondo_img)
        except Exception as e:
            print(f"⚠️ Error al cargar fondo: {e}")
            self.canvas.configure(bg='black')
        
        self._draw_glow_text("Cargando datos...", 280, "#00FFFF", 32)

    # Versión segura para Windows sin dependencias adicionales
    def _set_window_icon(self):
        try:
            if sys.platform == 'win32':
                # Rutas para Windows (.ico)
                icon_paths = [
                    resource_path(os.path.join('assets', 'icono.ico')),
                    resource_path('icono.ico')
                ]
                
                for path in icon_paths:
                    if os.path.exists(path):
                        try:
                            self.root.iconbitmap(path)
                            return
                        except Exception as e:
                            print(f"Error al cargar icono {path}: {str(e)}")
                            continue
                
                print("⚠️ No se encontró icono .ico válido para Windows")
            
            # Comportamiento para Linux/Mac (.png)
            icon_path = resource_path(os.path.join('assets', 'icono.png'))
            if os.path.exists(icon_path):
                try:
                    img = tk.PhotoImage(file=icon_path)
                    self.root.tk.call('wm', 'iconphoto', self.root._w, img)
                except Exception as e:
                    print(f"Error al cargar icono PNG: {str(e)}")
                    
        except Exception as e:
            print(f"Error inesperado en _set_window_icon: {str(e)}")


    def _draw_glow_text(self, text, y, color="#00ffff", font_size=36):
        """Dibuja texto con efecto de resplandor sin ImageTk"""
        try:
            font = (ImageFont.truetype(self.font_path, font_size) 
                   if os.path.exists(self.font_path) 
                   else ImageFont.load_default())
            
            # Crear imagen PIL
            img = Image.new("RGBA", (500, 60), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            text_width = draw.textlength(text, font=font)
            x_position = (500 - text_width) // 2
            
            # Efecto de resplandor
            for offset in range(1, 6):
                draw.text((x_position + offset, 10 + offset), 
                         text, font=font, fill=color + "40")
            
            draw.text((x_position, 10), text, font=font, fill=color)

            # Convertir a PhotoImage
            bio = BytesIO()
            img.save(bio, format="PNG")
            img_tk = tk.PhotoImage(data=bio.getvalue())
            
            self.canvas.create_image(0, y, anchor='nw', image=img_tk, tags="text")
            self.imagenes_texto.append(img_tk)  # Evita garbage collection

        except Exception as e:
            print(f"⚠️ Error al dibujar texto: {e}")

    def _actualizar(self):
        try:
            self.canvas.delete("text")
            self.imagenes_texto.clear()

            self.monitor.update()
            metrics = self.monitor.get_metrics()

            if not all(key in metrics for key in ['cpu_usage', 'total_co2']):
                raise ValueError("Faltan métricas esenciales")

            y = 30
            self._draw_glow_text(f"CPU: {metrics['cpu_usage']:.1f}%", y, "#00FFFF", 54)
            y += 65
            self._draw_glow_text(f"RAM: {metrics['ram_usage']:.1f}%", y, "#00FFFF", 54)
            y += 65
            self._draw_glow_text(f"Consumo: {metrics['current']:.2f} W", y, "#00FFFF", 38)
            y += 65
            self._draw_glow_text(f"Promedio: {metrics['average']:.2f} W", y, "#00FFFF", 38)
            y += 65
            self._draw_glow_text(f"Co2: {metrics['total_co2']:.2f} g", y, "#00FFFF", 42)

        except Exception as e:
            print(f" Error crítico: {e}")
            self._draw_glow_text("Error: Reinicia la app", 200, "#FF0000", 24)

        finally:
            self.root.after(1000, self._actualizar)

    def _al_cerrar(self):
        try:
            total = self.monitor.get_metrics()['total_co2']
            self.canvas.delete("text")
            self.imagenes_texto.clear()
            self._draw_glow_text(f"Co2 acumulado final: {total:.2f} g", 450, "#FFFFFF", 40)
            self.root.after(5000, self.root.destroy)
        except Exception:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()
