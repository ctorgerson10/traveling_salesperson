import queue
import tkinter as tk
from tkinter.ttk import *

from lib.city import City
from lib.search import search_this_map
from lib.variables import Variables


class DrawIt:

    def __init__(self):
        super(DrawIt, self).__init__()
        self.root = tk.Tk()
        self.root.title('Dr Bs City Demo')
        self.screen = Screen()

        width = int(Variables.WIDTH)
        height = int(Variables.HEIGHT * 1.2)
        self.root.geometry(str(width) + "x" + str(height))
        self.screen.grid(row=0, columnspan=5, sticky="N, S, E, W")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        button = Button(self.root, text='(Re)make Map',
                        command=self.remake_cities)
        button.grid(row=1, column=0)
        self.entry = Entry(self.root)
        label = Label(self.root, text="Number of cities")
        label.grid(row=1, column=2)
        self.entry.insert(0, "10")
        self.entry.grid(row=1, column=3)
        button2 = Button(self.root, text='Search this map',
                         command=self.search)
        button2.grid(row=1, column=4)

    def remake_cities(self):
        self.screen.remake_cities(int(self.entry.get()))

    def search(self):
        self.screen.search()


class Screen(tk.Canvas):

    def __init__(self):
        super(Screen, self).__init__()
        self.things_to_draw = queue.Queue()
        self.current_search = []
        self.remake_cities(Variables.NUM_CITIES)
        self.configure(background='black')

        self.paint()

    def paint(self):
        if self.things_to_draw.qsize() > 0:
            c = self.things_to_draw.get()
            if c is not None and len(c) >= 2:
                # erase the background
                self.create_rectangle(0, 0, Variables.WIDTH, Variables.HEIGHT * 2, fill="White")
                # draw the connections
                for i in range(1, len(c)):
                    a = c[i - 1]
                    b = c[i]
                    self.create_line(a.x, a.y, b.x, b.y, fill="Blue")
                # draw the final connection
                self.create_line(c[0].x, c[0].y, c[len(c) - 1].x, c[len(c) - 1].y, fill="Blue")

                # Draw the cities
                half_city = Variables.CITY_SIZE / 2
                for city in c:
                    self.create_oval(city.x - half_city, city.y - half_city, city.x + half_city, city.y + half_city,
                                     fill='Black')

        self.after(Variables.SLEEP_TIME, self.paint)

    def remake_cities(self, num_cities):
        print("Making cities", num_cities)
        self.current_search = [City() for _ in range(num_cities)]
        self.clear_searches()
        self.add_search_step(self.current_search)

    def add_possible_solution(self, c):
        self.add_search_step(c)

    def clear_searches(self):
        self.things_to_draw = queue.Queue()

    def add_search_step(self, c: list[City] | None):
        self.things_to_draw.put(c)

    def search(self):
        self.clear_searches()
        self.add_search_step(self.current_search)
        things_to_display = search_this_map(self.current_search)
        if things_to_display is not None and len(things_to_display) > 0:
            for li in things_to_display:
                self.add_search_step(li)
        else:
            self.add_search_step(None)
