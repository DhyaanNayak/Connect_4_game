# Connect 4 Game Featuring Three AI Opponents with Increasing Difficulty Levels

In this Connect 4 game implementation, we employ a score-based system to evaluate a player's performance. The scoring is determined by the number of "2 in a line" and "3 in a line" connections, with consideration given to the potential for extending these connections.

## Scoring Criteria:

### 1.	Piece Connections:

•	We assess connections in every orientation (horizontal, vertical, and diagonal).

•	Scores are awarded independently of orientation, with higher emphasis on longer connections.

•	A 3-piece connection is scored higher than a 2-piece connection, reflecting its greater strategic value.

### 2.	Blocking Opponent's Win:

•	Recognizing the importance of defensive play, blocking the opponent's 3-piece and 4-piece connections is prioritized.

•	Successfully preventing an opponent's potential win is rewarded with a higher score than achieving a 3-piece connection for the player.

### 3.	Positioning Near the Center:

•	We incentivize placing pieces near the center of the board.

•	Central positions offer increased opportunities for future connections, aligning with our strategic objective of securing wins.

-----

This scoring system reflects our strategic emphasis on both offensive and defensive manoeuvres.
The agent is guided to prioritize actions that enhance its winning potential while actively thwarting the opponent's strategic advances. 
The preference for central positioning further optimizes the agent's chances of achieving successful connections. 
