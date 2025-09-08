from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import random, string


class WordSearchApp(App):
    def build(self):
        main = BoxLayout(orientation='vertical')
        self.grid = GridLayout(cols=10, rows=10, size_hint=(1, 0.9))
        btn = Button(text='Generate', size_hint=(1, 0.1))
        btn.bind(on_press=lambda x: self.generate())
        main.add_widget(self.grid)
        main.add_widget(btn)
        self.generate()
        return main

    def generate(self):
        self.grid.clear_widgets()
        words = ['PYTHON', 'KIVY', 'CODE', 'APP', 'MOBILE']
        grid = [[random.choice(string.ascii_uppercase) for _ in range(10)] for _ in range(10)]

        # Place words randomly
        for word in words:
            placed = False
            attempts = 0
            while not placed and attempts < 50:
                row, col = random.randint(0, 9), random.randint(0, 9)
                direction = random.choice([(0, 1), (1, 0), (1, 1)])  # horizontal, vertical, diagonal
                if self.can_place_word(grid, word, row, col, direction):
                    self.place_word(grid, word, row, col, direction)
                    placed = True
                attempts += 1

        # Create UI grid
        for row in grid:
            for letter in row:
                lbl = Label(text=letter, font_size='20sp')
                self.grid.add_widget(lbl)

    def can_place_word(self, grid, word, row, col, direction):
        dr, dc = direction
        for i, char in enumerate(word):
            r, c = row + i * dr, col + i * dc
            if r >= 10 or c >= 10 or r < 0 or c < 0:
                return False
        return True

    def place_word(self, grid, word, row, col, direction):
        dr, dc = direction
        for i, char in enumerate(word):
            r, c = row + i * dr, col + i * dc
            grid[r][c] = char


WordSearchApp().run()