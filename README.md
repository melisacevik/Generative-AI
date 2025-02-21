# Generative AI

## Modül 2:

Bu repo, en son yapay zeka modellerini kullanarak ses, görüntü ve metin oluşturma ve işleme için Python betikleri 
içerir. Projeler, Streamlit aracılığıyla kullanıcı dostu arayüzlerle entegre edilerek kolay etkileşim imkanı sunar. 
Aşağıda, bu repoda bulunan temel bileşenlerin ve özelliklerin bir özeti bulunmaktadır.

## Özellikler

### Ses İşlemleri ([`audio_ops.py`](https://github.com/melisacevik/Generative-AI/blob/master/module2/audio1/audio_ops.py))
- **Metinden Konuşmaya (Text-to-Speech)**: OpenAI modellerini kullanarak gerçekçi ve yüksek kaliteli ses üretimi sağlar.
- **Ses Transkripsiyonu**: Whisper ve AssemblyAI'nin Conformer modellerini kullanarak ses dosyalarını metne çevirir.
- **Çeviri**: Transkribe edilen sesleri farklı dillere çevirerek çok dilli erişilebilirlik sunar.

### Görüntü İşlemleri ([`image_ops.py`](https://github.com/melisacevik/Generative-AI/blob/master/module2/image101/image_ops.py))
- **Görüntü Oluşturma**: DALL-E ve Stable Diffusion modelleriyle özgün ve yaratıcı görseller üretir.
- **Varyasyonlar**: Mevcut görsellerin farklı versiyonlarını üreterek yaratıcı keşifler yapmanıza olanak tanır.
- **Özel Sanat Eserleri**: Stable Diffusion kullanarak kişiselleştirilmiş sanat eserleri oluşturur.

### Metin İşlemleri ([`app.py`](https://github.com/melisacevik/Generative-AI/blob/master/module2/text101/app.py) ve [`chat.py`](https://github.com/melisacevik/Generative-AI/blob/master/module2/text101/chat.py))
- **Metin Üretimi**: OpenAI'nin dil modellerini kullanarak yaratıcı ve etkileyici metinler üretir.
- **Özetleme**: Uzun metinleri hızlıca özetleyerek içeriğin kısa versiyonlarını oluşturur.
- **Çeviri**: Girilen metni farklı dillere çevirerek geniş bir kitleye hitap eder.
- **Chatbot Arayüzü**: OpenAI'nin dil modelleriyle etkileşimli diyalog deneyimi sunan bir sohbet botu içerir.

## Gereksinimler
- Python 3.8+
- Streamlit
- OpenAI API
- StabilityAI API

## Kurulum
1. Repoyu klonlayın:
   ```sh
   git clone https://github.com/melisacevik/Generative-AI.git
   ```
2. Gerekli paketleri yükleyin:
   ```sh
   pip install -r requirements.txt
   ```

## Modül 3

### VoiceDraw: Sesli Komutlarla Görsel Oluşturma

VoiceDraw, kullanıcıların sesli komutlarla görseller oluşturmasını sağlayan bir uygulamadır. Uygulama, ses kaydını alıp metne çevirir ve ardından yapay zeka modelleriyle görsel üretir.

![Ekran Resmi 2025-02-21 16.01.31.png](..%2FEkran%20Resmi%202025-02-21%2016.01.31.png)


### 📌 Özellikler
- **Ses Kaydı:** Kullanıcıdan sesli giriş alır.
- **Metne Dönüştürme:** OpenAI Whisper API ile sesi metne çevirir.
- **Görsel Üretimi:**
  - OpenAI DALL-E 3 kullanarak metinden görsel üretir.
  - Google Gemini Vision Pro kullanarak görsel bazlı düzenlemeler yapar.
- **Streamlit Arayüzü:** Kullanıcı dostu bir arayüz sunar.
- **Görsel İndirme:** Üretilen görselleri indirilebilir hale getirir.

## Modül 4

### 1️⃣ LangChain: Model Karşılaştırma

Bu çalışma, farklı yapay zeka dil modellerinin performanslarını karşılaştırmak için bir arayüz sunar.

![Ekran Resmi 2025-02-13 10.34.02.png](..%2FEkran%20Resmi%202025-02-13%2010.34.02.png)

#### 📌 Özellikler
- **Model Karşılaştırma:**
  - **GPT-4 Turbo**
  - **Gemini Pro**
  - **Deepseek Chat**
  - Kullanıcı girdisine bağlı olarak farklı modellerin yanıtlarını karşılaştırır ve süre ölçümü yapar.

#### 🚀 Kullanım
```bash
streamlit run module4/model.py
```

#### 📂 Dosya Yapısı
```
├── model.py          # Streamlit tabanlı model karşılaştırma arayüzü
├── modelhelper.py    # Farklı yapay zeka modellerinin API entegrasyonu
```

---

### 2️⃣ LangChain: Bellek Genişletme (RAG)

Bu çalışma, bellek genişletme teknikleri kullanarak modelin dış kaynaklardan bilgi almasını sağlar.

![Ekran Resmi 2025-02-21 16.17.30.png](..%2FEkran%20Resmi%202025-02-21%2016.17.30.png)

![Ekran Resmi 2025-02-21 16.18.58.png](..%2FEkran%20Resmi%202025-02-21%2016.18.58.png)


#### 📌 Özellikler
- **Web Üzerinden Bilgi Alma:** Belirtilen URL’den içerik toplayarak sorulara daha kapsamlı yanıt verir.
- **PDF Desteği:** PDF dosyalarını işler ve metinden bilgi çıkararak yanıt oluşturur.
- **Özel Prompt Kullanımı:** Modelin dış bilgi kaynaklarına erişimini sağlayarak daha bilinçli yanıtlar oluşturmasını destekler.

#### 🚀 Kullanım
```bash
streamlit run module4/rag.py
```

#### 📂 Dosya Yapısı
```
├── rag.py            # Streamlit tabanlı bellek genişletme uygulaması
├── raghelper.py      # Web ve PDF üzerinden içerik alarak bellek genişletme işlevselliği
```

Bu modül, farklı büyük dil modellerinin karşılaştırmasını yaparak kullanıcıların en iyi modeli seçmesine yardımcı olmayı ve ek bellek genişletme teknikleriyle daha verimli bilgi edinmesini sağlamayı amaçlamaktadır.

