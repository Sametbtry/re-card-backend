from database import engine
from sqlalchemy import text

def run_migration():
    try:
        with engine.begin() as con:
            con.execute(text('ALTER TABLE flashcards ADD COLUMN example_translation TEXT;'))
            print("Başarılı: 'example_translation' kolonu 'flashcards' tablosuna eklendi.")
    except Exception as e:
        print("Bilgi: Kolon zaten eklenmiş olabilir veya bir hata oluştu:", e)

if __name__ == '__main__':
    run_migration()
