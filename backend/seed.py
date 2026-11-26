"""Sample articles inserted into an empty database so the site is never blank."""

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Article

# Cover images are left empty on purpose: the frontend then shows the category's
# own illustration, so the demo works without any external image host.
SAMPLE_ARTICLES = [
    {
        "slug": "kaygi-ve-uyku-iliskisi",
        "title": "Kaygı ve Uyku İlişkisi",
        "category": "uyku-ve-beden",
        "date": date(2026, 3, 10),
        "summary": "Kaygı uykuyu, uykusuzluk da kaygıyı besler. Bu döngüyü kırmak için küçük ama etkili adımlar.",
        "content": (
            "<p>Kaygı ile uyku arasında iki yönlü bir ilişki vardır. Zihin akşam saatlerinde yarının "
            "planlarıyla meşgulken uykuya dalmak zorlaşır; yetersiz uyku ise ertesi gün kaygıya karşı "
            "daha savunmasız hissetmemize yol açar.</p>"
            "<h2>Döngüyü fark etmek</h2>"
            "<p>İlk adım, yatakta geçirilen zamanın düşünme zamanına dönüşüp dönüşmediğini fark etmektir. "
            "Yirmi dakikadan uzun süre uyuyamıyorsanız kalkıp loş ışıkta sakin bir şeyle ilgilenmek, "
            "yatağı yeniden uykuyla eşleştirmeye yardım eder.</p>"
            "<h2>Uyku hijyeni</h2>"
            "<ul><li>Her gün aynı saatte kalkmak</li><li>Yatmadan bir saat önce ekranları bırakmak</li>"
            "<li>Öğleden sonra kafeini azaltmak</li><li>Endişeleri yatmadan önce bir kâğıda yazmak</li></ul>"
            "<p>Bu adımlar kısa sürede mucize yaratmaz ama birkaç hafta düzenli uygulandığında fark edilir. "
            "Uyku sorunu uzun süredir devam ediyorsa bir uzmana danışmak en doğru adımdır.</p>"
        ),
    },
    {
        "slug": "oz-sefkat-nedir",
        "title": "Öz Şefkat Nedir?",
        "category": "farkindalik",
        "date": date(2026, 3, 2),
        "summary": "Kendinize, zor bir gün geçiren bir arkadaşınıza davrandığınız kadar nazik davranmak.",
        "content": (
            "<p>Öz şefkat, zorlandığımız anlarda kendimize eleştiri yerine anlayışla yaklaşmaktır. "
            "Hata yaptığımızda içimizdeki sesin tonu, bir sonraki adımı atma isteğimizi doğrudan etkiler.</p>"
            "<h2>Üç temel bileşen</h2>"
            "<p><strong>Nezaket:</strong> kendini yargılamak yerine destekleyici bir dil kullanmak. "
            "<strong>Ortak insanlık:</strong> zorlanmanın herkesin yaşadığı bir deneyim olduğunu hatırlamak. "
            "<strong>Farkındalık:</strong> duyguyu bastırmadan ya da büyütmeden olduğu gibi görmek.</p>"
            "<p>Küçük bir egzersiz: zor bir anda elinizi göğsünüze koyup kendinize 'Bu şu an zor ve "
            "zorlanmam çok normal' demeyi deneyin.</p>"
        ),
    },
    {
        "slug": "basarinin-psikolojisi-kucuk-adimlarin-gucu",
        "title": "Başarının Psikolojisi: Küçük Adımların Gücü",
        "category": "kisisel-gelisim",
        "date": date(2026, 2, 22),
        "summary": "Büyük hedefler, her gün atılan küçük ve sürdürülebilir adımlarla gerçeğe dönüşür.",
        "content": (
            "<p>Başarı, büyük hedeflere ulaşmak için atılan küçük adımların toplamıdır. Küçük adımlar "
            "motivasyonu artırır, özgüveni güçlendirir ve sürdürülebilir bir ilerleme için sağlam bir "
            "temel oluşturur.</p>"
            "<h2>Neden küçük?</h2>"
            "<p>Beyin, tamamlanan her görevi bir ödül olarak algılar. Hedefi 'her gün 10 dakika' gibi "
            "küçük parçalara bölmek, başlamanın önündeki direnci azaltır ve süreklilik sağlar.</p>"
            "<p>Bugün atabileceğiniz en küçük adım nedir? Onu yazın ve hemen başlayın.</p>"
        ),
    },
    {
        "slug": "sinir-koymak-sevgisizlik-degildir",
        "title": "Sınır Koymak Sevgisizlik Değildir",
        "category": "iliskiler",
        "date": date(2026, 2, 12),
        "summary": "Sağlıklı sınırlar ilişkileri uzaklaştırmaz, aksine onları daha güvenli hâle getirir.",
        "content": (
            "<p>Birçoğumuz 'hayır' demeyi karşımızdakini kırmakla eş tutarız. Oysa net sınırlar, "
            "ilişkide iki tarafın da neyi bekleyebileceğini bilmesini sağlar ve kırgınlıkların "
            "birikmesini önler.</p>"
            "<h2>Sınırı nazikçe ifade etmek</h2>"
            "<p>'Ben' diliyle konuşmak işe yarar: 'Akşamları dinlenmeye ihtiyacım var, bu yüzden "
            "telefonlara sabah dönmek istiyorum.' Açıklama kısa, ton sakin olsun.</p>"
            "<p>İlk denemeler rahatsız hissettirebilir; bu, yanlış bir şey yaptığınız anlamına gelmez.</p>"
        ),
    },
    {
        "slug": "stresle-basa-cikmanin-yollari",
        "title": "Stresle Başa Çıkmanın Yolları",
        "category": "kaygi-ve-stres",
        "date": date(2026, 1, 15),
        "summary": "Günlük hayatın stresiyle başa çıkmak için kısa ve uygulanabilir stratejiler.",
        "content": (
            "<p>Stres, vücudun zorluklara verdiği doğal bir tepkidir. Sorun stresin kendisi değil, "
            "uzun süre dinmeden devam etmesidir.</p>"
            "<h2>4-7-8 nefes tekniği</h2>"
            "<p>Dört saniye nefes alın, yedi saniye tutun, sekiz saniyede verin. Birkaç tekrar, "
            "sinir sistemine 'güvendesin' mesajı verir.</p>"
            "<h2>Gün içinde mikro molalar</h2>"
            "<p>Her doksan dakikada bir, beş dakikalık bir yürüyüş ya da pencereden dışarı bakmak "
            "dikkatin toparlanmasına yardım eder.</p>"
        ),
    },
    {
        "slug": "kaygi-bir-alarm-sistemidir",
        "title": "Kaygı Bir Alarm Sistemidir",
        "category": "kaygi-ve-stres",
        "date": date(2026, 1, 5),
        "summary": "Kaygının işlevini anlamak, onunla savaşmak yerine onu yönetmeyi kolaylaştırır.",
        "content": (
            "<p>Kaygı, bizi tehlikeye karşı uyaran eski ve kullanışlı bir alarm sistemidir. Bazen ise "
            "gerçek bir tehlike yokken de çalar: bir sunum, bir mesajın geç gelmesi ya da belirsiz "
            "bir gelecek.</p>"
            "<h2>Alarmı susturmak yerine dinlemek</h2>"
            "<p>'Şu an gerçekten tehlikede miyim?' sorusu, düşünceyle gerçeği ayırmaya yardım eder. "
            "Kaygıyı adlandırmak bile yoğunluğunu azaltabilir.</p>"
        ),
    },
    {
        "slug": "erteleme-tembellik-degil",
        "title": "Erteleme Tembellik Değil, Duygu Yönetimidir",
        "category": "kisisel-gelisim",
        "date": date(2025, 12, 20),
        "summary": "İşleri ertelememizin asıl nedeni çoğu zaman görevin uyandırdığı rahatsız duygulardır.",
        "content": (
            "<p>Erteleme genellikle zaman yönetimi sorunu olarak görülür. Araştırmalar ise çoğu zaman "
            "görevin uyandırdığı sıkıntı, belirsizlik ya da başarısızlık korkusundan kaçtığımızı gösterir.</p>"
            "<h2>Beş dakika kuralı</h2>"
            "<p>Kendinize yalnızca beş dakika çalışma sözü verin. Başladıktan sonra devam etmek, "
            "başlamaktan çok daha kolaydır.</p>"
        ),
    },
    {
        "slug": "dinlemek-bir-beceridir",
        "title": "Dinlemek Bir Beceridir",
        "category": "iliskiler",
        "date": date(2025, 12, 8),
        "summary": "Cevap vermek için değil, anlamak için dinlemek ilişkileri nasıl değiştirir?",
        "content": (
            "<p>Konuşurken çoğumuz karşımızdakini dinlemek yerine vereceğimiz cevabı hazırlarız. "
            "Etkin dinleme, karşımızdakinin söylediğini ve hissettiğini kendi cümlelerimizle geri "
            "yansıtmaktır.</p>"
            "<p>'Yani bu durum seni yalnız hissettirdi, doğru mu anladım?' gibi bir cümle, "
            "tavsiyeden çok daha fazla iyi gelebilir.</p>"
        ),
    },
]


def seed_if_empty(db: Session) -> int:
    if db.scalar(select(func.count()).select_from(Article)):
        return 0
    db.add_all(Article(author="Psikopedi", **data) for data in SAMPLE_ARTICLES)
    db.commit()
    return len(SAMPLE_ARTICLES)
