# Stil Rehberi — Araç Sahipleri El Kitabı

Bu dosya, kitabın tüm bölümlerinin uyması gereken yazım ve biçim standardını tanımlar.

## Kitap Kimliği

- **Yayıncı:** KUŞCU SİGORTA BİLGİ MERKEZİ — Yayın No: 001
- **Kitap adı:** ARAÇ SAHİPLERİ EL KİTABI
- **Alt başlık:** Kaza • Hasar • Acil Durumlar • Sigorta Süreçleri
- **Hazırlayan:** Abdurrahman KUŞCU — Sigorta Danışmanı
- **Motto:** "Bilgi, doğru zamanda kullanıldığında en güçlü güvencedir."

## Dil ve Ton

1. **"Biz" dili** kullanılır; "ben" dili kullanılmaz. ("Bu rehberde öneriyoruz…")
2. Resmî fakat samimi; okuyucuya üstten bakmayan, güven veren bir ton.
3. Talimat dili yerine sohbet dili: okuyucuyla konuşulur, emir yağdırılmaz.
4. Sade Türkçe; gereksiz sigortacılık terimi kullanılmaz. Kullanılması zorunlu terimler ilk geçtiği yerde bir cümleyle açıklanır.
5. **Reklam yok:** poliçe satışı, şirket övgüsü, "bize ulaşın" çağrısı bölüm metinlerinde YER ALMAZ. Kitabın değeri içeriğidir.
6. **İddia yok:** "Türkiye'nin en iyisi/en kapsamlısı" gibi ifadeler kullanılmaz.
7. **Hukuki temkin:** Mahkemede veya eksper raporunda savunulamayacak hiçbir cümle yazılmaz. Kesin hüküm ("sigorta kesinlikle öder/ödemez") yerine koşullu ifade ("poliçe kapsamına ve olayın koşullarına göre değerlendirilir") kullanılır.
8. Korkutma dili kullanılmaz; risk anlatılır, panik üretilmez.

## Standart İfadeler

- **Bildirim cümlesi (her olay bölümünde aynen):**
  "Sigorta şirketinizi veya sigorta danışmanınızı en kısa sürede bilgilendirin. Araç bir şirket adına kayıtlıysa ayrıca şirket yetkilisine veya filo sorumlusuna bilgi verin."
- **Acil numara standardı:** Türkiye'de tüm acil çağrılar **112** tek numarasında birleşmiştir. Kitapta acil durumlar için yalnızca 112 verilir; polis/jandarma/itfaiye/ambulans ayrımı 112 çağrı merkezince yapılır. (155/156/110 hâlâ çalışır; ancak kitabın standardı 112'dir. Bu fark yalnızca 51. bölümdeki acil iletişim listesinde bir kez açıklanır.)
- Kusur değerlendirmesini **Sigorta Bilgi ve Gözetim Merkezi (SBM)** süreci belirler; olay yerinde kusur tartışması yapılmaz.

## Bölüm Şablonu (6-47 arası olay bölümleri)

Her bölüm dosyası şu sırayla yazılır. Başlık biçimleri aynen korunur:

```markdown
# Bölüm N — Bölüm Adı

*Tek cümlelik bölüm mottosu (italik).*

## 📍 Senaryo

(4-10 satırlık, hikâyeleştirilmiş gerçekçi bir olay. Saat, hava, ortam
detayı verilir. "Şimdi ne yapmalısınız?" benzeri bir soruyla biter.)

## Bu Bölümde Öğrenecekleriniz

(3-6 madde, "…öğreneceksiniz / …bileceksiniz" kalıbıyla.)

## Ayrıntılı Anlatım

(Konunun özü. Gerektiği kadar ara başlık (###) kullanılır. Tanımlar,
süreç mantığı, sigorta boyutu burada anlatılır.)

## ✅ Adım Adım Yapılması Gerekenler

(Numaralı liste; her adım kalın bir başlık + 1-3 cümle açıklama.)

## ❌ Yapılmaması Gerekenler

(Madde listesi; her maddenin neden zararlı olduğu kısaca belirtilir.)

> ### 🤔 Neden?
> (Bölümün en kritik davranış kuralının arkasındaki mantık. En az bir
> tane zorunludur; gerekirse metin içinde birden fazla kullanılabilir.)

> ### 💡 Kuşcu Sigorta Uzman Görüşü
> (Saha tecrübesine dayalı, 2-4 cümlelik pratik değerlendirme.
> Reklamsız, tarafsız.)

> ### 📚 Mevzuat Kutusu
> (Konuyla ilgili temel düzenlemeler madde madde. Yalnızca ilgiliyse.)

## 📋 Kontrol Listesi

(☐ işaretli, olay sonrası tamamlanması gereken işlemler.)

## Uygulamada En Çok Karşılaşılan Sorular

(3-5 soru-cevap. Soru kalın, cevap 2-4 cümle.)

## 📌 Bölüm Özeti

(✔ işaretli 5-8 madde; bir dakikada tekrar edilebilir.)

> ### 🟦 Gerçek Hayattan
> *(Bu bölüm, baskı öncesinde gerçek hasar dosyalarından seçilecek
> örneklerle zenginleştirilecektir.)*
```

## Kutu Standardı

Kutular Markdown alıntı bloğu (`>`) ile yazılır. Kullanılabilecek kutular:

- ⚠️ **Dikkat** — hak kaybı veya güvenlik riski uyarısı
- 💡 **Kuşcu Sigorta Uzman Görüşü** — saha tecrübesi (kişi adıyla kutu açılmaz)
- 📌 **Bilmeniz Gereken** — süreci kolaylaştıran temel bilgi
- 📚 **Mevzuat Kutusu** — ilgili düzenlemeler
- 🤔 **Neden?** — davranış kuralının mantığı
- 🟦 **Gerçek Hayattan** — şimdilik yalnızca yer tutucu metin

## Uzunluk ve Dosya Kuralları

- Olay bölümleri: yaklaşık 600-1.200 kelime. Sayfa doldurma yasak; işine yaramayan içerik kitaba girmez.
- Dosya adı: `NN-turkce-slug.md` (küçük harf, Türkçe karakter yok, tire ile).
- H1 yalnızca bir kez, "Bölüm N — Ad" biçiminde.
- Emoji yalnızca yukarıdaki standart kutu/bölüm başlıklarında kullanılır; metin içinde kullanılmaz.

## Terminoloji

| Doğru | Yanlış / kaçınılacak |
|---|---|
| Kaza Tespit Tutanağı (ilk geçişte), sonra KTT | tutanak formu, anlaşma tutanağı |
| Mobil Kaza Tutanağı (Sigortam360 uygulaması) | mobil KTT uygulaması (eski adlandırmalar) |
| Sigorta Bilgi ve Gözetim Merkezi (SBM) | Tramer (yalnızca halk arasındaki adı olarak bir kez anılabilir) |
| 112 Acil Çağrı Merkezi | 155 Polis İmdat, 156 Jandarma (metin içinde kullanılmaz) |
| sigorta danışmanı | acenteci, sigortacı abi |
| zorunlu trafik sigortası | mecburi sigorta |
| rayiç bedel | piyasa fiyatı |

## Doğruluk

Sayı, süre, kurum adı ve mevzuat bilgisi içeren her cümle
`dogrulanmis-bilgiler.md` dosyasındaki doğrulanmış bilgilere dayanmak
zorundadır. Orada olmayan bir sayı/süre yazılamaz; emin olunmayan bilgi
koşullu dille ("güncel bilgiyi sigorta şirketinizden teyit edin") verilir.
