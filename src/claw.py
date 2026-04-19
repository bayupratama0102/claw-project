import sys, os, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Database

class CLAW:
    def __init__(self):
        self.nama = "CLAW"
        self.versi = "0.2.0"
        self.db = Database()
        self.commands = {
            "help": self.show_help,
            "jadwal": self.handle_jadwal,
            "catatan": self.handle_catatan,
            "ai": self.handle_ai_chat,
            "info": self.show_info,
            "exit": self.exit
        }

    def show_banner(self):
        print("=" * 60)
        print("  CLAW - Coordinator Local Assistant Worker v0.2.0")
        print("=" * 60)
        print()
        print("  Kementerian ATR/BPN | Ketik 'help' untuk bantuan")
        print()

    def show_help(self):
        print()
        print("PERINTAH: help | jadwal | catatan | ai | info | exit")
        print()

    def show_info(self):
        print()
        print("CLAW v0.2.0 | Model: Qwen 2.5 7B | Ollama lokal")
        print()

    def handle_jadwal(self):
        print()
        print("MENU JADWAL: 1.Tambah  2.Lihat  3.Kembali")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1":
            judul = input("Judul: ").strip()
            tanggal = input("Tanggal (YYYY-MM-DD): ").strip()
            waktu = input("Waktu (HH:MM): ").strip()
            kategori = input("Kategori: ").strip() or "umum"
            if judul and tanggal:
                hasil = self.db.tambah_jadwal(judul, tanggal, waktu, kategori)
                print(f"Tersimpan: {hasil['judul']}")
        elif pilihan == "2":
            jadwal = self.db.lihat_jadwal()
            if not jadwal:
                print("Belum ada jadwal")
            else:
                for j in jadwal:
                    print(f"  {j['tanggal']} {j['waktu']} - {j['judul']}")
        print()

    def handle_catatan(self):
        print()
        print("MENU CATATAN: 1.Tambah  2.Lihat  3.Kembali")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1":
            judul = input("Judul: ").strip()
            isi = input("Isi: ").strip()
            if judul and isi:
                hasil = self.db.tambah_catatan(judul, isi, [])
                print(f"Tersimpan: {hasil['judul']}")
        elif pilihan == "2":
            try:
                with open("./data/catatan.json", "r", encoding="utf-8") as f:
                    catatan = json.load(f)
                if not catatan:
                    print("Belum ada catatan")
                else:
                    for c in catatan:
                        print(f"  {c['judul']}: {c['isi'][:60]}")
            except Exception as e:
                print(f"Error: {e}")
        print()

    def handle_ai_chat(self):
        print()
        print("MODE AI CHAT | Ketik 'kembali' untuk keluar")
        print()
        try:
            from ai_engine import AIEngine
            ai = AIEngine()
        except Exception as e:
            print(f"Error: {e}")
            return
        if not ai.check_status():
            print("Ollama tidak aktif. Pastikan icon llama di system tray.")
            return
        print("AI siap!")
        print()
        while True:
            try:
                pesan = input("Anda > ").strip()
                if pesan.lower() in ["kembali", "exit", "q"]:
                    return
                if not pesan:
                    continue
                jawaban = ai.chat(pesan)
                if jawaban:
                    print(f"{jawaban}\n")
            except KeyboardInterrupt:
                return
            except Exception as e:
                print(f"Error: {e}")

    def exit(self):
        print("Sampai jumpa!")
        return True

    def run(self):
        self.show_banner()
        while True:
            try:
                perintah = input("CLAW > ").strip().lower()
                if not perintah:
                    continue
                if perintah in self.commands:
                    if self.commands[perintah]() is True:
                        break
                else:
                    print("Perintah tidak dikenal. Ketik 'help'.\n")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    CLAW().run()
