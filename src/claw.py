"""
CLAW - Coordinator's Local Assistant Worker
Versi 0.1.0 - Alpha
"""

import sys
import os

# Tambah path untuk import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database

class CLAW:
    def __init__(self):
        self.nama = "CLAW"
        self.versi = "0.1.0"
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
        print("  🤖 CLAW - Coordinator's Local Assistant Worker")
        print("  Versi 0.1.0 | Bahasa Indonesia")
        print("=" * 60)
        print()
        print("  Asisten pribadi untuk Koordinator Subseksi")
        print("  Pengukuran Dasar dan Pemetaan & Tematik")
        print("  Kementerian ATR/BPN")
        print()
        print("  Ketik 'help' untuk bantuan")
        print()
    
    def show_help(self):
        """Tampilkan daftar perintah - HANYA SATU METHOD INI"""
        print()
        print("📋 DAFTAR PERINTAH:")
        print("  help      - Tampilkan bantuan ini")
        print("  jadwal    - Kelola jadwal dan reminder")
        print("  catatan   - Buat dan lihat catatan")
        print("  ai        - Chat dengan AI (Qwen 2.5 14B)")
        print("  info      - Info tentang CLAW")
        print("  exit      - Keluar dari CLAW")
        print()
    
    def show_info(self):
        print()
        print("ℹ️  TENTANG CLAW")
        print(f"  Nama: {self.nama}")
        print(f"  Versi: {self.versi}")
        print(f"  Status: Alpha Development")
        print()
        print("  Fitur yang akan datang:")
        print("  • Chat dengan AI Lokal (Qwen 2.5)")
        print("  • Proactive reminders")
        print("  • Template dokumen ATR/BPN")
        print("  • Integrasi dengan Ollama")
        print()
    
    def handle_jadwal(self):
        print()
        print("📅 MENU JADWAL")
        print("  1. Tambah jadwal")
        print("  2. Lihat jadwal")
        print("  3. Kembali")
        print()
        
        pilihan = input("Pilih (1-3): ").strip()
        
        if pilihan == "1":
            judul = input("Judul: ").strip()
            tanggal = input("Tanggal (YYYY-MM-DD): ").strip()
            waktu = input("Waktu (HH:MM): ").strip()
            kategori = input("Kategori (rapat/deadline/umum): ").strip() or "umum"
            
            if judul and tanggal:
                hasil = self.db.tambah_jadwal(judul, tanggal, waktu, kategori)
                print(f"\n✅ Jadwal ditambahkan: {hasil['judul']}")
            else:
                print("\n❌ Judul dan tanggal wajib diisi!")
            
        elif pilihan == "2":
            jadwal = self.db.lihat_jadwal()
            if not jadwal:
                print("\n📭 Belum ada jadwal")
            else:
                print("\n📋 DAFTAR JADWAL:")
                for j in jadwal:
                    status = "✅" if j['selesai'] else "⏳"
                    print(f"  {status} {j['tanggal']} {j['waktu']} - {j['judul']} ({j['kategori']})")
        
        print()
    
    def handle_catatan(self):
        print()
        print("📝 MENU CATATAN")
        print("  1. Tambah catatan")
        print("  2. Lihat catatan")
        print("  3. Kembali")
        print()
        
        pilihan = input("Pilih (1-3): ").strip()
        
        if pilihan == "1":
            judul = input("Judul: ").strip()
            isi = input("Isi: ").strip()
            
            if judul and isi:
                tags_input = input("Tags (pisah koma, opsional): ").strip()
                tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
                
                hasil = self.db.tambah_catatan(judul, isi, tags)
                print(f"\n✅ Catatan disimpan: {hasil['judul']}")
            else:
                print("\n❌ Judul dan isi wajib diisi!")
            
        elif pilihan == "2":
            import json
            try:
                with open("./data/catatan.json", 'r', encoding='utf-8') as f:
                    catatan = json.load(f)
                
                if not catatan:
                    print("\n📭 Belum ada catatan")
                else:
                    print("\n📋 DAFTAR CATATAN:")
                    for c in catatan:
                        print(f"  • {c['judul']}: {c['isi'][:50]}...")
            except Exception as e:
                print(f"\n❌ Error membaca catatan: {e}")
        
        print()
    
    def handle_ai_chat(self):
        """Mode chat dengan AI"""
        print()
        print("🤖 MODE AI CHAT")
        print("  Ketik pesanmu untuk berbicara dengan AI")
        print("  Ketik 'kembali' untuk keluar dari mode AI")
        print()
        
        try:
            from ai_engine import AIEngine
            ai = AIEngine()
        except ImportError as e:
            print(f"❌ Error import AI Engine: {e}")
            return
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        if not ai.check_status():
            print("❌ Ollama tidak berjalan. Tidak bisa chat dengan AI.")
            print("   Pastikan Ollama aktif di system tray (icon 🦙).")
            return
        
        print("✅ AI siap! Mulai chat...")
        print("(Ketik 'kembali' untuk keluar)")
        print()
        
        while True:
            try:
                pesan = input("Anda > ").strip()
                
                if pesan.lower() in ['kembali', 'exit', 'quit', 'q']:
                    print("👋 Keluar dari mode AI chat.")
                    print()
                    return  # ← Gunakan return, bukan break
                
                if not pesan:
                    continue
                
                print("🤖 AI sedang berpikir...")
                jawaban = ai.chat(pesan)
                print(f"\n{jawaban}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Keluar dari mode AI...")
                return
            except EOFError:
                print("\n❌ Input terputus.")
                return
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Coba lagi atau ketik 'kembali' untuk keluar.\n")
    
    def exit(self):
        print()
        print("👋 Sampai jumpa! CLAW siap membantu kapan saja.")
        print()
        return True
    
    def run(self):
        self.show_banner()
        
        while True:
            try:
                perintah = input("CLAW > ").strip().lower()
                
                if not perintah:
                    continue
                
                if perintah in self.commands:
                    result = self.commands[perintah]()
                    if result is True:
                        break
                else:
                    print("\n❓ Perintah tidak dikenal. Ketik 'help' untuk bantuan.\n")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Keluar...")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    claw = CLAW()
    claw.run()