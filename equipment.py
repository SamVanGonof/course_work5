from dataclasses import dataclass, field
from random import uniform

import marshmallow_dataclass
import json


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        return uniform(self.min_damage, self.max_damage)


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class EquipmentData:
    weapons: list[Weapon] = field(default_factory=list)
    armors: list[Armor] = field(default_factory=list)


class Equipment:
    @staticmethod
    def _json_read(path: str) -> EquipmentData:
        """
        Загрузка данных из json с экипировкой в EquipmentData
        """
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)

        with open(path, encoding='UTF-8') as file:
            return equipment_schema().load(json.load(file))

    def __init__(self, path_data: str) -> None:
        self.equipment: EquipmentData = self._json_read(path_data)

    def get_weapon(self, weapon_name: str) -> Weapon:
        """
        Получение оружия по его имени
        """
        return next(filter(lambda x: x.name == weapon_name, self.equipment.weapons))

    def get_armor(self, name_armor: str) -> Armor:
        """
        Получение брони по его имени
        """
        return next(filter(lambda x: x.name == name_armor, self.equipment.armors))

    def get_weapon_name(self) -> list[str]:
        """
        Получение списка имен оружия
        """
        return list(map(lambda x: x.name, self.equipment.weapons))

    def get_armor_name(self) -> list[str]:
        """
        Получение списка имен брони
        """
        return list(map(lambda x: x.name, self.equipment.armors))
