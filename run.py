 #!/usr/bin/env python3

from random import random, choice

class Game:
    def __init__(self):
        self.grid = [[0, 0, 0, 0] for n in range(4)]
        self.randomTile()
        self.randomTile()
        self.score = 0

    def __str__(self):
        s = 'You see several tiles on the grid.'
        lets = 'ABCD'
        for r in range(4):
            for c in range(4):
                if self.grid[r][c]:
                    s += ('\nThe tile %s%d holds the number %d.'
                        % (lets[r], c + 1, self.grid[r][c]))
        return s

    def consolidate(self, row):
        # Copy original row to see if any blocks have moved
        orig = list(row)

        # Push all tiles to the beginning of the row
        offset = 0
        i = 0
        while i + offset < len(row):
            if row[i + offset] != 0:
                row[i] = row[i + offset]
                i += 1
            else:
                offset += 1
        while i < len(row):
            row[i] = 0
            i += 1

        # Combine blocks that are two of a kind, calculating score
        score = 0
        i = 0
        while i < len(row) - 1:
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                score += row[i]
                for j in range(i + 1, len(row) - 1):
                    row[j] = row[j + 1]
                row[-1] = 0
            i += 1

        # Return tuple containing whether the row was changed, and the score
        return row != orig, score

    def moveUp(self):
        didMove = False
        for c in range(4):
            row = []
            for r in range(4):
                row.append(self.grid[r][c])
            moved, score = self.consolidate(row)
            didMove = didMove or moved
            self.score += score
            for r in range(4):
                self.grid[r][c] = row[r]
        if didMove:
            self.randomTile()
        return didMove

    def moveDown(self):
        didMove = False
        for c in range(4):
            row = []
            for r in range(4):
                row.append(self.grid[r][c])
            row.reverse()
            moved, score = self.consolidate(row)
            row.reverse()
            didMove = didMove or moved
            self.score += score
            for r in range(4):
                self.grid[r][c] = row[r]
        if didMove:
            self.randomTile()
        return didMove

    def moveLeft(self):
        didMove = False
        for r in range(4):
            row = list(self.grid[r])
            moved, score = self.consolidate(row)
            didMove = didMove or moved
            self.score += score
            self.grid[r] = row
        if didMove:
            self.randomTile()
        return didMove

    def moveRight(self):
        didMove = False
        for r in range(4):
            row = list(self.grid[r])
            row.reverse()
            moved, score = self.consolidate(row)
            row.reverse()
            didMove = didMove or moved
            self.score += score
            self.grid[r] = row
        if didMove:
            self.randomTile()
        return didMove

    def randomTile(self):
        # Find all empty positions
        positions = []
        for r in range(4):
            for c in range(4):
                if self.grid[r][c] == 0:
                    positions.append((r, c))

        # Give up if there are no possible moves
        if len(positions) == 0:
            return

        # Use a 2 90% of the time, a 4 10% of the time
        if random() < 0.9:
            val = 2
        else:
            val = 4

        # Add tile to grid
        r, c = choice(positions)
        self.grid[r][c] = val

    def isGameOver(self):
        for r in range(4):
            for c in range(4):
                # Check empty tiles
                if self.grid[r][c] == 0:
                    return False
                # Check horizontally adjacent tiles
                if r < 3 and self.grid[r][c] == self.grid[r + 1][c]:
                    return False
                # Check horizontally adjacent tiles
                if c < 3 and self.grid[r][c] == self.grid[r][c + 1]:
                    return False
        return True

    def isWin(self):
        for r in range(4):
            for c in range(4):
                if self.grid[r][c] == 2048:
                    return True
        return False

game = None

def processCommand(command):
    global game
    msg = ''
    stop = False
    # Tokenize command
    tokens = []
    for w in command.split():
        if w:
            tokens.append(w.lower())
    if tokens[0] == 'quit':
        msg = 'You gave up. Your final score was %d.' % game.score
        stop = True
    elif tokens[0] == 'move':
        if len(tokens) > 1:
            func = None
            if tokens[1] == 'up':
                func = game.moveUp
            elif tokens[1] == 'down':
                func = game.moveDown
            elif tokens[1] == 'left':
                func = game.moveLeft
            elif tokens[1] == 'right':
                func = game.moveRight
            if func:
                if func():
                    msg = str(game)
                    if game.isGameOver():
                        msg = 'You lost. Your final score was %d.' % game.score
                        stop = True

                    if game.isWin():
                        msg = 'You win! Now go outside.'
                        stop = True
                else:
                    msg = 'That did nothing. What are you doing?'
    elif tokens[0] == 'panic':
        msg = 'You panic as expected.'

    # Catch all message
    if not msg:
        msg = 'What?'

    return msg, stop

def main():
    global game
    game = Game()
    try:
        while True:
            line = input('> ')
            msg, stop = processCommand(line)
            print(msg)
            if stop:
                break
    except:
        print()

if __name__ == '__main__':
    main()
