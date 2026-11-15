"""Compatibilidad: implementación organizada dentro de amac."""

from amac.cultivos.catalogo import (
    CROPS_DB,
)
from amac.cultivos.consultas import (
    get_all_crops,
    get_crop,
    get_crops_by_category,
    get_compatible_crops,
)
