from dataclasses import dataclass

from skills import FeroKick, PowerInject, Skill


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


warrior = UnitClass(name='Воин',
                    max_health=60.0,
                    max_stamina=30.0,
                    attack=0.8,
                    stamina=0.9,
                    armor=1.2,
                    skill=FeroKick())

thief = UnitClass(name='Вор',
                  max_health=50.0,
                  max_stamina=25.0,
                  attack=1.5,
                  stamina=1.2,
                  armor=1.0,
                  skill=PowerInject())

dict_class: dict[str, UnitClass] = {warrior.name: warrior,
                                    thief.name: thief}
