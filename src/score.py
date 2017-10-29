from functools import total_ordering


@total_ordering
class Score(object):
    def __init__(self, pseudo: str, score: int) -> None:
        self.pseudo = pseudo
        self.score = score

    def __eq__(self, other: 'Score') -> bool:
        return self.score == other.score

    def __lt__(self, other: 'Score') -> bool:
        return self.score < other.score

    def __str__(self):
        return self.pseudo + " " + str(self.score) + "\n"


class ScoreManager(object):
    class __ScoreManager:
        def __init__(self) -> None:
            self.best_score_file = "best_score.data"
            self.scores = self.load_score_file()

        def load_score_file(self) -> [Score]:
            try:
                with open(self.best_score_file, "r") as f:
                    scores = [score.strip().split(" ") for score in f]
                    scores = [Score(e[0], int(e[1])) for e in scores]
                    return scores
            except FileNotFoundError:
                return []

    instance = None

    def __init__(self) -> None:
        if not ScoreManager.instance:
            ScoreManager.instance = ScoreManager.__ScoreManager()

    def update_score_file(self) -> None:
        with open(self.instance.best_score_file, 'w') as f:
            for score in self.instance.scores:
                f.write(str(score))

    def pos_as_score(self, score: Score) -> int:
        for i, s in enumerate(self.instance.scores):
            if s > score:
                pass
            else:
                return i
        return -1

    def add_score(self, score: Score, pos: int) -> None:
        self.instance.scores.insert(pos, score)
        if len(self.instance.scores) > 10:
            self.instance.scores.pop()
        self.update_score_file()


def test():
    score = ScoreManager()
    score1 = Score("Baba", 100)
    for i in range(10):
        score.add_score(score1, 0)


def test2():
    score = ScoreManager()
    score1 = Score("Tata", 150)
    p = score.pos_as_score(score1)
    score.add_score(score1, p)


def test3():
    score = ScoreManager()
    score1 = Score("Tata", 15)
    p = score.pos_as_score(score1)
    if p != -1:
        score.add_score(score1, p)
