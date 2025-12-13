# Machine Learning Projects

Bu repository, çeşitli makine öğrenmesi projelerini içermektedir.

## 📋 Projeler

- **Classification**: Sınıflandırma projeleri
- **Clustering**: Kümeleme analizleri
- **Regression**: Regresyon analizleri

## 🚀 Kurulum

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/akifk11/machine-learning-apps.git
cd machine-learning-apps
```

### 2. Virtual Environment Oluşturun

#### Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Windows (CMD):
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### Linux/Mac:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

Virtual environment aktifken:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Jupyter Notebook Kullanımı

Eğer Jupyter Notebook kullanacaksanız:

```bash
pip install jupyter
jupyter notebook
```

## 📦 Gereksinimler

Proje için gerekli Python paketleri `requirements.txt` dosyasında listelenmiştir.

## 🔧 Virtual Environment Kullanımı

### Virtual Environment'i Aktifleştirme

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

Aktif olduğunda terminalinizde `(.venv)` öneki görünecektir:
```
(.venv) PS C:\Users\akif\Desktop\code\machine-learning-project>
```

### Virtual Environment'ten Çıkma

```bash
deactivate
```

### Virtual Environment'i Güncelleme

Yeni bir paket yükledikten sonra `requirements.txt` dosyasını güncelleyin:

```bash
pip freeze > requirements.txt
```

## 📁 Proje Yapısı

```
machine-learning-project/
├── .venv/              # Virtual environment (Git'te ignore edilir)
├── classification/     # Sınıflandırma projeleri
├── clustering/         # Kümeleme projeleri
├── regression/         # Regresyon projeleri
├── regression-2/      # İyileştirilmiş regresyon projeleri
├── requirements.txt    # Python bağımlılıkları
└── README.md          # Bu dosya
```

## ⚠️ Önemli Notlar

- **Virtual Environment**: `.venv/` klasörü Git tarafından ignore edilir. Her geliştirici kendi bilgisayarında virtual environment oluşturmalıdır.
- **Büyük Dosyalar**: `.gitignore` dosyasında büyük dosyalar (`.csv`, `.pkl`, `data/`, `models/`) ignore edilmiştir.
- **Python Versiyonu**: Python 3.8 veya üzeri önerilir.

## 🐛 Sorun Giderme

### Virtual Environment Aktifleştirme Hatası (Windows PowerShell)

Eğer PowerShell'de execution policy hatası alırsanız:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Paket Yükleme Hataları

Eğer paket yükleme sırasında hata alırsanız:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Jupyter Kernel Hatası

Eğer Jupyter Notebook'ta kernel bulunamıyorsa:

```bash
python -m ipykernel install --user --name=.venv
```

## 📝 Katkıda Bulunma

1. Yeni bir branch oluşturun: `git checkout -b feature/yeni-ozellik`
2. Değişikliklerinizi commit edin: `git commit -m 'Yeni özellik eklendi'`
3. Branch'inizi push edin: `git push origin feature/yeni-ozellik`
4. Pull Request oluşturun

## 📄 Lisans

Bu proje [LICENSE](LICENSE) dosyasında belirtilen lisans altındadır.

## 👤 Yazar

**Akif K.**

- GitHub: [@akifk11](https://github.com/akifk11)

---

**Not**: Bu proje eğitim amaçlıdır ve sürekli geliştirilmektedir.

