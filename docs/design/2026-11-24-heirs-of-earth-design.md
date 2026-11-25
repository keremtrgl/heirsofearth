# Dünyanın Mirasçıları (Heirs of Earth) Tasarımı

## Amaç ve neden
RimWorld 1.6 için sıfırdan, Harmony kullanan, bütün oyunu etkileyen büyük bir mod. Yüzyıllar önce Dünya'dan kalkan koloni gemilerinin torunları, RimWorld gezegenlerinde gerçek kültürlerin mirasını taşıyan devletler kurmuş. Oyuncu bu devletlerden birinin kolu olarak ya da bağımsız başlar. Diğer kültürlerin bilgisini ticaret, öğretmen, ittifak ve fetihle zamanla öğrenir. Sonunda birkaç kültürü birleştiren, kendine özgü bir koloni kurar.

Kullanıcının istediği: "gerçek hayattan şeyler", yüzlerce araştırma, tüm oyuna ve tüm kolonilere etki eden, çok detaylı, profesyonel ve uzun oynanışlı bir mod. Starfall ve KUT hikâye modlarıydı. Bu mod oyunun genelini genişletir.

## Kullanıcının verdiği kararlar
- Gerçek dünyadan esinlenen devletler, zaman olarak "Dünya'dan gelen torun devletler" (bugünün ülkeleri değil).
- Oyuncunun ilişkisi: "ikisi birden". Bir mirasla ya da bağımsız başlanır, diğer kültürler zamanla öğrenilir.
- Dokuz devlet: Nova Roma, Yamato, Nordheim, Tianxia, Yeni Hellas, Albion, Yeni Kemet, Pars, İnti.
- Bağımlılık olarak yalnızca Harmony.
- Aşamalı yayın: 1.0'da çekirdek sistemler ve üç devlet, sonra üçer devletlik iki büyük güncelleme.
- Görseller vanilla tarzında, kodla çizilir. Seri üretimden önce örnek set onaylanır.

## Hedefler
- Toplam yaklaşık 300 araştırma: 9 devlet x 28-34 + 40 ortak "Dünya Mirası" araştırması.
- Her devletin ayrı oyun tarzı, iklimi, askerleri, kıyafetleri, silahları, binaları, yemekleri ve kural değiştiren gelenekleri.
- Devletler dünya haritasında yaşayan gruplar olur: ticaret, savaş, ittifak, yerleşim kaybetme.
- Her devletin 4-5 aşamalı hikâye zinciri ve sonunda efsanevi bir eseri.
- Mevcut kayıtlara eklenebilmesi.
- İngilizce ve Türkçe tam çeviri.

## Hedef dışı
- 1.0'a kadar DLC içeriği. Mod DLC'siz, yalnızca Core ve Harmony ile tam çalışır. DLC ekleri 1.0'dan sonra gelir (bkz. "DLC ekleri").
- Uzay çağı. Devlet dalları sanayi çağında biter, sonrası vanilla ile devam eder.
- Binek hayvanı veya deniz savaşı gibi motorun desteklemediği sistemler.
- RimWorld 1.7 desteği (ileride ayrı iş).

## Anti-hedefler (teknik olarak çalışsa da başarısızlık sayılır)
- Bugünün ülkelerini, gerçek kişileri, gerçek markaları ya da dinleri kötü göstermek.
- Türk veya Moğol kökenli bir devlet (KUT ile çakışmasın).
- Yapay zeka kokan, düz, kâğıt gibi görseller ya da kendi içinde tutarsız stil.
- Harmony yamalarının başka modları bozması ya da bir yama bozulunca oyunun çökmesi.
- Vanilla dengesini anlamsız güç enflasyonuyla bozmak. Her yeni şey bir bedel veya seçimle gelir.

## Kısıtlar
- RimWorld 1.6.4871, yalnızca Core. Harmony `brrainz.harmony` 1.6, derleme `0Harmony.dll`'e karşı yapılır.
- Yazar adı Kerem. packageId: `kerem.heirs`.
- Oyun az açılır. Her sürüm çevrimdışı derleme, XML ve çeviri denetiminden geçer, sonra tek açılışlık otomatik oyun içi test yapılır (Starfall'daki test modu düzeni).
- Steam güncellemeleri oyunun Upload düğmesiyle değil, SteamUGC ile yapılır, açıklama korunur.

## Yaklaşımlar
1. **Aşamalı yayın (seçilen):** 1.0 çekirdek sistemler + Roma, Yamato, Nordheim. 2.0 Hellas, Tianxia, Albion. 3.0 Kemet, Pars, İnti ve oyun sonu. Erken oynanabilir, her aşama ayrı test edilir, geri bildirim sonraki devletleri iyileştirir.
2. **Hepsi birden:** İlk gün tam, ama uzun süre oynanabilir bir şey olmaz ve tek testte çok fazla şey birikir.
3. **Görsel yolu:** Vanilla tarzında kodla çizim (seçilen). Yapay zeka üretimi stil tutarsızlığı ve "yapay zeka kokusu" yüzünden, vanilla görsellerini renklendirmek ise devletlerin karakterini kaybettirdiği için ana yol değil. Renklendirilmiş vanilla görselleri sadece sıradan ara malzemeler ve bazı giyilen kıyafet katmanları için kullanılır.

## Sistemler

### 1. Devletler
Her devlet bir `FactionDef` + 5-7 `PawnKindDef`. Hepsi insan, yeni ırk yok. Her devletin:
- Yönetici unvanı, yerleşim adları, kendi renk ve sancağı.
- Asker kademeleri (ör. Roma: Hastatus, Lejyoner, Centurio, Medicus, Konsül).
- Kültürüne uygun kıyafet, silah ve ticaret malı. Tüccarları, baskıncıları ve ziyaretçileri bunlarla gelir.
- Kültürel eğilim: hangi devletle doğal dost ya da rakip olduğu.

| Devlet | Güçlü yanı | İmza eşya ve bina | Örnek gelenek (kural değişikliği) | Efsanevi eser ve hikâye |
|---|---|---|---|---|
| Nova Roma Cumhuriyeti | Düzenli ordu, inşaat | Scutum kalkanı, gladius, pilum, lorica, Roma yolu, Roma betonu, hamam | Roma Yolları: yolda yürüme ve kervan hızı | Kartal Sancağı, "Kayıp Kartal" |
| Yamato Şogunluğu | Usta savaşçı, zanaat | Katana, yumi, yari, yoroi, dojo, çay evi | Usta Zanaat: kalite şansı | Gök Kılıcı, "Kırık Hanedan" |
| Nordheim Krallığı | Soğuk, akın, hayatta kalma | Dane baltası, yuvarlak kalkan, kürk pelerin, uzun ev, sauna | Kuzey Kanı: soğuk dayanımı | Fırtına Boynuzu, "Kış Ayini" |
| Yeni Hellas Birliği | Bilim, tıp | Dory, aspis, akademi, tiyatro, şifahane | Hipokrat Yemini: ameliyat başarısı | Gök Hesaplayıcı, "Kayıp Kütüphane" |
| Tianxia Hanedanlığı | Barut, ilaç, ticaret | Arbalet, ateş mızrağı, ateşli ok bataryası, porselen fırını | Hekimlik: ilaç etkisi | Ejder Kazanı, "Saray Sınavı" |
| Albion Dominyonu | Sanayi, seri üretim | Tüfek, süngü, buhar makinesi, dokuma fabrikası | Fabrika Düzeni: üretim hızı | Büyük Kazan, "Demir Devrim" |
| Yeni Kemet Krallığı | Sıcak iklim, tarım, anıt | Khopesh, sulama kanalı, dikili taş, papirüs atölyesi | Nehir Toprağı: tarla verimi | Güneş Diski, "Kum Altındaki Şehir" |
| Pars Satraplığı | Ticaret, diplomasi | Pul zırh, ipek kaftan, kanat, bahçe, halı tezgâhı | Kraliyet Postası: kervan hızı ve ticaret fiyatı | Kralın Gözü, "Kraliyet Yolu" |
| İnti İmparatorluğu | Dağ, depolama, kıtlık | Sapan, makana, teraslar, kollka ambarı, düğüm kayıt masası | Kollka: yiyecek bozulma süresi | Altın İp, "Düğümlerin Dili" |

### 2. Miras ve başlangıç
- Her devlet için bir senaryo + bağımsız senaryo. Mevcut bir kayıtta oyuncu mirasını bir kez "Miras" penceresinden seçer.
- Mirasın devlet dalı açık başlar. Kolonistlerin geçmişi, kıyafetleri ve başlangıç eşyaları o kültüre uyar.
- Mirasın devletiyle iyi ilişkiyle başlanır. Bağımsız başlayan herkesle nötr başlar ama ilk bilgiye daha kolay ulaşır.

### 3. Araştırma yapısı
- Kendi araştırma sekmesi: "Dünya Mirası". Devlet dalları sütunlar halinde, çağlara göre satırlar (Kabile, Ortaçağ, Sanayi).
- Her araştırma vanilla öncülleriyle bağlanır, böylece vanilla ilerleyişi bozulmaz.
- **Kültür Bilgisi:** Her devlet için ayrı bir bilgi puanı. Bir yabancı devletin araştırması, o devletin bilgisi yeterli değilse başlatılamaz (Harmony yaması). Bilgi kaynakları:
  - O devletten alınan eşyaları **Kültür Masası**'nda inceleyip parçalamak.
  - O kültürden gelen kolonisti öğretmen yapmak (araştırma yaparken bonus bilgi).
  - İttifakta devletin hediye olarak yolladığı kitaplar.
  - Fethedilen yerleşimlerden yağmalanan arşivler.
  - Hikâye zinciri adımları.
- Tempo ayarı araştırma maliyetini ve bilgi kazanımını ölçekler.

### 4. Gelenekler (kural değiştiren araştırmalar)
- Her devlette 6-8 "gelenek" araştırması oyunun bir kuralını değiştirir.
- İlke: mümkünse vanilla araçlarla (StatPart, hediff, yetenek) yapılır, Harmony sadece vanilla'nın izin vermediği yerde.
- Planlanan Harmony noktaları: araştırma başlatma kontrolü, kervan hızı, hasat verimi, ticaret fiyatı, yolda yürüme hızı, ameliyat başarısı, yiyecek bozulma süresi, yerleşim ele geçirme, baskın kompozisyonu.
- Her yama ayrı bir sınıfta, kendi denetimiyle yüklenir. Bir yama uygulanamazsa log'a bir kez yazılır ve sadece o özellik kapanır, oyun çalışmaya devam eder.
- Yamalar mümkün olduğunca Postfix olur. Vanilla kodu atlayan Prefix ve Transpiler sadece başka yol yoksa kullanılır.

### 5. Yaşayan dünya siyaseti
- Bir oyun bileşeni devletler arası ilişkileri tutar ve ayda bir günceller.
- Devletler birbirine savaş açar, ittifak kurar, barış yapar. Savaşta yerleşim el değiştirebilir, bir devlet yıkılabilir.
- Oyuncuya gelen olaylar: elçiler, haraç talepleri, evlilik teklifleri (kolonist katılır), savaşa katılma çağrısı, ateşkes arabuluculuğu, devlet çöküşü.
- Ayardan kapatılabilir ya da sıklığı ayarlanabilir.

### 6. Devlet hikâyeleri
- Her devlette 4-5 aşamalı görev zinciri (teslimat, inşa, savaş, dünya haritasında bölge, seçim).
- Zincirin sonunda efsanevi eser ve o kültürün en üst teknolojisi açılır.
- 3.0'da oyun sonu: "Dünya Konseyi". Oyuncu devletleri barışla birleştirebilir ya da tek güç olarak hükmedebilir.

### 7. Arayüz
- "Mirasçılar" sekmesi: Miras, Kültür Bilgisi, Diplomasi (ilişki tablosu), Gelenekler ve Kronik bölümleri.

### 8. Görseller ve ses
- Vanilla tarzında, kodla çizim: kalın koyu dış hat, yumuşak gölge, hafif dolgu dokusu, sınırlı palet, sol üstten ışık.
- Örnek set: lejyoner kalkanı, katana, Nordheim baltası, Roma su kemeri ve devlet sancağı. Kullanıcı onaylayınca seri üretim.
- Giyilen kıyafetler en büyük iş: gövde kıyafeti 5 vücut tipi x 3 yön, başlık 3 yön. Şablonlu çizim, gerektiğinde vanilla katmanların renklendirilmesi.
- Ses: çoğunlukla vanilla sesler, birkaç imza ses (boru, gong, savaş borusu) sentezle.

### 9. Ayarlar
Tempo, siyaset sıklığı, devletler arası savaş açık/kapalı, her gelenek grubunun açık/kapalı olması, baskın gücü.

### 10. DLC ekleri (kullanıcı kararı: 1.0'dan sonra)
- Aynı mod içinde, DLC'si olana ek özellik; DLC'si olmayan normal modu oynar. Ayrı yama modu yok.
- Araçlar: `LoadFolders.xml` içinde `IfModActive` ile DLC'ye özel klasörler (`Royalty/`, `Ideology/`...), tek satırlık tanımlarda `MayRequire="Ludeon.RimWorld.Ideology"`, kodda `ModsConfig.IdeologyActive` gibi kontroller.
- Mod klasör yapısı 0.1'den itibaren `LoadFolders.xml` ile kurulur, böylece ekler sonradan yapı değiştirmeden eklenir.
- Sıra: önce Ideology (devletlere özel inanç ve gelenek paketleri, ritüeller, sancak süsleri; gerçek dinlere dokunulmaz) ve Royalty (Konsül, Şogun gibi devlet unvanları ve ayrıcalıkları). Sonra Biotech ve Anomaly'ye küçük ekler.
- Gerçek halklara ayrı gen tipi verilmez (anti-hedef).
- Kullanıcının oyununda DLC yok: DLC kısımları yalnızca çevrimdışı denetlenir, oyunda test edilemez. Bu yüzden küçük, dikkatli adımlarla ve her kod yolu DLC kontrolünün arkasında eklenir.

## Yayın planı
| Sürüm | İçerik |
|---|---|
| 0.1 (iç) | Harmony önyüklemesi ve yama denetimi, Kültür Bilgisi, araştırma sekmesi, Roma'nın ilk 8 araştırması. Sadece test. |
| 1.0 Eski Dünyanın Çocukları | Roma, Yamato, Nordheim; 40 ortak + 3x30 araştırma (~130); 4 senaryo; temel siyaset (ilişkiler, elçiler, haraç, devletler arası savaş); 3 hikâye zinciri; ~110 eşya ve bina. |
| 2.0 Akıl ve Ateş | Hellas, Tianxia, Albion (~95 araştırma); tam siyaset (yerleşim ele geçirme, ittifak çağrısı, evlilik); 3 hikâye zinciri. |
| 2.1 Eksikler | Mevcut kayıtlara yeni devletleri ekleme; Roma, Yamato, Nordheim sanayi satırı; Tianxia ateşli ok bataryası; Albion dokuma fabrikası; Hellas akademi ve şifahane yapıları; imza sesler. |
| 3.0 Kum, Dağ ve Yol | Kemet, Pars, İnti; ticaret yolları; oyun sonu "Dünya Konseyi". |
| 3.x DLC ekleri | Ideology ve Royalty ekleri, sonra Biotech ve Anomaly'ye küçük ekler. DLC'si olmayanlar için hiçbir şey değişmez. (Kullanıcı kararı 2026-11-24: önce eksikler, sonra 3.0.) |

Durum (2026-11-24): 0.1, 1.0 ve 2.0.0 bitti ve test edildi (2.0: 1380 geçti / 0 kaldı). 2.0.0 Steam'e yüklenmedi.

## Kalite güvencesi
- Çevrimdışı: derleme, XML ve Def referans denetimi, çeviri denetimi (Starfall'daki validator uyarlanır), denge tablosu (araştırma maliyeti, silah ve zırh değerleri vanilla karşılıklarıyla kıyaslanır).
- Oyun içi: her sürüm için tek açılışlık otomatik test (bütün eşyaları üretir, araştırmaları açar, siyaset olaylarını ve hikâye zincirlerini koşturur, kaydedip yükler, yamaların hepsinin uygulandığını doğrular). Test temizse aynı açılışta Steam'e yükler.

## Uygulayana kalanlar
- Sınıf ve dosya yapısı, yama hedeflerinin tam metot adları (1.6 DLL'ine karşı doğrulanacak).
- Araştırma ağacının tam yerleşimi ve maliyetleri.
- Her devletin eşya ve araştırma listesinin ayrıntısı (devlet devlet, uygulama planında).
