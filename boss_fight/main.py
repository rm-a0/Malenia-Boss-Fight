from tkinter import *
import os

from constants import WIDTH, HEIGHT, DELAY
from entities.player import Player
from entities.weapon import Weapon
from entities.boss import Boss
from entities.estus_flask import EstustFlask
from ui.game_ui import GameUI

#get the directory for assets and join them
scriptDirectory = os.path.dirname(os.path.abspath(__file__))
assetsDirectory = os.path.join(scriptDirectory, 'assets')

def fullscreen(event, root):
    current_state = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not current_state)

def disableMouse(event):
    return "break"

def healEvent(event, player, estusFlask, gameUI):
    estusFlask.heal(player, event)
    gameUI.updateEstusFlaskCounter(event)

def bindKeys(canvas, player):
    #UI RELEATED KEYBINDS
    canvas.bind("<F11>", fullscreen)

    #PLAYER RELEATED KEYBINDS
    #fix clunky movement in the future - refine left and right movement (probably not happening cuz tkinter is shit)
    #make jumping more realistic - add exponential and log fucntions
    canvas.bind("<KeyPress-a>", player.moveLeft)
    canvas.bind("<KeyRelease-a>", player.stopMoveLeft)
    canvas.bind("<KeyPress-d>", player.moveRight)
    canvas.bind("<KeyRelease-d>", player.stopMoveRight)
    canvas.bind("<space>", player.jump)
    canvas.bind("<KeyPress-Shift_L>", player.roll)
    canvas.bind("<Button-1>", player.attack)

    #ITEM RELEATED KEYBINDS
    canvas.bind("<e>", lambda event: healEvent(event))

def checkGameEnd(canvas, player, boss):
    if player.healthPoints <= 0:
        canvas.create_text(WIDTH/2, HEIGHT/2, text="YOU DIED", font=("Helvetica", 18), fill="red")
        return True
    elif boss.healthPoints <= 0:
        canvas.create_text(WIDTH/2, HEIGHT/2, text="YOU WON", font=("Helvetica", 18), fill="red")
        return True
    else:
        return False

def updateGame(canvas, player, boss, gameUI):
    try: 
        #converts delay to seconds
        dt = DELAY / 1000.0

        if checkGameEnd(canvas, player, boss) == False:
            #update entities
            player.updatePosition(dt)
            player.applyGravity(dt)
            player.refillStamina()
            #player.applyStatusEffect()

            #update UI
            gameUI.updatePlayerHealthBar()
            gameUI.updateBossHealthBar()
            gameUI.updateStaminaBar()
            gameUI.updateManaBar()

            #recursive call
            canvas.after(DELAY, updateGame, canvas, player, boss, gameUI)
    except: 
        print("Error updating game")

def main():
    #create root
    root = Tk()
    root.title('Title')

    #create canvas
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
    canvas.pack()
    canvas.focus_set()

    #disable cursor and mouse movement
    root.config(cursor="none")

    #import images
    rune_background = PhotoImage(file=os.path.join(assetsDirectory, 'rune_background.PNG'))
    rune_frame = PhotoImage(file=os.path.join(assetsDirectory, 'rune_frame.PNG'))
    godricks_rune = PhotoImage(file=os.path.join(assetsDirectory, 'godricks_rune.PNG'))

    #create objects
    player = Player(canvas, name='Player1', healthPoints=800, mana=100, stamina=700)
    weapon = Weapon(canvas, name='Sword', damage=45, weight=50, reach=150)
    boss = Boss(canvas, name='Boss', healthPoints=900)
    estusFlask = EstustFlask(quantity=12, healing=280)
    gameUI = GameUI(canvas, player, boss, estusFlask, rune_background, rune_frame, godricks_rune)

    #equip weapon
    player.equipWeapon(weapon)

    #pass boss and player instance to each other (used for interaciton)
    player.createBossInstance(boss)
    boss.createPlayerInstance(player)

    #bind keys
    bindKeys(canvas, player)

    #game loop
    canvas.after(DELAY, updateGame, canvas, player, boss, gameUI)

    #delete later
    print(f"delay: {DELAY} ms")
    print(f"delta time: {DELAY/1000} ms")

    root.mainloop()

if __name__ == "__main__":
    main()