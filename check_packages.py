#!/usr/bin/env python
"""Kütüphane kontrol scripti"""
import sys

packages = {
    'numpy': 'numpy',
    'pandas': 'pandas',
    'scikit-learn': 'sklearn',
    'xgboost': 'xgboost',
    'lightgbm': 'lightgbm',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
    'openpyxl': 'openpyxl',
    'joblib': 'joblib'
}

print("=" * 60)
print("📦 KÜTÜPHANE KONTROLÜ")
print("=" * 60)

installed = []
missing = []

for name, pkg in packages.items():
    try:
        module = __import__(pkg)
        version = getattr(module, '__version__', 'Yüklü (versiyon bilgisi yok)')
        print(f"✅ {name:20s} → {version}")
        installed.append(name)
    except ImportError:
        print(f"❌ {name:20s} → YÜKLÜ DEĞİL")
        missing.append(name)

print("=" * 60)
print(f"\n📊 Özet:")
print(f"   ✅ Yüklü: {len(installed)}/{len(packages)}")
print(f"   ❌ Eksik: {len(missing)}/{len(packages)}")

if missing:
    print(f"\n⚠️ Eksik kütüphaneleri yüklemek için:")
    print(f"   python -m pip install {' '.join(missing)}")
    sys.exit(1)
else:
    print("\n✅ Tüm kütüphaneler yüklü!")
    sys.exit(0)

