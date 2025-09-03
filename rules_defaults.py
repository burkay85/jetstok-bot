# rules_defaults.py

# Her alan için öncelik sıralı varsayılan değerler
PRIORITY_DEFAULTS = {
    # Genel
    "Yaş": ["Belirtilmemiş", "5+ Yaş", "2 – 3 Yaş", "6 – 8 Yaş", "7 – 8 Yaş", "9 – 10 Yaş"],
    "Boyut": ["Belirtilmemiş"],
    "Piller Kutuya Dahil Mi?": ["Belirtilmemiş", "Hayır"],
    "Pili ile mi çalışır?": ["Belirtilmemiş", "Hayır"],
    "Web Color": ["Belirtilmemiş", "Çok Renkli"],
    "Renk": ["Belirtilmemiş", "Siyah", "Beyaz", "Kırmızı"],
    "Menşei": ["Belirtilmemiş", "TR"],
    "Garanti Süresi": ["Belirtilmemiş", "2 Yıl"],
    "Garanti Tipi": ["Belirtilmemiş", "İthalatçı Garantili"],
    "Durum": ["Belirtilmemiş", "Sıfır"],
    "Üretim Yeri": ["Belirtilmemiş", "Türkiye"],

    # Giyim
    "Cinsiyet": ["Belirtilmemiş", "Unisex"],
    "Kumaş Tipi": ["Belirtilmemiş", "Pamuk"],
    "Kol Tipi": ["Belirtilmemiş", "Kısa Kol"],
    "Yaka Tipi": ["Belirtilmemiş", "Bisiklet Yaka"],
    "Desen": ["Belirtilmemiş", "Düz Renk"],
    "Kalıp": ["Belirtilmemiş", "Regular Fit"],
    "Paça Tipi": ["Belirtilmemiş", "Düz Paça"],
    "Sezon": ["Belirtilmemiş", "Mevsimlik"],
    "Ortam": ["Belirtilmemiş", "Günlük"],

    # Ayakkabı
    "Taban Malzemesi": ["Belirtilmemiş", "Poliüretan"],
    "Dış Materyal": ["Belirtilmemiş", "Suni Deri"],
    "İç Materyal": ["Belirtilmemiş", "Tekstil"],
    "Topuk Tipi": ["Belirtilmemiş", "Düz"],
    "Topuk Boyu": ["Belirtilmemiş", "3 cm"],
    "Bağlama Şekli": ["Belirtilmemiş", "Bağcıklı"],
    "Kullanım Alanı": ["Belirtilmemiş", "Günlük"],

    # Elektronik
    "Mouse Tipi": ["Belirtilmemiş", "Kablosuz"],
    "Bağlantılar": ["Belirtilmemiş", "USB"],
    "Ekran Boyutu": ["Belirtilmemiş", "15.6 inç"],
    "İşletim Sistemi": ["Belirtilmemiş", "FreeDOS"],
    "Bellek Kapasitesi": ["Belirtilmemiş", "8 GB"],
    "Disk Kapasitesi": ["Belirtilmemiş", "512 GB"],
    "Disk Türü": ["Belirtilmemiş", "SSD"],
    "İşlemci Tipi": ["Belirtilmemiş", "Intel Core i5"],
    "Priz Tipi": ["Belirtilmemiş", "C / F"],
    "Frekans": ["Belirtilmemiş", "50 Hz / 60 Hz"],
    "Voltaj": ["Belirtilmemiş", "12V"],

    # Ev & Yaşam
    "Materyal": ["Belirtilmemiş", "Plastik"],
    "Kapasite": ["Belirtilmemiş", "2 L"],
    "Kullanım Şekli": ["Belirtilmemiş", "Elektrikli"],
    "Enerji Sınıfı": ["Belirtilmemiş", "A+"],
    "Bıçak Sayısı": ["Belirtilmemiş", "2"],
    "Renk Seçeneği": ["Belirtilmemiş", "Beyaz"],

    # Oyuncak
    "Karakter": ["Belirtilmemiş", "Yok"],
    "Malzeme": ["Belirtilmemiş", "Plastik"],
    "Tür": ["Belirtilmemiş", "Eğitici Oyuncak"],
    "Kutu İçeriği": ["Belirtilmemiş", "Ana Ürün + Aksesuarlar"],
    "Kullanım Yaşı": ["Belirtilmemiş", "3+"],
    "Oyuncu Sayısı": ["Belirtilmemiş", "4-10 Kişi", "5-10 Kişi"], # --- YENİ EKLENDİ ---

    # Anne & Bebek
    "Beden": ["Belirtilmemiş", "Standart"],
    "Kilit Tipi": ["Belirtilmemiş", "Güvenli Klips"],
    "Taşıma Kapasitesi": ["Belirtilmemiş", "15 kg"],
    "Yıkanabilirlik": ["Belirtilmemiş", "Evet"],
    "Bez Tipi": ["Belirtilmemiş", "Tek Kullanımlık"],

    # Kozmetik
    "Cilt Tipi": ["Belirtilmemiş", "Tüm Cilt Tipleri"],
    "Koku Tipi": ["Belirtilmemiş", "Çiçeksi"],
    "Form": ["Belirtilmemiş", "Sprey"],
    "Hacim": ["Belirtilmemiş", "50 ml"],
    "SPF": ["Belirtilmemiş", "30"],

    # Spor
    "Ağırlık": ["Belirtilmemiş", "1 kg"],
    "Ekipman Türü": ["Belirtilmemiş", "Dambıl"],
    "Malzeme Türü": ["Belirtilmemiş", "Demir"],

    # Evcil Hayvan
    "Hayvan Türü": ["Belirtilmemiş", "Kedi"],
    "Mama Tipi": ["Belirtilmemiş", "Kuru Mama"],
    "Gramaj": ["Belirtilmemiş", "500 gr"],
    "İçerik": ["Belirtilmemiş", "Tavuklu"],

    # Kitap & Kırtasiye
    "Dil": ["Belirtilmemiş", "Türkçe"],
    "Basım Dili": ["Belirtilmemiş", "Türkçe"],
    "Kapak Tipi": ["Belirtilmemiş", "Karton Kapak"],
    "Sayfa Sayısı": ["Belirtilmemiş", "160"],
    "Kağıt Tipi": ["Belirtilmemiş", "1. Hamur"],

    # Otomotiv
    "Araç Tipi": ["Belirtilmemiş", "Otomobil"],
    "Uygunluk": ["Belirtilmemiş", "Universal"],

    # Takı & Aksesuar
    "Maden": ["Belirtilmemiş", "Çelik"],
    "Kaplama": ["Belirtilmemiş", "Altın Kaplama"],
    "Taş Tipi": ["Belirtilmemiş", "Zirkon"],
    "Uzunluk": ["Belirtilmemiş", "45 cm"],

    # Paket İçeriği
    "Paket İçeriği": ["Tekli", "Belirtilmemiş"],

    # Diğer
    "Ürün Tipi": ["Belirtilmemiş", "Tekli"],
    "Model": ["Belirtilmemiş", "Standart"],
    "Marka": ["Belirtilmemiş", "OEM"],
    "Özellik": ["Belirtilmemiş"],
}

# Opsiyonel olarak rastgele değer kullanılabilecek alanlar
RANDOM = {
    "Yaş": ["Belirtilmemiş", "5+ Yaş", "2 – 3 Yaş", "6 – 8 Yaş", "7 – 8 Yaş", "9 – 10 Yaş"],
    "Koku Tipi": ["Çiçeksi", "Odunsu", "Baharatlı", "Meyveli"],
    "Topuk Boyu": ["2 cm", "3 cm", "5 cm", "8 cm"],
    "Disk Kapasitesi": ["256 GB", "512 GB", "1 TB"],
    "Renk": ["Siyah", "Beyaz", "Mavi", "Kırmızı", "Yeşil", "Çok Renkli"],
    "SPF": ["15", "30", "50", "100"],
}

# Fonksiyon: Öncelik sırasına göre en uygun değeri getirir
def get_default_options_for_field(field):
    """Belirtilen alan için öncelik sırasına göre tüm varsayılan seçenekleri bir liste olarak döndürür."""
    options = PRIORITY_DEFAULTS.get(field, [])
    # Listede boş veya None değer varsa onları temizleyip döndür.
    return [opt for opt in options if opt]