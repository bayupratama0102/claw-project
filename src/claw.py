import sys, os, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Database

class CLAW:
    def __init__(self):
        self.db = Database()
        self.commands = {"help":self.show_help,"jadwal":self.handle_jadwal,"catatan":self.handle_catatan,"ai":self.handle_ai_chat,"exit":self.exit}

    def show_banner(self):
        print("="*60)
        print("  CLAW v0.2.0 | ATR/BPN | Ketik 'help'")
        print("="*60)

    def show_help(self):
        print("\nPerintah: help | jadwal | catatan | ai | exit\n")

    def handle_jadwal(self):
        print("\n1.Tambah  2.Lihat  3.Kembali")
        p = input("Pilih: ").strip()
        if p == "1":
            j = input("Judul: ").strip()
            t = input("Tanggal (YYYY-MM-DD): ").strip()
            w = input("Waktu (HH:MM): ").strip()
            k = input("Kategori: ").strip() or "umum"
            if j and t:
                self.db.tambah_jadwal(j, t, w, k)
                print("Tersimpan!")
        elif p == "2":
            data = self.db.lihat_jadwal()
            if not data:
                print("Belum ada jadwal")
            else:
                for d in data:
                    print(f"  {d['tanggal']} {d['waktu']} - {d['judul']}")
        print()

    def handle_catatan(self):
        print("\n1.Tambah  2.Lihat  3.Kembali")
        p = input("Pilih: ").strip()
        if p == "1":
            j = input("Judul: ").strip()
            i = input("Isi: ").strip()
            if j and i:
                self.db.tambah_catatan(j, i, [])
                print("Tersimpan!")
        elif p == "2":
            try:
                with open("./data/catatan.json","r",encoding="utf-8") as f:
                    data = json.load(f)
                if not data:
                    print("Belum ada catatan")
                else:
                    for d in data:
                        print(f"  {d['judul']}: {d['isi'][:60]}")
            except Exception as e:
                print(f"Error: {e}")
        print()

    def handle_ai_chat(self):
        print("\nMODE AI | Ketik 'kembali' untuk keluar\n")
        try:
            from ai_engine import AIEngine
            ai = AIEngine()
        except Exception as e:
            print(f"Error: {e}")
            return
        if not ai.check_status():
            print("Ollama tidak aktif!")
            return
        print("AI siap!\n")
        while True:
            try:
                pesan = input("Anda > ").strip()
                if pesan.lower() in ["kembali","exit","q"]:
                    return
                if not pesan:
                    continue
                jawaban = ai.chat(pesan)
                if jawaban:
                    print(f"{jawaban}\n")
            except KeyboardInterrupt:
                return

    def exit(self):
        print("Sampai jumpa!")
        return True

    def run(self):
        self.show_banner()
        while True:
            try:
                cmd = input("CLAW > ").strip().lower()
                if not cmd:
                    continue
                if cmd in self.commands:
                    if self.commands[cmd]() is True:
                        break
                else:
                    print("Tidak dikenal. Ketik 'help'\n")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    CLAW().run()