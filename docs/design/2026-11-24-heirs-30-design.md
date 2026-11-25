# Dünyanın Mirasçıları 3.0 "Kum, Dağ ve Yol" – tasarım eki

Ana tasarım: `2026-11-24-heirs-of-earth-design.md`. Bu ek, oradaki 3.0 satırını uygulanabilir hale getirir.
Kullanıcı nasıl yapılacağını bana bıraktı ("sonra 3.0'a geç"); aşağıdaki her karar benim kararımdır ve düzeltilebilir.

## Amaç
- Dokuz devletin son üçünü eklemek: Yeni Kemet, Pars, İnti. Her biri Hellas/Tianxia/Albion ile aynı derinlikte.
- Barışçıl oyuncuya uzun vadeli bir ekonomi vermek: ticaret yolları.
- Oyuna bir hedef vermek: Dünya Konseyi (barışla birleşme ya da tek güç olarak hükmetme). Oyun bitince oyuncu devam edebilir.

## Kapsam dışı
- DLC ekleri (3.x).
- Yeni dünya haritası nesneleri (yol çizimi vb.). Ticaret yolları arayüzde ve mektuplarda yaşar, haritaya çizilmez.
- Oyuncunun yerleşim ele geçirmesi için yeni savaş mekaniği. Vanilla yerleşim yok etme kullanılır.

## 1. Üç devlet (her biri: ~16 araştırma, 6-7 gelenek, 3-4 silah, 3 kıyafet, 2-3 bina, 1 zemin, yemek, ticaret malı, 7 birim türü, 12 geçmiş, senaryo, arşiv, 4-5 adımlı zincir, efsanevi eser)
Sanayi satırı baştan gelir (2.1'de ilk üç devlete eklenen gibi).

| Devlet | Renk / amblem | İmzalar | Gelenekler (örnek) | Zincir ve eser |
|---|---|---|---|---|
| Yeni Kemet Krallığı | kum altını + lacivert, şahin | khopesh, kompozit yay, keten kalasiris, nemes başlık, dikili taş, papirüs atölyesi (papirüs → kitap/bilgi), sulama kanalı zemini, ekmek | Nehir Toprağı (hasat verimi), Kâtip Okulu, Güneş Takvimi, Taş Ustaları, Nil Mühendisliği (sanayi) | "Kum Altındaki Şehir" → Güneş Diski (gökyüzünü açar, ruh hâli) |
| Pars Satraplığı | lal kırmızısı + altın, griffin | pul zırh, ipek kaftan, kanatlı miğfer, akinakes, Pers bahçesi (güzellik + eğlence), halı tezgâhı (halı = ticaret/sanat malı), jezail (sanayi) | Kraliyet Postası (kervan hızı, ticaret fiyatı), Satrap Hukuku, Bahçe Kültürü, Ölümsüzler | "Kraliyet Yolu" → Kralın Gözü (tüm devletlerle ilişki artışı + kervan ziyareti) |
| İnti İmparatorluğu | kırmızı-turuncu + toprak yeşili, kondor | sapan, makana sopası, alpaka yünü tunik, teras zemini (verimli), kollka ambarı (yiyecek çürümesini yavaşlatır), kipu kayıt masası (araştırma tesisi) | Kollka (yiyecek bozulma süresi), Mit'a (inşaat), Dağ Akciğeri (yürüme/dayanıklılık), Chaski Koşucuları | "Düğümlerin Dili" → Altın İp (kıtlıkta tüm koloniye yiyecek) |

Dostluk/rekabet: Kemet ↔ Hellas dost, Pars ↔ Tianxia dost (İpek Yolu), Pars ↔ Roma rakip, İnti tek başına (nötr), İnti ↔ Albion rakip.
Dini ve modern ülke sembolleri kullanılmaz (şahin, griffin, kondor amblemleri).

## 2. Ticaret yolları
- Mirasçılar sekmesinde yeni bölüm "Ticaret Yolları".
- Şart: devletle iyi ilişki (goodwill ≥ 25), devlet oyuncuya düşman değil, en fazla 3 yol (Pars Kraliyet Postası ile 4).
- Kurma bedeli: gümüş (mesafeye göre 400–900). Her 15 günde bir yol kervanı gelir: o devletin ticaret malları + gümüş (değer ≈ kurma bedelinin %35'i, Kraliyet Postası ile %50).
- Yol riskleri: devlet bir savaştaysa her sefer %25 ihtimalle kervan yağmalanır (mektup). Devlet oyuncuya düşman olursa yol kapanır.
- Her başarılı sefer devletle +2 ilişki verir. Kronik kaydı tutulur.
- Ayardan kapatılabilir (siyaset ayarına bağlı).

## 3. Dünya Konseyi (oyun sonu)
- Açılma: oyuncu en az 3 devlet zincirini bitirmiş ya da 3 ticaret yolu 1 yıl boyunca açık kalmış olmalı. Açıldığında mektup gelir ve "Konsey Salonu" binası araştırılabilir.
- Konsey Salonu (5x5, pahalı, Sanayi). İnşa edilince her mevsim bir "Konsey Toplantısı" çağrılabilir (sekmeden).
- İki yol:
  - **Birleşme (barış):** Toplantıda her yaşayan devlet oy verir. Oy = goodwill ≥ 60 ise evet, ittifak varsa kesin evet, savaşta olduğu bir devlet "evet" verdiyse hayır. Yaşayan devletlerin 2/3'ü evet derse zafer. Hayır diyenler için sekmede neden yazar.
  - **Hükmetme (güç):** Yaşayan her devlet ya çökmüş ya da oyuncuya "biat etmiş" olmalı. Biat: oyuncuya düşman bir devletin yerleşimlerinin yarısı yok edildiğinde ya da ele geçtiğinde, devlet biat teklif eder (mektup: kabul = barış + düzenli haraç, ret = savaş sürer). Oyuncu bir devletin son yerleşimini yok ederse devlet çöker.
- Zafer: kronik kaydı, büyük mektup, vanilla kapanış (`GameVictoryUtility.ShowCredits`) ve "devam et" seçeneği. Oyun silinmez.
- Ayar: "Dünya Konseyi oyun sonu" açık/kapalı.

## 4. Mevcut kayıtlar
- 2.1'deki "eksik devletleri ekle" mekanizması üç yeni devleti eski kayıtlara otomatik ekler.

## 5. Test
- Probe30: devletlerin içerik kontrolleri (doku, araştırma çakışması, birim türleri, senaryolar), yol kur/sefer/yağma/kapanma, konsey açılma, oylama, biat ve çöküş, zafer çağrısı (credits gösterilmeden).
- Denge: heirs_check referanslarına uyum (silahlar 0.8–1.2 aralığı, sanayi silahları vanilla tüfekten zayıf).

## 6. Aşamalar
- 3.0a: üç devletin içeriği + görseller + zincirler.
- 3.0b: ticaret yolları.
- 3.0c: Dünya Konseyi.
- Her aşama sonunda tek oyun testi. Steam'e yükleme kullanıcı onayı olmadan yapılmaz.
