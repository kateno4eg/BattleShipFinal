from random import randint
import time
from extensions import BoardException, BoardWrongShipException
from innerlogic import Dot, Board, Ship


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_board()
        computer = self.random_board()
        computer.hid = True

        self.ai = AI(computer, player)
        self.user = User(player, computer)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("Приветствуем вас в игре Морской Бой!")
        print("Формат ввода: x y, где x - номер строки, y - номер столбца.")

    @staticmethod
    def hstack(first, second):
        first_sp = first.split("\n")
        second_sp = second.split("\n")
        max_width = max(map(len, first_sp))

        max_len = max(len(first_sp), len(second_sp))
        first_sp += [""] * (max_len - len(first_sp))
        second_sp += [""] * (max_len - len(second_sp))

        text = []
        for f, s in zip(first_sp, second_sp):
            text.append(f"{f: <{max_width}}     {s: <{max_width}}")

        return "\n".join(text)

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            user_board = "Доска пользователя:\n\n" + str(self.user.board)
            ai_board = "Доска компьютера:\n\n" + str(self.ai.board)
            print(self.hstack(user_board, ai_board))
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("-" * 20)
                print("Ходит компьютер! Вычисление координат ракетного удара ... ")
                time.sleep(3)
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.user.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
