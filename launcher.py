import os, sys, platform, subprocess, threading, signal, ctypes
import tkinter as tk
from tkinter import ttk

PYTHON = sys.executable  # mevcut python yolu

# ================= Cartiva Renk Paleti =================
CARTIVA = {
    "bg":      "#0f1222",
    "panel":   "#151935",
    "card":    "#1b2045",
    "ink":     "#e7ebff",
    "muted":   "#aeb6da",
    "accent":  "#6bd0ff",
    "good":    "#29d67d",
    "bad":     "#ff5c7a",
    "warn":    "#ffb020",
}

# ---------------- Uyku/ekran koruyucu engelleme ----------------
class SleepBlocker:
    def __init__(self):
        self.os = platform.system()
        self._proc = None

    def start(self):
        try:
            if self.os == "Windows":
                # ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000040)
                print("✅ Windows uyku engelleme aktif.")
            elif self.os == "Darwin":
                self._proc = subprocess.Popen(["/usr/bin/caffeinate", "-dimsu"])
                print("✅ macOS uyku engelleme aktif (caffeinate).")
            else:
                print("ℹ️ Uyku engelleme bu işletim sisteminde desteklenmiyor.")
        except Exception as e:
            print(f"⚠️ Uyku engelleme başlatılamadı: {e}")

    def stop(self):
        try:
            if self.os == "Windows":
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
                print("✅ Windows uyku engelleme kapatıldı.")
            elif self._proc:
                self._proc.terminate()
                self._proc = None
                print("✅ macOS uyku engelleme kapatıldı.")
        except Exception as e:
            print(f"⚠️ Uyku engelleme durdurulamadı: {e}")


# ---------------- Bot çalıştırıcı ----------------
class BotRunner:
    def __init__(self, log_callback, use_external_terminal=False):
        self.proc = None
        self.thread = None
        self.log_cb = log_callback
        self.use_external_terminal = use_external_terminal
        self.sleep_blocker = SleepBlocker()

    def _env(self):
        return os.environ.copy()

    def start(self):
        if self.proc:
            self.log_cb("Zaten çalışıyor.\n")
            return

        self.sleep_blocker.start()
        cwd = os.path.dirname(os.path.abspath(__file__))

        if self.use_external_terminal and platform.system() == "Windows":
            CREATE_NEW_CONSOLE = 0x00000010
            self.proc = subprocess.Popen(
                [PYTHON, "-u", "jetstok_trendyol_bot.py"],
                cwd=cwd, env=self._env(),
                creationflags=CREATE_NEW_CONSOLE
            )
            self.log_cb("Windows’ta ayrı bir terminal açıldı.\n")

        elif self.use_external_terminal and platform.system() == "Darwin":
            # macOS Terminal.app’te aç
            safe_cwd = cwd.replace('"', '\\"')
            safe_py = PYTHON.replace('"', '\\"')

            script = (
                'tell application "Terminal"\n'
                '    activate\n'
                '    do script "cd {cwd}; {py} -u jetstok_trendyol_bot.py"\n'
                'end tell\n'
            ).format(cwd=safe_cwd, py=safe_py)

            subprocess.run(["osascript", "-e", script])
            self.log_cb("macOS Terminal’da başlatıldı.\n")

        else:
            # İç panelde log göster (tek pencere)
            self.proc = subprocess.Popen(
                [PYTHON, "-u", "jetstok_trendyol_bot.py"],
                cwd=cwd, env=self._env(),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
            )
            self.thread = threading.Thread(target=self._pump_logs, daemon=True)
            self.thread.start()
            self.log_cb("Bot başlatıldı.\n")

    def _pump_logs(self):
        assert self.proc and self.proc.stdout
        for line in self.proc.stdout:
            self.log_cb(line)
        rc = self.proc.wait()
        self.log_cb(f"\nBot kapandı. Çıkış kodu: {rc}\n")
        self.proc = None
        self.sleep_blocker.stop()

    def stop(self):
        if self.proc:
            try:
                if platform.system() == "Windows":
                    self.proc.send_signal(signal.CTRL_BREAK_EVENT if hasattr(signal, "CTRL_BREAK_EVENT") else signal.SIGTERM)
                else:
                    self.proc.terminate()
            except Exception:
                pass
        self.proc = None
        self.sleep_blocker.stop()
        self.log_cb("Durduruldu.\n")


# ---------------- Basit Tk GUI (ttk yerine tk) ----------------
from tkinter import scrolledtext

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        os.environ.setdefault("TK_SILENCE_DEPRECATION", "1")

        # Pencere
        self.title("Jetstok Trendyol Bot – Başlatıcı")
        self.geometry("900x580")
        self.minsize(760, 480)
        self.configure(bg=CARTIVA["bg"])

        # Üst bar (tamamen tk ile)
        top = tk.Frame(self, bg=CARTIVA["bg"])
        top.pack(fill="x", padx=14, pady=(14, 8))

        self.title_lbl = tk.Label(
            top, text="Cartiva • Jetstok Trendyol Bot",
            bg=CARTIVA["bg"], fg=CARTIVA["ink"],
            font=("Arial", 16, "bold")
        )
        self.title_lbl.pack(side="left", padx=(0, 12))

        self.external_var = tk.BooleanVar(value=False)
        self.chk_ext = tk.Checkbutton(
            top, text="Ayrı Terminal Aç", variable=self.external_var,
            bg=CARTIVA["bg"], fg=CARTIVA["ink"], selectcolor=CARTIVA["panel"],
            activebackground=CARTIVA["bg"], activeforeground=CARTIVA["ink"],
            highlightthickness=0
        )
        self.chk_ext.pack(side="left")

        self.start_btn = tk.Button(
            top, text="Başlat",
            bg=CARTIVA["accent"], fg="#0a0f1e", activebackground=CARTIVA["accent"],
            activeforeground="#0a0f1e", bd=0, padx=16, pady=6,
            font=("Arial", 12, "bold"),
            command=self.on_start
        )
        self.start_btn.pack(side="right")

        self.stop_btn = tk.Button(
            top, text="Durdur",
            bg=CARTIVA["card"], fg=CARTIVA["ink"], activebackground=CARTIVA["panel"],
            activeforeground=CARTIVA["ink"], bd=0, padx=16, pady=6,
            font=("Arial", 12, "bold"),
            command=self.on_stop
        )
        self.stop_btn.pack(side="right", padx=(0, 10))

        # Panel çerçevesi
        frame = tk.Frame(self, bg=CARTIVA["panel"], highlightthickness=1, highlightbackground="#222849")
        frame.pack(fill="both", expand=True, padx=14, pady=8)

        # Log başlık
        hdr = tk.Frame(frame, bg=CARTIVA["card"])
        hdr.pack(fill="x")
        tk.Label(
            hdr, text="Çalışma Günlüğü (Log)",
            bg=CARTIVA["card"], fg=CARTIVA["muted"],
            font=("Arial", 11, "bold"), pady=8, padx=10
        ).pack(side="left")

        # Log alanı (ScrolledText)
        self.log = scrolledtext.ScrolledText(
            frame, height=26, wrap="word",
            bg=CARTIVA["card"], fg=CARTIVA["ink"],
            insertbackground=CARTIVA["ink"],  # imleç
            relief="flat", bd=0, padx=12, pady=12,
            font=("Arial", 12)
        )
        self.log.pack(fill="both", expand=True)

        # Alt çubuk
        status = tk.Frame(self, bg=CARTIVA["bg"])
        status.pack(fill="x", padx=14, pady=(4, 12))
        self.status_lbl = tk.Label(status, text="Hazır.", bg=CARTIVA["bg"], fg=CARTIVA["muted"])
        self.status_lbl.pack(side="left")

        # Runner
        self.runner = BotRunner(self._append_log)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # İlk satır
        self._append_log("Hazır.\n")

    def _append_log(self, text):
        self.log.insert("end", text)
        self.log.see("end")
        if "başlatıldı" in text.lower():
            self.status_lbl.config(text="Çalışıyor…", fg=CARTIVA["good"])
        elif "durduruldu" in text.lower():
            self.status_lbl.config(text="Durduruldu.", fg=CARTIVA["bad"])
        else:
            self.status_lbl.config(text="Güncelleniyor…", fg=CARTIVA["muted"])
        try:
            with open("bot_log.txt", "a", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            pass

    def on_start(self):
        self.runner.use_external_terminal = self.external_var.get()
        self.runner.start()

    def on_stop(self):
        self.runner.stop()
        self.status_lbl.config(text="Durduruldu.", fg=CARTIVA["bad"])

    def on_close(self):
        self.runner.stop()
        self.destroy()



if __name__ == "__main__":
    App().mainloop()
