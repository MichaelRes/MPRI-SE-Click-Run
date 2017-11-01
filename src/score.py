from functools import total_ordering
import pygame as pg

@total_ordering
class Score(object):
    """
    The class to represent a score.
    """
    def __init__(self, pseudo: str, score: int) -> None:
        self.pseudo = pseudo
        self.score = score

    def update(self, frame):
        """
        Update the score given the new actual frame.
        @param frame: The current frame.
        @type frame: int
        @rtype: None
        """
        self.score += frame

    def __eq__(self, other):
        """
        Function to check if two score are equal.
        @param other: the other score to compare with.
        @type other: Score
        @return: True if they are equal, False otherwise.
        @rtype: bool
        """
        return self.score == other.score

    def __lt__(self, other):
        """
        Function to check if one score is lower than another.
        @param other: the other score to compare with.
        @type other: Score
        @return: True if he is lower, False otherwise.
        @rtype: bool
        """
        return self.score < other.score

    def __str__(self):
        """
        Function to represent a score by a string.
        @return: The string representing the score.
        @rtype: str
        """
        return self.pseudo + " " + str(self.score) + "\n"

    def draw(self, surface, font):
        """
        @param surface: The surface the score will be displayed.
        @type surface: pygame.Surface
        @param font: The font the score will be render on.
        @type font: pygame.font.Font
        @type: None
        """
        s = font.render("Score : " + str(self.score), 1, (255, 0, 0))
        surface.blit(s, (20, 20))


class ScoreManager(object):
    """
    The class to represent the best score.
    This class is a singleton.
    """
    class __ScoreManager:
        def __init__(self):
            """
            @rtype: None
            """
            self.best_score_file = "best_score.data"
            self.scores = self.load_score_file()

        def load_score_file(self):
            """
            Function to load the score file.
            @return: The table of score.
            @rtype: list[Score]
            """
            try:
                with open(self.best_score_file, "r") as f:
                    scores = [score.strip().split(" ") for score in f]
                    scores = [Score(e[0], int(e[1])) for e in scores]
                    return scores
            except FileNotFoundError:
                return []

    instance = None
    max_number_of_score = 10

    def __init__(self) -> None:
        if not ScoreManager.instance:
            ScoreManager.instance = ScoreManager.__ScoreManager()

    def update_score_file(self):
        """
        Function to update the score file by adding the new best score.
        @rtype: None
        """
        with open(self.instance.best_score_file, 'w') as f:
            for score in self.instance.scores:
                f.write(str(score))

    def pos_as_score(self):
        """
        Function to check what would be the position of the given score
        in the best score.
        @param score: The score the user want to check the position.
        @type score: Score
        @return: The position if this score was to be inserted in the best score.
        @rtype: int
        """
        i = 0
        for s in self.instance.scores:
            if s > score:
                i += 1
            else:
                return i
        return i

    def add_score(self, score, pos):
        """
        Function to add a score to the best scores.
        @param score: The score to be inserted.
        @type score: Score
        @param pos: The position where it belongs.
        @type pos: int
        @rtype: None
        """
        self.instance.scores.insert(pos, score)
        if len(self.instance.scores) > 10:
            self.instance.scores.pop()
        self.update_score_file()
