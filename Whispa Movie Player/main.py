import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


from router import Router
from ui_movies import MoviesFrame
from ui_mylist import MyListFrame
from ui_preview import PreviewFrame
from ui_player import PlayerFrame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Theme
PRIMARY = "#b8a1f2"
WINDOW_BG = "#c5b3f0"
NAV_BG = PRIMARY
NAV_TEXT = "#111"
NAV_TEXT_ACCENT = "#5940B3"

# title map
FILENAME_TITLE_MAP = {
    "movie1": "Tangled",
    "movie2": "Brave",
    "movie3": "Mulan",
    "movie4": "Beauty and the Beast",
    "movie5": "Moana",
    "movie6": "The Little Mermaid",
    "movie7": "The Lion King",
    "movie8": "Aladdin",
    "movie9": "Encanto",
    "movie10": "Frozen",
    "movie11": "Coco",
    "movie12": "Inside Out",
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Whispa Movie Player")
        self.config(bg=WINDOW_BG)
        self.minsize(1440, 900)

        # ttk style tweaks
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TEntry", padding=6)
        style.configure("TButton", padding=6)

        icon_path = os.path.join(BASE_DIR, "assets", "logo.png")
        if os.path.exists(icon_path):
            try:
                icon_img = Image.open(icon_path)
                self.iconphoto(False, ImageTk.PhotoImage(icon_img))
            except Exception:
                pass

        self.create_navbar()

        self.container = tk.Frame(self, bg=WINDOW_BG)
        self.container.pack(side="top", fill="both", expand=True)

        self.state = {"saved": [], "movies": []}

        self.load_movies()

        self.router = Router(self.container, self)

        self.router.register("movies", MoviesFrame)
        self.router.register("mylist", MyListFrame)
        self.router.register("preview", PreviewFrame)
        self.router.register("player", PlayerFrame)

        self.router.show("movies")

    #NAVBAR
    def create_navbar(self):
        self.nav = tk.Frame(self, bg=NAV_BG, height=72)
        self.nav.pack(side="top", fill="x")

        logo_path = os.path.join(BASE_DIR, "assets", "logo_whispa.png")
        if os.path.exists(logo_path):
            try:
                im = Image.open(logo_path).resize((160, 48), Image.LANCZOS)
                self._logo_img = ImageTk.PhotoImage(im)
                logo_lbl = tk.Label(self.nav, image=self._logo_img, bg=NAV_BG)
            except Exception:
                logo_lbl = tk.Label(self.nav, text="Whispa", font=("Helvetica", 18, "bold"), bg=NAV_BG, fg=NAV_TEXT)
        else:
            logo_lbl = tk.Label(self.nav, text="Whispa", font=("Helvetica", 18, "bold"), bg=NAV_BG, fg=NAV_TEXT)
        logo_lbl.pack(side="left", padx=12, pady=10)

        mid = tk.Frame(self.nav, bg=NAV_BG)
        mid.pack(side="left", padx=10)
        btn_style = {
            "bg": NAV_BG,
            "fg": NAV_TEXT_ACCENT,
            "bd": 0,
            "activebackground": NAV_BG,
            "padx": 18,
            "pady": 12,
            "font": ("Helvetica", 13, "bold"),
            "relief": "flat",
        }
        movies_btn = tk.Button(mid, text="Movies", command=lambda: self.router.show("movies"), **btn_style)
        movies_btn.pack(side="left", padx=6, pady=0)
        mylist_btn = tk.Button(mid, text="My List", command=lambda: self.router.show("mylist"), **btn_style)
        mylist_btn.pack(side="left", padx=6, pady=0)

        right = tk.Frame(self.nav, bg=NAV_BG)
        right.pack(side="right", padx=12)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(right, textvariable=self.search_var, width=36)
        self.search_entry.pack(side="left", padx=(0,6), pady=12)
        self._placeholder_text = "Search movies..."
        self.search_entry.insert(0, self._placeholder_text)

        def on_focus_in(ev):
            if self.search_entry.get().strip() == self._placeholder_text:
                self.search_entry.delete(0, "end")
        def on_focus_out(ev):
            if not self.search_entry.get().strip():
                self.search_entry.insert(0, self._placeholder_text)
        self.search_entry.bind("<FocusIn>", on_focus_in)
        self.search_entry.bind("<FocusOut>", on_focus_out)
        self.search_entry.bind("<Return>", lambda e: self.perform_search())

        logout_btn = tk.Button(
            right,
            text="Back to Home",
            command=lambda: self.back_to_home(),
            bg=NAV_BG,
            fg=NAV_TEXT_ACCENT,
            bd=0,
            font=("Helvetica", 13, "bold"),
            padx=12,
            pady=12
        )
        logout_btn.pack(side="left", padx=6, pady=0)

    # navbar functions/visibility
    def hide_navbar(self):
        try:
            self.nav.pack_forget()
        except Exception:
            pass

    def show_navbar(self):
        try:
            self.nav.pack(side="top", fill="x")
        except Exception:
            pass

    #load movies
    def load_movies(self):
        self.state["movies"] = [
                    {
                        "id": 1,
                        "title": "Tangled",
                        "poster": "Whispa Movie Player/assets/posters/movie1.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie1.mp4",
                        "description": "Beautiful princess Rapunzel has been locked away in a tower since she was captured as a baby by an old hag. Her magical long blonde hair has the power to provide eternal youth, and the evil Gothel uses this power to keep her young. At the age of 18, Rapunzel becomes curious about the outside world, and when a prince uses her tower as a refuge, she asks him to help her escape.",
                        "cast": "Mandy Moore, Zachary Levi",
                        "genre": "Animation, Adventure, Family",
                        "duration": "1h 40m",
                        "age": "PG"
                    },
                    {
                        "id": 2,
                        "title": "Brave",
                        "poster": "Whispa Movie Player/assets/posters/movie2.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie2.mp4",
                        "description": "Merida (Kelly Macdonald), the impetuous but courageous daughter of Scottish King Fergus (Billy Connolly) and Queen Elinor (Emma Thompson), is a skilled archer who wants to carve out her own path in life. Her defiance of an age-old tradition angers the Highland lords and leads to chaos in the kingdom. Merida seeks help from an eccentric witch (Julie Walters), who grants her an ill-fated wish. Now, Merida must discover the true meaning of courage and undo a beastly curse before it's too late.",
                        "cast": "Kelly Macdonald, Billy Connolly",
                        "genre": "Animation, Adventure, Family",
                        "duration": "1h 33m",
                        "age": "PG"
                    },
                    {
                        "id": 3,
                        "title": "Mulan",
                        "poster": "Whispa Movie Player/assets/posters/movie3.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie3.mp4",
                        "description": "To keep her ailing father from serving in the Imperial Army, a fearless young woman disguises herself as a man and battles northern invaders in China.",
                        "cast": "Ming-Na Wen, Eddie Murphy",
                        "genre": "Animation, Action, Adventure",
                        "duration": "1h 28m",
                        "age": "PG"
                    },
                    {
                        "id": 4,
                        "title": "Beauty and the Beast",
                        "poster": "Whispa Movie Player/assets/posters/movie4.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie4.mp4",
                        "description": "An arrogant prince is cursed to live as a terrifying beast until he finds true love. Strangely, his chance comes when he captures an unwary clockmaker, whose place is then taken by his bold and beautiful daughter Belle. Helped by the Beast's similarly enchanted servants, including a clock, a teapot and a candelabra, Belle begins to see the sensitive soul behind the fearsome facade. But as time runs out, it soon becomes obvious that Belle's cocky suitor Gaston is the real beast of the piece.",
                        "cast": "Paige O’Hara, Robby Benson",
                        "genre": "Animation, Family, Fantasy",
                        "duration": "1h 24m",
                        "age": "G"
                    },
                    {
                        "id": 5,
                        "title": "Moana",
                        "poster": "Whispa Movie Player/assets/posters/movie5.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie5.mp4",
                        "description": "An adventurous teenager sails out on a daring mission to save her people. During her journey, Moana meets the once-mighty demigod Maui, who guides her in her quest to become a master way-finder. Together they sail across the open ocean on an action-packed voyage, encountering enormous monsters and impossible odds. Along the way, Moana fulfills the ancient quest of her ancestors and discovers the one thing she always sought: her own identity.",
                        "cast": "Auli'i Cravalho, Dwayne Johnson",
                        "genre": "Animation, Adventure, Comedy",
                        "duration": "1h 47m",
                        "age": "PG"
                    },
                    {
                        "id": 6,
                        "title": "The Little Mermaid",
                        "poster": "Whispa Movie Player/assets/posters/movie6.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie6.mp4",
                        "description": "In Disney's beguiling animated romp, rebellious 16-year-old mermaid Ariel (Ron Clements) is fascinated with life on land. On one of her visits to the surface, which are forbidden by her controlling father, King Triton, she falls for a human prince. Determined to be with her new love, Ariel makes a dangerous deal with the sea witch Ursula (John Musker) to become human for three days. But when plans go awry for the star-crossed lovers, the king must make the ultimate sacrifice for his daughter.",
                        "cast": "Jodi Benson, Samuel E. Wright",
                        "genre": "Animation, Family, Fantasy",
                        "duration": "1h 23m",
                        "age": "G"
                    },
                    {
                        "id": 7,
                        "title": "The Lion King",
                        "poster": "Whispa Movie Player/assets/posters/movie7.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie7.mp4",
                        "description": "Simba idolizes his father, King Mufasa, and takes to heart his own royal destiny on the plains of Africa. But not everyone in the kingdom celebrates the new cub's arrival. Scar, Mufasa's brother -- and former heir to the throne -- has plans of his own. The battle for Pride Rock is soon ravaged with betrayal, tragedy and drama, ultimately resulting in Simba's exile. Now, with help from a curious pair of newfound friends, Simba must figure out how to grow up and take back what is rightfully his.",
                        "cast": "Matthew Broderick, James Earl Jones",
                        "genre": "Animation, Adventure, Drama",
                        "duration": "1h 28m",
                        "age": "G"
                    },
                    {
                        "id": 8,
                        "title": "Aladdin",
                        "poster": "Whispa Movie Player/assets/posters/movie8.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie8.mp4",
                        "description": "Aladdin is a lovable street urchin who meets Princess Jasmine, the beautiful daughter of the sultan of Agrabah. While visiting her exotic palace, Aladdin stumbles upon a magic oil lamp that unleashes a powerful, wisecracking, larger-than-life genie. As Aladdin and the genie start to become friends, they must soon embark on a dangerous mission to stop the evil sorcerer Jafar from overthrowing young Jasmine's kingdom.",
                        "cast": "Scott Weinger, Robin Williams",
                        "genre": "Animation, Adventure, Comedy",
                        "duration": "1h 28m",
                        "age": "G"
                    },
                    {
                        "id": 9,
                        "title": "Encanto",
                        "poster": "Whispa Movie Player/assets/posters/movie9.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie9.mp4",
                        "description": "Encanto tells the tale of an extraordinary family, the Madrigals, who live hidden in the mountains of Colombia, in a magical house, in a vibrant town.",
                        "cast": "Stephanie Beatriz, María Cecilia Botero",
                        "genre": "Animation, Adventure, Comedy",
                        "duration": "1h 39m",
                        "age": "PG"
                    },
                    {
                        "id": 10,
                        "title": "Frozen",
                        "poster": "Whispa Movie Player/assets/posters/movie10.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie10.mp4",
                        "description": "When their kingdom becomes trapped in perpetual winter, fearless Anna (Kristen Bell) joins forces with mountaineer Kristoff (Jonathan Groff) and his reindeer sidekick to find Anna's sister, Snow Queen Elsa (Idina Menzel), and break her icy spell. Although their epic journey leads them to encounters with mystical trolls, a comedic snowman (Josh Gad), harsh conditions, and magic at every turn, Anna and Kristoff bravely push onward in a race to save their kingdom from winter's cold grip.",
                        "cast": "Kristen Bell, Idina Menzel",
                        "genre": "Animation, Adventure, Comedy",
                        "duration": "1h 42m",
                        "age": "PG"
                    },
                    {
                        "id": 11,
                        "title": "Coco",
                        "poster": "Whispa Movie Player/assets/posters/movie11.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie11.mp4",
                        "description": "Despite his family's generations-old ban on music, young Miguel dreams of becoming an accomplished musician like his idol Ernesto de la Cruz. Desperate to prove his talent, Miguel finds himself in the stunning and colorful Land of the Dead. After meeting a charming trickster named Héctor, the two new friends embark on an extraordinary journey to unlock the real story behind Miguel's family history.",
                        "cast": "Anthony Gonzalez, Gael García Bernal",
                        "genre": "Animation, Adventure, Family",
                        "duration": "1h 45m",
                        "age": "PG"
                    },
                    {
                        "id": 12,
                        "title": "Inside Out",
                        "poster": "Whispa Movie Player/assets/posters/movie12.jpg",
                        "trailer": "Whispa Movie Player/assets/trailers/movie12.mp4",
                        "description": "Riley (Kaitlyn Dias) is a happy, hockey-loving 11-year-old Midwestern girl, but her world turns upside-down when she and her parents move to San Francisco. Riley's emotions -- led by Joy (Amy Poehler) -- try to guide her through this difficult, life-changing event. However, the stress of the move brings Sadness (Phyllis Smith) to the forefront. When Joy and Sadness are inadvertently swept into the far reaches of Riley's mind, the only emotions left in Headquarters are Anger, Fear and Disgust.",
                        "cast": "Amy Poehler, Phyllis Smith",
                        "genre": "Animation, Adventure, Comedy",
                        "duration": "1h 35m",
                        "age": "PG"
                    }
                ]

    # search function
    def perform_search(self):
        q = self.search_var.get().strip()
        if not q or q == getattr(self, "_placeholder_text", ""):
            self.router.show("movies")
            return
        q_low = q.lower()
        matches = [m for m in self.state["movies"] if q_low in m["title"].lower()]
        if not matches:
            tokens = [t for t in q_low.split() if t]
            if tokens:
                def score(m):
                    t = m["title"].lower()
                    return sum((1 for tk in tokens if tk in t))
                scored = sorted(self.state["movies"], key=lambda m: score(m), reverse=True)
                matches = [m for m in scored if score(m) > 0]
        self.router.show("movies", params={"filter": matches})

    #log out/back to home
    def back_to_home(app):
        app.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
