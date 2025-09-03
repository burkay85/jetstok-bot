import os, re, time, sys, platform, subprocess, ctypes, signal, datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout, expect

from rules_defaults import get_default_options_for_field

# ================== AYARLAR ==================
load_dotenv()
BASE = os.getenv("PANEL_URL", "https://app.jetstok.com")
LIST_URL = os.getenv("LIST_URL", "https://app.jetstok.com/products-2/not-live")
EMAIL = os.getenv("EMAIL", "modafiks@gmail.com")
PASSWORD = os.getenv("PASSWORD", "modafiksjet")

# Headless arka plan çalıştırma
HEADLESS = os.getenv("HEADLESS", "1").strip() not in ["0", "false", "False"]
# Ekip manuel giriş yapacaksa ENTER bekleyelim
MANUAL_LOGIN_FALLBACK = True  # bu senaryoda özellikle açık

SLOW_MO_MS = int(os.getenv("SLOW_MO_MS", "0" if HEADLESS else "250"))
TIMEOUT = int(os.getenv("TIMEOUT", "30000"))

# ================== LOG ==================
LOG_FILE = os.getenv("LOG_FILE", "bot_log.txt")

def log(msg: str):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

# ================== UYKU / EKRAN KORUYUCU BLOK ==================
class SleepBlocker:
    def __init__(self):
        self.os = platform.system()
        self._proc = None

    def start(self):
        try:
            if self.os == "Windows":
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000040)
                log("✅ Windows uyku engelleme aktif.")
            elif self.os == "Darwin":
                self._proc = subprocess.Popen(["/usr/bin/caffeinate", "-dimsu"])
                log("✅ macOS caffeinate başlatıldı.")
            else:
                try:
                    self._proc = subprocess.Popen(
                        ["systemd-inhibit", "--why=Running bot", "--mode=block", "sleep", "9999999"]
                    )
                    log("✅ Linux systemd-inhibit aktif.")
                except Exception:
                    log("ℹ️ Uyku engelleme desteklenmiyor (Linux).")
        except Exception as e:
            log(f"⚠️ Uyku engelleme başlatılamadı: {e}")

    def stop(self):
        try:
            if self.os == "Windows":
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
                log("✅ Windows uyku engelleme kapatıldı.")
            elif self._proc:
                self._proc.terminate()
                self._proc = None
                log("✅ macOS/Linux uyku engelleme kapatıldı.")
        except Exception as e:
            log(f"⚠️ Uyku engelleme durdurulamadı: {e}")

# ================== YARDIMCI FONKSİYONLAR ==================
def by_label_select_in_container(container, label_text, value):
    label_text_clean = label_text.replace('*', '').strip()
    log(f"- '{label_text_clean}' alanı için '{value}' deneniyor...")
    page = container.page
    try:
        select2_container = container.locator(".select2-container").first
        if select2_container.count() > 0:
            select2_container.click()
            page.wait_for_timeout(400)
            option_in_dropdown = page.locator(
                ".select2-results__option",
                has_text=re.compile(re.escape(value), re.IGNORECASE)
            ).first
            option_in_dropdown.wait_for(state="visible", timeout=2000)
            option_in_dropdown.click()
            log(f"  ✓ '{value}' seçildi.")
            page.wait_for_timeout(200)
            return True
        return False
    except Exception:
        log(f"  ✗ '{value}' seçeneği bulunamadı veya seçilemedi.")
        if page.locator(".select2-container--open").count() > 0:
            page.keyboard.press("Escape")
        return False

def open_trendyol_drawer(page):
    log("Trendyol çekmecesi açılmaya çalışılıyor...")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    trendyol_link = page.locator('a:has(img[src*="trendyol.png"])')
    trendyol_link.wait_for(state="visible", timeout=10000)
    trendyol_link.click()
    drawer_header = page.get_by_text("Pazaryeri Entegrasyonu").first
    drawer_header.wait_for(state="visible", timeout=TIMEOUT)
    log("✅ Trendyol çekmecesi başarıyla açıldı!")
    page.wait_for_timeout(1000)

def expand_ana_urun(page):
    log("Ana Ürün alanı genişletiliyor...")
    ana_urun_header = page.locator("a.accordion-head:has-text('Ana Ürün')").nth(1)
    ana_urun_header.wait_for(state="visible")
    accordion_body = ana_urun_header.locator("xpath=following-sibling::div[1]")
    if 'show' not in (accordion_body.get_attribute('class') or ''):
        log("Başlık kapalı, açmak için tıklanıyor...")
        ana_urun_header.click(force=True)
        log("Formun tamamen açılması bekleniyor...")
        expect(accordion_body).to_have_class(re.compile("show"), timeout=15000)
    else:
        log("Alan zaten açık görünüyor.")
    first_label_in_form = accordion_body.locator("label").first
    expect(first_label_in_form).to_be_visible(timeout=10000)
    log("✅ Alan genişletildi ve form hazır.")
    page.wait_for_timeout(500)

def fill_required_attributes(page):
    log("Gerekli alanlar dolduruluyor...")
    ana_urun_header = page.locator("a.accordion-head:has-text('Ana Ürün')").nth(1)
    visible_form_container = ana_urun_header.locator("xpath=following-sibling::div[contains(@class, 'show')]")
    form_groups = visible_form_container.locator(".form-group:visible").all()
    log(f"{len(form_groups)} görünür form grubu bulundu.")
    for group in form_groups:
        try:
            label_element = group.locator("label").first
            label_text = (label_element.text_content() or "").strip().replace("*", "").strip()
            if group.locator(".select2-container").count() == 0:
                continue
            current_value_element = group.locator(".select2-selection__rendered").first
            current_value = (current_value_element.inner_text() or "").strip()
            log(f"- '{label_text}' alanı mevcut değer: '{current_value}'")
            if current_value.lower() in ["seçim yapın", "belirtilmemiş", ""]:
                default_options = get_default_options_for_field(label_text)
                field_filled = False
                for option in default_options:
                    if by_label_select_in_container(group, label_text, option):
                        field_filled = True
                        break
                if not field_filled:
                    log(f"  ✗ UYARI: '{label_text}' alanı için listedeki hiçbir varsayılan değer bulunamadı.")
            else:
                log(f"  ✓ '{label_text}' zaten dolu, atlanıyor.")
        except Exception:
            pass
        page.wait_for_timeout(300)
    log("✅ Görünür alanlar kontrol edildi.")

def publish_on_marketplace_and_save(page):
    log("Pazaryerinde satışa açılıyor...")
    try:
        publish_button = page.locator("button[onclick*='ProductTransfer']").first
        publish_button.scroll_into_view_if_needed(timeout=5000)
        publish_button.click(force=True)
        page.wait_for_timeout(1500)
        ok_button = page.locator("button:has-text('Evet'), button:has-text('Onayla'), button:has-text('Tamam')").first
        if ok_button.count() > 0:
            ok_button.click()
            page.wait_for_timeout(2500)
            log("✅ Satışa açma onaylandı.")
        else:
            log("⚠ Onay butonu çıkmadı veya gerekmedi.")
        log("✅ Ürün satışa açıldı.")
    except Exception as e:
        log(f"❌ Satışa Aç butonuna tıklanamadı: {e}")
        return False
    log("Ana ürün değişiklikleri kaydediliyor...")
    save_button = page.locator("button", has_text="Kaydet").last
    save_button.click(force=True)
    page.wait_for_timeout(2500)
    log("✅ Ana ürün kaydedildi.")
    return True

def wait_list_table(page):
    log("Ürün listesinin yüklenmesi bekleniyor...")
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)
    page.locator("table tbody tr").first.wait_for(timeout=TIMEOUT)
    log("✅ Liste yüklendi.")

def open_first_row(page):
    log("Listedeki ilk ürün açılıyor...")
    rows = page.locator("table tbody tr")
    rows.first.wait_for(timeout=TIMEOUT)
    links = rows.first.locator('a:not(:has(img))')
    if links.count() > 0:
        links.first.click()
    else:
        rows.first.locator('a').first.click()
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)

def go_back_to_list(page):
    log("Ürün listesine geri dönülüyor...")
    modal_header = page.get_by_text("Pazaryeri Entegrasyonu").first
    if modal_header.is_visible():
        log("Trendyol çekmecesi açık, kapatılıyor...")
        try:
            modal_save_button = page.locator(".sidenav-footer button", has_text="Kaydet").first
            if modal_save_button.is_visible():
                modal_save_button.click()
            else:
                page.keyboard.press("Escape")
        except Exception:
            page.keyboard.press("Escape")
        page.wait_for_timeout(1500)
    back_link = page.get_by_role("link", name=re.compile(r"Geri", re.I)).first
    back_link.click(force=True)
    try:
        wait_list_table(page)
    except PWTimeout:
        log("Liste yüklenemedi, sayfa yeniden yükleniyor...")
        page.reload()
        wait_list_table(page)

# ================== GİRİŞ (EKİP TIKLAYACAK) ==================
def do_login(page):
    # Headless ise uyarı
    if HEADLESS:
        log("⚠ Bu modda ekip giriş yapacak. Lütfen HEADLESS=0 ile çalıştırın; aksi halde butonlara tıklayamazsınız.")
    log("\n>>> Giriş sayfasına gidiliyor...")
    page.goto(BASE, wait_until="domcontentloaded")

    # E-posta & şifreyi otomatik doldur
    try:
        email_input = page.locator('input[name="formModel.Email"]')
        email_input.wait_for(state="visible", timeout=15000)
        email_input.fill(EMAIL)
        pwd_input = page.locator('input[name="formModel.Password"]')
        pwd_input.fill(PASSWORD)
        log("✅ E-posta ve şifre dolduruldu. (Giriş butonuna ekip basacak.)")

        # Şifre alanına odak bırakalım (ekip gerekirse düzeltip tıklasın)
        pwd_input.focus()

        # Kullanıcıyı bilgilendir
        log("Lütfen tarayıcıda 'Giriş Yap' butonuna basın; 2FA/Doğrulama varsa tamamlayın.")
        log("Hazır olduğunuzda bu terminale dönüp ENTER'a basın. Otomatik algılama da var (panel açılırsa beklemeden devam eder).")

    except Exception as e:
        log(f"⚠ Giriş formu doldurulamadı: {e}. Yine de manuel giriş yapabilirsiniz.")

    # Otomatik algılama döngüsü (dashboard/list belirirse devam)
    def logged_in_detected() -> bool:
        try:
            # Panelde sık görülen göstergeler: menü/çıkış linki ya da ürün listesi
            if "products-2" in page.url or "dashboard" in page.url.lower():
                return True
            if page.locator("a:has-text('Çıkış')").count() > 0:
                return True
            if page.locator("table tbody tr").count() > 0:
                return True
        except Exception:
            pass
        return False

    # 3 dakikaya kadar login'i otomatik algılamaya çalış
    for _ in range(180):
        if logged_in_detected():
            log("✅ Giriş algılandı (otomatik).")
            return True
        page.wait_for_timeout(1000)

    # Hâlâ algılanmadıysa ENTER bekle
    if MANUAL_LOGIN_FALLBACK:
        try:
            input(">>> Giriş tamamlandıysa ENTER'a basın...")
        except EOFError:
            # paketlenmiş çalıştırmada stdin yoksa 5 sn daha bekleyip devam
            page.wait_for_timeout(5000)
        log("▶︎ Manuel onay alındı, devam ediliyor.")
        return True

    return False

# ================== ANA AKIŞ ==================
def run(list_url=LIST_URL):
    sleep_block = SleepBlocker()
    sleep_block.start()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO_MS if not HEADLESS else 0,
            args=["--disable-blink-features=AutomationControlled"]
        )
        ctx = browser.new_context()
        page = ctx.new_page()
        page.set_default_timeout(TIMEOUT)

        if not do_login(page):
            log("❌ Giriş yapılamadı, işlem sonlandırılıyor.")
            browser.close()
            sleep_block.stop()
            return

        log("Giriş yapıldı, ürün listesine gidiliyor...")
        page.goto(list_url, wait_until="domcontentloaded")

        processed_count = 0
        while True:
            try:
                wait_list_table(page)
            except PWTimeout:
                log("Sayfada işlenecek ürün kalmadı.")
                break

            if page.locator("table tbody tr").count() == 0:
                log("Tüm ürünler işlendi.")
                break

            processed_count += 1
            log(f"\n--- Toplam {processed_count}. ürün işleniyor ---")

            try:
                open_first_row(page)
                open_trendyol_drawer(page)
                expand_ana_urun(page)
                fill_required_attributes(page)
                log("Form dolduruldu. Ürün satışa açılıyor...")
                success = publish_on_marketplace_and_save(page)

                if not success:
                    log("UYARI: Ürün satışa açılamadı, bir sonraki ürüne geçiliyor.")

                go_back_to_list(page)
                log(f"--- 🎉 Ürün {processed_count} işlemi tamamlandı ---")

            except Exception as e:
                log(f"HATA: Ürün {processed_count} işlenirken bir sorun oluştu: {e}")
                try:
                    page.screenshot(path=f'error_item_{processed_count}.png')
                    log(f"Ekran görüntüsü kaydedildi: error_item_{processed_count}.png")
                except Exception as ss_e:
                    log(f"Ekran görüntüsü alınamadı: {ss_e}")
                try:
                    log("Hata sonrası listeye dönülmeye çalışılıyor...")
                    page.goto(list_url)
                    continue
                except Exception as goto_e:
                    log(f"Listeye dönülemedi, işlem durduruluyor: {goto_e}")
                    break

        log("\nTüm ürünler işlendi. İşlem tamamlandı.")
        page.wait_for_timeout(2000)
        browser.close()
    sleep_block.stop()

if __name__ == "__main__":
    run()
