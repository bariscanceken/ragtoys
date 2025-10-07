## ragtoys

Bu proje, hayali bir şirket olan "ragtoys" için RAG (Retrieval-Augmented Generation) destekli bir etkileşim uygulamasıdır. Kullanıcılar oyuncak tasarımları çizerek bir yarışmaya katılır; çizimlerini kaydedip/gönderir ve asistanla sohbet eder. Asistanın ürettiği son yanıt ElevenLabs TTS ile otomatik seslendirilir. Amaç, çocukların hayal gücünü oyuncak tasarımlarına dönüştüren bir yarışma deneyimi sunmaktır.

### Özellikler
- Çizim tuvali (Streamlit Drawable Canvas)
- Çizimi kaydetme ve gönderme akışı (SQLite)
- RAG tabanlı yanıt üretimi (LangChain + LangGraph)
- ElevenLabs ile son asistan mesajını otomatik seslendirme (gizli autoplay)
- Kullanıcı kayıt/girişi, e-posta doğrulama ve şifre sıfırlama

## Gereksinimler
- Python 3.10+
- Windows (test edilen ortam)

### Bağımlılıklar
Tüm bağımlılıklar `requirements.txt` içerisinde listelidir:
- Streamlit, streamlit-drawable-canvas, Pillow
- LangChain, LangGraph, Chroma eklentileri
- ElevenLabs SDK
- bcrypt, python-dotenv, vb.

## Kurulum
1) Sanal ortam oluşturun (önerilir):
```bash
python -m venv .venv
.venv\\Scripts\\activate
```

2) Bağımlılıkları kurun:
```bash
pip install -r requirements.txt
```

3) Ortam değişkenlerini ayarlayın:
- Proje kök dizinine `.env` dosyası oluşturun ve aşağıdaki anahtarları ekleyin (ihtiyaçlarınıza göre düzenleyin):
```env
# ElevenLabs (TTS) zorunlu
ELEVEN_API_KEY=YOUR_ELEVENLABS_API_KEY

# OpenAI (RAG için LangChain / LangGraph zincirlerinde gerekebilir)
OPENAI_API_KEY=YOUR_OPENAI_API_KEY

# Tavsiye: web araması için (kullanıyorsanız)
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

## Çalıştırma
Streamlit uygulamasını başlatın:
```bash
streamlit run main.py
```

Uygulama açıldığında giriş/kayıt ekranını göreceksiniz. Giriş yaptıktan sonra ana sayfaya yönlendirilirsiniz.

## Kullanım
- Sol tarafta çizim tuvali bulunur. Çizgi kalınlığı/renk/arka plan ayarlarını soldaki menüden yapın.
- "Çizimi Kaydet" ile tuvali veritabanına kaydedin.
- "Çizimi Gönder" ile mevcut tuvali veya son kaydı `sent` tablosuna gönderin; görsel anlık olarak görüntülenir.
- Sağ sütunda sohbet alanı bulunur. Mesaj yazdığınızda RAG akışı tetiklenir; yanıt aynı alanda görünür.
- Asistanın son mesajı ElevenLabs TTS ile otomatik çalınır (gizli `<audio autoplay>`; dosya diske yazılmaz).

## Yapı ve Önemli Dosyalar
- `main.py`: Streamlit arayüzü, çizim/sohbet akışı, TTS entegrasyonu
- `graph/`: LangGraph akışı ve düğümler
  - `graph/graph.py`: akış tanımı ve derleme
  - `graph/nodes/`: retrieve/generate/grade/web_search düğümleri
- `ingestion.py`: veri alımı/indeksleme (varsa kullanımınıza göre uyarlayın)

### Dosya Yapısı
```
ragtoys/
  docs/
    ragtoys.pdf
  graph/
    graph.py
    node_constans.py
    state.py
    chains/
      answer_grader.py
      generation.py
      hallucination_grader.py
      retrieval_grader.py
      router.py
    nodes/
      generate.py
      grade_documents.py
      retrieve.py
      web_search.py
  ingestion.py
  main.py
  README.md
  requirements.txt
  graph.png
  logo.jpeg
```

## Veritabanı
- Varsayılan SQLite dosya yolu kod içerisinde sabittir: 
`ragtoys.db`
- Kendi ortamınıza göre yolu güncelleyebilirsiniz.

## Ortam Değişkenleri
- `ELEVEN_API_KEY` (zorunlu): ElevenLabs API anahtarı, TTS için kullanılır.
- `OPENAI_API_KEY` (opsiyonel): RAG akışında OpenAI model(ler)i kullanılıyorsa gerekir.
- `TAVILY_API_KEY` (opsiyonel): Web araması için Tavily kullanılıyorsa gerekir.

Örnek `.env` içeriği:
```env
# ElevenLabs (TTS) zorunlu
ELEVEN_API_KEY=YOUR_ELEVENLABS_API_KEY

# RAG için OpenAI (opsiyonel)
OPENAI_API_KEY=YOUR_OPENAI_API_KEY

# Web araması için Tavily (opsiyonel)
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

Notlar:
- Varsayılan SQLite veritabanı yolu `main.py` içinde sabit tanımlıdır (`ragtoys.db`). Kendi ortamınıza göre bu yolu kodda güncelleyebilirsiniz.

## Sorun Giderme
- Ses çalmıyor: Tarayıcıda otomatik oynatma kısıtları olabilir. Sayfayla etkileşime (tıklama) geçtikten sonra deneyin. `ELEVEN_API_KEY` değerini doğrulayın.
- Ses kalitesi düşük: `main.py` içinde `output_format` veya `model_id` değerlerini yükseltebilirsiniz (örn. `mp3_44100_128`, `eleven_multilingual_v2`).
- Veritabanı hatası: SQLite yolunu ve dosya izinlerini kontrol edin.

## Lisans
Bu proje MIT lisansı ile lisanslanmıştır. Ayrıntılar için `LICENSE` dosyasına bakın.