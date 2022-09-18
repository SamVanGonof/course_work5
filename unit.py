from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint

from base_classes import UnitClass
from equipment import Weapon, Armor

STAMINA_AFTER_MOVE = 1


class BaseUnit(ABC):
    def __init__(self, name: str, unit: UnitClass):
        self.name = name
        self.unit_class = unit
        self.health_points = unit.max_health
        self.stamina_points = unit.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = True

    def get_weapon(self, weapon: Weapon):
        """
        Метод присваивания оружия
        """
        self.weapon = weapon

    def get_armor(self, armor: Armor):
        """
        Присваивание брони
        """
        self.armor = armor

    def _count_damage(self, target: BaseUnit) -> float:
        """
        Подсчет нанесенного урона и вычет выносливости защищаемого
        """
        damage = 0
        if target.stamina_points > target.weapon.stamina_per_hit:
            target.stamina_points -= target.weapon.stamina_per_hit
            target.stamina_points = round(target.stamina_points, 1)

            if self.stamina_points > self.armor.stamina_per_turn:
                self.stamina_points -= self.armor.stamina_per_turn
                self.stamina_points = round(self.stamina_points, 1)

                damage = target.weapon.damage * target.unit_class.attack - self.armor.defence
            else:
                damage = target.weapon.damage * target.unit_class.attack

        self.get_damage(damage)
        return round(damage, 1)

    def get_damage(self, damage: int):
        """
        Получение урона
        """
        if damage  > 0:
            self.health_points -= damage
            self.health_points = round(self.health_points, 1)

    def skill_attack(self, target: BaseUnit) -> str:
        """
        Применение навыка
        """
        if self._is_skill_used:
            return 'Навык уже использован.'

        return self.unit_class.skill.using_skill(self, target)

    def _hit_target(self, target: BaseUnit) -> str:
        """
        Удар по цели
        """
        if self.stamina_points > self.weapon.stamina_per_hit:
            damage = target._count_damage(self)

            if target.stamina_points > target.armor.stamina_per_turn and damage <= 0.0:
                return f"{self.name} используя {self.weapon.name} наносит удар, " \
                        f"но {target.armor.name} cоперника его останавливает."

            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} " \
                    f"соперника и наносит {damage} урона."

        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

    @abstractmethod
    def hit(self, target: BaseUnit):
        pass


class Player(BaseUnit):
    def hit(self, target: BaseUnit):
        return self._hit_target(target)


class Enemy(BaseUnit):
    def hit(self, target: BaseUnit):
        if 5 > randint(0, 100) and self._is_skill_used:
            self._is_skill_used = False
            return self.unit_class.skill.using_skill(self, target)

        return self._hit_target(target)
