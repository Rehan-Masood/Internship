import random

def create_player():
    """Creates the player's nested dictionary."""
    player = {
        "name": "Hero",
        "health": 100,
        "max_health": 100,
        "attack": 20,
        "defense": 10,
        "potions": 3,
        "gold": 0
    }
    return player

def create_enemy(name, health, attack, defense, gold_reward):
    """Creates a single enemy's dictionary."""
    enemy = {
        "name": name,
        "health": health,
        "max_health": health,
        "attack": attack,
        "defense": defense,
        "gold_reward": gold_reward
    }
    return enemy

def get_wave(wave_number):
    """Returns the list of enemies (nested dictionaries) for a given wave."""
    if wave_number == 1:
        return [
            create_enemy("Goblin 1", 30, 10, 3, 15),
            create_enemy("Goblin 2", 30, 10, 3, 15)
        ]
    elif wave_number == 2:
        return [
            create_enemy("Orc 1", 50, 15, 6, 25),
            create_enemy("Orc 2", 50, 15, 6, 25)
        ]
    else:
        return [
            create_enemy("Dragon (Final Boss)", 150, 25, 10, 100)
        ]

def attack_enemy(attacker, defender):
    """
    Damage Formula: (Attack - Defense) + Random(0,10)
    Random > 8  -> Critical Hit (2x damage)
    Random < 2  -> Miss (0 damage)
    Returns: (damage, result_type)
    """
    rand_num = random.randint(0, 10)

    if rand_num < 2:
        return 0, "miss"

    damage = (attacker["attack"] - defender["defense"]) + rand_num
    if damage < 0:
        damage = 0

    if rand_num > 8:
        damage = damage * 2
        return damage, "critical"

    return damage, "normal"

def use_potion(player):
    """Uses a potion to restore 30 health points."""
    if player["potions"] <= 0:
        print("You have no potions left!")
        return False

    player["potions"] -= 1
    player["health"] += 30
    if player["health"] > player["max_health"]:
        player["health"] = player["max_health"]

    print("You used a potion! Health increased by 30 points.")
    return True

def shop(player):
    """Opens the shop after each wave."""
    print("\n===== SHOP =====")
    print(f"Your Gold Coins: {player['gold']}")

    shopping = True
    while shopping:
        print("\n1. Buy Attack Power (+5 Attack) - 20 Gold")
        print("2. Buy Potion (+1 Potion) - 15 Gold")
        print("3. Exit Shop")

        choice = input("Enter your choice: ")

        if choice == "1":
            if player["gold"] >= 20:
                player["gold"] -= 20
                player["attack"] += 5
                print("Your Attack Power increased!")
            else:
                print("You don't have enough gold.")
        elif choice == "2":
            if player["gold"] >= 15:
                player["gold"] -= 15
                player["potions"] += 1
                print("You bought a potion!")
            else:
                print("You don't have enough gold.")
        elif choice == "3":
            shopping = False
            print("You left the shop.")
        else:
            print("Invalid Input, try again.")

def show_status(player, enemy):
    print("\n---------------------------------------------")
    print(f"{player['name']}  |  Health: {player['health']}/{player['max_health']}  |  Potions: {player['potions']}  |  Gold: {player['gold']}")
    print(f"{enemy['name']}  |  Health: {enemy['health']}/{enemy['max_health']}")
    print("---------------------------------------------")

def battle(player, enemy, game_log):
    """
    Runs the battle against a single enemy.
    Return values: "won", "dead", "ran"
    """
    print(f"\n{enemy['name']} appears! The battle begins.")

    while player["health"] > 0 and enemy["health"] > 0:
        show_status(player, enemy)
        print("1. Attack")
        print("2. Heal")
        print("3. Run")

        choice = input("Choose your move (1/2/3): ")

        if choice == "1":
            damage, result = attack_enemy(player, enemy)
            if result == "miss":
                print("Your attack missed!")
            elif result == "critical":
                print(f"Critical Hit! You dealt {damage} damage to {enemy['name']}.")
            else:
                print(f"You dealt {damage} damage to {enemy['name']}.")

            enemy["health"] -= damage
            if enemy["health"] < 0:
                enemy["health"] = 0

        elif choice == "2":
            use_potion(player)
            game_log["potions_used"] += 1

        elif choice == "3":
            return "ran"

        else:
            print("Invalid Input, try again.")
            continue

        if enemy["health"] > 0:
            e_damage, e_result = attack_enemy(enemy, player)
            if e_result == "miss":
                print(f"{enemy['name']}'s attack missed!")
            elif e_result == "critical":
                print(f"{enemy['name']} landed a critical hit! You took {e_damage} damage.")
            else:
                print(f"{enemy['name']} dealt {e_damage} damage to you.")

            player["health"] -= e_damage
            if player["health"] < 0:
                player["health"] = 0

    if player["health"] <= 0:
        return "dead"
    else:
        return "won"

def print_final_report(player, game_log, outcome):
    print("\n\n=============== FINAL REPORT ===============")
    print("+---------------------------+------------------+")
    print("| Detail                    | Value            |")
    print("+---------------------------+------------------+")
    print(f"| Enemies Defeated          | {game_log['enemies_defeated']:<16} |")
    print(f"| Potions Used              | {game_log['potions_used']:<16} |")
    print(f"| Total Gold Earned         | {game_log['total_gold_earned']:<16} |")
    print(f"| Remaining Health          | {player['health']:<16} |")
    print(f"| Final Outcome             | {outcome:<16} |")
    print("+---------------------------+------------------+")

    if game_log["log"]:
        print("\nBattle Log:")
        for entry in game_log["log"]: 
            print(f"   - {entry}")

    print("\n====================================================")
    print("Game Over. Thanks for playing!")
    print("====================================================\n")


# ------------------------------------------------------------
# MAIN GAME
# ------------------------------------------------------------

def main():
    print("========================================================")
    print("   WELCOME TO COMBAT WARRIOR : The Ultimate Battle Game!")
    print("=========================================================")
    print("Instructions:")
    print("You are a brave Warrior who must fight 5 dangerous enemies:")
    print("Wave 1: 2 Goblins  |  Wave 2: 2 Orcs  |  Wave 3: Dragon (Final Boss)")
    print("\nOn each turn you will have 3 options:")
    print("1. Attack - Attack the enemy")
    print("2. Heal   - Use a potion to restore health")
    print("3. Run    - Flee from the battle")
    print("\nDefeating an enemy will earn you Gold Coins.")
    print("After each Wave, a Shop will open where you can buy Attack Power or Potions.")
    print("============================================================================\n")

    player = create_player()
    game_log = {
        "enemies_defeated": 0,
        "potions_used": 0,
        "total_gold_earned": 0,
        "log": []
    }

    game_over = False
    outcome = "Victory! All enemies defeated"

    for wave_number in [1, 2, 3]:
        if game_over:
            break

        enemies = get_wave(wave_number)
        print(f"\n\n########## Wave {wave_number} Begins ##########")

        for enemy in enemies:
            result = battle(player, enemy, game_log)

            if result == "dead":
                print(f"\nYou were defeated by {enemy['name']}.")
                outcome = "Defeat - Warrior was defeated"
                game_over = True
                break

            elif result == "ran":
                print("\nYou fled from the battle. The game ends here.")
                outcome = "Ran Away - Warrior fled"
                game_over = True
                break

            elif result == "won":
                print(f"\nYou defeated {enemy['name']}!")
                player["gold"] += enemy["gold_reward"]
                game_log["total_gold_earned"] += enemy["gold_reward"]
                game_log["enemies_defeated"] += 1
                game_log["log"].append(f"Defeated {enemy['name']} (+{enemy['gold_reward']} Gold)")

        if not game_over and wave_number != 3:
            shop(player)

    print_final_report(player, game_log, outcome)


if __name__ == "__main__":
    main()
