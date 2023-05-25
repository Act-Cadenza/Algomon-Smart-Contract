# Algomon-Smart-Contract


### Overview

This is a Blockchain-Based Game or Dapp game developed using Algorand's Pyteal, a smart contract language. The game utilizes Pyteal's global and local states to store necessary values for gameplay. Players can explore a virtual map and engage in the challenge of capturing monsters.


### Application ID

The smart contract's application ID deployed on Algorand's testnet is as follows: ---------

How the smart contract works 

## Defining the states

To facilitate the game mechanics, local states are utilized to store the stats of both players and monsters. Once a player opts-in , those values will be added into their local states to ensure that the values are different from each user. The local states were also used to determine if they are currently in a battle, capturing a monster, defeated by a monster or a monster is defeated.

### Local States
- localPlayerHp (int): Stores the player's hit points (HP).
- localDmg (int): Stores the player's attack damage.
- localMonsHp (int): Stores the monster's hit points (HP).
- localMonsDmg (int): Stores the monster's attack damage.
- localScore (int): Keeps a tally of the player's score.
- localTotal (int): Copies the values of globalScore  which is the total score of all players.
- isInBattle (int): Indicates whether the player is engaged in a battle (1 for true, 0 for false).
- isCaught (int): Signals if a monster has been captured (1 for true, 0 for false).
- isBattleOver (int): Indicates if the battle has concluded (1 for true, 0 for false).
- isGameOver (int): Denotes whether the game has concluded (1 for true, 0 for false).
- isButtonDisabled (int): Controls the state of various buttons in the game (1 for disabled, 0 for enabled).


In addition to local states, global state variables are employed to store the cumulative number of monsters captured by all players. This global score represents the combined achievements of the entire player community.

### Global State
- globalScore (int): Represents the total number of monsters captured across all players.

## Lifecycle

### App Creation

The game's lifecycle commences with the creation of the application. At this stage, the smart contract is set up, initializing the necessary parameters and structures for gameplay.

### Account Opt-In

Once an account opts-in to the smart contract, the player's and monster's stats, such as HP and attack damage, are set. Additionally, states related to ongoing battles (isInBattle), captures (isCaught), game-over conditions (isGameOver), button disablement (isButtonDisabled), and battle conclusion (isBattleOver) are set to their initial values (false or 0).

### Proceed

This calls the handleclick subroutine, which sets states such as isButtonDisabled and isInBattle to true,  the player exits the map, and proceeds to the isInBattle screen. Additionally, the value of localTotal is updated by retrieving the current value of globalScore.

### Attack_mons

This will triggers the attack subroutine. Before proceeding, it verifies if both the player and the monster have HP greater than 0. Upon successful validation, the stats of the player and monster are stored in their respective scratch variables.

Next, a series of conditions calculate and store the damage inflicted by the player and monster upon each other.

Firstly, a condition checks if the monster's current HP is greater than the player's attack damage. If true, the monster's HP is reduced by the player's attack damage. If false, the monster's HP is set to 0, isInBattleOver is set to true, the player exits the battle, and proceeds to the isInBattleOver screen.

Similarly, another condition examines whether the player's current HP is greater than the monster's attack damage. If true, the player's HP is reduced by the monster's attack damage. If false, the player's HP is set to 0, isGameOver is set to true, the player exits the battle, and proceeds to the isGameOver screen.

### Run

This will triggers the backmap subroutine, where the monster's HP is restored to full, and the player respawns on the map for another attempt. Additionally, states such as isInBattle, isCaught, isGameOver, isButtonDisabled, and isInBattleOver are reset to their initial values (false or 0). Moreover, the value of localTotal is updated by retrieving the current value of globalScore.

### Captured

This will invokes the capture subroutine, which first verifies if both the player and the monster have HP greater than 0. Once the validation succeeds, the localScore and globalScore variables are stored in their respective scratch variables. Subsequently, the localScore and globalScore are incremented by 1. Additionally, the isInBattle state is set to false or 0, and the monster's HP is replenished to full.

### Revive

This will call the  revive subroutine , replenishing both the player's and the monster's HP to full. The player respawns on the map for another attempt, while states such as isInBattle, isCaught, isGameOver, isButtonDisabled, and isBattleOver are reset to their initial values (false or 0). Furthermore, the value of localTotal is updated by retrieving the current value of globalScore.

## Demo

Here's a [video recording](https://drive.google.com/file/d/1_yhyL0xmOX6I1B8BQtzkijeFIiADcQfH/view?usp=sharing) demonstrating the user's interactions with the dApp.

[![IMAGE ALT TEXT HERE](https://github.com/Act-Cadenza/Algomon/assets/71002490/942a69b5-d5e0-4287-aabf-965353089ff7)](https://drive.google.com/file/d/1_yhyL0xmOX6I1B8BQtzkijeFIiADcQfH/view?usp=sharing)

Here is the [demo link](https://algomon.vercel.app/) hosted in vercel to try it out.


