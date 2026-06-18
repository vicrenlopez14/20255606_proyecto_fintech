"""
Materia: Desarrollo de Aplicaciones Informáticas (ESEN 2026)
Proyecto Integrador: Backend - Caso Fintech
Módulo: Capa de Lógica de Negocio y Dominio (Semana 5 Consolidada)
Catedrático: Lic. Alvin Portillo
"""

from typing import Optional

class Credit:
    """
    Representa la entidad 'Credit' (Crédito).
    Maneja los atributos públicos del producto financiero solicitado.
    """
    def __init__(self, amount: float, rate: float, approved: bool = False):
        self.amount: float = amount      # Monto solicitado
        self.rate: float = rate          # Tasa de interés anual (ej: 0.12 para 12%)
        self.approved: bool = approved    # Estado de aprobación en el sistema

    def calculate_risk(self) -> bool:
        """
        Regla de Negocio: Evalúa si el crédito representa un riesgo alto.
        Retorna True si el monto supera los $50,000 o la tasa supera el 15% (0.15).
        """
        if self.amount > 50000.0 or self.rate > 0.15:
            return True   # Riesgo Alto
        return False      # Riesgo Bajo


class Client:
    """
    Representa la entidad 'Client' (Cliente).
    Aplica encapsulamiento estricto (Name Mangling) para proteger la información
    financiera sensible e implementa una relación de Agregación con 'Credit'.
    """
    def __init__(self, id_client: int, name: str, income: float):
        # Atributos privados (Ocultos mediante Name Mangling)
        self.__id_client: int = id_client
        self.__name: str = name
        self.__income: float = income
        
        # Relación de Agregación: El cliente 'tiene un' crédito, pero puede existir sin él.
        # Se inicializa vacío (None) demostrando que las vidas de los objetos son independientes.
        self.credit: Optional[Credit] = None

    # --- Getters Públicos (Decoradores @property) ---
    # Permiten el acceso seguro de lectura a los datos desde la futura capa de API.
    
    @property
    def id_client(self) -> int:
        return self.__id_client

    @property
    def name(self) -> str:
        return self.__name

    @property
    def income(self) -> float:
        return self.__income

    # --- Métodos de Interacción ---

    def assign_credit(self, credit: Credit) -> None:
        """
        Establece la relación de agregación asociando un objeto Crédito al Cliente.
        """
        self.credit = credit

    def get_profile(self) -> str:
        """
        Formatea el estado completo del cliente y su situación financiera actual.
        Demuestra la comunicación entre el objeto Cliente y su objeto Crédito agregado.
        """
        profile = f"--- PERFIL DEL CLIENTE #{self.__id_client} ---\n"
        profile += f"Nombre: {self.__name}\n"
        profile += f"Ingresos Mensuales: ${self.__income:,.2f}\n"
        
        # Validación de la agregación
        if self.credit:
            status = "Aprobado" if self.credit.approved else "Pendiente de Aprobación"
            risk = "ALTO" if self.credit.calculate_risk() else "BAJO"
            profile += f"Crédito Solicitado: ${self.credit.amount:,.2f} (Tasa: {self.credit.rate * 100}%)\n"
            profile += f"Estado de la Solicitud: {status}\n"
            profile += f"Nivel de Riesgo Evaluado: {risk}\n"
        else:
            profile += "Crédito Asociado: Ninguno activo en este momento.\n"
            
        return profile


# --- Bloque de Prueba y Validación en Consola ---
if __name__ == "__main__":
    print("=== CONTROL DE CALIDAD DE SOFTWARE: VERIFICACIÓN DE OBJETOS ===\n")

    # 1. Creación de datos de prueba de forma independiente
    cliente_regular = Client(id_client=101, name="Carlos Ramos", income=1800.0)
    credito_aprobado = Credit(amount=15000.0, rate=0.08, approved=True)

    # 2. Prueba del estado inicial (Agregación vacía)
    print("Paso 1: Validando cliente nuevo sin productos:")
    print(cliente_regular.get_profile())

    # 3. Activación de la Agregación
    cliente_regular.assign_credit(credito_aprobado)
    print("Paso 2: Validando vinculación de crédito (Agregación):")
    print(cliente_regular.get_profile())

    # 4. Auditoría de Seguridad: Verificación del Encapsulamiento
    print("Paso 3: Validando el escudo de aislamiento (Encapsulamiento):")
    try:
        # Esto debe fallar y disparar la excepción obligatoriamente
        print(cliente_regular.__income)
    except AttributeError:
        print("[OK] Encapsulamiento Exitoso: El atributo '__income' está protegido contra accesos directos.")
        print(f"[OK] Acceso Autorizado mediante Getter Seguro: ${cliente_regular.income:,.2f}\n")
    
    print("=== COMPROBACIÓN COMPLETADA: CÓDIGO LISTO PARA LA CAPA DE SERVIDOR ===")