import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.exceptions import ConvergenceWarning
import warnings

warnings.filterwarnings("ignore", category=ConvergenceWarning)

df = pd.read_csv("upk_catalog.csv")
df.columns = df.columns.str.strip()
print(df.columns)

df_clean = df[['dist', 'rc_min', 'bl', 'age', 'l', 'b']].copy()

df_clean = df_clean.replace([np.inf, -np.inf], np.nan).dropna()

# Korelasyon matrisi
corr = df_clean[['dist', 'rc_min', 'bl', 'age']].corr()
print("\nKorelasyon matrisi:")
print(corr)

plt.figure(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Korelasyon Matrisi")
plt.tight_layout()
plt.show()

def silhouette_k3(data):
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(data)
    return silhouette_score(data, labels)

# =========================
# 1. KÜMELEME (age - rc_min)
# =========================

vec = df_clean[['age', 'rc_min']].values
norms = np.linalg.norm(vec, axis=1, keepdims=True)
soft_normed_da = vec / norms

scaled_da = StandardScaler().fit_transform(soft_normed_da)

kmeans_da = KMeans(n_clusters=3, random_state=42, n_init='auto')
df_clean['cluster_da'] = kmeans_da.fit_predict(scaled_da)

n_before_da = len(df_clean)
print("Kümeleme-1 (age-rc_min) öncesi:", n_before_da)

# Outlier temizleme (küme merkezine uzaklık)
centers_da = kmeans_da.cluster_centers_
distances_da = np.linalg.norm(scaled_da - centers_da[df_clean['cluster_da'].values], axis=1)
df_clean['dist_da'] = distances_da

threshold_da = df_clean['dist_da'].mean() + 0.5 * df_clean['dist_da'].std()
df_clean = df_clean[df_clean['dist_da'] <= threshold_da].reset_index(drop=True)
df_clean.drop(columns=['dist_da'], inplace=True)

# Yeniden eğitme
vec = df_clean[['age', 'rc_min']].values
norms = np.linalg.norm(vec, axis=1, keepdims=True)
soft_normed_da = vec / norms
scaled_da = StandardScaler().fit_transform(soft_normed_da)

kmeans_da = KMeans(n_clusters=3, random_state=42, n_init='auto')
df_clean['cluster_da'] = kmeans_da.fit_predict(scaled_da)

n_after_da = len(df_clean)
print(f"Silinen eleman sayısı (age-rc_min): {n_before_da - n_after_da}")

# 1. görsel
plt.figure(figsize=(7, 5))
sns.scatterplot(
    x=df_clean['rc_min'],
    y=df_clean['age'],
    hue=df_clean['cluster_da'],
    palette='Set2',
    s=80
)
plt.title("rc_min - age")
plt.xlabel("rc_min")
plt.ylabel("age")
plt.show()

# 1. kümeleme skoru
sil_da = silhouette_score(scaled_da, df_clean['cluster_da'])
print(f"\n(age-rc_min) Silhouette Skoru: {sil_da:.4f}")
print("\n(age-rc_min) Küme Eleman Sayıları:")
print(df_clean['cluster_da'].value_counts().sort_index())

# =======================
# 2. KÜMELEME (dist - bl)
# =======================

scaler_de = StandardScaler()
scaled_de = scaler_de.fit_transform(df_clean[['dist', 'bl']])

kmeans_de = KMeans(n_clusters=3, random_state=42, n_init='auto')
df_clean['cluster_de'] = kmeans_de.fit_predict(scaled_de)

n_before_de = len(df_clean)
print("\nKümeleme-2 (dist-bl) öncesi:", n_before_de)

# Outlier temizleme (küme merkezine uzaklık)
centers_de = kmeans_de.cluster_centers_
distances_de = np.linalg.norm(scaled_de - centers_de[df_clean['cluster_de'].values], axis=1)
df_clean['dist_de'] = distances_de

threshold_de = df_clean['dist_de'].mean() + 0.5 * df_clean['dist_de'].std()
df_clean = df_clean[df_clean['dist_de'] <= threshold_de].reset_index(drop=True)
df_clean.drop(columns=['dist_de'], inplace=True)

# Yeniden eğitme
scaler_de = StandardScaler()
scaled_de = scaler_de.fit_transform(df_clean[['dist', 'bl']])

kmeans_de = KMeans(n_clusters=3, random_state=42, n_init='auto')
df_clean['cluster_de'] = kmeans_de.fit_predict(scaled_de)

n_after_de = len(df_clean)
print(f"Silinen eleman sayısı (dist-bl): {n_before_de - n_after_de}")


# l-b FİLTRESİ

# Her küme için l-b merkezlerini hesapla
cluster_centers_lb = df_clean.groupby('cluster_de')[['l', 'b']].mean()

lb_dist = []
for i in range(len(df_clean)):
    c = df_clean.loc[i, 'cluster_de']
    center = cluster_centers_lb.loc[c].values
    point = df_clean.loc[i, ['l', 'b']].values
    lb_dist.append(np.linalg.norm(point - center))

df_clean['lb_dist'] = lb_dist

# l-b aykırı eşik değeri
threshold_lb = df_clean['lb_dist'].mean() + 0.9 * df_clean['lb_dist'].std()
df_clean['is_outlier_angular'] = df_clean['lb_dist'] > threshold_lb

n_before_lb = len(df_clean)
lb_outlier_count = df_clean['is_outlier_angular'].sum()

# l-b aykırılarını çıkar
df_clean = df_clean[df_clean['is_outlier_angular'] == False].reset_index(drop=True)

# Geçici sütunları temizle
df_clean.drop(columns=['lb_dist', 'is_outlier_angular'], inplace=True)

n_after_lb = len(df_clean)
print(f"Silinen eleman sayısı (l-b filtresi): {n_before_lb - n_after_lb}")

# Yeniden eğitme
scaler_de_final = StandardScaler()
scaled_de_final = scaler_de_final.fit_transform(df_clean[['dist', 'bl']])

kmeans_de_final = KMeans(n_clusters=3, random_state=42, n_init='auto')
df_clean['cluster_de_final'] = kmeans_de_final.fit_predict(scaled_de_final)

# 2. görsel
plt.figure(figsize=(7, 5))
sns.scatterplot(
    x=df_clean['dist'],
    y=df_clean['bl'],
    hue=df_clean['cluster_de_final'],
    palette='Set2',
    s=80
)
plt.title("dist - bl")
plt.xlabel("dist")
plt.ylabel("bl")
plt.show()

# Final silhouette skoru
sil_de_final = silhouette_score(scaled_de_final, df_clean['cluster_de_final'])
print(f"\n(dist-bl) l-b filtresi sonrası Silhouette Skoru: {sil_de_final:.4f}")
print("\n(dist-bl) l-b filtresi sonrası Küme Eleman Sayıları:")
print(df_clean['cluster_de_final'].value_counts().sort_index())