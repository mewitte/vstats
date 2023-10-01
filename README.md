# VStats Scout Match

Scout Match is a module to parse input files containing DataVolley style codes and parses them into an array structure.

## Limitations

At this point, only basic codes are supported. A basic code follows the following format:

([\*|a])(\[0-9\](2))([S|R|A|B|D|E|F])([H|M|Q|T|U|F|O]?)([#|+|!|/|-|=])

Each Capture group has the following meaning:

1. \* for home team, a for away team
2. player number in double digit form, i.e. 08
3. Action
  * S: Serve
  * R: Reception
  * A: Attack
  * B: Block
  * D: Dig
  * E: Set
  * F: Free Ball
4. Optional specification of the ball, currently not used for the report
5. Quality of the action, each having a different meaning for each action.

| Codes | # | + | ! | / | - | = |
|---|---|---|---|---|---|---|
| S | Service winner | Good serve - Opponent highball set | Acceptable serve - Opponent has less set options | Very Ggood serve - opponent cannot attack | Bad serve - Good or perfect opponent receive | Mistake - Opponent point |
| R | Perfect Receive | Good receive - Close to perfect | Acceptable Receive - Setter position moved | Very bad receive - No attack possible | Bad receive - Highball set | Mistake - Opponent point |
| A | Point | Good attack - Next attack on attacker's side | Recycle | Attack into Block - Opponent point | Bad attack - next attack on opponent's side | Mistake - Opponent point |
| B | Kill Block | Good Block - Next attack on blocker's side | Opponent recycle | Opponent tool | Bad block - next attack on opponent's side | Mistake - Opponent point |
| D | Perfect dig | Good dig - Close to perfect | Acceptable dig - setter position moved | Very bad dig - No attack possible | Bad dig - Highball set | Mistake - Opponent point |
| E | Perfect set | Good set - minimal inaccuracy | Acceptable set - bigger inaccuracy | Very bad set - No attack possible | Bad set - very big inaccuracy | Mistake - Opponent point |
| F | Perfect freeball | Good freeball - Close to perfect | Acceptable freeball - setter has to move | Very bad freeball - No attack possible | Bad freeball - Highball set | Mistake - Opponent point |

At this point, rallies are not checked for a valid flow of events or for completeness.

## Input

For input, this module takes a filepath to a folder, containing text files, named x.txt, where x is a number from 1 to 5, corresponding to the set played. The text files contain basic codes. Each line represents a single rally.

## Output

This package will create match reports in textform in the folder the match is in.
