"""
Database sederhana untuk CLAW
Menyimpan jadwal, catatan, dan memory
"""

import json
import os
from datetime import datetime

class Database:
    def __init__(self, data_dir="./data"):
        self.data_dir = data_dir
        self._ensure_files()
    
    def _ensure_files(self):
        """Pastikan file database ada"""
        files = {
            "jadwal.json": [],
            "catatan.json": [],
            "memory.json": []
        }
        
        for filename, default in files.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(default, f, indent=2, ensure_ascii=False)
    
    def tambah_jadwal(self, judul, tanggal, waktu, kategori="umum"):
        """Tambah jadwal baru"""
        filepath = os.path.join(self.data_dir, "jadwal.json")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            jadwal = json.load(f)
        
        jadwal_baru = {
            "id": len(jadwal) + 1,
            "judul": judul,
            "tanggal": tanggal,
            "waktu": waktu,
            "kategori": kategori,
            "dibuat": datetime.now().isoformat(),
            "selesai": False
        }
        
        jadwal.append(jadwal_baru)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(jadwal, f, indent=2, ensure_ascii=False)
        
        return jadwal_baru
    
    def lihat_jadwal(self, hari="semua"):
        """Lihat jadwal"""
        filepath = os.path.join(self.data_dir, "jadwal.json")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            jadwal = json.load(f)
        
        if hari == "semua":
            return jadwal
        
        # Filter berdasarkan hari (simplified)
        return [j for j in jadwal if hari in j['tanggal']]
    
    def tambah_catatan(self, judul, isi, tags=None):
        """Tambah catatan"""
        filepath = os.path.join(self.data_dir, "catatan.json")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            catatan = json.load(f)
        
        catatan_baru = {
            "id": len(catatan) + 1,
            "judul": judul,
            "isi": isi,
            "tags": tags or [],
            "dibuat": datetime.now().isoformat()
        }
        
        catatan.append(catatan_baru)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(catatan, f, indent=2, ensure_ascii=False)
        
        return catatan_baru

# Test
if __name__ == "__main__":
    db = Database()
    print("Database siap!")
    print("File tersedia:")
    for f in os.listdir("./data"):
        print(f"  - {f}")