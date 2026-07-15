# Combat Warrior

A terminal-based Python battle game where you fight through enemy waves, earn gold, and upgrade your warrior between rounds.

## Demo Video
<video src="https://github.com/user-attachments/assets/f23118d0-dfc2-4cd3-8db4-53f638fb2eed" controls width="600"></video>


## Game Overview

You play as a warrior with:
- Health and max health
- Attack and defense stats
- Potions for healing
- Gold for shop upgrades

### Enemy Waves
- Wave 1: Goblin 1, Goblin 2
- Wave 2: Orc 1, Orc 2
- Wave 3: Dragon (Final Boss)

Defeat all enemies to win.

## Combat System

Each turn, choose one action:
- `1` Attack
- `2` Heal (use potion)
- `3` Run (ends the game)

### Damage Rules
Damage is calculated using:

`(Attack - Defense) + Random(0, 10)`

Special outcomes:
- Random `< 2`: Miss (0 damage)
- Random `> 8`: Critical hit (double damage)

## Shop System

After Wave 1 and Wave 2, a shop opens.

Shop options:
- Buy Attack Power `+5 Attack` for `20 Gold`
- Buy Potion `+1 Potion` for `15 Gold`
- Exit Shop

## Final Report

At game end, a final report is shown with:
- Enemies defeated
- Potions used
- Total gold earned
- Remaining health
- Final outcome
- Battle log summary

## Requirements

- Python 3.x
- Standard library only (`random`)

## How to Run

From the project folder:

```bash
python Warrior.py
```

If `python` is not mapped, use:

```bash
python3 Warrior.py
```

## Project Structure

- `Warrior.py` - Main game script
- `README.md` - Project documentation
