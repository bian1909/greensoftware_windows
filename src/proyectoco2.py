import psutil
import time
from collections import deque


class EnergyMonitor:
    def __init__(self):
        # Parámetros de consumo (ajustar según tu hardware)
        self.cpu_min_power = 3.0      # Watts en reposo
        self.cpu_max_power = 40.0     # Watts bajo carga máxima
        self.ram_watts_per_gb = 0.3    # Consumo RAM por GB
        # Factor de emisiones (kgCO₂/kWh)
        self.co2_per_kwh = 0.475
        
        # Sistema de acumulación
        self.total_co2 = 0.0           # kg CO₂ acumulado
        self.power_history = deque(maxlen=20)  # Historial de consumo
        
        # Para cálculos de promedio
        self.last_update = time.time()
        self.last_usage = 0.0
        self.cumulative_power = 0.0

    def get_cpu_power(self):
        """Calcula consumo de CPU con modelo no lineal"""
        usage = psutil.cpu_percent(interval=1) / 100
        # Filtro de suavizado
        usage = 0.7 * usage + 0.3 * self.last_usage
        self.last_usage = usage
        power_range = self.cpu_max_power - self.cpu_min_power
        return self.cpu_min_power + power_range * (usage ** 1.8)

    def get_ram_power(self):
        """Calcula consumo de RAM"""
        ram_used = psutil.virtual_memory().used / (1024 ** 3)  # GB
        return ram_used * self.ram_watts_per_gb

    def update(self):
        """Actualiza mediciones y acumula CO₂"""
        now = time.time()
        elapsed = now - self.last_update
        
        # Obtener consumo actual
        current_power = self.get_cpu_power() + self.get_ram_power()
        self.power_history.append(current_power)
        
        # Calcular energía consumida (kWh) y CO₂ acumulado
        energy_kwh = (current_power / 1000) * (elapsed / 3600)
        self.total_co2 += energy_kwh * self.co2_per_kwh
        
        # Actualizar para siguiente ciclo
        self.last_update = now
        return current_power

    def get_metrics(self):
        avg_power = sum(self.power_history) / len(self.power_history) if self.power_history else 0
        return {
            'current': self.power_history[-1] if self.power_history else 0,
            'average': avg_power,
            'total_co2': self.total_co2 * 1000,  # Convertir a gramos
            'cpu_usage': psutil.cpu_percent(),
            'ram_usage': psutil.virtual_memory().percent
        }


def main():
    monitor = EnergyMonitor()
    print("Monitor de energía iniciado (Ctrl+C para detener)...")
    
    try:
        while True:
            monitor.update()
            metrics = monitor.get_metrics()
            
            # Limpiar pantalla (funciona en Linux y Windows)
            print("\033[H\033[J", end="")
            
            print(" MONITOR EN TIEMPO REAL ")
            print(f"Consumo actual: {metrics['current']:.2f}W")
            print(f"Promedio (últ. 5s): {metrics['average']:.2f}W")
            print(f"CO₂ acumulado: {metrics['total_co2']:.2f}g")
            print(f"\nCPU: {metrics['cpu_usage']:.1f}% | RAM: {metrics['ram_usage']:.1f}%")
            
            time.sleep(1)  # Actualizar cada 0.5 segundos
            
    except KeyboardInterrupt:
        print("\nMonitor detenido")
        print(f"\nRESUMEN FINAL:")
        print(f"Total CO₂ generado: {metrics['total_co2']:.2f}g")


if __name__ == "__main__":
    main()