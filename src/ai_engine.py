"""
AI Engine untuk CLAW
Menghubungkan CLAW dengan Ollama (AI Lokal)
"""

import requests
import json
from typing import List, Dict, Optional

class AIEngine:
    def __init__(self, model: str = "qwen2.5:14b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_generate = f"{base_url}/api/generate"
        self.api_chat = f"{base_url}/api/chat"
        self.conversation_history: List[Dict] = []
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Kirim pesan ke AI dan dapatkan jawaban
        """
        try:
            # Build messages
            messages = []
            
            # System prompt (personality CLAW)
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            else:
                messages.append({
                    "role": "system",
                    "content": self._get_default_system_prompt()
                })
            
            # Add history (last 5 conversations)
            messages.extend(self.conversation_history[-10:])
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Send to Ollama
            response = requests.post(
                self.api_chat,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 2048
                    }
                },
                timeout=300  # ← 5 menit untuk task kompleks
        )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result["message"]["content"]
                
                # Save to history
                self.conversation_history.append({
                    "role": "user",
                    "content": message
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                # Trim history if too long (keep last 20)
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
                return assistant_message
            else:
                return f"❌ Error: AI tidak merespons (Status {response.status_code})"
                
        except requests.exceptions.ConnectionError:
            return "❌ Error: Tidak bisa terhubung ke Ollama. Pastikan Ollama berjalan di background."
        except requests.exceptions.Timeout:
            return "❌ Error: AI terlalu lama merespons. Coba lagi."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _get_default_system_prompt(self) -> str:
        """
        Personality CLAW untuk AI
        """
        return """Kamu adalah CLAW (Coordinator's Local Assistant Worker), asisten pribadi untuk Koordinator Subseksi Pengukuran Dasar dan Pemetaan & Tematik di Kementerian ATR/BPN.

Karakteristikmu:
- Profesional tapi ramah
- Berbahasa Indonesia yang baik dan formal
- Memahami istilah pertanahan, pemetaan, dan administrasi pemerintahan
- Inisiatif dalam memberikan saran
- Selalu menggunakan bahasa Indonesia dalam merespons

Kamu membantu dengan:
- Jadwal dan reminder pekerjaan
- Catatan dan ringkasan
- Template dokumen administrasi
- Informasi terkait pertanahan dan pemetaan
- Pengingat deadline dan rapat

Jawabanmu harus:
- Jelas dan terstruktur
- Singkat tapi informatif
- Menggunakan format yang mudah dibaca (bullet points, numbering)
- Profesional sesuai konteks pemerintahan"""
    
    def clear_history(self):
        """Hapus riwayat percakapan"""
        self.conversation_history = []
    
    def check_status(self) -> bool:
        """Cek apakah Ollama berjalan"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False


# Test
if __name__ == "__main__":
    print("🤖 Testing AI Engine...")
    ai = AIEngine()
    
    if ai.check_status():
        print("✅ Ollama terhubung!")
        print("💬 Testing chat...")
        response = ai.chat("Halo, perkenalkan dirimu!")
        print(f"\nAI: {response}")
    else:
        print("❌ Ollama tidak terhubung. Pastikan Ollama berjalan.")