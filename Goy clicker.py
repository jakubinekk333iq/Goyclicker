import tkinter as tk
from tkinter import ttk
import math
import random
import json
import os
import time

class GoybuckClicker:
    def __init__(self):
        # Modern Professional Color Palette
        self.colors = {
            "bg_main": "#0f172a",      # Slate 900
            "bg_panel": "#1e293b",     # Slate 800
            "bg_input": "#334155",     # Slate 700
            "text_main": "#f8fafc",    # Slate 50
            "text_muted": "#94a3b8",   # Slate 400
            "accent": "#6366f1",       # Indigo 500
            "accent_hover": "#4f46e5", # Indigo 600
            "success": "#10b981",      # Emerald 500
            "danger": "#ef4444",       # Red 500
            "warning": "#f59e0b",      # Amber 500
            "gold": "#eab308",         # Yellow 500
        }

        self.goybucks = 0
        self.total_earned = 0
        self.cps = 0
        self.cpc = 1
        self.multiplier = 1
        self.israelcoins = 0
        self.rebirths = 0
        self.clicks = 0
        self.last_save = time.time()

        self.level = 1
        self.xp = 0
        self.player_hp = 20
        self.hand_angle = 0.0

        self.weapon_stats = {
            "fists":            {"dmg": 1,  "crit": 0.0, "crit_dmg": 1,  "tier": 0},
            "wooden_sword":     {"dmg": 4,  "crit": 0.0, "crit_dmg": 4,  "tier": 1},
            "wooden_axe":       {"dmg": 3,  "crit": 0.5, "crit_dmg": 5,  "tier": 1},
            "stone_sword":      {"dmg": 7,  "crit": 0.0, "crit_dmg": 7,  "tier": 2},
            "stone_axe":        {"dmg": 6,  "crit": 0.5, "crit_dmg": 8,  "tier": 2},
            "iron_sword":       {"dmg": 12, "crit": 0.0, "crit_dmg": 12, "tier": 3},
            "iron_axe":         {"dmg": 10, "crit": 0.5, "crit_dmg": 14, "tier": 3},
            "golden_sword":     {"dmg": 18, "crit": 0.0, "crit_dmg": 18, "tier": 4},
            "golden_axe":       {"dmg": 15, "crit": 0.5, "crit_dmg": 22, "tier": 4},
            "diamond_sword":    {"dmg": 28, "crit": 0.0, "crit_dmg": 28, "tier": 5},
            "diamond_axe":      {"dmg": 22, "crit": 0.5, "crit_dmg": 35, "tier": 5},
            "platinum_sword":   {"dmg": 42, "crit": 0.0, "crit_dmg": 42, "tier": 6},
            "platinum_axe":     {"dmg": 35, "crit": 0.5, "crit_dmg": 55, "tier": 6},
            "kyle_sword":       {"dmg": 63, "crit": 0.0, "crit_dmg": 63, "tier": 7},
            "miss_bailey_handshake": {"dmg": 85, "crit": 0.10, "crit_dmg": 120, "tier": 8},
        }
        self.armour_stats = {
            "none":               {"red": 0.0, "tier": 0},
            "leather_armour":     {"red": 0.5, "tier": 1},
            "chainmail":          {"red": 1.0, "tier": 2},
            "iron_armour":        {"red": 2.0, "tier": 3},
            "golden_armour":      {"red": 3.0, "tier": 4},
            "diamond_armour":     {"red": 5.0, "tier": 5},
            "platinum_armour":    {"red": 8.0, "tier": 6},
            "my_g_leader_armour": {"red": 12.0,"tier": 7},
        }

        self.inventory = {k: 0 for k in list(self.weapon_stats.keys()) + list(self.armour_stats.keys())
                          if k not in ("fists", "none")}
        self.equipped_weapon = "fists"
        self.equipped_armour = "none"

        self.gamble_paths = {
            "wooden_sword":   ("stone_sword",    "iron_sword"),
            "wooden_axe":     ("stone_axe",      "iron_axe"),
            "leather_armour": ("chainmail",      "iron_armour"),
            "stone_sword":    ("iron_sword",     "golden_sword"),
            "stone_axe":      ("iron_axe",       "golden_axe"),
            "chainmail":      ("iron_armour",    "golden_armour"),
            "iron_sword":     ("golden_sword",   "diamond_sword"),
            "iron_axe":       ("golden_axe",     "diamond_axe"),
            "iron_armour":    ("golden_armour",  "diamond_armour"),
            "golden_sword":   ("diamond_sword",  "platinum_sword"),
            "golden_axe":     ("diamond_axe",    "platinum_axe"),
            "golden_armour":  ("diamond_armour", "platinum_armour"),
            "diamond_sword":  ("platinum_sword", "kyle_sword"),
            "diamond_axe":    ("platinum_axe",   "platinum_axe"),
            "diamond_armour": ("platinum_armour","my_g_leader_armour"),
            "platinum_sword": ("kyle_sword",     None),
            "platinum_axe":   ("platinum_axe",   None),
            "platinum_armour":("my_g_leader_armour", None),
            "kyle_sword":       ("miss_bailey_handshake", None),
            "my_g_leader_armour":(None, None),
            "miss_bailey_handshake": (None, None),
        }

        self.crates = {
            "Wooden Crate":   {"cost": 400,       "loot": ["leather_armour", "wooden_sword", "wooden_axe"]},
            "Stone Crate":    {"cost": 4000,      "loot": ["chainmail", "stone_sword", "stone_axe"]},
            "Iron Crate":     {"cost": 40000,     "loot": ["iron_armour", "iron_sword", "iron_axe"]},
            "Golden Crate":   {"cost": 400000,    "loot": ["golden_armour", "golden_sword", "golden_axe"]},
            "Diamond Crate":  {"cost": 4000000,   "loot": ["diamond_armour", "diamond_sword", "diamond_axe"]},
            "Platinum Crate": {"cost": 50000000,  "weighted": [
                ("platinum_armour",    0.327), ("platinum_sword",     0.327), ("platinum_axe",       0.327),
                ("kyle_sword",         0.010), ("my_g_leader_armour", 0.009),
            ]},
            "Mythic Crate": {"cost": 500000000,  "weighted": [
                ("platinum_armour",    0.327), ("platinum_sword",     0.327), ("platinum_axe",       0.327),
                ("kyle_sword",         0.005), ("my_g_leader_armour", 0.005),
                ("miss_bailey_handshake", 0.009),
            ]},
            "Spell Crate": {"cost": 100000, "weighted": [
                ("Sharpness I", 0.25), ("Protection I", 0.25), ("Sharpness II", 0.15), ("Protection II", 0.15),
                ("Flame I", 0.10), ("Thorns I", 0.10)
            ]},
        }

        self.bosses = {
            "Kyle Fairclough": {"hp": 80,  "atk": 6,  "special": 0.20, "xp": 120,  "gold": 800,     "req_level": 3,  "req_boss": None},
            "Che":             {"hp": 220, "atk": 14, "special": 0.25, "xp": 500,  "gold": 8000,    "req_level": 6,  "req_boss": "Kyle Fairclough"},
            "My G Leader":     {"hp": 550, "atk": 22, "special": 0.30, "xp": 2000, "gold": 80000,   "req_level": 10, "req_boss": "Che"},
            "Riley":           {"hp": 1200,"atk": 30, "special": 0.35, "xp": 5000, "gold": 250000,  "req_level": 14, "req_boss": "My G Leader"},
            "Steven Ibudimua": {"hp": 2200,"atk": 40, "special": 0.35, "xp": 15000,"gold": 1000000, "req_level": 18, "req_boss": "Riley"},
            "Goatis":          {"hp": 3500,"atk": 55, "special": 0.40, "xp": 25000,"gold": 2500000, "req_level": 22, "req_boss": "Steven Ibudimua"},
            "Ben Rea":         {"hp": 6000,"atk": 70, "special": 0.45, "xp": 40000,"gold": 6000000, "req_level": 26, "req_boss": "Goatis"},
            "Matthew Alty":    {"hp": 10000,"atk": 85,"special": 0.50, "xp": 70000,"gold": 12000000,"req_level": 30, "req_boss": "Ben Rea"},
        }
        self.bosses_defeated = {k: 0 for k in self.bosses}

        self.combat = None
        self.combat_win = None

        self.upgrades = {
            "Kyle Faircloughs": {"cost": 15, "cpc": 1, "count": 0, "type": "cpc"},
            "My G Leaders": {"cost": 100, "cps": 1, "count": 0, "type": "cps"},
            "Che Barcelo": {"cost": 1100, "cpc": 5, "count": 0, "type": "cpc"},
            "C K Dramas": {"cost": 12000, "cps": 47, "count": 0, "type": "cps"},
            "Gohst Duo": {"cost": 130000, "cps": 260, "count": 0, "type": "cps"},
            "Miss Parishes 'Stage'": {"cost": 50000, "cps": 100, "cpc": 10, "count": 0, "type": "both"},
            "Jadens Weakness (Martin)": {"cost": 500000, "cps": 500, "cpc": 50, "count": 0, "type": "both"},
            "The Screws": {"cost": 5000000, "cps": 2000, "cpc": 200, "count": 0, "type": "both"},
            "Steven Raphael Ibudimua": {"cost": 10000000, "cpc": 500, "count": 0, "type": "cpc"},
        }

        self.achievements = {
            "First Click":        {"req": 1, "type": "clicks", "done": False},
            "Hundred Club":       {"req": 100, "type": "goybucks", "done": False},
            "Kyle Fan":           {"req": 10, "type": "upgrade_Kyle Faircloughs", "done": False},
            "Gohstly":            {"req": 10, "type": "upgrade_Gohst Duo", "done": False},
            "Millionaire":        {"req": 1000000, "type": "goybucks", "done": False},
            "Legendary Set":      {"req": 1, "type": "legendary_set", "done": False},
            "Mythic God":         {"req": 1, "type": "mythic_set", "done": False},
        }
        
        self.skill_tree = {
            "Miss Bailey Handshake": {"cost": 2, "desc": "+20% Money Making", "bought": False},
            "Mr Banks Money Boost": {"cost": 5, "desc": "+50% Money Making", "bought": False},
            "Mr Crossfields Overtime": {"cost": 3, "desc": "Boosts last 2x longer", "bought": False},
            "Riley Rage Criticals": {"cost": 4, "desc": "+25% Crit Chance globally", "bought": False},
            "Israelcoin Yield": {"cost": 5, "desc": "+1 Israelcoin per Rebirth", "bought": False},
        }

        self.stages = {
            "The Stage": {"unlocked": True, "cost": 0, "cps_mult": 1.0, "cpc_mult": 1.0, "bg": "#0f172a"},
            "Stephens Stage 1": {"unlocked": False, "cost": 5, "cps_mult": 1.5, "cpc_mult": 1.5, "bg": "#2e1a2e"},
            "The Backrooms": {"unlocked": False, "cost": 15, "cps_mult": 2.5, "cpc_mult": 2.5, "bg": "#d4c450"},
            "The Bailey Boxing Ring": {"unlocked": False, "cost": 40, "cps_mult": 5.0, "cpc_mult": 5.0, "bg": "#2e1a1a"},
        }
        self.current_stage = "The Stage"

        self.boosts = {
            "Where is the Boost?": {"cost": 50000, "duration": 60, "desc": "Bosses 75% chance to hit themselves", "active_until": 0},
            "Miss Wadwha Crashouts": {"cost": 100000, "duration": 60, "desc": "1.5x Money, higher crits", "active_until": 0},
            "Riley Rage": {"cost": 200000, "duration": 60, "desc": "100% Crit Chance in combat", "active_until": 0},
            "Scitzo Meds": {"cost": 500000, "duration": 120, "desc": "More Golden Goybucks & they give 2x", "active_until": 0},
        }

        self.enchantments = {
            "Sharpness I": {"cost": 50000, "type": "weapon", "desc": "+2 DMG"},
            "Sharpness II": {"cost": 150000, "type": "weapon", "desc": "+5 DMG"},
            "Sharpness III": {"cost": 500000, "type": "weapon", "desc": "+10 DMG"},
            "Sharpness IV": {"cost": 1500000, "type": "weapon", "desc": "+20 DMG"},
            "Sharpness V": {"cost": 5000000, "type": "weapon", "desc": "+40 DMG"},
            "Flame I": {"cost": 100000, "type": "weapon", "desc": "1.2x Crit DMG"},
            "Flame II": {"cost": 300000, "type": "weapon", "desc": "1.5x Crit DMG"},
            "Flame III": {"cost": 1000000, "type": "weapon", "desc": "2.0x Crit DMG"},
            "Protection I": {"cost": 50000, "type": "armour", "desc": "+1.0 DEF"},
            "Protection II": {"cost": 150000, "type": "armour", "desc": "+2.5 DEF"},
            "Protection III": {"cost": 500000, "type": "armour", "desc": "+5.0 DEF"},
            "Protection IV": {"cost": 1500000, "type": "armour", "desc": "+10.0 DEF"},
            "Protection V": {"cost": 5000000, "type": "armour", "desc": "+20.0 DEF"},
            "Thorns I": {"cost": 100000, "type": "armour", "desc": "10% reflect 2 dmg"},
            "Thorns II": {"cost": 300000, "type": "armour", "desc": "20% reflect 5 dmg"},
            "Thorns III": {"cost": 1000000, "type": "armour", "desc": "30% reflect 10 dmg"},
        }
        self.spell_inventory = {k: 0 for k in self.enchantments}
        self.item_enchants = {k: {} for k in list(self.weapon_stats.keys()) + list(self.armour_stats.keys())}

        self.root = tk.Tk()
        self.root.title("Goybuck Clicker")
        self.root.geometry("1280x800")
        self.root.configure(bg=self.colors["bg_main"])
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_ui()
        self.load_game()
        self.player_hp = self.get_max_hp()
        self.refresh_all_tabs()
        self.game_loop()

    # ================= STATS =================
    def get_max_hp(self): return 20 + 8 * (self.level - 1)
    def xp_needed(self): return int(50 * self.level ** 1.5)
    def rebirth_req(self): return int(1_000_000 * (1.5 ** self.rebirths))
    
    def get_attack(self):
        base = self.weapon_stats[self.equipped_weapon]["dmg"] + 2 * (self.level - 1)
        enchants = self.item_enchants.get(self.equipped_weapon, {})
        for i, name in enumerate(["Sharpness I", "Sharpness II", "Sharpness III", "Sharpness IV", "Sharpness V"]):
            if name in enchants: base += [2, 5, 10, 20, 40][i]
        return base * (1 + 0.005 * sum(self.bosses_defeated.values()))

    def get_armour(self):
        base = self.armour_stats[self.equipped_armour]["red"]
        enchants = self.item_enchants.get(self.equipped_armour, {})
        for i, name in enumerate(["Protection I", "Protection II", "Protection III", "Protection IV", "Protection V"]):
            if name in enchants: base += [1.0, 2.5, 5.0, 10.0, 20.0][i]
        return base

    def get_boss_dmg_mult(self): return 1 + 0.005 * sum(self.bosses_defeated.values())
    def get_prestige_mult(self): return 1 + (self.rebirths * 0.25)
    def get_ach_mult(self): return 1 + (sum(1 for a in self.achievements.values() if a["done"]) * 0.05)
    def is_boost_active(self, name): return time.time() < self.boosts[name]["active_until"]

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_needed():
            self.xp -= self.xp_needed()
            self.level += 1
            self.player_hp = self.get_max_hp()

    def exp_dmg(self, w):
        s = self.weapon_stats[w]
        return s["dmg"] * (1 - s["crit"]) + s["crit_dmg"] * s["crit"]

    def auto_equip(self, item):
        if item in self.weapon_stats:
            if self.exp_dmg(item) > self.exp_dmg(self.equipped_weapon): self.equipped_weapon = item
        elif item in self.armour_stats:
            if self.armour_stats[item]["red"] > self.armour_stats[self.equipped_armour]["red"]: self.equipped_armour = item

    def fmt_item(self, item): return item.replace('_', ' ').title()

    def item_info(self, item):
        if item in self.weapon_stats:
            s = self.weapon_stats[item]
            stats = f"DMG {s['dmg']}" + (f" | Crit {int(s['crit']*100)}%→{s['crit_dmg']}" if s["crit"] else "")
            return s["tier"], "Weapon", stats
        s = self.armour_stats[item]
        return s["tier"], "Armour", f"DEF -{s['red']:g}/hit"

    def tier_tag(self, tier):
        if tier >= 8: return "mythic"
        if tier >= 7: return "legendary"
        if tier >= 5: return "epic"
        if tier >= 3: return "rare"
        return "common"

    # ================= HANDS =================
    def draw_hand(self, c, x, y, angle, tag):
        dx, dy = math.cos(angle), math.sin(angle)
        px, py = -dy, dx
        skin, line = "#e8b088", "#c48a62"
        sx, sy = x - dx*22, y - dy*22
        c.create_oval(sx-11, sy-11, sx+11, sy+11, fill="#7a4a2a", outline="", tags=tag)
        c.create_oval(x-14, y-12, x+14, y+12, fill=skin, outline=line, width=1, tags=tag)
        for off in (-10, -3.5, 3.5, 10):
            fxp = x + dx*20 + px*off
            fyp = y + dy*20 + py*off
            c.create_oval(fxp-4, fyp-7, fxp+4, fyp+7, fill=skin, outline=line, width=1, tags=tag)
        tx, ty = x + dx*6 - px*16, y + dy*6 - py*16
        c.create_oval(tx-6, ty-5, tx+6, ty+5, fill=skin, outline=line, width=1, tags=tag)

    def hand_loop(self):
        c = self.click_btn
        if self.inventory.get("miss_bailey_handshake", 0) > 0:
            self.hand_angle = (self.hand_angle + 0.12) % (2 * math.pi)
            c.delete("hands")
            for i in range(8):
                a = self.hand_angle + i * (2 * math.pi / 8)
                self.draw_hand(c, 250 + 218*math.cos(a), 250 + 218*math.sin(a), a + math.pi, "hands")
        else:
            c.delete("hands")
        self.root.after(120, self.hand_loop)

    # ================= UI =================
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Professional Notebook Styling
        style.configure('TNotebook', background=self.colors["bg_main"], borderwidth=0)
        style.configure('TNotebook.Tab', background=self.colors["bg_panel"], foreground=self.colors["text_muted"], 
                       padding=[12, 6], font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', self.colors["accent"])], 
                 foreground=[('selected', '#ffffff')])
        
        # Frame & Label Styling
        style.configure('TFrame', background=self.colors["bg_main"])
        style.configure('TLabel', background=self.colors["bg_main"], foreground=self.colors["text_main"], 
                       font=('Segoe UI', 10))
        
        # Progressbar Styling
        style.configure('Green.Horizontal.TProgressbar', troughcolor=self.colors["bg_input"], 
                       background=self.colors["success"], thickness=8, borderwidth=0)
        style.configure('Red.Horizontal.TProgressbar', troughcolor=self.colors["bg_input"], 
                       background=self.colors["danger"], thickness=8, borderwidth=0)
        
        # Combobox & Treeview Styling
        style.configure('TCombobox', fieldbackground=self.colors["bg_input"], background=self.colors["bg_panel"], 
                       foreground=self.colors["text_main"], arrowcolor=self.colors["accent"], font=('Segoe UI', 10))
        style.map('TCombobox', fieldbackground=[('readonly', self.colors["bg_input"])])
        
        style.configure('Treeview', background=self.colors["bg_panel"], fieldbackground=self.colors["bg_panel"], 
                       foreground=self.colors["text_main"], rowheight=22, font=('Segoe UI', 10))
        style.configure('Treeview.Heading', background=self.colors["bg_input"], foreground=self.colors["text_main"], 
                       font=('Segoe UI', 10, 'bold'))
        style.map('Treeview', background=[('selected', self.colors["accent"])], foreground=[('selected', '#ffffff')])
        
        self.root.option_add("*TCombobox*Listbox.background", self.colors["bg_panel"])
        self.root.option_add("*TCombobox*Listbox.foreground", self.colors["text_main"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.colors["accent"])

        main_frame = tk.Frame(self.root, bg=self.colors["bg_main"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.main_frame = main_frame

        # Left Panel (Dashboard)
        left = tk.Frame(main_frame, bg=self.colors["bg_main"], width=540)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)
        self.left_frame = left

        # Right Panel (Tabs)
        right = tk.Frame(main_frame, bg=self.colors["bg_main"])
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.right_frame = right

        # --- Dashboard Header ---
        hdr = tk.Frame(left, bg=self.colors["bg_panel"], padx=12, pady=10)
        hdr.pack(fill=tk.X, pady=(0, 10))
        self.goybucks_label = tk.Label(hdr, text="0 goybucks", font=("Segoe UI", 20, "bold"), 
                                      fg=self.colors["gold"], bg=self.colors["bg_panel"])
        self.goybucks_label.pack()
        self.ic_hud_label = tk.Label(hdr, text="0 🪙 Israelcoins", font=("Segoe UI", 12, "bold"), 
                                    fg=self.colors["accent"], bg=self.colors["bg_panel"])
        self.ic_hud_label.pack()

        # --- Stats Row ---
        row2 = tk.Frame(left, bg=self.colors["bg_main"])
        row2.pack(fill=tk.X, padx=4, pady=(0, 8))
        self.cps_label = tk.Label(row2, text="0.0 gps", font=("Segoe UI", 10), fg=self.colors["text_muted"], bg=self.colors["bg_main"])
        self.cps_label.grid(row=0, column=0, sticky="w")
        self.cpc_label = tk.Label(row2, text="1 gpc", font=("Segoe UI", 10), fg=self.colors["text_muted"], bg=self.colors["bg_main"])
        self.cpc_label.grid(row=0, column=1, sticky="w", padx=16)
        self.level_label = tk.Label(row2, text="⭐ Lv 1 (0/50 xp)", font=("Segoe UI", 10, "bold"), 
                                   fg=self.colors["accent"], bg=self.colors["bg_main"])
        self.level_label.grid(row=0, column=2, sticky="e")
        row2.columnconfigure(0, weight=1); row2.columnconfigure(1, weight=1); row2.columnconfigure(2, weight=1)

        self.xp_bar = ttk.Progressbar(left, style="Green.Horizontal.TProgressbar", mode='determinate', maximum=50, value=0)
        self.xp_bar.pack(fill=tk.X, padx=4, pady=(0, 10))

        # --- Combat Stats Card ---
        stats_card = tk.Frame(left, bg=self.colors["bg_panel"], padx=10, pady=8)
        stats_card.pack(fill=tk.X, pady=(0, 10))
        self.stats_label = tk.Label(stats_card, text="HP 20/20 | ATK 1 | DEF 0 | Boss +0.0%", 
                                   font=("Segoe UI", 10), fg=self.colors["text_main"], bg=self.colors["bg_panel"], anchor="w")
        self.stats_label.pack(fill=tk.X)
        self.multiplier_label = tk.Label(stats_card, text="Multiplier: 1x (10 CPS → 2x)", 
                                        font=("Segoe UI", 10, "bold"), fg=self.colors["danger"], bg=self.colors["bg_panel"], anchor="w")
        self.multiplier_label.pack(fill=tk.X, pady=(4, 0))

        self.prestige_btn = tk.Button(left, text="REBIRTH", command=self.prestige, bg=self.colors["accent"], 
                                     fg="white", font=("Segoe UI", 11, "bold"), state=tk.DISABLED, relief=tk.FLAT, cursor="hand2", bd=0)
        self.prestige_btn.pack(fill=tk.X, padx=4, pady=(0, 10), ipady=4)

        # --- Main Click Canvas ---
        self.click_btn = tk.Canvas(left, width=520, height=520, bg=self.colors["bg_panel"], 
                                  highlightthickness=2, highlightbackground=self.colors["accent"])
        self.click_btn.pack(pady=(0, 10))
        self.click_btn.bind("<Button-1>", lambda e: self.click())
        self.draw_icon()

        # --- Tabs ---
        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.tab_upgrades = ttk.Frame(self.notebook)
        self.tab_crates = ttk.Frame(self.notebook)
        self.tab_inventory = ttk.Frame(self.notebook)
        self.tab_gamble = ttk.Frame(self.notebook)
        self.tab_adventure = ttk.Frame(self.notebook)
        self.tab_achievements = ttk.Frame(self.notebook)
        self.tab_skilltree = ttk.Frame(self.notebook)
        self.tab_stages = ttk.Frame(self.notebook)
        self.tab_boosts = ttk.Frame(self.notebook)
        self.tab_spells = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_upgrades, text="Upgrades")
        self.notebook.add(self.tab_crates, text="Crates")
        self.notebook.add(self.tab_inventory, text="Inventory")
        self.notebook.add(self.tab_gamble, text="Gamble")
        self.notebook.add(self.tab_adventure, text="Adventure")
        self.notebook.add(self.tab_achievements, text="Feats")
        self.notebook.add(self.tab_skilltree, text="Skill Tree")
        self.notebook.add(self.tab_stages, text="Stages")
        self.notebook.add(self.tab_boosts, text="Boosts")
        self.notebook.add(self.tab_spells, text="Spells")

        self.setup_upgrades_tab()
        self.setup_crates_tab()
        self.setup_inventory_tab()
        self.setup_gamble_tab()
        self.setup_adventure_tab()
        self.setup_achievements_tab()
        self.setup_skilltree_tab()
        self.setup_stages_tab()
        self.setup_boosts_tab()
        self.setup_spells_tab()

        self.golden_btn = tk.Button(self.root, text="💰 GOLDEN GOYBUCK 💰", command=self.click_golden, 
                                   bg=self.colors["gold"], fg="#000", font=("Segoe UI", 12, "bold"), relief=tk.FLAT, bd=0)
        self.golden_active = False
        self.root.after(120, self.hand_loop)

    def tag_trees(self, *tvs):
        for tv in tvs:
            tv.tag_configure("mythic", foreground="#d946ef")
            tv.tag_configure("legendary", foreground="#f43f5e")
            tv.tag_configure("epic", foreground="#3b82f6")
            tv.tag_configure("rare", foreground="#eab308")
            tv.tag_configure("common", foreground=self.colors["text_main"])

    def setup_upgrades_tab(self):
        tk.Label(self.tab_upgrades, text="⚔ UPGRADES", font=("Segoe UI", 14, "bold"), 
                fg=self.colors["gold"], bg=self.colors["bg_main"]).pack(pady=(10, 10))
        self.upgrade_buttons = {}
        for name in self.upgrades:
            frame = tk.Frame(self.tab_upgrades, bg=self.colors["bg_panel"], padx=10, pady=4)
            frame.pack(fill=tk.X, pady=3, padx=10)
            btn = tk.Button(frame, text=f"{name} [0]", command=lambda n=name: self.buy_upgrade(n),
                           bg=self.colors["bg_input"], fg=self.colors["text_main"], font=("Segoe UI", 10, "bold"), 
                           relief=tk.FLAT, cursor="hand2", bd=0)
            btn.pack(side=tk.LEFT, ipady=3, ipadx=8)
            info = tk.Label(frame, text="", fg=self.colors["text_muted"], bg=self.colors["bg_panel"], font=("Segoe UI", 9))
            info.pack(side=tk.RIGHT, padx=8)
            self.upgrade_buttons[name] = btn

    def setup_crates_tab(self):
        tk.Label(self.tab_crates, text="📦 CRATE SHOP", font=("Segoe UI", 14, "bold"), 
                fg=self.colors["gold"], bg=self.colors["bg_main"]).pack(pady=(10, 10))
        body = tk.Frame(self.tab_crates, bg=self.colors["bg_main"])
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.crate_tv = ttk.Treeview(body, columns=("Cost",), show=("tree", "headings"), height=8, selectmode="browse")
        self.crate_tv.heading("#0", text="Crate"); self.crate_tv.heading("Cost", text="Cost (gb)")
        self.crate_tv.column("#0", width=120); self.crate_tv.column("Cost", width=90)
        self.crate_tv.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        for name, cr in self.crates.items():
            self.crate_tv.insert("", "end", iid=name, text=name, values=(f"{cr['cost']:,}",))
        self.loot_tv = ttk.Treeview(body, columns=("Chance", "Type", "Stats"), show=("tree", "headings"), height=8)
        self.loot_tv.heading("#0", text="Loot"); self.loot_tv.heading("Chance", text="%")
        self.loot_tv.heading("Type", text="Type"); self.loot_tv.heading("Stats", text="Stats")
        self.loot_tv.column("#0", width=130); self.loot_tv.column("Chance", width=45)
        self.loot_tv.column("Type", width=55); self.loot_tv.column("Stats", width=150)
        self.loot_tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tag_trees(self.crate_tv, self.loot_tv)
        self.crate_tv.bind("<<TreeviewSelect>>", lambda e: self.show_crate_loot())
        bottom = tk.Frame(self.tab_crates, bg=self.colors["bg_main"])
        bottom.pack(fill=tk.X, padx=10, pady=5)
        self.buy_crate_btn = tk.Button(bottom, text="BUY SELECTED", command=self.buy_selected_crate,
                                      bg=self.colors["accent"], fg="white", font=("Segoe UI", 11, "bold"), 
                                      relief=tk.FLAT, cursor="hand2", bd=0)
        self.buy_crate_btn.pack(side=tk.LEFT, ipadx=12, ipady=4)
        self.crate_result = tk.Label(bottom, text="", font=("Segoe UI", 10, "bold"), 
                                    fg=self.colors["gold"], bg=self.colors["bg_main"], anchor="w")
        self.crate_result.pack(side=tk.LEFT, padx=12, fill=tk.X, expand=True)
        self.crate_tv.selection_set("Wooden Crate")
        self.show_crate_loot()

    def setup_inventory_tab(self):
        self.inv_equipped_label = tk.Label(self.tab_inventory, text="", font=("Segoe UI", 11, "bold"), 
                                          fg=self.colors["gold"], bg=self.colors["bg_main"])
        self.inv_equipped_label.pack(pady=(10, 5))
        cols = ("Count", "Type", "Stats", "Status")
        self.inv_tv = ttk.Treeview(self.tab_inventory, columns=cols, show=("tree", "headings"), height=16)
        for cid, wdt in zip(("#0",) + cols, (160, 45, 55, 180, 70)):
            self.inv_tv.column(cid, width=wdt)
        self.inv_tv.heading("#0", text="Item"); self.inv_tv.heading("Count", text="Qty")
        self.inv_tv.heading("Type", text="Type"); self.inv_tv.heading("Stats", text="Stats"); self.inv_tv.heading("Status", text="Status")
        sb = ttk.Scrollbar(self.tab_inventory, orient="vertical", command=self.inv_tv.yview)
        self.inv_tv.configure(yscrollcommand=sb.set)
        self.inv_tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=5)
        sb.pack(side=tk.LEFT, fill=tk.Y, pady=5)
        self.tag_trees(self.inv_tv)
        side = tk.Frame(self.tab_inventory, bg=self.colors["bg_main"])
        side.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        self.inv_action_btn = tk.Button(side, text="EQUIP / USE", command=self.handle_inv_action, 
                                       bg=self.colors["success"], fg="white", font=("Segoe UI", 10, "bold"), 
                                       relief=tk.FLAT, cursor="hand2", bd=0)
        self.inv_action_btn.pack(fill=tk.X, ipady=4)
        self.inv_bonus_label = tk.Label(side, text="", font=("Segoe UI", 10, "bold"), 
                                       fg=self.colors["warning"], bg=self.colors["bg_main"], justify="left")
        self.inv_bonus_label.pack(pady=10)

    def setup_gamble_tab(self):
        tk.Label(self.tab_gamble, text=" GAMBLE — 30% +1 tier | 2% +2 tiers | 68% lost", 
                font=("Segoe UI", 12, "bold"), fg=self.colors["gold"], bg=self.colors["bg_main"]).pack(pady=(10, 10))
        row = tk.Frame(self.tab_gamble, bg=self.colors["bg_main"]); row.pack(pady=5)
        tk.Label(row, text="Item:", fg=self.colors["text_muted"], bg=self.colors["bg_main"], font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.gamble_combo = ttk.Combobox(row, state="readonly", width=30, font=("Segoe UI", 10))
        self.gamble_combo.pack(side=tk.LEFT)
        self.gamble_combo.bind("<<ComboboxSelected>>", lambda e: self.update_gamble_preview())
        self.gamble_preview = tk.Label(self.tab_gamble, text="", font=("Segoe UI", 10), 
                                      fg=self.colors["accent"], bg=self.colors["bg_main"], justify="left")
        self.gamble_preview.pack(pady=5)
        self.gamble_result = tk.Label(self.tab_gamble, text="", font=("Segoe UI", 11, "bold"), 
                                     fg=self.colors["gold"], bg=self.colors["bg_main"])
        self.gamble_result.pack(pady=5)
        tk.Button(self.tab_gamble, text="🎲 GAMBLE (consumes 1)", command=self.do_gamble,
                 bg=self.colors["danger"], fg="white", font=("Segoe UI", 11, "bold"), 
                 relief=tk.FLAT, cursor="hand2", bd=0).pack(pady=8, ipadx=15, ipady=4)

    def setup_adventure_tab(self):
        eq = tk.Frame(self.tab_adventure, bg=self.colors["bg_main"]); eq.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(eq, text="Weapon:", fg=self.colors["text_muted"], bg=self.colors["bg_main"], font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.adv_wcombo = ttk.Combobox(eq, state="readonly", width=20, font=("Segoe UI", 10))
        self.adv_wcombo.pack(side=tk.LEFT, padx=5)
        tk.Label(eq, text="Armour:", fg=self.colors["text_muted"], bg=self.colors["bg_main"], font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.adv_acombo = ttk.Combobox(eq, state="readonly", width=20, font=("Segoe UI", 10))
        self.adv_acombo.pack(side=tk.LEFT, padx=5)
        self.adv_wcombo.bind("<<ComboboxSelected>>", lambda e: self.set_weapon(self._wmap.get(self.adv_wcombo.get(), self.equipped_weapon)))
        self.adv_acombo.bind("<<ComboboxSelected>>", lambda e: self.set_armour(self._amap.get(self.adv_acombo.get(), self.equipped_armour)))
        self.adv_stats = tk.Label(self.tab_adventure, text="", font=("Segoe UI", 10, "bold"), 
                                 fg=self.colors["gold"], bg=self.colors["bg_main"])
        self.adv_stats.pack(pady=5)
        cols = ("HP", "ATK", "Reward", "XP", "Wins", "Status")
        self.boss_tv = ttk.Treeview(self.tab_adventure, columns=cols, show=("tree", "headings"), height=8)
        for cid, wdt in zip(("#0",) + cols, (110, 50, 45, 90, 50, 40, 130)):
            self.boss_tv.column(cid, width=wdt)
        self.boss_tv.heading("#0", text="Boss"); self.boss_tv.heading("HP", text="HP"); self.boss_tv.heading("ATK", text="ATK")
        self.boss_tv.heading("Reward", text="Gold"); self.boss_tv.heading("XP", text="XP")
        self.boss_tv.heading("Wins", text="Wins"); self.boss_tv.heading("Status", text="Status")
        self.boss_tv.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        tk.Button(self.tab_adventure, text=" FIGHT SELECTED", command=self.fight_selected,
                 bg=self.colors["danger"], fg="white", font=("Segoe UI", 11, "bold"), 
                 relief=tk.FLAT, cursor="hand2", bd=0).pack(pady=5, ipadx=15, ipady=4)

    def setup_achievements_tab(self):
        tk.Label(self.tab_achievements, text=" ACHIEVEMENTS (+5% CPS each)", font=("Segoe UI", 14, "bold"), 
                fg=self.colors["gold"], bg=self.colors["bg_main"]).pack(pady=(10, 10))
        self.ach_labels = {}
        for name in self.achievements:
            lbl = tk.Label(self.tab_achievements, text=f"🔒 {name}", font=("Segoe UI", 10), 
                          fg=self.colors["text_muted"], bg=self.colors["bg_main"], anchor="w")
            lbl.pack(fill=tk.X, padx=15, pady=2)
            self.ach_labels[name] = lbl

    def setup_skilltree_tab(self):
        tk.Label(self.tab_skilltree, text="🌳 SKILL TREE", font=("Segoe UI", 14, "bold"), 
                fg=self.colors["gold"], bg=self.colors["bg_main"]).pack(pady=(10, 10))
        self.ic_label = tk.Label(self.tab_skilltree, text=f"Israelcoins: 0", font=("Segoe UI", 12, "bold"), 
                                fg=self.colors["accent"], bg=self.colors["bg_main"])
        self.ic_label.pack()
        self.skill_labels = {}
        for name, data in self.skill_tree.items():
            f = tk.Frame(self.tab_skilltree, bg=self.colors["bg_panel"])
            f.pack(fill=tk.X, padx=15, pady=3)
            tk.Label(f, text=f"{name} | {data['desc']} | Cost: {data['cost']} IC", 
                    font=("Segoe UI", 10), fg=self.colors["text_main"], bg=self.colors["bg_panel"], justify="left").pack(side=tk.LEFT)
            btn = tk.Button(f, text="UNLOCK" if not data["bought"] else "UNLOCKED", command=lambda n=name: self.buy_skill(n),
                           bg=self.colors["bg_input"] if not data["bought"] else self.colors["success"], 
                           fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                           state=tk.DISABLED if data["bought"] else tk.NORMAL, bd=0)
            btn.pack(side=tk.RIGHT, ipadx=10, ipady=3)
            self.skill_labels[name] = btn

    def setup_stages_tab(self):
        tk.Label(self.tab_stages, text="🏟 STAGES", font=("Segoe UI", 14, "bold"), 
                fg=self.colors["gold"], bg=self.colors["bg_main"]).pack(pady=(10, 10))
        self.stage_buttons = {}
        for name, st in self.stages.items():
            f = tk.Frame(self.tab_stages, bg=self.colors["bg_panel"])
            f.pack(fill=tk.X, padx=15, pady=3)
            color_box = tk.Canvas(f, width=28, height=28, bg=st["bg"], highlightthickness=1, highlightbackground=self.colors["text_muted"])
            color_box.pack(side=tk.LEFT, padx=5)
            tk.Label(f, text=f"{name} | CPS: x{st['cps_mult']} | CPC: x{st['cpc_mult']} | Cost: {st['cost']} IC", 
                    font=("Segoe UI", 10), fg=self.colors["text_main"], bg=self.colors["bg_panel"], justify="left").pack(side=tk.LEFT)
            btn_text = "EQUIP" if st["unlocked"] else f"UNLOCK ({st['cost']} IC)"
            btn = tk.Button(f, text=btn_text, command=lambda n=name: self.handle_stage(n),
                           bg=self.colors["bg_input"] if not st["unlocked"] else self.colors["success"], 
                           fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, bd=0)
            btn.pack(side=tk.RIGHT, ipadx=10, ipady=3)
            self.stage_buttons[name] = btn

    def setup_boosts_tab(self):
        tk.Label(self.tab_boosts, text="💊 BOOSTS", font=("Segoe UI", 14, "bold"), 
                fg=self.colors["gold"], bg=self.colors["bg_main"]).pack(pady=(10, 10))
        self.boost_buttons = {}
        self.boost_timers = {}
        for name, b in self.boosts.items():
            f = tk.Frame(self.tab_boosts, bg=self.colors["bg_panel"])
            f.pack(fill=tk.X, padx=15, pady=3)
            tk.Label(f, text=f"{name} | {b['desc']} | Cost: {b['cost']:,} gb | Dur: {b['duration']}s", 
                    font=("Segoe UI", 10), fg=self.colors["text_main"], bg=self.colors["bg_panel"], justify="left").pack(side=tk.LEFT)
            timer_lbl = tk.Label(f, text="", font=("Segoe UI", 10, "bold"), fg=self.colors["accent"], bg=self.colors["bg_panel"])
            timer_lbl.pack(side=tk.RIGHT, padx=10)
            btn = tk.Button(f, text="ACTIVATE", command=lambda n=name: self.activate_boost(n),
                           bg=self.colors["danger"], fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, bd=0)
            btn.pack(side=tk.RIGHT, ipadx=10, ipady=3)
            self.boost_buttons[name] = btn
            self.boost_timers[name] = timer_lbl

    def setup_spells_tab(self):
        tk.Label(self.tab_spells, text="✨ ENCHANTMENT SPELLS", font=("Segoe UI", 14, "bold"), 
                fg=self.colors["gold"], bg=self.colors["bg_main"]).pack(pady=(10, 10))
        cols = ("Type", "Effect", "Cost", "Owned")
        self.spell_tv = ttk.Treeview(self.tab_spells, columns=cols, show=("tree", "headings"), height=14)
        self.spell_tv.heading("#0", text="Spell Name")
        self.spell_tv.heading("Type", text="Type")
        self.spell_tv.heading("Effect", text="Effect")
        self.spell_tv.heading("Cost", text="Cost (gb)")
        self.spell_tv.heading("Owned", text="Owned")
        self.spell_tv.column("#0", width=120)
        self.spell_tv.column("Type", width=60)
        self.spell_tv.column("Effect", width=120)
        self.spell_tv.column("Cost", width=80)
        self.spell_tv.column("Owned", width=50)
        
        sb = ttk.Scrollbar(self.tab_spells, orient="vertical", command=self.spell_tv.yview)
        self.spell_tv.configure(yscrollcommand=sb.set)
        self.spell_tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=5)
        sb.pack(side=tk.LEFT, fill=tk.Y, pady=5)
        self.tag_trees(self.spell_tv)
        
        side = tk.Frame(self.tab_spells, bg=self.colors["bg_main"])
        side.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        tk.Button(side, text="BUY SELECTED", command=self.buy_selected_spell, 
                 bg=self.colors["accent"], fg="white", font=("Segoe UI", 10, "bold"), 
                 relief=tk.FLAT, cursor="hand2", bd=0).pack(fill=tk.X, ipady=4)
        self.spell_info_lbl = tk.Label(side, text="Select a spell to buy", font=("Segoe UI", 9), 
                                      fg=self.colors["text_muted"], bg=self.colors["bg_main"], justify="left")
        self.spell_info_lbl.pack(pady=10)

    # ================= REFRESH =================
    def show_crate_loot(self):
        sel = self.crate_tv.selection()
        if not sel: return
        cr = self.crates[sel[0]]
        self.loot_tv.delete(*self.loot_tv.get_children())
        entries = cr["weighted"] if "weighted" in cr else [(it, 1.0/len(cr["loot"])) for it in cr["loot"]]
        for item, w in entries:
            if item in self.enchantments:
                self.loot_tv.insert("", "end", text=self.fmt_item(item), values=(f"{w*100:.0f}", "Spell", self.enchantments[item]['desc']), tags=("epic",))
            else:
                tier, typ, stats = self.item_info(item)
                self.loot_tv.insert("", "end", text=self.fmt_item(item), values=(f"{w*100:.0f}", typ, stats), tags=(self.tier_tag(tier),))

    def buy_selected_crate(self):
        sel = self.crate_tv.selection()
        if sel: self.buy_crate(sel[0])

    def refresh_inventory(self):
        self.inv_equipped_label.config(text=f"Equipped: {self.fmt_item(self.equipped_weapon)} | {self.fmt_item(self.equipped_armour)}")
        self.inv_tv.delete(*self.inv_tv.get_children())
        for w in self.weapon_stats:
            if w == "fists" or self.inventory.get(w, 0) <= 0: continue
            tier, typ, stats = self.item_info(w)
            enchants = self.item_enchants.get(w, {})
            if enchants: stats += " | " + ", ".join([f"{k} x{v}" for k, v in enchants.items()])
            self.inv_tv.insert("", "end", iid=w, text=self.fmt_item(w),
                               values=(self.inventory[w], typ, stats, "EQUIPPED" if w == self.equipped_weapon else ""),
                               tags=(self.tier_tag(tier),))
        for a in self.armour_stats:
            if a == "none" or self.inventory.get(a, 0) <= 0: continue
            tier, typ, stats = self.item_info(a)
            enchants = self.item_enchants.get(a, {})
            if enchants: stats += " | " + ", ".join([f"{k} x{v}" for k, v in enchants.items()])
            self.inv_tv.insert("", "end", iid=a, text=self.fmt_item(a),
                               values=(self.inventory[a], typ, stats, "EQUIPPED" if a == self.equipped_armour else ""),
                               tags=(self.tier_tag(tier),))
        for spell, count in self.spell_inventory.items():
            if count > 0:
                self.inv_tv.insert("", "end", iid=f"spell_{spell}", text=self.fmt_item(spell),
                                   values=(count, "Spell", self.enchantments[spell]['type'].title(), "CLICK TO USE"),
                                   tags=("epic",))
        self.inv_bonus_label.config(text=f"Boss Win Bonus:\n+{sum(self.bosses_defeated.values())*0.5:.1f}% DMG")

    def handle_inv_action(self):
        sel = self.inv_tv.selection()
        if not sel: return
        item = sel[0]
        if item.startswith("spell_"):
            self.use_spell(item[6:])
        else:
            if item in self.weapon_stats and item != "fists": self.equipped_weapon = item
            elif item in self.armour_stats and item != "none": self.equipped_armour = item
            else: return
            self.refresh_all_tabs(); self.update_display()

    def use_spell(self, spell_name):
        if self.spell_inventory.get(spell_name, 0) <= 0: return
        spell = self.enchantments[spell_name]
        target_type = spell["type"]
        
        if target_type == "weapon":
            targets = [w for w in self.weapon_stats if w != "fists" and self.inventory.get(w, 0) > 0]
        else:
            targets = [a for a in self.armour_stats if a != "none" and self.inventory.get(a, 0) > 0]
            
        if not targets:
            self.crate_result.config(text=f"No valid {target_type}s to enchant!", fg=self.colors["danger"])
            return
            
        popup = tk.Toplevel(self.root)
        popup.title(f"Enchant with {self.fmt_item(spell_name)}")
        popup.geometry("340x200")
        popup.configure(bg=self.colors["bg_panel"])
        
        tk.Label(popup, text=f"Select {target_type} to enchant:", bg=self.colors["bg_panel"], 
                fg=self.colors["text_main"], font=("Segoe UI", 11, "bold")).pack(pady=10)
        
        combo = ttk.Combobox(popup, values=[self.fmt_item(t) for t in targets], state="readonly", font=("Segoe UI", 10))
        combo.pack(pady=5)
        combo.set(self.fmt_item(targets[0]))
        
        self._spell_target_map = {self.fmt_item(t): t for t in targets}
        
        def apply():
            selected = self._spell_target_map.get(combo.get(), targets[0])
            self.apply_enchantment(spell_name, selected)
            popup.destroy()
            
        tk.Button(popup, text="Apply Enchantment", command=apply, bg=self.colors["accent"], 
                 fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, bd=0).pack(pady=10)

    def apply_enchantment(self, spell_name, target):
        self.spell_inventory[spell_name] -= 1
        self.item_enchants[target][spell_name] = self.item_enchants[target].get(spell_name, 0) + 1
        self.refresh_all_tabs()
        self.update_display()

    def refresh_gamble(self):
        candidates = [self.fmt_item(k) for k in self.gamble_paths if self.inventory.get(k, 0) > 0 and self.gamble_paths[k][0] is not None]
        self._gmap = {self.fmt_item(k): k for k in self.gamble_paths if self.inventory.get(k, 0) > 0 and self.gamble_paths[k][0] is not None}
        self.gamble_combo["values"] = candidates
        if self.gamble_combo.get() not in candidates:
            self.gamble_combo.set(candidates[0] if candidates else "")
        self.update_gamble_preview()

    def update_gamble_preview(self):
        key = self._gmap.get(self.gamble_combo.get())
        if not key:
            self.gamble_preview.config(text="Nothing to gamble — win or buy some gear first!")
            return
        plus1, plus2 = self.gamble_paths[key]
        text = f"You own: {self.fmt_item(key)} x{self.inventory[key]}\n30% → {self.fmt_item(plus1)}"
        if plus2 and plus2 != plus1: text += f"\n2%  → {self.fmt_item(plus2)}"
        text += "\n68% → lost"
        self.gamble_preview.config(text=text)

    def refresh_adventure(self):
        weapons = [w for w in self.weapon_stats if w == "fists" or self.inventory.get(w, 0) > 0]
        armours = [a for a in self.armour_stats if a == "none" or self.inventory.get(a, 0) > 0]
        self._wmap = {self.fmt_item(w): w for w in weapons}
        self._amap = {self.fmt_item(a): a for a in armours}
        self.adv_wcombo["values"] = list(self._wmap); self.adv_wcombo.set(self.fmt_item(self.equipped_weapon))
        self.adv_acombo["values"] = list(self._amap); self.adv_acombo.set(self.fmt_item(self.equipped_armour))
        self.adv_stats.config(text=f"Lv {self.level} | HP {int(self.player_hp)}/{self.get_max_hp()} | ATK {self.get_attack():.1f} | DEF {self.get_armour():g} | Boss +{sum(self.bosses_defeated.values())*0.5:.1f}%")
        self.boss_tv.delete(*self.boss_tv.get_children())
        for name, b in self.bosses.items():
            unlocked = self.level >= b["req_level"] and (b["req_boss"] is None or self.bosses_defeated.get(b["req_boss"], 0) > 0)
            status = "READY" if unlocked else f"Lv{b['req_level']}" + (f"+{b['req_boss']}" if b["req_boss"] else "")
            self.boss_tv.insert("", "end", iid=name, text=name,
                                values=(b["hp"], b["atk"], f"{b['gold']:,}", b["xp"], self.bosses_defeated[name], status))

    def fight_selected(self):
        sel = self.boss_tv.selection()
        if not sel: return
        name = sel[0]
        b = self.bosses[name]
        if self.level >= b["req_level"] and (b["req_boss"] is None or self.bosses_defeated.get(b["req_boss"], 0) > 0):
            self.start_bossfight(name)

    def refresh_skilltree(self):
        self.ic_label.config(text=f"Israelcoins: {self.israelcoins}")
        for name, data in self.skill_tree.items():
            btn = self.skill_labels[name]
            if data["bought"]:
                btn.config(text="UNLOCKED", bg=self.colors["success"], state=tk.DISABLED)
            else:
                if self.israelcoins >= data["cost"]:
                    btn.config(text=f"UNLOCK ({data['cost']} IC)", bg=self.colors["bg_input"], state=tk.NORMAL)
                else:
                    btn.config(text=f"UNLOCK ({data['cost']} IC)", bg=self.colors["bg_input"], state=tk.DISABLED)

    def refresh_stages(self):
        for name, st in self.stages.items():
            btn = self.stage_buttons[name]
            if st["unlocked"]:
                if name == self.current_stage:
                    btn.config(text="EQUIPPED", bg=self.colors["danger"], state=tk.DISABLED)
                else:
                    btn.config(text="EQUIP", bg=self.colors["success"], state=tk.NORMAL)
            else:
                if self.israelcoins >= st["cost"]:
                    btn.config(text=f"UNLOCK ({st['cost']} IC)", bg=self.colors["bg_input"], state=tk.NORMAL)
                else:
                    btn.config(text=f"UNLOCK ({st['cost']} IC)", bg=self.colors["bg_input"], state=tk.DISABLED)

    def refresh_spells(self):
        self.spell_tv.delete(*self.spell_tv.get_children())
        for name, data in self.enchantments.items():
            owned = self.spell_inventory.get(name, 0)
            self.spell_tv.insert("", "end", iid=name, text=self.fmt_item(name), 
                                 values=(data['type'].title(), data['desc'], f"{data['cost']:,}", owned),
                                 tags=("epic",))

    def refresh_all_tabs(self):
        self.refresh_inventory()
        self.refresh_gamble()
        self.refresh_adventure()
        self.refresh_skilltree()
        self.refresh_stages()
        self.refresh_spells()

    def refresh_upgrades(self):
        for name, upg in self.upgrades.items():
            self.upgrade_buttons[name].config(text=f"{name} [{upg['count']}]")
            stat_text = ""
            if upg.get('cpc', 0) > 0: stat_text += f"+{upg['cpc']} gpc "
            if upg.get('cps', 0) > 0: stat_text += f"+{upg['cps']} gps"
            info_label = self.upgrade_buttons[name].master.winfo_children()[1]
            info_label.config(text=f"Cost: {upg['cost']:,} | {stat_text}")

    # ================= BILL ART =================
    def draw_icon(self):
        c = self.click_btn
        w, h = 520, 520
        self.draw_bill_base(c, w, h)
        self.draw_guilloche_patterns(c, w, h)
        self.draw_bill_text_and_borders(c, w, h)
        self.draw_detailed_seals(c, w, h)
        c.create_polygon(130, 280, 270, 280, 290, 420, 110, 420, fill="#000000", stipple="gray25")
        c.create_polygon(30, 320, 170, 320, 190, 420, 10, 420, fill="#000000", stipple="gray25")
        c.create_polygon(230, 310, 370, 310, 390, 420, 210, 420, fill="#000000", stipple="gray25")
        self.draw_middle_man(c)
        self.draw_left_boy(c)
        self.draw_right_boy(c)

    def draw_bill_base(self, c, w, h):
        c.create_rectangle(0, 0, w, h, fill="#85bb65")
        for _ in range(500):
            x, y = random.randint(0, w), random.randint(0, h)
            c.create_rectangle(x, y, x+2, y+2, fill="#7aaf5a", outline="")

    def draw_guilloche_patterns(self, c, w, h):
        colors = ["#7aaf5a", "#90c070", "#6a9c52"]
        for i in range(0, w, 40):
            for j in range(0, h, 40):
                cx, cy = i + 20, j + 20
                for r in range(10, 30, 5):
                    c.create_oval(cx-r, cy-r, cx+r, cy+r, outline=colors[(i+j)//40 % 3], width=1)

    def draw_bill_text_and_borders(self, c, w, h):
        c.create_rectangle(10, 10, w-10, h-10, outline="#1a472a", width=4)
        c.create_rectangle(15, 15, w-15, h-15, outline="#2e5c2e", width=2)
        c.create_rectangle(20, 20, w-20, h-20, outline="#4a7c4e", width=1, dash=(4, 4))
        for x, y in [(40, 45), (w-40, 45), (40, h-30), (w-40, h-30)]:
            c.create_oval(x-15, y-15, x+15, y+15, outline="#1a472a", width=2)
            c.create_text(x, y, text="1", font=("Times", 18, "bold"), fill="#1a472a")
        c.create_text(w/2, 35, text="THE UNITED GOYIMS OF AMERICA", font=("Times", 14, "bold"), fill="#1a472a")
        c.create_text(w/2, 55, text="ONE GOYBUCK", font=("Times", 20, "bold"), fill="#1a472a")
        c.create_text(w/2, h-20, text="IN GOYS WE TRUST", font=("Times", 14, "bold"), fill="#1a472a")
        c.create_text(w/2, 75, text="FEDERAL RESERVE NOTE", font=("Times", 10), fill="#2e5c2e")
        c.create_text(80, 100, text="G0Y333IQQ", font=("Courier", 12, "bold"), fill="#1a472a")
        c.create_text(w-80, h-100, text="G0Y333IQQ", font=("Courier", 12, "bold"), fill="#1a472a")

    def draw_detailed_seals(self, c, w, h):
        cx, cy = 100, 250
        c.create_oval(cx-40, cy-40, cx+40, cy+40, fill="#5a8c42", outline="#1a472a", width=2)
        c.create_oval(cx-30, cy-30, cx+30, cy+30, outline="#1a472a", width=1)
        c.create_text(cx, cy, text="G", font=("Times", 30, "bold"), fill="#1a472a")
        for i in range(0, 360, 15):
            rad = math.radians(i)
            c.create_line(cx+35*math.cos(rad), cy+35*math.sin(rad), cx+42*math.cos(rad), cy+42*math.sin(rad), fill="#1a472a", width=2)
        cx, cy = w-100, 250
        for r in range(45, 35, -1):
            shade = int(100 + (45-r)*10)
            c.create_oval(cx-r, cy-r, cx+r, cy+r, fill=f"#{shade:02x}{shade:02x}{shade//2:02x}", outline="")
        c.create_oval(cx-35, cy-35, cx+35, cy+35, outline="#1a472a", width=2)
        c.create_polygon(cx, cy+25, cx-22, cy-12, cx+22, cy-12, fill="#0a2a1a")
        c.create_polygon(cx, cy-25, cx+22, cy+12, cx-22, cy+12, fill="#1a472a")
        c.create_polygon(cx, cy-20, cx+17, cy+9, cx-17, cy+9, fill="#2e5c2e")
        c.create_polygon(cx, cy+20, cx-17, cy-9, cx+17, cy-9, fill="#05150a")

    def draw_star(self, c, cx, cy, size, fill_color):
        c.create_polygon(cx, cy-size, cx+size*0.866, cy+size/2, cx-size*0.866, cy+size/2, fill=fill_color, outline="")
        c.create_polygon(cx, cy+size, cx-size*0.866, cy-size/2, cx+size*0.866, cy-size/2, fill=fill_color, outline="")

    def draw_nametag(self, c, x, y, w, h, text):
        c.create_rectangle(x, y, x+w, y+h, fill="#FFFFFF", outline="#CCCCCC", width=1)
        c.create_rectangle(x, y, x+w, y+5, fill="#E94560", outline="")
        c.create_oval(x+5, y+8, x+9, y+12, fill="#AAAAAA")
        c.create_oval(x+w-9, y+8, x+w-5, y+12, fill="#AAAAAA")
        c.create_text(x+w/2, y+h/2+3, text=text, font=("Arial", 8, "bold"), fill="#000000")

    def draw_middle_man(self, c):
        c.create_polygon(140, 280, 260, 280, 280, 420, 120, 420, fill="#2a2a2a")
        c.create_polygon(140, 280, 200, 280, 200, 420, 120, 420, fill="#1a1a1a")
        c.create_line(160, 300, 150, 380, fill="#111111", width=2)
        c.create_line(240, 300, 250, 380, fill="#3a3a3a", width=2)
        c.create_line(200, 290, 200, 400, fill="#111111", width=1)
        c.create_text(232, 342, text="P", font=("Arial", 28, "bold"), fill="#000000")
        c.create_text(230, 340, text="P", font=("Arial", 28, "bold"), fill="#ffffff")
        c.create_polygon(180, 240, 220, 240, 220, 290, 180, 290, fill="#dcb088")
        c.create_polygon(180, 240, 200, 240, 200, 290, 180, 290, fill="#c49a72")
        c.create_oval(195, 260, 205, 270, fill="#b88a62")
        c.create_polygon(180, 240, 220, 240, 210, 250, 190, 250, fill="#a07050")
        c.create_polygon(170, 150, 230, 150, 235, 200, 225, 250, 200, 260, 175, 250, 165, 200, fill="#f0c8a0")
        c.create_polygon(170, 150, 200, 150, 200, 260, 175, 250, 165, 200, fill="#dcb088")
        c.create_polygon(220, 180, 235, 200, 225, 230, 215, 210, fill="#f5d0b0")
        c.create_polygon(165, 140, 235, 140, 240, 160, 230, 150, 170, 150, 160, 160, fill="#4a3b32")
        c.create_polygon(165, 140, 200, 140, 200, 150, 170, 150, 160, 160, fill="#3a2b22")
        for i in range(30):
            x = random.randint(165, 235); y = random.randint(140, 155)
            c.create_line(x, y, x+random.randint(-5, 5), y+random.randint(5, 15), fill="#2a1b12", width=1)
        c.create_polygon(180, 142, 220, 142, 225, 148, 175, 148, fill="#5a4b42")
        c.create_arc(165, 120, 235, 160, start=0, extent=180, fill="#111111", outline="#000000", width=2)
        c.create_arc(165, 120, 235, 160, start=0, extent=180, fill="#222222")
        for _ in range(100):
            px = random.randint(170, 230); py = random.randint(125, 145)
            if (px-200)**2/30**2 + (py-140)**2/15**2 < 1: c.create_rectangle(px, py, px+1, py+1, fill="#333333", outline="")
        self.draw_star(c, 200, 135, 12, "#FFD700")
        c.create_rectangle(172, 185, 198, 205, outline="#111111", width=4, fill="#e0f0ff")
        c.create_rectangle(202, 185, 228, 205, outline="#111111", width=4, fill="#e0f0ff")
        c.create_rectangle(168, 192, 172, 198, fill="#111111")
        c.create_rectangle(228, 192, 232, 198, fill="#111111")
        c.create_line(198, 195, 202, 195, fill="#111111", width=3)
        c.create_line(172, 190, 160, 185, fill="#111111", width=4)
        c.create_line(228, 190, 240, 185, fill="#111111", width=4)
        c.create_polygon(174, 187, 185, 187, 178, 203, fill="#ffffff")
        c.create_polygon(187, 187, 195, 187, 188, 203, fill="#ffffff", stipple="gray50")
        c.create_polygon(204, 187, 215, 187, 208, 203, fill="#ffffff")
        c.create_polygon(217, 187, 225, 187, 218, 203, fill="#ffffff", stipple="gray50")
        c.create_oval(183, 192, 189, 198, fill="#5b8c5a")
        c.create_oval(213, 192, 219, 198, fill="#5b8c5a")
        c.create_oval(185, 193, 188, 197, fill="#000000")
        c.create_oval(215, 193, 218, 197, fill="#000000")
        c.create_polygon(175, 182, 195, 180, 195, 184, 175, 186, fill="#3a2b22")
        c.create_polygon(205, 180, 225, 182, 225, 186, 205, 184, fill="#3a2b22")
        c.create_polygon(195, 195, 205, 195, 205, 225, 200, 230, 195, 225, fill="#dcb088")
        c.create_line(195, 225, 205, 225, fill="#c49a72", width=2)
        c.create_polygon(185, 235, 215, 235, 210, 242, 190, 242, fill="#c47a6a")
        c.create_line(188, 238, 212, 238, fill="#8a4a3a", width=2)
        c.create_oval(160, 190, 172, 210, fill="#f0c8a0")
        c.create_oval(228, 190, 240, 210, fill="#dcb088")
        self.draw_nametag(c, 160, 300, 40, 20, "che")

    def draw_left_boy(self, c):
        c.create_polygon(40, 320, 160, 320, 180, 420, 20, 420, fill="#666666")
        c.create_polygon(40, 320, 100, 320, 100, 420, 20, 420, fill="#555555")
        for _ in range(40):
            sx, sy = random.randint(50, 150), random.randint(330, 410)
            c.create_oval(sx, sy, sx+3, sy+3, fill="#aaaaaa", outline="")
        c.create_polygon(80, 270, 120, 270, 120, 330, 80, 330, fill="#e0b89c")
        c.create_polygon(80, 270, 100, 270, 100, 330, 80, 330, fill="#c49a72")
        c.create_polygon(70, 180, 130, 180, 135, 230, 125, 280, 100, 290, 75, 280, 65, 230, fill="#f5d0b5")
        c.create_polygon(70, 180, 100, 180, 100, 290, 75, 280, 65, 230, fill="#e0b89c")
        c.create_polygon(65, 170, 135, 170, 140, 190, 130, 180, 70, 180, 60, 190, fill="#e8c985")
        c.create_polygon(65, 170, 100, 170, 100, 180, 70, 180, 60, 190, fill="#d4b46a")
        for i in range(50):
            x = random.randint(65, 135); y = random.randint(165, 185)
            c.create_line(x, y, x+random.randint(-3, 3), y+random.randint(5, 15), fill="#c0a050", width=1)
        c.create_arc(65, 150, 135, 190, start=0, extent=180, fill="#111111", outline="#000000", width=2)
        c.create_arc(65, 150, 135, 190, start=0, extent=180, fill="#2a2a2a")
        self.draw_star(c, 100, 165, 10, "#FFD700")
        c.create_oval(83, 212, 89, 219, fill="#7a9c9a")
        c.create_oval(113, 212, 119, 219, fill="#7a9c9a")
        c.create_oval(85, 213, 88, 218, fill="#000000")
        c.create_oval(115, 213, 118, 218, fill="#000000")
        c.create_polygon(95, 220, 105, 220, 105, 245, 100, 250, 95, 245, fill="#e0b89c")
        c.create_polygon(85, 260, 115, 260, 110, 266, 90, 266, fill="#c47a6a")
        c.create_oval(60, 215, 72, 235, fill="#f5d0b5")
        c.create_oval(128, 215, 140, 235, fill="#e0b89c")
        c.create_rectangle(110, 300, 114, 420, fill="#ffffff", outline="#cccccc", width=1)
        self.draw_nametag(c, 50, 340, 50, 20, "kyle bro")

    def draw_right_boy(self, c):
        c.create_polygon(240, 310, 360, 310, 380, 420, 220, 420, fill="#1a237e")
        c.create_polygon(240, 310, 300, 310, 300, 420, 220, 420, fill="#0f165e")
        c.create_line(300, 310, 300, 420, fill="#aaaaaa", width=3)
        c.create_rectangle(296, 350, 304, 365, fill="#aaaaaa", outline="#666666")
        c.create_polygon(280, 260, 320, 260, 320, 320, 280, 320, fill="#e0b89c")
        c.create_polygon(280, 260, 300, 260, 300, 320, 280, 320, fill="#c49a72")
        c.create_polygon(270, 170, 330, 170, 335, 220, 325, 270, 300, 280, 275, 270, 265, 220, fill="#f5d0b5")
        c.create_polygon(270, 170, 300, 170, 300, 280, 275, 270, 265, 220, fill="#e0b89c")
        c.create_polygon(265, 160, 335, 160, 340, 180, 330, 170, 270, 170, 260, 180, fill="#d4b46a")
        c.create_polygon(265, 160, 300, 160, 300, 170, 270, 170, 260, 180, fill="#c0a050")
        for i in range(50):
            x = random.randint(265, 335); y = random.randint(155, 175)
            c.create_line(x, y, x+random.randint(-3, 3), y+random.randint(5, 15), fill="#b09040", width=1)
        c.create_arc(265, 140, 335, 180, start=0, extent=180, fill="#111111", outline="#000000", width=2)
        c.create_arc(265, 140, 335, 180, start=0, extent=180, fill="#2a2a2a")
        self.draw_star(c, 300, 155, 10, "#FFD700")
        c.create_oval(283, 207, 289, 213, fill="#333333")
        c.create_oval(313, 207, 319, 213, fill="#333333")
        c.create_polygon(295, 215, 305, 215, 305, 240, 300, 245, 295, 240, fill="#e0b89c")
        c.create_polygon(280, 250, 320, 250, 310, 270, 290, 270, fill="#4a1a1a")
        c.create_polygon(282, 250, 318, 250, 315, 258, 285, 258, fill="#ffffff")
        c.create_polygon(290, 262, 310, 262, 305, 270, 295, 270, fill="#c45a5a")
        c.create_oval(260, 205, 272, 225, fill="#f5d0b5")
        c.create_oval(328, 205, 340, 225, fill="#e0b89c")
        c.create_rectangle(290, 290, 294, 420, fill="#ffffff", outline="#cccccc", width=1)
        self.draw_nametag(c, 245, 330, 50, 20, "my g")
        self.draw_nametag(c, 245, 352, 50, 20, "leader")

    # ================= CORE =================
    def click(self):
        self.clicks += 1
        earned = self.cpc * self.multiplier * self.get_prestige_mult() * self.get_ach_mult()
        self.goybucks += earned
        self.total_earned += earned
        self.gain_xp(1)
        self.check_achievements()
        self.update_display()

    def buy_upgrade(self, name):
        upg = self.upgrades[name]
        if self.goybucks >= upg["cost"]:
            self.goybucks -= upg["cost"]
            upg["count"] += 1
            upg["cost"] = math.ceil(upg["cost"] * 1.01)
            self.recalc_stats()
            self.check_achievements()
            self.update_display()

    def buy_selected_spell(self):
        sel = self.spell_tv.selection()
        if not sel: return
        name = sel[0]
        data = self.enchantments[name]
        if self.goybucks >= data["cost"]:
            self.goybucks -= data["cost"]
            self.spell_inventory[name] = self.spell_inventory.get(name, 0) + 1
            self.update_display()
            self.refresh_spells()

    def buy_skill(self, name):
        data = self.skill_tree[name]
        if not data["bought"] and self.israelcoins >= data["cost"]:
            self.israelcoins -= data["cost"]
            data["bought"] = True
            self.recalc_stats()
            self.refresh_all_tabs()

    def handle_stage(self, name):
        st = self.stages[name]
        if st["unlocked"]:
            self.equip_stage(name)
        else:
            if self.israelcoins >= st["cost"]:
                self.israelcoins -= st["cost"]
                st["unlocked"] = True
                self.equip_stage(name)
                self.refresh_stages()

    def equip_stage(self, name):
        self.current_stage = name
        st = self.stages[name]
        bg = st["bg"]
        self.root.configure(bg=bg)
        try:
            self.main_frame.configure(bg=bg)
            self.left_frame.configure(bg=bg)
            self.right_frame.configure(bg=bg)
            for c1 in self.main_frame.winfo_children():
                try: 
                    if isinstance(c1, tk.Frame): c1.configure(bg=bg)
                except: pass
        except: pass
        
        if name == "The Backrooms":
            self.click_btn.configure(bg="#c9b840")
        else:
            self.click_btn.configure(bg=self.colors["bg_panel"])
            
        self.recalc_stats()
        self.update_display()
        self.refresh_stages()

    def activate_boost(self, name):
        b = self.boosts[name]
        if self.goybucks >= b["cost"]:
            self.goybucks -= b["cost"]
            duration = b["duration"]
            if self.skill_tree["Mr Crossfields Overtime"]["bought"]:
                duration *= 2
            b["active_until"] = time.time() + duration
            self.recalc_stats()
            self.update_display()

    def recalc_stats(self):
        base_cps = sum(u.get("cps", 0) * u["count"] for u in self.upgrades.values())
        base_cpc = 1 + sum(u.get("cpc", 0) * u["count"] for u in self.upgrades.values())
        
        stage = self.stages.get(self.current_stage, self.stages["The Stage"])
        base_cps *= stage["cps_mult"]
        base_cpc *= stage["cpc_mult"]

        money_mult = 1.0
        if self.skill_tree["Miss Bailey Handshake"]["bought"]: money_mult += 0.20
        if self.skill_tree["Mr Banks Money Boost"]["bought"]: money_mult += 0.50
        base_cps *= money_mult
        base_cpc *= money_mult

        if self.is_boost_active("Miss Wadwha Crashouts"):
            base_cps *= 1.5
            base_cpc *= 1.5

        self.cps = base_cps
        self.cpc = base_cpc
        self.multiplier = 2 if self.cps >= 10 else 1

    def check_achievements(self):
        for name, ach in self.achievements.items():
            if ach["done"]: continue
            val = 0
            if ach["type"] == "clicks": val = self.clicks
            elif ach["type"] == "goybucks": val = self.goybucks
            elif ach["type"].startswith("upgrade_"): val = self.upgrades[ach["type"].split("_", 1)[1]]["count"]
            elif ach["type"] == "legendary_set": val = 1 if (self.inventory.get("kyle_sword", 0) > 0 and self.inventory.get("my_g_leader_armour", 0) > 0) else 0
            elif ach["type"] == "mythic_set": val = 1 if (self.inventory.get("miss_bailey_handshake", 0) > 0) else 0
            if val >= ach["req"]:
                ach["done"] = True
                self.ach_labels[name].config(text=f"✅ {name} (Unlocked!)", fg=self.colors["success"])

    def prestige(self):
        req = self.rebirth_req()
        if self.goybucks >= req:
            self.rebirths += 1
            base_coins = 1
            if self.skill_tree["Israelcoin Yield"]["bought"]: base_coins += 1
            self.israelcoins += base_coins
            
            self.goybucks = 0
            for k in self.upgrades:
                base = {
                    "Kyle Faircloughs": 15, "My G Leaders": 100, "Che Barcelo": 1100, "C K Dramas": 12000, "Gohst Duo": 130000,
                    "Miss Parishes 'Stage'": 50000, "Jadens Weakness (Martin)": 500000, "The Screws": 5000000,
                    "Steven Raphael Ibudimua": 10000000
                }[k]
                self.upgrades[k]["cost"] = base
                self.upgrades[k]["count"] = 0
            self.recalc_stats()
            self.update_display()
            self.refresh_all_tabs()

    def spawn_golden(self):
        chance = 0.05
        if self.is_boost_active("Scitzo Meds"): chance = 0.15
        if not self.golden_active and random.random() < chance:
            self.golden_active = True
            self.golden_btn.place(x=random.randint(50, 800), y=random.randint(50, 500))
            self.golden_btn.lift()

    def click_golden(self):
        if self.golden_active:
            bonus_mult = 2.0 if self.is_boost_active("Scitzo Meds") else 1.0
            base_bonus = max(self.cps * self.multiplier * 60, 100)
            bonus = base_bonus * self.get_prestige_mult() * self.get_ach_mult() * bonus_mult
            self.goybucks += bonus
            self.total_earned += bonus
            self.gain_xp(25)
            self.golden_btn.place_forget()
            self.golden_active = False
            self.update_display()
            self.refresh_all_tabs()

    # ================= CRATES / GAMBLE =================
    def roll_crate(self, cr):
        if "weighted" in cr:
            r, acc = random.random(), 0.0
            for item, w in cr["weighted"]:
                acc += w
                if r < acc: return item
            return cr["weighted"][-1][0]
        return random.choice(cr["loot"])

    def buy_crate(self, name):
        cr = self.crates[name]
        if self.goybucks < cr["cost"]:
            self.crate_result.config(text="Not enough goybucks!", fg=self.colors["danger"]); return
        self.goybucks -= cr["cost"]
        item = self.roll_crate(cr)
        if item in self.enchantments:
            self.spell_inventory[item] += 1
        else:
            self.inventory[item] += 1
            self.auto_equip(item)
        self.check_achievements()
        mythic = ("kyle_sword", "my_g_leader_armour", "miss_bailey_handshake")
        if item in mythic:
            self.crate_result.config(text=f"🌟 LEGENDARY! {self.fmt_item(item)}!", fg="#d946ef")
        else:
            self.crate_result.config(text=f"{name} → {self.fmt_item(item)}!", fg=self.colors["success"])
        self.update_display()
        self.refresh_all_tabs()

    def do_gamble(self):
        item = self._gmap.get(self.gamble_combo.get())
        if not item or self.inventory.get(item, 0) < 1:
            self.gamble_result.config(text="Out of items!", fg=self.colors["danger"]); return
        plus1, plus2 = self.gamble_paths[item]
        self.inventory[item] -= 1
        r = random.random()
        mythic = ("kyle_sword", "my_g_leader_armour", "miss_bailey_handshake")
        if r < 0.30 and plus1:
            result = plus1
            self.inventory[result] += 1
            self.auto_equip(result)
            self.gamble_result.config(text=f" SUCCESS! +1 tier → {self.fmt_item(result)}", fg="#d946ef" if result in mythic else self.colors["success"])
        elif r < 0.32 and plus2:
            result = plus2
            self.inventory[result] += 1
            self.auto_equip(result)
            self.gamble_result.config(text=f" JACKPOT! +2 tiers → {self.fmt_item(result)}", fg="#d946ef" if result in mythic else self.colors["accent"])
        else:
            self.gamble_result.config(text="💥 Fizzle. Item consumed, no upgrade.", fg=self.colors["danger"])
        self.check_achievements()
        self.update_display()
        self.refresh_all_tabs()

    def set_weapon(self, v):
        self.equipped_weapon = v
        self.refresh_adventure(); self.update_display()

    def set_armour(self, v):
        self.equipped_armour = v
        self.refresh_adventure(); self.update_display()

    # ================= COMBAT =================
    def draw_boss_portrait(self, c, name):
        c.create_rectangle(0, 0, 220, 160, fill="#1e293b", outline="")
        fx, fy = 110, 85
        
        # ================= HIGHLY DETAILED BOSSES =================
        if name == "Ben Rea":
            # Background
            c.create_rectangle(0, 0, 220, 160, fill="#334155")
            # Cap (Black with BOSS text)
            c.create_polygon(fx-42, fy-38, fx+42, fy-38, fx+45, fy-8, fx-45, fy-8, fill="#0f172a")
            c.create_polygon(fx-45, fy-8, fx+45, fy-8, fx+40, fy-3, fx-40, fy-3, fill="#1e293b")
            c.create_text(fx, fy-22, text="BOSS", fill="#64748b", font=("Arial", 7, "bold"))
            # Face Base (Sunburned/Pinkish)
            c.create_oval(fx-34, fy-32, fx+34, fy+32, fill="#fca5a5")
            # Cheek Shading
            c.create_oval(fx-28, fy-10, fx-15, fy+5, fill="#f87171", outline="")
            c.create_oval(fx+15, fy-10, fx+28, fy+5, fill="#f87171", outline="")
            # Nose
            c.create_polygon(fx-8, fy-15, fx+8, fy-15, fx+5, fy+5, fx-5, fy+5, fill="#fca5a5")
            c.create_line(fx, fy-15, fx, fy+5, fill="#f87171", width=1)
            # Eyes (Blue)
            c.create_oval(fx-22, fy-12, fx-12, fy-6, fill="white")
            c.create_oval(fx-19, fy-10, fx-14, fy-7, fill="#3b82f6")
            c.create_oval(fx-17, fy-9, fx-15, fy-8, fill="#000000")
            c.create_oval(fx-18, fy-10, fx-16, fy-9, fill="white") # Highlight
            c.create_oval(fx+12, fy-12, fx+22, fy-6, fill="white")
            c.create_oval(fx+14, fy-10, fx+19, fy-7, fill="#3b82f6")
            c.create_oval(fx+15, fy-9, fx+17, fy-8, fill="#000000")
            c.create_oval(fx+16, fy-10, fx+18, fy-9, fill="white") # Highlight
            # Eyebrows (Thick, reddish)
            c.create_polygon(fx-24, fy-16, fx-10, fy-14, fx-10, fy-11, fx-24, fy-13, fill="#78350f")
            c.create_polygon(fx+10, fy-14, fx+24, fy-16, fx+24, fy-13, fx+10, fy-11, fill="#78350f")
            # Beard (Highly detailed, multiple overlapping polygons for texture)
            beard_colors = ["#78350f", "#92400e", "#a16207", "#854d0e"]
            for i in range(40):
                bx = fx + random.randint(-30, 30)
                by = fy + random.randint(0, 30)
                bs = random.randint(3, 8)
                c.create_polygon(bx-bs, by-bs, bx+bs, by-bs, bx+bs, by+bs, bx-bs, by+bs, 
                                fill=random.choice(beard_colors), outline="")
            # Mouth (Slight smile visible through beard)
            c.create_arc(fx-12, fy+12, fx+12, fy+20, start=0, extent=180, style=tk.ARC, outline="#451a03", width=2)
            # Shirt (White collar)
            c.create_polygon(fx-38, fy+32, fx+38, fy+32, fx+38, fy+75, fx-38, fy+75, fill="#f8fafc")
            c.create_polygon(fx-15, fy+32, fx+15, fy+32, fx+10, fy+45, fx-10, fy+45, fill="#e2e8f0")

        elif name == "Goatis":
            # Background (Forest floor - highly detailed)
            for _ in range(80):
                rx = random.randint(0, 220)
                ry = random.randint(0, 160)
                rs = random.randint(2, 6)
                c.create_polygon(rx-rs, ry-rs, rx+rs, ry-rs, rx+rs, ry+rs, rx-rs, ry+rs, 
                                fill=random.choice(["#4d7c0f", "#65a30d", "#713f12", "#57534e"]), outline="")
            # Body (Gaunt, pale, collarbones)
            c.create_polygon(fx-25, fy+30, fx+25, fy+30, fx+35, fy+75, fx-35, fy+75, fill="#fef3c7")
            # Collarbone shading
            c.create_line(fx-20, fy+35, fx-5, fy+40, fill="#d6d3d1", width=2)
            c.create_line(fx+20, fy+35, fx+5, fy+40, fill="#d6d3d1", width=2)
            # Head (Balding top, pale)
            c.create_oval(fx-28, fy-35, fx+28, fy+15, fill="#fef3c7")
            # Bald spot shading
            c.create_oval(fx-15, fy-30, fx+15, fy-10, fill="#fde68a", outline="")
            # Long straggly hair (sides)
            hair_colors = ["#44403c", "#57534e", "#78716c"]
            for i in range(30):
                hx = fx + random.choice([-1, 1]) * random.randint(25, 35)
                hy = fy + random.randint(-20, 30)
                hs = random.randint(2, 5)
                c.create_polygon(hx-hs, hy-hs, hx+hs, hy-hs, hx+hs, hy+hs, hx-hs, hy+hs, 
                                fill=random.choice(hair_colors), outline="")
            # Face (Gaunt, sunken)
            # Sunken cheeks
            c.create_oval(fx-22, fy-5, fx-10, fy+10, fill="#e7e5e4", outline="")
            c.create_oval(fx+10, fy-5, fx+22, fy+10, fill="#e7e5e4", outline="")
            # Eyes (Sunken, dark)
            c.create_oval(fx-18, fy-10, fx-8, fy-4, fill="#1c1917")
            c.create_oval(fx-16, fy-9, fx-10, fy-5, fill="white")
            c.create_oval(fx-14, fy-8, fx-12, fy-6, fill="#000000")
            c.create_oval(fx+8, fy-10, fx+18, fy-4, fill="#1c1917")
            c.create_oval(fx+10, fy-9, fx+16, fy-5, fill="white")
            c.create_oval(fx+12, fy-8, fx+14, fy-6, fill="#000000")
            # Nose (Thin)
            c.create_polygon(fx-5, fy-5, fx+5, fy-5, fx+3, fy+8, fx-3, fy+8, fill="#d6d3d1")
            # Mouth (Slight grimace)
            c.create_line(fx-8, fy+12, fx+8, fy+12, fill="#78350f", width=2)
            c.create_line(fx-6, fy+12, fx-6, fy+15, fill="#78350f", width=1)
            c.create_line(fx+6, fy+12, fx+6, fy+15, fill="#78350f", width=1)

        elif name == "Matthew Alty":
            # Background (Blue sky with clouds)
            c.create_rectangle(0, 0, 220, 160, fill="#bae6fd")
            for _ in range(15):
                cx = random.randint(0, 220)
                cy = random.randint(0, 80)
                cr = random.randint(10, 25)
                c.create_oval(cx-cr, cy-cr, cx+cr, cy+cr, fill="white", outline="")
            # Hair (Curly, light brown - highly detailed with overlapping ovals)
            hair_colors = ["#d4a373", "#e6c288", "#c19a6b", "#faedcd"]
            for i in range(50):
                hx = fx + random.randint(-32, 32)
                hy = fy + random.randint(-35, -10)
                hr = random.randint(4, 10)
                c.create_oval(hx-hr, hy-hr, hx+hr, hy+hr, fill=random.choice(hair_colors), outline="")
            # Face Base
            c.create_oval(fx-30, fy-25, fx+30, fy+35, fill="#fde047") # Slightly tan/yellowish
            c.create_oval(fx-30, fy-25, fx+30, fy+35, fill="#fcd34d") # More natural skin tone
            # Cheeks (Rosy)
            c.create_oval(fx-25, fy+5, fx-15, fy+15, fill="#fca5a5", outline="")
            c.create_oval(fx+15, fy+5, fx+25, fy+15, fill="#fca5a5", outline="")
            # Glasses (Large wire frames)
            c.create_rectangle(fx-26, fy-12, fx-6, fy+4, outline="#475569", width=3)
            c.create_rectangle(fx+6, fy-12, fx+26, fy+4, outline="#475569", width=3)
            c.create_line(fx-6, fy-4, fx+6, fy-4, fill="#475569", width=3) # Bridge
            c.create_line(fx-26, fy-4, fx-32, fy-2, fill="#475569", width=2) # Left arm
            c.create_line(fx+26, fy-4, fx+32, fy-2, fill="#475569", width=2) # Right arm
            # Glasses reflection
            c.create_line(fx-22, fy-8, fx-18, fy-2, fill="white", width=2)
            c.create_line(fx+10, fy-8, fx+14, fy-2, fill="white", width=2)
            # Eyes behind glasses
            c.create_oval(fx-22, fy-8, fx-10, fy-2, fill="white")
            c.create_oval(fx-18, fy-6, fx-14, fy-3, fill="#3b82f6")
            c.create_oval(fx-17, fy-5, fx-15, fy-4, fill="#000000")
            c.create_oval(fx+10, fy-8, fx+22, fy-2, fill="white")
            c.create_oval(fx+14, fy-6, fx+18, fy-3, fill="#3b82f6")
            c.create_oval(fx+15, fy-5, fx+17, fy-4, fill="#000000")
            # Nose
            c.create_polygon(fx-6, fy-2, fx+6, fy-2, fx+4, fy+10, fx-4, fy+10, fill="#fcd34d")
            c.create_line(fx, fy-2, fx, fy+10, fill="#fbbf24", width=1)
            # Smile (Showing teeth)
            c.create_arc(fx-14, fy+14, fx+14, fy+26, start=0, extent=180, fill="white", outline="#78350f", width=2)
            c.create_line(fx-10, fy+20, fx+10, fy+20, fill="#e5e7eb", width=1) # Teeth line
            # Shirt (Striped Polo - White/Maroon/Black with Adidas logo)
            c.create_polygon(fx-38, fy+35, fx+38, fy+35, fx+38, fy+75, fx-38, fy+75, fill="#ffffff")
            c.create_rectangle(fx-38, fy+45, fx+38, fy+50, fill="#881337") # Maroon stripe
            c.create_rectangle(fx-38, fy+60, fx+38, fy+65, fill="#0f172a") # Black stripe
            # Adidas Logo (Three triangles)
            c.create_polygon(fx-18, fy+42, fx-14, fy+37, fx-10, fy+42, fill="#0f172a")
            c.create_polygon(fx-8, fy+42, fx-4, fy+35, fx+0, fy+42, fill="#0f172a")
            c.create_polygon(fx+2, fy+42, fx+6, fy+33, fx+10, fy+42, fill="#0f172a")

        # ================= LEGACY BOSSES (Simplified) =================
        elif name == "Che":
            c.create_polygon(fx-45, fy+35, fx+45, fy+35, fx+55, 160, fx-55, 160, fill="#2a2a2a")
            c.create_oval(fx-32, fy-35, fx+32, fy+35, fill="#f0c8a0")
            c.create_polygon(fx-34, fy-18, fx+34, fy-18, fx+38, fy-6, fx-38, fy-6, fill="#4a3b32")
            c.create_arc(fx-34, fy-52, fx+34, fy-12, start=0, extent=180, fill="#111111", outline="#000000", width=2)
            c.create_rectangle(fx-24, fy-8, fx-6, fy+6, outline="#111111", width=3, fill="#e0f0ff")
            c.create_rectangle(fx+6, fy-8, fx+24, fy+6, outline="#111111", width=3, fill="#e0f0ff")
            c.create_line(fx-6, fy, fx+6, fy, fill="#111111", width=3)
            c.create_line(fx-10, fy+20, fx+10, fy+20, fill="#8a4a3a", width=2)
        elif name == "Kyle Fairclough":
            c.create_polygon(fx-45, fy+35, fx+45, fy+35, fx+55, 160, fx-55, 160, fill="#666666")
            c.create_oval(fx-32, fy-35, fx+32, fy+35, fill="#f0c8a0")
            c.create_polygon(fx-34, fy-18, fx+34, fy-18, fx+38, fy-6, fx-38, fy-6, fill="#e8c985")
            c.create_arc(fx-34, fy-52, fx+34, fy-12, start=0, extent=180, fill="#111111", outline="#000000", width=2)
            for ex in (fx-16, fx+6):
                c.create_oval(ex, fy-6, ex+10, fy+2, fill="#ffffff")
                c.create_oval(ex+3, fy-4, ex+7, fy, fill="#000000")
            c.create_line(fx-10, fy+20, fx+10, fy+20, fill="#8a4a3a", width=2)
            c.create_line(fx+4, fy+18, fx+4, 160, fill="#ffffff", width=3)
        elif name == "My G Leader":
            c.create_polygon(fx-45, fy+35, fx+45, fy+35, fx+55, 160, fx-55, 160, fill="#1a237e")
            c.create_oval(fx-32, fy-35, fx+32, fy+35, fill="#f0c8a0")
            c.create_polygon(fx-34, fy-18, fx+34, fy-18, fx+38, fy-6, fx-38, fy-6, fill="#d4b46a")
            c.create_arc(fx-34, fy-52, fx+34, fy-12, start=0, extent=180, fill="#111111", outline="#000000", width=2)
            for ex in (fx-16, fx+6):
                c.create_oval(ex, fy-6, ex+10, fy+2, fill="#ffffff")
                c.create_oval(ex+3, fy-4, ex+7, fy, fill="#000000")
            c.create_oval(fx-12, fy+14, fx+12, fy+30, fill="#4a1a1a")
            c.create_rectangle(fx-10, fy+14, fx+10, fy+19, fill="#ffffff")
        elif name == "Riley":
            c.create_polygon(fx-45, fy+35, fx+45, fy+35, fx+55, 160, fx-55, 160, fill="#8a8a8a")
            for i in range(6):
                c.create_line(fx-52, fy+42+i*12, fx+52, fy+42+i*12, fill="#6a6a6a", width=2)
            c.create_oval(fx-44, fy-26, fx+20, fy+44, fill="#f5d0b5")
            c.create_polygon(fx-46, fy-4, fx-32, fy-32, fx+2, fy-40, fx+22, fy-22, fx+16, fy-4, fx-8, fy-18, fx-30, fy-10, fill="#a0522d")
            c.create_polygon(fx+14, fy-24, fx+28, fy+8, fx+18, fy+14, fx+8, fy-8, fill="#a0522d")
            c.create_rectangle(fx-38, fy-8, fx-12, fy+14, outline="#1a1a1a", width=3, fill="#e8f0ff")
            c.create_rectangle(fx-8, fy+2, fx+18, fy+24, outline="#1a1a1a", width=3, fill="#e8f0ff")
            c.create_line(fx-12, fy+4, fx-8, fy+8, fill="#1a1a1a", width=3)
            c.create_oval(fx-30, fy-2, fx-20, fy+8, fill="#7a9cc0")
            c.create_oval(fx-2, fy+8, fx+8, fy+18, fill="#7a9cc0")
            c.create_line(fx-26, fy+26, fx-6, fy+32, fill="#c47a6a", width=2)
        elif name == "Steven Ibudimua":
            c.create_polygon(fx-50, fy+32, fx+50, fy+32, fx+60, 160, fx-60, 160, fill="#9a9a9a")
            c.create_polygon(fx-16, fy+32, fx-38, fy+44, fx-18, fy+78, fx-8, fy+45, fill="#8a8a8a")
            c.create_polygon(fx+16, fy+32, fx+38, fy+44, fx+18, fy+78, fx+8, fy+45, fill="#8a8a8a")
            c.create_polygon(fx-16, fy+32, fx+16, fy+32, fx, fy+62, fill="#ffffff")
            c.create_polygon(fx-5, fy+36, fx+5, fy+36, fx+9, fy+78, fx, fy+88, fx-9, fy+78, fill="#141414")
            c.create_oval(fx-38, fy-8, fx-30, fy+8, fill="#8a5a3a")
            c.create_oval(fx+30, fy-8, fx+38, fy+8, fill="#8a5a3a")
            c.create_oval(fx-32, fy-38, fx+32, fy+34, fill="#8a5a3a")
            c.create_arc(fx-33, fy-46, fx+33, fy-4, start=0, extent=180, fill="#241a12", outline="")
            c.create_polygon(fx-32, fy-2, fx-26, fy+22, fx-12, fy+34, fx+12, fy+34, fx+26, fy+22, fx+32, fy-2,
                             fx+24, fy+2, fx+18, fy+20, fx+8, fy+26, fx-8, fy+26, fx-18, fy+20, fx-24, fy+2, fill="#241a12")
            c.create_polygon(fx-13, fy+8, fx+13, fy+8, fx+9, fy+15, fx-9, fy+15, fill="#241a12")
            c.create_line(fx-8, fy+20, fx+8, fy+20, fill="#5a3020", width=2)
            for ex in (fx-18, fx+6):
                c.create_oval(ex, fy-12, ex+12, fy-4, fill="#f0e0d0")
                c.create_oval(ex+3, fy-10, ex+8, fy-6, fill="#2a1a10")
                c.create_line(ex-1, fy-16, ex+13, fy-16, fill="#241a12", width=3)
            
        c.create_text(fx, 152, text=name, font=("Segoe UI", 10, "bold"), fill=self.colors["gold"])

    def start_bossfight(self, name):
        if self.combat: return
        b = self.bosses[name]
        self.player_hp = self.get_max_hp()
        self.combat = {"boss": name, "hp": float(b["hp"]), "heals": 3, "over": False, "busy": False}
        win = tk.Toplevel(self.root)
        self.combat_win = win
        win.title(f"BOSS: {name}")
        win.configure(bg=self.colors["bg_main"])
        win.geometry("520x660")
        win.protocol("WM_DELETE_WINDOW", self.flee_combat)
        port = tk.Canvas(win, width=220, height=160, bg=self.colors["bg_panel"], highlightthickness=0)
        port.pack(pady=10)
        self.draw_boss_portrait(port, name)
        self.boss_hp_bar = ttk.Progressbar(win, style="Red.Horizontal.TProgressbar", mode='determinate', maximum=b["hp"], value=b["hp"])
        self.boss_hp_bar.pack(fill=tk.X, padx=20, pady=(10, 2))
        self.boss_hp_lbl = tk.Label(win, text=f"{name}: {b['hp']} HP", fg=self.colors["danger"], 
                                   bg=self.colors["bg_main"], font=("Segoe UI", 11, "bold"))
        self.boss_hp_lbl.pack()
        self.player_hp_bar = ttk.Progressbar(win, style="Green.Horizontal.TProgressbar", mode='determinate', maximum=self.get_max_hp(), value=self.get_max_hp())
        self.player_hp_bar.pack(fill=tk.X, padx=20, pady=(10, 2))
        self.player_hp_lbl = tk.Label(win, text=f"You: {int(self.player_hp)} HP", fg=self.colors["success"], 
                                     bg=self.colors["bg_main"], font=("Segoe UI", 11, "bold"))
        self.player_hp_lbl.pack()
        self.combat_log = tk.Text(win, height=10, width=55, bg=self.colors["bg_panel"], fg=self.colors["success"], 
                                 state=tk.DISABLED, font=("Consolas", 10), relief=tk.FLAT, borderwidth=2)
        self.combat_log.pack(pady=10, padx=15)
        btnf = tk.Frame(win, bg=self.colors["bg_main"]); btnf.pack(pady=8)
        self.atk_btn = tk.Button(btnf, text="⚔ ATTACK", command=self.combat_attack, bg=self.colors["danger"], 
                                fg="white", font=("Segoe UI", 11, "bold"), relief=tk.FLAT, width=10, bd=0)
        self.heal_btn = tk.Button(btnf, text="🧪 HEAL (3)", command=self.combat_heal, bg=self.colors["success"], 
                                 fg="white", font=("Segoe UI", 11, "bold"), relief=tk.FLAT, width=10, bd=0)
        self.flee_btn = tk.Button(btnf, text=" FLEE", command=self.flee_combat, bg=self.colors["bg_input"], 
                                 fg="white", font=("Segoe UI", 11, "bold"), relief=tk.FLAT, width=10, bd=0)
        self.atk_btn.grid(row=0, column=0, padx=10, ipady=5)
        self.heal_btn.grid(row=0, column=1, padx=10, ipady=5)
        self.flee_btn.grid(row=0, column=2, padx=10, ipady=5)
        self.combat_btns = [self.atk_btn, self.heal_btn]
        self.update_combat_bars()
        self.log_combat(f"{name} blocks your path! Turn-based battle begins.")

    def log_combat(self, msg):
        t = self.combat_log
        t.config(state=tk.NORMAL); t.insert(tk.END, msg + "\n"); t.see(tk.END); t.config(state=tk.DISABLED)

    def set_combat_buttons(self, state):
        for b in self.combat_btns: b.config(state=state)

    def update_combat_bars(self):
        b = self.bosses[self.combat["boss"]]
        self.boss_hp_bar['value'] = max(0, self.combat["hp"])
        self.boss_hp_lbl.config(text=f"{self.combat['boss']}: {max(0, int(self.combat['hp']))}/{b['hp']} HP")
        self.player_hp_bar['value'] = max(0, self.player_hp)
        self.player_hp_lbl.config(text=f"You: {max(0, int(self.player_hp))}/{self.get_max_hp()} HP")

    def combat_attack(self):
        if not self.combat or self.combat["over"] or self.combat["busy"]: return
        w = self.weapon_stats[self.equipped_weapon]
        bonus = 2 * (self.level - 1)
        mult = self.get_boss_dmg_mult()
        
        enchants = self.item_enchants.get(self.equipped_weapon, {})
        sharp_bonus = 0
        flame_mult = 1.0
        for i, name in enumerate(["Sharpness I", "Sharpness II", "Sharpness III", "Sharpness IV", "Sharpness V"]):
            if name in enchants: sharp_bonus += [2, 5, 10, 20, 40][i]
        for i, name in enumerate(["Flame I", "Flame II", "Flame III"]):
            if name in enchants: flame_mult = [1.2, 1.5, 2.0][i]
            
        base_dmg = w["dmg"] + bonus + sharp_bonus
        
        crit_chance = w["crit"]
        if self.skill_tree["Riley Rage Criticals"]["bought"]: crit_chance += 0.25
        if self.is_boost_active("Miss Wadwha Crashouts"): crit_chance += 0.20
        
        is_crit = random.random() < crit_chance
        if self.is_boost_active("Riley Rage"): is_crit = True
        
        if is_crit:
            dmg = (w["crit_dmg"] + bonus + sharp_bonus) * mult * flame_mult
            self.log_combat(f"💥 CRITICAL! Your {self.fmt_item(self.equipped_weapon)} hits for {dmg:.1f}!")
        else:
            dmg = base_dmg * mult
            self.log_combat(f"You hit {self.combat['boss']} for {dmg:.1f}.")
        self.combat["hp"] -= dmg
        self.end_player_turn()

    def combat_heal(self):
        if not self.combat or self.combat["over"] or self.combat["busy"] or self.combat["heals"] <= 0: return
        heal = int(self.get_max_hp() * 0.4)
        self.player_hp = min(self.get_max_hp(), self.player_hp + heal)
        self.combat["heals"] -= 1
        self.heal_btn.config(text=f"🧪 HEAL ({self.combat['heals']})")
        self.log_combat(f"You heal {heal} HP.")
        self.end_player_turn()

    def end_player_turn(self):
        self.update_combat_bars()
        if self.combat["hp"] <= 0:
            self.combat_victory(); return
        self.combat["busy"] = True
        self.set_combat_buttons(tk.DISABLED)
        self.combat_win.after(600, self.boss_turn)

    def boss_turn(self):
        if not self.combat or self.combat["over"]: return
        if not (self.combat_win and self.combat_win.winfo_exists()):
            self.combat = None; return
        b = self.bosses[self.combat["boss"]]
        mult = 1.0
        if random.random() < b["special"]:
            mult = 1.5
            specials = {"Kyle Fairclough": "whips you with his deal dough", "Che": "reveals my g leader being kicked from gohst duo",
                        "My G Leader": "nonchalantly ignores you", "Riley": "eats a creamy dreamy",
                        "Steven Ibudimua": "finds out the threes do nothing", "Goatis": "stares at you intensely",
                        "Ben Rea": "adjusts his cap menacingly", "Matthew Alty": "calculates your defeat"}
            self.log_combat(f"⚠ {self.combat['boss']} {specials.get(self.combat['boss'], 'attacks')}!")
            
        thorns_chance = 0.0
        thorns_dmg = 0
        enchants = self.item_enchants.get(self.equipped_armour, {})
        for i, name in enumerate(["Thorns I", "Thorns II", "Thorns III"]):
            if name in enchants:
                thorns_chance = [0.1, 0.2, 0.3][i]
                thorns_dmg = [2, 5, 10][i]
                
        if self.is_boost_active("Where is the Boost?") and random.random() < 0.75:
            dmg = max(1, b["atk"] * mult - self.get_armour())
            self.combat["hp"] -= dmg
            self.log_combat(f" {self.combat['boss']} is confused and hits themselves for {dmg:g}!")
        else:
            dmg = max(1, b["atk"] * mult - self.get_armour())
            self.player_hp -= dmg
            self.log_combat(f"{self.combat['boss']} hits you for {dmg:g}.")
            
            if random.random() < thorns_chance and thorns_dmg > 0:
                self.combat["hp"] -= thorns_dmg
                self.log_combat(f"🔥 Thorns reflects {thorns_dmg} damage to {self.combat['boss']}!")
            
        self.update_combat_bars()
        if self.combat["hp"] <= 0:
            self.combat_victory(); return
        if self.player_hp <= 0:
            self.combat_defeat(); return
        self.combat["busy"] = False
        self.set_combat_buttons(tk.NORMAL)

    def combat_victory(self):
        name = self.combat["boss"]; b = self.bosses[name]
        self.combat["over"] = True
        self.bosses_defeated[name] += 1
        self.goybucks += b["gold"]; self.total_earned += b["gold"]
        self.gain_xp(b["xp"])
        self.player_hp = self.get_max_hp()
        self.log_combat(f"🏆 VICTORY! +{b['gold']:,} gb, +{b['xp']} XP! Boss bonus now +{sum(self.bosses_defeated.values())*0.5:.1f}%")
        self.set_combat_buttons(tk.DISABLED)
        self.flee_btn.config(text="LEAVE", state=tk.NORMAL)
        self.update_display(); self.refresh_all_tabs()

    def combat_defeat(self):
        self.combat["over"] = True
        self.player_hp = self.get_max_hp()
        self.log_combat(" You were defeated... You crawl home to recover.")
        self.set_combat_buttons(tk.DISABLED)
        self.flee_btn.config(text="LEAVE", state=tk.NORMAL)
        self.refresh_all_tabs()

    def flee_combat(self):
        self.combat = None
        self.player_hp = self.get_max_hp()
        if self.combat_win and self.combat_win.winfo_exists(): self.combat_win.destroy()
        self.update_display()

    # ================= DISPLAY / SAVE =================
    def update_display(self):
        p_mult, a_mult = self.get_prestige_mult(), self.get_ach_mult()
        eff_cps = self.cps * self.multiplier * p_mult * a_mult
        eff_cpc = self.cpc * self.multiplier * p_mult * a_mult
        self.goybucks_label.config(text=f"{int(self.goybucks):,} goybucks")
        self.ic_hud_label.config(text=f"{self.israelcoins} 🪙 Israelcoins")
        self.cps_label.config(text=f"{eff_cps:.1f} gps")
        self.cpc_label.config(text=f"{eff_cpc:.1f} gpc")
        self.level_label.config(text=f"⭐ Lv {self.level} ({int(self.xp)}/{self.xp_needed()} xp)")
        self.xp_bar['maximum'] = self.xp_needed()
        self.xp_bar['value'] = self.xp
        bonus = sum(self.bosses_defeated.values()) * 0.5
        self.stats_label.config(text=f"HP {int(self.player_hp)}/{self.get_max_hp()} | ATK {self.get_attack():.1f} | DEF {self.get_armour():g} | Boss +{bonus:.1f}%")
        if self.multiplier == 2:
            self.multiplier_label.config(text="🔥 2x MULTIPLIER ACTIVE! 🔥", fg=self.colors["success"])
        else:
            self.multiplier_label.config(text="Multiplier: 1x (10 CPS → 2x)", fg=self.colors["danger"])
        req = self.rebirth_req()
        if self.goybucks >= req:
            base_coins = 1 + (1 if self.skill_tree["Israelcoin Yield"]["bought"] else 0)
            self.prestige_btn.config(state=tk.NORMAL, text=f"REBIRTH #{self.rebirths+1} → +{base_coins}🪙 (needs {req:,})")
        else:
            self.prestige_btn.config(state=tk.DISABLED, text=f"REBIRTH #{self.rebirths+1} — needs {req:,} gb")
        self.refresh_upgrades()

    def save_game(self):
        data = {
            "goybucks": self.goybucks, "total_earned": self.total_earned, "clicks": self.clicks,
            "israelcoins": self.israelcoins, "rebirths": self.rebirths,
            "upgrades": {n: u["count"] for n, u in self.upgrades.items()},
            "achievements": {n: a["done"] for n, a in self.achievements.items()},
            "level": self.level, "xp": self.xp, "inventory": self.inventory,
            "equipped_weapon": self.equipped_weapon, "equipped_armour": self.equipped_armour,
            "bosses_defeated": self.bosses_defeated,
            "skill_tree": {k: v["bought"] for k, v in self.skill_tree.items()},
            "stages": {k: v["unlocked"] for k, v in self.stages.items()},
            "current_stage": self.current_stage,
            "spell_inventory": self.spell_inventory,
            "item_enchants": self.item_enchants,
        }
        with open("goybuck_save.json", "w") as f: json.dump(data, f)

    def load_game(self):
        if os.path.exists("goybuck_save.json"):
            with open("goybuck_save.json", "r") as f: data = json.load(f)
            self.goybucks = data.get("goybucks", 0)
            self.total_earned = data.get("total_earned", 0)
            self.clicks = data.get("clicks", 0)
            self.israelcoins = data.get("israelcoins", 0)
            self.rebirths = data.get("rebirths", 0)
            for n, count in data.get("upgrades", {}).items():
                if n in self.upgrades: self.upgrades[n]["count"] = count
            for n, done in data.get("achievements", {}).items():
                if n in self.achievements:
                    self.achievements[n]["done"] = done
                    if done: self.ach_labels[n].config(text=f"✅ {n} (Unlocked!)", fg=self.colors["success"])
            self.level = data.get("level", 1)
            self.xp = data.get("xp", 0)
            for k, v in data.get("inventory", {}).items():
                if k in self.inventory: self.inventory[k] = v
            w = data.get("equipped_weapon", "fists")
            self.equipped_weapon = w if w in self.weapon_stats else "fists"
            a = data.get("equipped_armour", "none")
            self.equipped_armour = a if a in self.armour_stats else "none"
            for k, v in data.get("bosses_defeated", {}).items():
                if k in self.bosses_defeated: self.bosses_defeated[k] = v
            for k, bought in data.get("skill_tree", {}).items():
                if k in self.skill_tree: self.skill_tree[k]["bought"] = bought
            for k, unlocked in data.get("stages", {}).items():
                if k in self.stages: self.stages[k]["unlocked"] = unlocked
            self.current_stage = data.get("current_stage", "The Stage")
            self.spell_inventory = data.get("spell_inventory", {k: 0 for k in self.enchantments})
            self.item_enchants = data.get("item_enchants", {k: {} for k in list(self.weapon_stats.keys()) + list(self.armour_stats.keys())})
            self.recalc_stats()
            self.equip_stage(self.current_stage)

    def on_close(self):
        self.save_game()
        self.root.destroy()

    def game_loop(self):
        p_mult, a_mult = self.get_prestige_mult(), self.get_ach_mult()
        eff_cps = self.cps * self.multiplier * p_mult * a_mult
        self.goybucks += eff_cps / 10
        self.total_earned += eff_cps / 10
        self.gain_xp(eff_cps / 200)
        self.spawn_golden()
        self.check_achievements()
        self.update_display()
        
        for name, b in self.boosts.items():
            if self.is_boost_active(name):
                rem = int(b["active_until"] - time.time())
                self.boost_timers[name].config(text=f"{rem}s")
                self.boost_buttons[name].config(state=tk.DISABLED, text="ACTIVE")
            else:
                self.boost_timers[name].config(text="")
                if self.goybucks >= b["cost"]:
                    self.boost_buttons[name].config(state=tk.NORMAL, text="ACTIVATE")
                else:
                    self.boost_buttons[name].config(state=tk.DISABLED, text="ACTIVATE")
                    
        if time.time() - self.last_save > 30:
            self.save_game()
            self.last_save = time.time()
        self.root.after(100, self.game_loop)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    GoybuckClicker().run()