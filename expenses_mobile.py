# Kivy-based Monthly Expenses mobile app
# Auto-generated project for GitHub Build.
# App Name: Monthly Expenses with logo of trade graph
# Package: com.shreepadmavati.expenses

import sqlite3
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
import os

KV = """
ScreenManager:
    MainScreen:

<MainScreen>:
    name: "main"
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(8)

        BoxLayout:
            size_hint_y: None
            height: dp(120)
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: 1,1,1,1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Image:
                source: "assets/icon.png"
                size_hint_x: None
                width: dp(100)

            BoxLayout:
                orientation: "vertical"
                spacing: dp(4)
                Label:
                    text: app.app_title
                    font_size: "18sp"
                    bold: True
                    halign: "left"
                    valign: "middle"
                    text_size: self.size
                Label:
                    text: "Simple expenses tracker (SQLite)"
                    font_size: "12sp"
                    halign: "left"
                    valign: "middle"
                    text_size: self.size

        GridLayout:
            cols: 1
            size_hint_y: None
            height: dp(160)
            spacing: dp(6)

            BoxLayout:
                spacing: dp(6)
                TextInput:
                    id: date_input
                    text: root.default_date
                    multiline: False
                    hint_text: "DD-MM-YYYY"
                TextInput:
                    id: cat_input
                    hint_text: "Category"
                    multiline: False

            BoxLayout:
                spacing: dp(6)
                TextInput:
                    id: amt_input
                    hint_text: "Amount (e.g., 250.00)"
                    multiline: False
                    input_filter: "float"
                TextInput:
                    id: note_input
                    hint_text: "Note"
                    multiline: False

            BoxLayout:
                size_hint_y: None
                height: dp(40)
                spacing: dp(6)
                Button:
                    text: "Add"
                    on_release: root.add_expense()
                Button:
                    text: "Export CSV"
                    on_release: root.export_csv()

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            Label:
                id: total_label
                text: "Total: ₹ 0.00"
                bold: True

        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: list_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                row_default_height: "48dp"
                spacing: dp(6)
"""
DB = "expenses_mobile.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        note TEXT
    )
    """)
    conn.commit()
    conn.close()

class MainScreen(Screen):
    def on_pre_enter(self):
        self.default_date = datetime.now().strftime("%d-%m-%Y")
        self.refresh_list()

    def add_expense(self):
        date_str = self.ids.date_input.text.strip()
        cat = self.ids.cat_input.text.strip()
        amt = self.ids.amt_input.text.strip()
        note = self.ids.note_input.text.strip()

        if not date_str or not cat or not amt:
            return
        try:
            amount = float(amt)
        except:
            return

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses(date, category, amount, note) VALUES (?, ?, ?, ?)",
                    (date_str, cat, amount, note))
        conn.commit()
        conn.close()

        self.ids.date_input.text = datetime.now().strftime("%d-%m-%Y")
        self.ids.cat_input.text = ""
        self.ids.amt_input.text = ""
        self.ids.note_input.text = ""
        self.refresh_list()

    def refresh_list(self):
        container = self.ids.list_container
        container.clear_widgets()
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT id, date, category, amount, note FROM expenses ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()

        total = 0.0
        for r in rows:
            _id, date_s, cat, amt, note = r
            total += float(amt)
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.button import Button

            row = BoxLayout(size_hint_y=None, height="40dp", spacing="6dp")
            lbl = Label(text=f"{date_s}  |  {cat}  |  ₹{float(amt):.2f}", halign="left", valign="middle", text_size=(None, None))
            row.add_widget(lbl)
            btn = Button(text="Del", size_hint_x=None, width="64dp")
            def _del(id=_id):
                conn = sqlite3.connect(DB)
                cur = conn.cursor()
                cur.execute("DELETE FROM expenses WHERE id=?", (id,))
                conn.commit()
                conn.close()
                self.refresh_list()
            btn.bind(on_release=lambda inst, id=_id: _del(id))
            row.add_widget(btn)
            container.add_widget(row)

        try:
            self.ids.total_label.text = f"Total: ₹ {total:,.2f}"
        except:
            pass

    def export_csv(self):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT id, date, category, amount, note FROM expenses ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        if platform == "android":
            try:
                from android.storage import primary_external_storage_path
                base = primary_external_storage_path()
            except:
                base = "/sdcard"
            out_dir = os.path.join(base, "ExpensesMobile")
            try:
                os.makedirs(out_dir, exist_ok=True)
            except:
                pass
            file_path = os.path.join(out_dir, f"expenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        else:
            out_dir = os.path.expanduser("~")
            file_path = os.path.join(out_dir, f"expenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                import csv
                writer = csv.writer(f)
                writer.writerow(["ID","Date","Category","Amount","Note"])
                for r in rows:
                    writer.writerow(r)
        except Exception as e:
            print("Export failed:", e)
            return

        print("Exported:", file_path)

class ExpensesApp(App):
    app_title = "Monthly Expenses with logo of trade graph"
    def build(self):
        init_db()
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        return sm

if __name__ == "__main__":
    ExpensesApp().run()
