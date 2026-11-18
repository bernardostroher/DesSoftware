"""Módulo que define os modelos de dados para notas, eventos, vozes e partituras."""
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar

@dataclass(frozen = True, slots = True)
class Nota:
    """Representa uma nota musical com suas propriedades."""
    nome: str
    oitava: int
    volume: int
    duracao: int
    acidente: str = ''

class TipoEvento(Enum):
    """Enumeração para os tipos de eventos musicais."""
    TROCA_INSTRUMENTO = 'troca_instrumento'
    DEFINIR_BPM = 'definir_bpm'
    ALTERAR_BPM = 'alterar_bpm'
    ATRASO = 'atraso'
    PAUSA = 'pausa'

@dataclass(frozen = True, slots = True)
class Evento:
    """Representa um evento musical com seu tipo e valor associado."""
    tipo: TipoEvento
    valor: int

@dataclass(slots = True)
class EstadoVoz:
    """Representa o estado atual de uma voz musical, incluindo oitava, volume e instrumento."""
    VOLUME_MAX: ClassVar[int] = 127
    OITAVA_MAX: ClassVar[int] = 9

    oitava: int
    volume: int
    instrumento: int
    ultima_nota: Nota | None = None

    def dobrar_volume(self):
        """Dobra o volume da voz, respeitando o limite máximo."""
        self.volume = min(self.volume * 2, self.VOLUME_MAX)

@dataclass(slots = True)
class Voz:
    """Representa uma voz musical, contendo uma lista de elementos musicais (notas e eventos)."""
    lista_elementos: list[Nota | Evento] = field(default_factory=list)

@dataclass(slots = True)
class Partitura:
    """Representa uma partitura musical, contendo uma lista de vozes."""
    vozes: list[Voz] = field(default_factory=list)

    def __post_init__(self):
        if len(self.vozes) > 4:
            raise ValueError("A partitura pode ter no máximo 4 vozes.")
