from abc import ABC, abstractmethod


class Skill(ABC):
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def attack(self):
        pass

    @property
    @abstractmethod
    def stamina_per_hit(self):
        pass

    @abstractmethod
    def skill_effect(self):
        """
        Нанесение урона навыком
        """
        pass

    def using_skill(self, user, target) -> str:
        """
        Использование навыка

        :param user: пользователь, использующий умение.
        :param target: цель под атакой пользователя.
        """
        self.user = user
        self.target = target

        if self.user.stamina_points > self.stamina_per_hit:
            return self.skill_effect()

        return f"{self.user.name} попытался {self.name}, но не хватило выносливости."


class FeroKick(Skill):
    name: str = 'Свирепый пинок'
    attack: int = 6
    stamina_per_hit: int = 12

    def skill_effect(self) -> str:
        self.target.get_damage(self.attack)
        self.user.stamina_points -= self.stamina_per_hit
        return f"{self.user.name} применил свирепый пинок и нанес {self.attack}"


class PowerInject(Skill):
    name: str = 'Могучий укол'
    attack: int = 5
    stamina_per_hit: int = 15

    def skill_effect(self) -> str:
        self.target.get_damage(self.attack)
        self.user.stamina_points -= self.stamina_per_hit
        return f"{self.user.name} применил могучий укол и нанес {self.attack}"
