# UPK Catalog Kümeleme Analizi

Bu proje, **`upk_catalog.csv`** veri dosyası üzerinde **K-Means kümeleme algoritması** uygulayarak iki farklı değişken seti üzerinden analiz gerçekleştirmektedir:
* `age` - `rc_min`
* `dist` - `bl`

Ayrıca proje kapsamında:

* Korelasyon matrisi oluşturulur
* Küme merkezlerine göre aykırı değer temizliği yapılır
* `l` - `b` uzayında ek filtreleme uygulanır
* Sonuçlar görselleştirilir
* **Silhouette Score** ile küme kalitesi değerlendirilir

---

## Kullanılan Teknolojiler

* Python 3.11.9
* pandas
* numpy
* matplotlib
* seaborn
* scikit-learn
* VİSUAL STUDIO CODE ortamında geliştirilmiştir.

---

## Proje Dosya Yapısı

```bash
UPKCLUSTER/
│
├──upk_catalog.csv
├── SAI_OCL_catalog.csv
├──SAI_OCL_with_lb.csv
├──kumeleme.py
└── README.md
```

Python kodunu doğrudan indirmek yerine kopyala–yapıştır yöntemiyle kullanıyorsanız, kod dosyasını kumeleme.py adıyla kaydetmeniz önerilir.
Ayrıca proje klasörünüzü UPKCLUSTER adıyla oluşturmanız ve upk_catalog.csv veri dosyasını da indirerek aynı klasöre yerleştirmeniz gerekmektedir.

---
## VSCode Üzerinde Çalıştırma

### 1. Projeyi Aç

VSCode üzerinden proje klasörünü açın.

---

### 2. Python Kurulu Olduğunu Kontrol Et

Terminalde aşağıdaki komutlardan birini çalıştırın:

```bash
python --version
```

veya

```bash
python3 --version
```
 Bu aşamadan itibaren bilgisayarınızda Python kurulu olduğu varsayılarak ilerlenmektedir.
Eğer Python sisteminizde kurulu değilse veya PATH değişkenine eklenmemişse, öncelikle kurulum ve yapılandırma işlemlerini tamamlayarak bu sorunu gideriniz.
Kurulum ve gerekli ayarların yapılmasının ardından aşağıdaki adımlarla devam edebilirsiniz.

---


### 3. Sanal Ortam Oluştur

Terminalde proje klasöründe şu komutu çalıştırın:

```bash
python -m venv venv
```

---

### 4. Sanal Ortamı Aktif Et

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

---

### 5. Gerekli Kütüphaneleri Yükle

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

---

### 6. CSV Dosyasını Proje Klasörüne Yerleştir

`upk_catalog.csv` dosyasının **kumeleme.py dosyasıyla aynı klasörde** bulunduğundan emin olun.

---

### 7. Kodu Çalıştır

Terminalden aşağıdaki komutu çalıştırın:

```bash
python kumeleme.py
```
 Alternatif olarak, VSCode kullanıyorsanız dosyayı açtıktan sonra editörün üst kısmında bulunan Run (▶) butonuna basarak da kodu çalıştırabilirsiniz.

Not: Bazı durumlarda VSCode sanal ortamı otomatik olarak seçmeyebilir ve farklı bir Python sürümü kullanabilir. Böyle bir durumda **Ctrl + Shift + P** tuşlarına basarak
**Python: Select Interpreter** seçeneğini açın ve oluşturduğunuz **venv** klasöründeki Python yorumlayıcısını seçin.
 
---

## Çıktılar

Kod çalıştırıldığında:

* `dist`, `rc_min`, `bl` ve `age` değişkenleri için korelasyon matrisi oluşturulur ve görselleştirilir
* `age` – `rc_min` değişkenleri kullanılarak K-Means kümeleme uygulanır ve sonuçlar grafik olarak gösterilir
* `dist` – `bl` değişkenleri kullanılarak ikinci bir K-Means kümeleme analizi uygulanır
* `l` – `b` uzayında açısal filtreleme ile ek aykırı değer temizliği yapılır
* Nihai kümeleme sonuçları grafik olarak görselleştirilir
* Küme kalitesi her işlem için **Silhouette Score** ile değerlendirilir
* Her kümede bulunan veri sayıları işlemler öncesi ve sonrası ayrı ayrı raporlanır

Bu analiz sayesinde veri setindeki yapısal kümeler daha net şekilde gözlemlenebilir.
