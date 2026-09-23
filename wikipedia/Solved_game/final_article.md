# Solved game

A solved game is a game whose outcome (win, lose or draw) can be correctly predicted from any position, assuming that both players play perfectly. This concept is usually applied to abstract strategy games, and especially to games with full information and no element of chance; solving such a game may use combinatorial game theory and/or computer assistance.

A two-player game can be solved on several levels:
Ultra-weak solution Prove whether the first player will win, lose or draw from the initial position, given perfect play on both sides.
This can be a non-constructive proof (possibly involving a strategy-stealing argument) that need not actually determine any moves of the perfect play.
Weak solution Provide an algorithm that secures a win for one player, or a draw for either, against any possible moves by the opponent, from the beginning of the game.
Strong solution Provide an algorithm that can produce perfect moves from any position, even if mistakes have already been made on one or both sides.
Despite their name, many game theorists believe that "ultra-weak" proofs are the deepest, most interesting and valuable.
"Ultra-weak" proofs require a scholar to reason about the abstract properties of the game, and show how these properties lead to certain outcomes if perfect play is realized.
By contrast, "strong" proofs often proceed by brute force—using a computer to exhaustively search a game tree to figure out what would happen if perfect play were realized.
The resulting proof gives an optimal strategy for every possible position on the board.
However, these proofs are not as helpful in understanding deeper reasons why some games are solvable as a draw, and other, seemingly very similar games are solvable as a win.
Given the rules of any two-person game with a finite number of positions, one can always trivially construct a minimax algorithm that would exhaustively traverse the game tree.
However, since for many non-trivial games such an algorithm would require an infeasible amount of time to generate a move in a given position, a game is not considered to be solved weakly or strongly unless the algorithm can be run by existing hardware in a reasonable time.
Many algorithms rely on a huge pre-generated database and are effectively nothing more.
A game is considered fully solved if an algorithm for drawing the game into a draw has been found, or if a win for one side has been proven under optimal strategy.
Even if a game is not solved, an algorithm may produce a good approximate solution.
Most research done in solving game problems is not fully peer-reviewed.
As a simple example of a strong solution, the game of tic-tac-toe is easily solvable as a draw for both players with perfect play (a result manually determinable).
Games like nim also admit a rigorous analysis using combinatorial game theory.
Whether a game is solved is not necessarily the same as whether it remains interesting for humans to play.
Even a strongly solved game can still be interesting if its solution is too complex to be memorized; conversely, a weakly solved game may lose its attraction if the winning strategy is simple enough to remember (e.g., Maharajah and the Sepoys).
An ultra-weak solution (e.g., Chomp or Hex on a sufficiently large board) generally does not affect playability.

In game theory, perfect play is the behavior or strategy of a player that leads to the best possible outcome for that player regardless of the response by the opponent.
Perfect play for a game is known when the game is solved.
Based on the rules of a game, every possible final position can be evaluated (as a win, loss or draw).
By backward reasoning, one can recursively evaluate a non-final position as identical to the position that is one move away and best valued for the player whose move it is.
Thus a transition between positions can never result in a better evaluation for the moving player, and a perfect move in a position would be a transition between positions that are equally evaluated.
As an example, a perfect player in a drawn position would always get a draw or win, never a loss.
If there are multiple options with the same outcome, perfect play is sometimes considered the fastest method leading to a good result, or the slowest method leading to a bad result.
The resolution provides proof that every move is optimal for the player.
This resolution produces at least one complete ideal game.
A computer program using the solution does not necessarily play optimally against an imperfect opponent.
Perfect play can be generalized to non-perfect information games, as the strategy that would guarantee the highest minimal expected outcome regardless of the strategy of the opponent.
As an example, the perfect strategy for rock paper scissors would be to randomly choose each of the options with equal (1/3) probability.
The disadvantage in this example is that this strategy will never exploit non-optimal strategies of the opponent, so the expected outcome of this strategy versus any strategy will always be equal to the minimal expected outcome.
Although the optimal strategy of a game may not (yet) be known, a game-playing computer might still benefit from solutions of the game from certain endgame positions (in the form of endgame tablebases), which will allow it to play perfectly after some point in the game.
This approach is only applicable to games where the number of possible moves can be stored in a database.
Specific information can be retrieved from the database within a reasonable time frame for these games.
Users input dozens of endgames into the software.
This approach differs from a perfect game which presents a solution starting from the first move.
Computer chess programs are well known for doing this.
The problem is formulated as a decision problem.
An algorithm is known for this state.
An optimal strategy was implemented.
According to Zermelo's theorem, one player has a winning strategy.
In this game, there are no draws.
A perfect play by the second player leads to a win for the second player.
This constitutes a winning strategy for the first player.
Based on the moves made, one player can win.
The first player has an unbeatable advantage.
This implies that the first player wins.
John Nash created a copycat strategy.
The copycat strategy was used in square board games.
A solved game can be predicted by mathematicians.
Mathematicians can determine if there is a winning strategy for the first player or the second player.
Mathematicians can determine if there is a non-losing strategy for the first player or the second player.
Mathematicians can determine the strategy.
Mathematicians can determine the best strategy for both sides.

Awari (a game of the Mancala family)
The variant of Oware allowing game ending "grand slams" was strongly solved by Henri Bal and John Romein at the Vrije Universiteit in Amsterdam, Netherlands (2002).
Either player can force the game into a draw.
Chopsticks Strongly solved.
If two players both play perfectly, the game will go on indefinitely.
Connect Four Solved first by James D. Allen on October 1, 1988, and independently by Victor Allis on October 16, 1988.
The first player can force a win.
Strongly solved by John Tromp's 8-ply database (Feb 4, 1995).
Weakly solved for all boardsizes where width+height is at most 15 (as well as 8×8 in late 2015) (Feb 18, 2006).
Free gomoku Solved by Victor Allis (1993).
The first player can force a win without opening rules.
Ghost Solved by Alan Frank using the Official Scrabble Players Dictionary in 1987.
Hexapawn 3×3 variant solved as a win for black, several other larger variants also solved.
Kalah Most variants solved by Geoffrey Irving, Jeroen Donkers and Jos Uiterwijk (2000) except Kalah (6/6).
The (6/6) variant was solved by Anders Carstensen (2011).
Strong first-player advantage was proven in most cases.
L game Easily solvable.
Either player can force the game into a draw.
Maharajah and the Sepoys This asymmetrical game is a win for the sepoys player with correct play.
Nim Strongly solved.
Nine men's morris Solved by Ralph Gasser (1993).
Either player can force the game into a draw.
Order and Chaos Order (First player) wins.
Ohvalhu Weakly solved by humans, but proven by computers.
(Dakon is, however, not identical to Ohvalhu, the game which actually had been observed by de Voogt) Pangki Strongly solved by Jason Doucette (2001).
The game is a draw.
There are only two unique first moves if you discard mirrored positions.
One forces the draw, and the other gives the opponent a forced win in 15 moves.
Pentago Strongly solved by Geoffrey Irving with use of a supercomputer at NERSC.
The first player wins.
Quarto Solved by Luc Goossens (1998).
Two perfect players will always draw.
Renju-like game without opening rules involved Claimed to be solved by János Wagner and István Virág (2001).
A first-player win.
Teeko Solved by Guy Steele (1998).
Depending on the variant either a first-player win or a draw.
Three men's morris Trivially solvable.
Either player can force the game into a draw.
Three musketeers Strongly solved by Johannes Laire in 2009, and weakly solved by Ali Elabridi in 2017.
It is a win for the blue pieces (Cardinal Richelieu's men, or, the enemy).
Tic-tac-toe Trivially strongly solvable because of the small game tree.
The game is a draw if no mistakes are made, with no mistake possible on the opening move.
Wythoff's game Strongly solved by W. A. Wythoff in 1907.

== Hex and Tic-Tac-Toe ==

The game Hex was solved by John Nash in 1947.
If the second player had a winning strategy, the first player could adopt it.
The game Hex includes a swap rule, and a winning strategy for Hex with exchange is known.
Tic-tac-toe on a 3x3 grid is a widely known game.
Even schoolchildren can manually determine the result of a perfect game of tic-tac-toe, and the outcome of tic-tac-toe with perfect play is determinable even by children manually.
Tic-tac-toe is in a state of 'drawn death'.
Therefore, one can doubt that the solution by Bal and Romein is valid.
Spanish Oware master Viktor Bautista Roca made a statement in front of his former website manqala.org.
The Awari Oracle is completely based on the research by Bal and Romein.
The Awari Oracle had several flaws in the endgame.
Both the manqala.org and Oracle websites were removed from the internet.
No further research on the topic appears to be possible.

== Kalah and Oware Variants ==

Mark Rawlings quantified the magnitude of the first player's victory in the (6/6) variant of Kalah in 2015.
The searches totaled 106 days of CPU time and involved more than 55 trillion nodes.
39 GB of endgame databases were created.
It was demonstrated that with perfect play, the first player wins by a margin of 2.
All mentioned results refer to the open-capture variant, which has very limited interest for standard play.
The analysis of the standard rules game for Kalah (6,4) has been published, and Kalah (6,4) is a win by 8 for the first player.
The analysis of the standard rules game for Kalah (6,5) has been published, and Kalah (6,5) is a win by 10 for the first player.
It has been demonstrated that the first player wins by at least 4 in Kalah (6,6) with standard rules.
Viktor Bautista i Roca is a Spanish master of Oware who announced on his former homepage manqala.org that the 'Awari Oracle' was entirely based on the research of Bal and Romein.
The 'Awari Oracle' had several flaws in the final phase, and one can doubt that the solution by Bal and Romein is valid.
The website manqala.org was removed from the internet, and the Awari Oracle website was removed from the internet.

All mentioned results refer to the 'Empty-pit Capture' variant, which has very limited interest for standard play.
Mark Rawlings quantified the magnitude of the first-player win in the (6/6) variant, and this analysis was conducted in 2015.
The analysis required 106 days of total CPU time, created 39 GB of endgame databases, and searched more than 55 trillion nodes.
It was proven that with perfect play, the first player wins by a margin of 2 points.
An analysis of the game with standard rules has been established for Kalah (6,4), where the first player wins by 8.
An analysis of the game with standard rules has been established for Kalah (6,5), where the first player wins by 10.
It has been proven that the first player wins by at least 4 in Kalah (6,6) with standard rules.

In Kalah(6,5), the first player wins by 10.
It has been proven that the first player wins by at least 4 points in Kalah(6,6).

== Mühle and Mill ==

Mühle was strongly solved, and the game always ends in a draw.
Peter Stahlhacke (Mr.
Data) and Alexander Szabari independently solved Mühle, and their solution was published in 2013.
The game of Mill was solved.
Poddavki, also known as Russian draughts, was solved by Osipov and Morozev in 2011.

== Othello and Reversi ==

Othello (Reversi) on 4x4 boards has been strongly solved, and Othello (Reversi) on 6x6 boards has been strongly solved.
The second player has a winning strategy in Othello (Reversi), and this winning strategy applies to the second player on 4x4 and 6x6 boards.
Reversi was weakly solved on a 4x4 board and on a 6x6 board.
The weak solutions for the 4x4 and 6x6 boards were found in July 1993.
Joel Feinstein solved the 4x4 and 6x6 Reversi games.

== Connect Four and Swap Rules ==

Connect Four without the swap rule requires a winning strategy for the first player, and no game can end in a draw under the no-swap rule.
The second player cannot have a winning strategy under the no-swap rule.

== Pentago and Palillos ==

The solution for Pentago was published in 2014.
The second player can always force a win in Palillos.
The second player can always force a win.

== Guess Who and Trilha ==

Mihai Nica strongly solved the game Guess Who? in 2016.
Ralph Gasser solved the game Trilha, and the solution was published in 1993.
The first player wins.

== Solitaire and Single-Player Games ==

The game Solitaire has been strongly solved if the first player starts in the middle column, in which case the player loses against a perfect opponent.

== General Game Theory and m,n,k Games ==

The solution applies to all variants where the last player to move wins, and the Sprague-Grundy theorem relates to these variants.
Winning strategies can be determined manually for games with up to 6 points, strategies have been investigated with computer assistance for games with up to 32 points, and strategies have been partially investigated for games with up to 47 points.
The game m, n, k is trivial to analyze.
The game was solved on 4x4 and 6x6 boards in July 1993, and the solution resulted in a second-player win.

== Dakon, Congklak, and Renju ==

Dakon is not identical to Congklak.
Congklak was effectively observed by de Voogt.
This is a game of type Renju.
In this variant, the first player either wins or draws.

== Six Men's Chess and Other Variants ==

Six Men's Chess is a solved game that is trivially solvable, was designed by Johannes Laire, and was released in 2009.
The game has three different definitions.
Screen-style Gomoku is a first-player win game.
These board games have been fully solved to date.

== Othello Large Boards ==

Jing Yang has demonstrated a winning strategy for 7x7, 8x8, and 9x9 boards.

== João de Prensar's Solution ==

The game was strongly solved by João de Prensar, who used 8 layers of a database to solve it.
Ed Gilbert solved the game.

English draughts (checkers)
This 8×8 variant of draughts was weakly solved on April 29, 2007, by the team of Jonathan Schaeffer.
From the standard starting position, both players can guarantee a draw with perfect play.
Checkers has a search space of 5×10²⁰ possible game positions.
The number of calculations involved was 10¹⁴, which were done over a period of 18 years.
The process involved from 200 desktop computers at its peak down to around 50.

Fanorona Weakly solved by Maarten Schadd.
The game is a draw.

Losing chess Weakly solved in 2016 as a win for White beginning with 1. e3.

Othello (Reversi) Weakly solved in 2023 by Hiroki Takizawa, a researcher at Preferred Networks.
From the standard starting position on an 8x8 board, a perfect play by both players will result in a draw.
Othello is the largest game solved to date, with a search space of 10²⁸ possible game positions.

Pentominoes Weakly solved by H. K. Orman.
It is a win for the first player.

Qubic Weakly solved by Oren Patashnik (1980) and Victor Allis.
The first player wins.

Sim Weakly solved: win for the second player.

Lambs and tigers Weakly solved by Yew Jin Lim (2007).
The game is a draw.

== English Draughts (Checkers) Solution ==

Ralph Gasser solved Mühle, which was weakly solved and published in 1993.
Räuber chess has been weakly solved.
Bagh-Chal was weakly solved by Yew Jin Lim.
The Chinook checkers program, known for Jonathan Schaeffer and the World Man-Machine Checkers Champion, will never transform a drawn position into a losing position.
Chinook can transition from a winning position to a drawn position.
Chinook does not expect the opponent to make a move that will not win but might lose, nor does it fully analyze such moves.
Chinook does not expect the opponent to play a move that will not win but could lose, and it does not analyze such moves completely.
The Chinook checkers program will never resign a drawn position from a losing position, though the Chinook program might resign a winning drawn position.
An endgame database of 39 gigabytes was created in the software Chinook.
The research took a total of 106 days of processor time and processed more than 55 trillion nodes. m,n,k-game checkers under American rules are known to result in a draw.

English draughts has been solved by the program Chinook.
The team's program was known as Chinook.
Chinook is referred to as the 'World Man-Machine Checkers Champion'.
The game is weakly solved as a first-player win.
Checkers was one of the popular games for which this outcome was predicted.
Checkers is a game with a wide draw margin where a draw threatens.

== Bagh-Chal ==

Bagh-Chal is also known as Tigers and Goats.
Yew Jin Lim weakly solved Bagh-Chal in 2007.

== Reversi (Othello) on Small Boards ==

Reversi (Othello) is weakly solved on a 4x4 board and on a 6x6 board.
On a 4x4 or 6x6 board, the second player has a winning strategy.
The first player in Reversi is Black.

== Other Solved Games ==

Congklak is weakly solved by humans and has been proven by computers.
GamesCrafters solved two games.
It was proven that with perfect play, the first player wins by 2.

Chess

Fully solving chess remains elusive, and it is speculated that the complexity of the game may preclude it ever being solved.
Through retrograde computer analysis endgame tablebases (strong solutions) have been found for all three- to seven-piece endgames, counting the two kings as pieces.
Some variants of chess on a smaller board with reduced numbers of pieces have been solved.
Some other popular variants have also been solved; for example, a weak solution to Maharajah and the Sepoys is an easily memorable series of moves that guarantees victory to the "sepoys" player.
Go The 5×5 board was weakly solved for all opening moves in 2002.
The 7×7 board was weakly solved in 2015.
Humans usually play on a 19×19 board, which is over 145 orders of magnitude more complex than 7×7.
Hex A strategy-stealing argument (as used by John Nash) shows that all square board sizes cannot be lost by the first player.
Combined with a proof of the impossibility of a draw, this shows that the game is a first player win (so it is ultra-weak solved).
On particular board sizes, more is known: it is strongly solved by several computers for board sizes up to 6×6.
Weak solutions are known for board sizes 7×7 (using a swapping strategy), 8×8, and 9×9; in the 8×8 case, a weak solution is known for all opening moves.
Strongly solving Hex on an N×N board is unlikely as the problem has been shown to be PSPACE-complete.
If Hex is played on an N×(N + 1) board then the player who has the shorter distance to connect can always win by a simple pairing strategy, even with the disadvantage of playing second.

International draughts All endgame positions with two through seven pieces were solved, as well as positions with 4×4 and 5×3 pieces where each side had one king or fewer, positions with five men versus four men, positions with five men versus three men and one king, and positions with four men and one king versus four men.
The endgame positions were solved in 2007 by Ed Gilbert of the United States.
Computer analysis showed that it was highly likely to end in a draw if both players played perfectly.
m,n,k-game It is trivial to show that the second player can never win; see strategy-stealing argument.
Almost all cases have been solved weakly for k ≤ 4.
Some results are known for k = 5.
The games are drawn for k ≥ 8.

== Chess complexity and conjectures ==

The claim concerns the usual 8x8 game board and also concerns larger game boards with an even number of rows and columns.
It is conjectured that two perfect players can force a draw.
The usual game has been almost completely analyzed, yet there are no strongly conjectured estimates.
These estimates do not favor the initial player (Black) on boards of 10x10 and larger, and there is no estimate that the first player's winning chances increase on 10x10 boards and larger.
Chess is an example of a game with an enormous number of possible states.
The impossibility of building a search tree in some games is due to an enormous number of possible states.
In such games, it is impossible to compile a database of all possible outcomes.
However, the algorithm for this perfect game is unknown.
Many chess problems remain unsolved.
Chess was one of the popular games for which this outcome was predicted.
Chess is a game with a wide draw margin where a draw threatens.

== Chess variants and endgame analysis ==

The context involves GamesCrafters.
These variants are known as Mini-chess.
This analysis was performed by Joel Feinstein.

== Go board sizes and solutions ==

This complexity applies to an n×n board.
For a 4x4 board, the game of Go is solved in the strong sense, and perfect play by the second player leads to a win.
In the specific case of a 6x6 board game, perfect play by the second player leads to a win.
Black has a winning strategy on 15x15 Go boards, and this result is known for board sizes up to 15x15.
Black wins.
Such a winning strategy is unknown today for the general board, and the actual number of responses has not been determined.

== Poker and approximation algorithms ==

Forte provides an algorithm for a game that is not yet solved, though the algorithm can provide a good approximation of the solution.
The Texas hold 'em poker robot Cepheus has limited guarantees, and a human player's lifetime is insufficient to statistically and significantly prove that Cepheus's strategy is not an exact solution.
The Cepheus bot for Texas hold 'em poker has reached the limit of its heads-up play, and a human lifetime playing against the Cepheus bot is insufficient to statistically prove that its strategy is not an exact solution.

== Reversi complexity ==

Reversi is a PSPACE-complete problem.
The game is called Morpion.

== Approximate solutions and verification ==

Even if a game is not solved, an algorithm may produce a good approximate solution.
An article in Science from January 2015 discusses this topic and mentions the Texas hold 'em poker bot Cepheus.
Cepheus guarantees that a human lifetime of play is insufficient to statistically prove its strategy is not an exact solution.
An article in Science announced this limitation.
Most research in the field of game solving is not fully peer-reviewed.
Small errors in programming can occur and lead to very different results.
Such errors generally go unnoticed.
An article in Science published since January 2015 discusses this topic.

== Draw death ==

Draw death is a possible stage in the development of a logical game, which usually refers to board games such as chess, checkers, and Go.
This stage occurs when the theory of the game has been developed to a certain level where any player who knows the theory can force a draw against an opponent regardless of their qualification, meaning the game will end in a draw in the worst-case scenario.
The concept of 'draw death' has occurred, and in any competition, most games will end in a draw.
The concept of a 'draw by stalemate' or similar draw conditions was predicted for many popular games, leading to proposals for rule changes and new game variants to avoid this situation.
These games continue to exist in practice and in their original versions.
Games with a known winning strategy have a zero draw margin.
Xiangqi and Renju are games with a wide draw margin where a draw threatens.
Go, Shogi, and Checkers (Stolbovye shashki) are games with a narrow draw margin.
In these games, the threat of a forced draw does not currently exist.

== Specific solved games ==

In this variant, the piece called 'dame' does not make long moves.
The game is Dobutsu shogi and was strongly resolved.
Maarten Schadd played the game.
The first player can force a win.
The game is Hex.
Jing Yang demonstrated a winning strategy that is a weak solution and applies to 7x7 boards, 8x8 boards, and 9x9 boards.
A winning strategy for Hex with the Cake Rule is known and applies to a 7x7 board.
The second player can always force a win.
Hiroki Takizawa is Japanese.

Computer chess Computer Go Computer Othello Game complexity God's algorithm Zermelo's theorem (game theory)
Victor Allis is the author of the work titled 'Beating the World Champion?' which is published in 'New Approaches to Board Games Research'.
David Eppstein is the author of the work titled 'Computational Complexity of Games and Puzzles'.
The complexity of games is a relevant concept in computer chess.
