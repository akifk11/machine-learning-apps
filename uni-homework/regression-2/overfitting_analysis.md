# ⚠️ Overfitting Analizi ve Çözüm Önerileri

## 🔍 Overfitting Belirtileri

### 📊 Train vs Test Performans Karşılaştırması

| Model | Train R² | Test R² | R² Farkı | Train RMSE | Test RMSE | RMSE Oranı (Test/Train) |
|-------|----------|---------|----------|------------|-----------|-------------------------|
| **Random Forest** | 0.9999 | 0.9997 | 0.0002 | 0.031 | 0.073 | **2.35x** ⚠️ |
| **Gradient Boosting** | 0.9999 | 0.9997 | 0.0002 | 0.048 | 0.081 | **1.69x** ⚠️ |
| **XGBoost** | 0.9995 | 0.9986 | 0.0009 | 0.100 | 0.161 | **1.61x** ⚠️ |
| **LightGBM** | 0.9994 | 0.9994 | 0.0000 | 0.105 | 0.109 | **1.04x** ✅ |
| **Ridge Regression** | 0.9532 | 0.9539 | -0.0007 | 0.944 | 0.941 | **1.00x** ✅ |
| **Linear Regression** | 0.9532 | 0.9539 | -0.0007 | 0.944 | 0.941 | **1.00x** ✅ |

### 🚨 Overfitting İşaretleri

1. **Random Forest**: 
   - Test RMSE, Train RMSE'den **2.35 kat** daha yüksek
   - Train R² = 0.9999 (neredeyse mükemmel)
   - Test R² = 0.9997 (hala çok yüksek ama train'den düşük)

2. **Gradient Boosting**:
   - Test RMSE, Train RMSE'den **1.69 kat** daha yüksek
   - Train R² = 0.9999
   - Test R² = 0.9997

3. **XGBoost**:
   - Test RMSE, Train RMSE'den **1.61 kat** daha yüksek
   - Train R² = 0.9995
   - Test R² = 0.9986

### ✅ Overfitting Olmayan Modeller

- **LightGBM**: Test/Train RMSE oranı 1.04x (çok iyi)
- **Ridge/Linear Regression**: Test/Train RMSE oranı ~1.00x (mükemmel)

---

## 🎯 Overfitting Nedenleri

### 1. **Model Kompleksliği Çok Yüksek**
- Random Forest ve Gradient Boosting modelleri çok derin ağaçlar kullanıyor olabilir
- Çok fazla ağaç sayısı (n_estimators) overfitting'e yol açabilir

### 2. **Özellik Sayısı Fazla Olabilir**
- Genişletilmiş özellik mühendisliği ile çok fazla özellik oluşturulmuş olabilir
- Bazı özellikler gürültü içerebilir

### 3. **Veri Seti Boyutu**
- %3 veri kullanılıyor (deneme amaçlı)
- Küçük veri seti üzerinde kompleks modeller overfitting'e yatkın

### 4. **Hiperparametre Optimizasyonu**
- RandomizedSearchCV ile sınırlı iterasyon (n_iter=6)
- Daha iyi hiperparametreler bulunabilir

---

## 💡 Çözüm Önerileri

### 1. **Model Kompleksliğini Azaltma**

#### Random Forest için:
```python
RandomForestRegressor(
    n_estimators=50,        # 100'den azalt
    max_depth=10,           # Daha sığ ağaçlar
    min_samples_split=20,   # Daha fazla örnek gerektir
    min_samples_leaf=10,    # Yaprak düğümlerinde daha fazla örnek
    max_features='sqrt',    # Özellik sayısını sınırla
    random_state=42
)
```

#### Gradient Boosting için:
```python
GradientBoostingRegressor(
    n_estimators=50,        # 100'den azalt
    max_depth=5,            # Daha sığ ağaçlar
    learning_rate=0.05,     # Daha düşük learning rate
    min_samples_split=20,
    min_samples_leaf=10,
    subsample=0.8,         # Her iterasyonda %80 veri kullan
    random_state=42
)
```

#### XGBoost için:
```python
XGBRegressor(
    n_estimators=50,
    max_depth=5,
    learning_rate=0.05,
    min_child_weight=5,
    subsample=0.8,
    colsample_bytree=0.8,  # Özellik örnekleme
    reg_alpha=0.1,         # L1 regularization
    reg_lambda=1.0,        # L2 regularization
    random_state=42
)
```

### 2. **Early Stopping Kullanma**

```python
# XGBoost ve LightGBM için early stopping
XGBRegressor(
    ...
    early_stopping_rounds=10,
    eval_set=[(X_test, y_test)]
)
```

### 3. **Cross-Validation ile Model Seçimi**

```python
from sklearn.model_selection import cross_val_score

# Her model için CV skorlarını karşılaştır
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
print(f"CV RMSE: {-cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
```

### 4. **Özellik Seçimi**

```python
from sklearn.feature_selection import SelectKBest, f_regression

# En önemli özellikleri seç
selector = SelectKBest(f_regression, k=20)  # En iyi 20 özellik
X_train_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)
```

### 5. **Daha Fazla Veri Kullanma**

- %3 yerine %10-20 veri kullanılabilir
- Daha fazla veri overfitting'i azaltır

### 6. **Regularization Artırma**

```python
# Ridge Regression için alpha değerini artır
Ridge(alpha=10.0)  # Varsayılan 1.0'dan daha yüksek

# Lasso Regression için alpha değerini artır
Lasso(alpha=1.0)   # Varsayılan 0.1'den daha yüksek
```

### 7. **Ensemble Yöntemleri**

```python
from sklearn.ensemble import VotingRegressor

# Daha basit modelleri birleştir
voting_model = VotingRegressor([
    ('rf', RandomForestRegressor(n_estimators=50, max_depth=10)),
    ('gb', GradientBoostingRegressor(n_estimators=50, max_depth=5)),
    ('xgb', XGBRegressor(n_estimators=50, max_depth=5))
])
```

---

## 📈 Önerilen Model Ayarları

### Random Forest (Overfitting Azaltılmış)
```python
RandomForestRegressor(
    n_estimators=50,
    max_depth=10,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1
)
```

### Gradient Boosting (Overfitting Azaltılmış)
```python
GradientBoostingRegressor(
    n_estimators=50,
    max_depth=5,
    learning_rate=0.05,
    min_samples_split=20,
    min_samples_leaf=10,
    subsample=0.8,
    random_state=42
)
```

### XGBoost (Overfitting Azaltılmış)
```python
XGBRegressor(
    n_estimators=50,
    max_depth=5,
    learning_rate=0.05,
    min_child_weight=5,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    n_jobs=-1
)
```

---

## 🎯 Sonuç ve Öneriler

### ⚠️ Overfitting Var mı?

**Evet**, özellikle Random Forest ve Gradient Boosting modellerinde overfitting belirtileri var:
- Test RMSE, Train RMSE'den 1.6-2.3 kat daha yüksek
- Train skorları çok yüksek (0.9999)

### ✅ Ne Yapmalı?

1. **Kısa Vadede**: Model kompleksliğini azalt (max_depth, n_estimators)
2. **Orta Vadede**: Daha fazla veri kullan (%10-20)
3. **Uzun Vadede**: Özellik seçimi ve daha iyi hiperparametre optimizasyonu

### 📊 Beklenen Sonuçlar

Overfitting azaltıldıktan sonra:
- Train R²: 0.9999 → 0.998-0.999 (biraz düşecek)
- Test R²: 0.9997 → 0.998-0.999 (aynı kalacak veya artacak)
- Test/Train RMSE Oranı: 2.35x → 1.1-1.2x (daha dengeli)

---

**Not**: Overfitting her zaman kötü değildir. Eğer test performansı hala çok iyiyse (R² > 0.99), model kullanılabilir. Ancak production'da beklenmedik veriler geldiğinde performans düşebilir.

