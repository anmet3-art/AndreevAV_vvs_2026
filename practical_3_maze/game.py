import copy
import random

ROWS, COLS = 8, 8
SYMBOLS = {"start":"S", "exit":"E", "plain":".", "chest":"C",
           "enemy":"M", "trap":"T", "key":"K", "portal":"P"}
LOOT = [
    {"name":"Короткий меч", "kind":"weapon", "damage":5},
    {"name":"Крепкий щит", "kind":"armor", "block":4},
    {"name":"Лечебный эликсир", "kind":"potion", "heal":25},
    {"name":"Настой маны", "kind":"mana", "power":8},
    {"name":"Монеты", "kind":"treasure", "amount":20},
    {"name":"Свиток", "kind":"scroll"},
]

def create_world():
    world = [[{"kind":random.choice(["plain","plain","chest","enemy","trap","portal"]),
               "loot":[], "state":{}} for _ in range(COLS)] for _ in range(ROWS)]
    world[0][0]["kind"], world[-1][-1]["kind"] = "start", "exit"
    kx, ky = random.choice([(r,c) for r in range(ROWS) for c in range(COLS)
                            if (r,c) not in [(0,0),(ROWS-1,COLS-1)]])
    world[kx][ky] = {"kind":"key", "loot":[{"name":"Ключ от ворот","kind":"key"}], "state":{}}
    for row in world:
        for room in row:
            if room["kind"] == "chest":
                room["loot"] = copy.deepcopy(random.sample(LOOT, random.randint(1,3)))
    return world

def show_map(world, seen, position):
    for r in range(ROWS):
        line=[]
        for c in range(COLS):
            if (r,c)==position: line.append("@")
            elif seen[r][c]: line.append(SYMBOLS[world[r][c]["kind"]])
            else: line.append("?")
        print(" ".join(line))

def describe(item):
    extras = ", ".join(f"{k}={v}" for k,v in item.items() if k not in ("name","kind"))
    return f"{item['name']} [{item['kind']}]" + (f" ({extras})" if extras else "")

def inventory_menu(hero):
    while True:
        bag=hero["bag"]
        print("\nРЮКЗАК")
        for i,obj in enumerate(bag): print(i, describe(obj))
        print("1 убрать по имени | 2 убрать по номеру | 3 сортировать | 4 обратная сортировка")
        print("5 перевернуть | 6 найти | 7 копия/срез | 8 shallow/deep copy | 9 применить | 0 назад")
        cmd=input("> ").strip()
        if cmd=="0": return
        elif cmd=="1":
            name=input("Название: ")
            for obj in bag:
                if obj["name"]==name: bag.remove(obj); print("Убрано"); break
            else: print("Такого предмета нет")
        elif cmd=="2":
            try: print("Убрано:", describe(bag.pop(int(input("Номер: ")))))
            except (ValueError,IndexError): print("Некорректный номер")
        elif cmd in ("3","4"):
            bag.sort(key=lambda x:(x["kind"],x["name"]), reverse=cmd=="4")
        elif cmd=="5": bag.reverse()
        elif cmd=="6":
            name=input("Что найти: ")
            found=next(((i,x) for i,x in enumerate(bag) if x["name"]==name),None)
            print(found if found else "Не найдено")
        elif cmd=="7":
            replica=bag.copy()
            print("Поверхностная копия:", [x["name"] for x in replica])
            print("Первые три:", [x["name"] for x in replica[:3]])
        elif cmd=="8":
            shallow=bag.copy(); deep=copy.deepcopy(bag)
            if bag and "damage" in bag[0]:
                shallow[0]["damage"] += 1
                print("После изменения shallow исходное значение:", bag[0]["damage"])
                bag[0]["damage"] -= 1
            if bag: deep[0]["name"] += " (копия)"
            print("Глубокая копия не меняет оригинал:", [x["name"] for x in bag])
        elif cmd=="9":
            for i,x in enumerate(bag): print(i,describe(x))
            try:
                idx=int(input("Предмет: ")); obj=bag[idx]
                if obj["kind"]=="potion":
                    hero["hp"]=min(100,hero["hp"]+obj["heal"]); bag.pop(idx); print("Здоровье восстановлено")
                elif obj["kind"]=="mana":
                    weapons=[(j,w) for j,w in enumerate(bag) if w["kind"]=="weapon"]
                    if weapons:
                        j,w=weapons[0]; w["damage"]=w.get("damage",0)+obj["power"]; bag.pop(idx); print("Оружие усилено")
                    else: print("Сначала найдите оружие")
                else: print("Этот предмет нельзя применить")
            except (ValueError,IndexError): print("Неверный номер")

def enter_room(room, hero):
    kind=room["kind"]
    if kind=="chest":
        print("Сундук:", ", ".join(x["name"] for x in room["loot"]))
        if input("Забрать содержимое? д/н: ").lower().startswith("д"):
            hero["bag"].extend(room["loot"]); room["loot"]=[]
    elif kind=="key":
        print("На камне лежит ключ.")
        if input("Взять ключ? д/н: ").lower().startswith("д"):
            hero["bag"].extend(room["loot"]); room["loot"]=[]
    elif kind=="trap" and not room["state"].get("used"):
        damage=max(0,random.randint(8,20)-sum(x.get("block",0) for x in hero["bag"]))
        hero["hp"]-=damage; room["state"]["used"]=True
        print("Ловушка нанесла",damage,"урона")
    elif kind=="enemy" and not room["state"].get("cleared"):
        monster=random.randint(22,35); print("Появился страж, здоровье:",monster)
        while monster>0 and hero["hp"]>0:
            print("Ваше HP:",hero["hp"],"| Страж:",monster)
            action=input("1 атаковать, 2 применить эликсир, 3 попытаться убежать: ")
            if action=="1":
                damage=random.randint(5,11)+sum(x.get("damage",0) for x in hero["bag"])
                monster-=damage; print("Урон:",damage)
            elif action=="2":
                potion=next((x for x in hero["bag"] if x["kind"]=="potion"),None)
                if potion: hero["hp"]=min(100,hero["hp"]+potion["heal"]); hero["bag"].remove(potion)
                else: print("Эликсира нет")
            elif action=="3" and random.random()<0.5:
                print("Удалось скрыться"); return
            if monster>0: hero["hp"]-=max(0,random.randint(3,10)-sum(x.get("block",0) for x in hero["bag"]))
        if monster<=0:
            room["state"]["cleared"]=True
            hero["bag"].append({"name":"Награда стража","kind":"treasure","amount":30})
            print("Страж побеждён")
    elif kind=="portal":
        print("Портал мерцает. Он переносит вас в случайную открытую область.")
        # Teleport is handled by the main loop after the room event.
    elif kind=="exit": print("Ворота заперты. Нужен ключ.")

def main():
    world=create_world(); seen=[[False]*COLS for _ in range(ROWS)]
    hero={"r":0,"c":0,"hp":100,"bag":[]}; seen[0][0]=True
    while hero["hp"]>0:
        pos=(hero["r"],hero["c"])
        print("\n"); show_map(world,seen,pos)
        has_key=any(x["kind"]=="key" for x in hero["bag"])
        print(f"Здоровье: {hero['hp']} | Ключ: {'есть' if has_key else 'нет'}")
        print("w/a/s/d — движение; i — рюкзак; q — выход")
        command=input("Действие: ").lower().strip()
        if command=="q": break
        if command=="i": inventory_menu(hero); continue
        delta={"w":(-1,0),"s":(1,0),"a":(0,-1),"d":(0,1)}.get(command)
        if not delta: print("Неизвестная команда"); continue
        nr,nc=hero["r"]+delta[0],hero["c"]+delta[1]
        if not (0<=nr<ROWS and 0<=nc<COLS): print("За границу карты пройти нельзя"); continue
        hero["r"],hero["c"]=nr,nc
        if (nr,nc)==(ROWS-1,COLS-1) and has_key:
            print("Победа! Ключ открыл ворота."); return
        if not seen[nr][nc]:
            seen[nr][nc]=True; enter_room(world[nr][nc],hero)
            if world[nr][nc]["kind"]=="portal":
                hero["r"],hero["c"]=random.randrange(ROWS),random.randrange(COLS)
                seen[hero["r"]][hero["c"]]=True
    print("Игра окончена. Осталось здоровья:",hero["hp"])
if __name__=="__main__": main()
