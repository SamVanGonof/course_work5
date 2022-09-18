from flask import Flask, render_template, request, redirect

from arena import Arena
from base_classes import dict_class
from equipment import Equipment
from unit import BaseUnit, Player, Enemy

app = Flask(__name__)

arena: Arena

equipment = Equipment('data/equipment.json')

result = {'header': "",
          'classes': dict_class.keys(),
          'weapons': equipment.get_weapon_name(),
          'armors': equipment.get_armor_name()}

heroes: dict[str, BaseUnit] = {}


@app.route('/')
def menu_page():
    """
    Кнопка начала игры
    """
    global arena
    arena = Arena()

    return render_template('index.html')


@app.route('/choose-hero/', methods=['GET', 'POST'])
def choose_hero():
    """
    Выбор героя
    """
    if request.method == 'GET':
        result['header'] = "Выберете героя"
        return render_template('hero_choosing.html', result=result)
    elif request.method == 'POST':
        data_unit = request.form
        new_player = Player(data_unit.get('name'), dict_class.get(data_unit.get('unit_class')))
        new_player.get_weapon(equipment.get_weapon(data_unit.get('weapon')))
        new_player.get_armor(equipment.get_armor(data_unit.get('armor')))
        heroes['player'] = new_player
        return redirect('/choose-enemy/')


@app.route('/choose-enemy/', methods=['GET', 'POST'])
def choose_enemy():
    """
    Выбор врага
    """
    if request.method == 'GET':
        result['header'] = "Выберете врага"
        return render_template('hero_choosing.html', result=result)
    elif request.method == 'POST':
        data_unit = request.form
        new_enemy = Enemy(data_unit.get('name'), dict_class.get(data_unit.get('unit_class')))
        new_enemy.get_weapon(equipment.get_weapon(data_unit.get('weapon')))
        new_enemy.get_armor(equipment.get_armor(data_unit.get('armor')))
        heroes['enemy'] = new_enemy
        return redirect('/fight/')


@app.route('/fight/')
def fight():
    """
    Начало игры
    """
    arena.start_game(**heroes)
    return render_template('fight.html', heroes=heroes)


@app.route('/fight/hit/')
def hit():
    """
    Кнопка удара
    """
    return render_template('fight.html', heroes=heroes, result=arena.hit_player())


@app.route('/fight/use-skill/')
def skill_attack():
    """
    Кнопка применения умения игроком
    """
    return render_template('fight.html', heroes=heroes, result=arena.use_skill_player())


@app.route('/fight/pass-turn/')
def skip_turn():
    """
    Пропуск хода
    """
    return render_template('fight.html', heroes=heroes, result=arena.next_turn())


@app.route('/fight/end-fight/')
def end_fight():
    """
    Конец игры, и переход на кнопку начала игры
    """
    arena.end_final_game()
    return redirect('/')
