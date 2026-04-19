# Skill: Jadwal

## Deskripsi
Mengelola jadwal, reminder, dan deadline untuk Koordinator Subseksi Pengukuran Dasar dan Pemetaan & Tematik.

## Tools
- `jadwal_tambah(judul, tanggal, waktu, kategori)` - Tambah jadwal baru
- `jadwal_lihat(hari)` - Lihat jadwal hari tertentu
- `jadwal_hapus(judul)` - Hapus jadwal
- `reminder_cek()` - Cek reminder yang akan datang

## Contoh Penggunaan
User: "Rapat koordinasi besok jam 10"
→ jadwal_tambah(judul="Rapat Koordinasi", tanggal="besok", waktu="10:00", kategori="rapat")

User: "Deadline laporan pemetaan 25 April"
→ jadwal_tambah(judul="Laporan Pemetaan", tanggal="2026-04-25", waktu="23:59", kategori="deadline")

## Format Penyimpanan
Data disimpan di: `./data/jadwal.json`