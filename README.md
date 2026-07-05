# Flashcard PWA - Backend API

Bu proje, bir Flashcard Progressive Web App (PWA) uygulamasının backend sistemidir. [FastAPI](https://fastapi.tiangolo.com/) kullanılarak geliştirilmiş olup, veritabanı olarak **PostgreSQL** ve ORM olarak **SQLAlchemy** kullanmaktadır.

## 🚀 Özellikler

- **Hızlı ve Modern**: FastAPI sayesinde yüksek performanslı, asenkron ve kolay geliştirilebilir.
- **Kullanıcı Doğrulama (Auth)**: JWT tabanlı güvenli kimlik doğrulama, şifre hashleme (Bcrypt).
- **CRUD İşlemleri**: Flashcard (Bilgi Kartı) oluşturma, okuma, güncelleme ve silme.
- **Öğrenme Sistemi (Review)**: Kartları tekrarlama ve gözden geçirme (Spaced Repetition vb.) için özel uç noktalar (endpoints).
- **Otomatik API Dokümantasyonu**: FastAPI'nin sunduğu hazır Swagger UI ve ReDoc entegrasyonu.

## 🛠️ Teknolojiler

- **Python 3.x**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Pydantic**
- **Docker & Docker Compose**

## 🏛️ Mimari ve Proje Yapısı

Proje, sürdürülebilirliği ve test edilebilirliği artırmak adına katmanlı bir mimari yaklaşımıyla tasarlanmıştır. Her katman kendi sorumluluğuna sahiptir:

1. **Routers (Kontrolcüler / Endpoints)**: Gelen HTTP isteklerini karşılar, veriyi doğrular (Pydantic şemaları ile) ve iş katmanına iletir. 
2. **Services (İş Mantığı)**: Aralıklı tekrar algoritması ve dış API (Pexels) entegrasyonu gibi temel iş kurallarının koşturulduğu çekirdek katmandır.
3. **CRUD (Veri Erişim Katmanı)**: Veritabanı ile doğrudan iletişime geçen, `SQLAlchemy` sorgularını barındıran katmandır.
4. **Models (Veritabanı Modelleri)**: Veritabanı tablolarının Python nesnesi olarak karşılıklarıdır (ORM nesneleri).
5. **Schemas (Pydantic Modelleri)**: API üzerinden alınan ve gönderilen verinin tip denetimini ve serileştirilmesini/seri dışına çıkarılmasını (serialization/deserialization) sağlar.

```bash
backend/
├── crud/           # Veritabanı işlemleri (Create, Read, Update, Delete)
├── models/         # SQLAlchemy veritabanı modelleri
├── routers/        # FastAPI endpoint (route) tanımlamaları (auth, flashcards, review)
├── schemas/        # Pydantic modelleri (Veri doğrulama ve serileştirme)
├── services/       # İş mantığı ve yardımcı servisler
├── config.py       # Uygulama ayarları (Çevre değişkenleri yönetimi)
├── database.py     # Veritabanı bağlantısı ayarları ve Session yönetimi
└── main.py         # FastAPI ana uygulama dosyası
```

### Services Katmanı Detayları
Uygulamanın temel öğrenme ve zenginleştirme mantığı **Services** katmanında soyutlanmıştır:
- **Aralıklı Tekrar Algoritması**: Kullanıcının bir karta verdiği cevaba göre, o kartın tekrar ne zaman gözden geçirileceğini hesaplayan algoritmadır. Öğrenilmesi zor olan kartların daha sık, kolay öğrenilenlerin ise daha seyrek gösterilmesini sağlayarak öğrenme verimini maksimize eder.
- **Pexels API Entegrasyonu**: Kartların görsel hafıza ile daha iyi hatırlanması için Pexels üzerinden dinamik olarak yüksek kaliteli stok görseller çekilir. Bu servis entegrasyonu, kullanıcıların kart oluştururken diledikleri anahtar kelimeye göre otomatik görsel bulmalarına olanak tanır.
### Veritabanı Yönetimi
Projeyle ilişkili veritabanı tabloları, `database.py` üzerinde oluşturulan yapılandırma ile PostgreSQL'e bağlanır. `Base.metadata.create_all` mantığı kullanılarak tabloların şemaları ayağa kalkarken senkronize edilir.

### Güvenlik ve Yetkilendirme
API güvenliği, OAuth2 standartlarına uygun olarak tasarlanmış JWT (JSON Web Token) tabanlı bir sistemle sağlanmaktadır. Kullanıcı şifreleri veritabanına kaydedilirken `bcrypt` algoritması ile tek yönlü olarak hashlenmektedir.

## 📚 Temel API Endpointleri (v2)

REST standartlarına uygun olarak güncellenmiş yeni endpointler:

- **Auth** (`/api/v2/auth`)
  - `/register` (POST): Yeni kullanıcı kaydı.
  - `/login` (POST): Kullanıcı girişi ve token alınması.
- **Users** (`/api/v2/users`)
  - `/me/stats` (GET): Kullanıcının öğrenme istatistikleri.
- **Cards** (`/api/v2/cards`)
  - `/` (GET, POST): Kendi kartlarınızı listeleme ve yeni kart oluşturma.
  - `/{card_id}` (PATCH, DELETE): Belirli bir kartı güncelleme ve silme.
  - `/public` (GET): Herkese açık (public) paylaşılan kartları listeleme.
  - `/images/search` (GET): Pexels üzerinden kelimeye uygun görsel arama.
- **Reviews** (`/api/v2/reviews`)
  - `/due-progress` (GET): Bugün çalışılması gereken kartların ilerleme (progress) verilerini getirir.
  - `/library` (GET): Kullanıcının tüm kartlarına ait ilerleme verilerini getirir.
  - `/due` (GET): Bugün çalışılması gereken (süresi gelmiş) kartları getirir.
  - `/` (PUT): Öğrenme seansında karta verilen cevaba göre (0: Unuttum, 1: Zor, 2: Kolay vs.) aralıklı tekrar algoritmasını (Spaced Repetition) çalıştırır.
  - `/progress/{card_id}` (GET): Belirli bir kartın sonraki tekrar tarihini ve çalışma istatistiklerini getirir.

*(API dökümantasyonunun tam detaylı ve interaktif hali uygulama çalışırken `/docs` veya `/redoc` adreslerinden incelenebilir.)*

## ⚙️ Kurulum ve Çalıştırma 

Uygulama aktif olarak deploy edilmiş durumdadır. Ancak projeyi yerelde test etmek isterseniz şu adımları izleyebilirsiniz:

1. Depoyu klonlayıp sanal ortam (venv) oluşturun.
2. `pip install -r requirements.txt` ile bağımlılıkları yükleyin.
3. `.env` dosyası oluşturarak `DATABASE_URL` (PostgreSQL) ve `SECRET_KEY` değişkenlerini ayarlayın.
4. Uygulamayı `uvicorn main:app --reload` ile başlatın.
5. (Opsiyonel) Proje Docker desteği de sunar: `docker-compose -f docker-compose.prod.yml up -d --build`.
