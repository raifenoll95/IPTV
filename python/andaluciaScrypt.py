import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# URL del video en vivo
url = "https://www.canalsurmas.es/videos/131772-canal-sur-andalucia"

# Configuración de Selenium con Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # No abrir ventana de navegador

# Inicializar el WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Activar las herramientas de desarrollo de Chrome para capturar tráfico de red
driver.execute_cdp_cmd('Network.enable', {})

try:
    # Navegar a la página
    driver.get(url)

    # Esperar un poco para que cargue el contenido
    time.sleep(5)

    # Buscar el botón de "play" y hacer clic en él para iniciar el video
    play_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Play"]')
    play_button.click()

    # Esperar a que la solicitud del video sea realizada
    time.sleep(5)

    # Capturar las solicitudes de red
    requests = driver.execute_cdp_cmd('Network.getResponseBody', {})

    # Buscar el enlace M3U8 en las solicitudes de red
    m3u8_url = None
    for request in requests['responses']:
        if '.m3u8' in request['url']:
            m3u8_url = request['url']
            break
    
    # Ver si se encontró el enlace M3U8
    if m3u8_url:
        print(f"✅ Enlace M3U8 encontrado: {m3u8_url}")

        # Guardar el enlace M3U8 en un archivo .m3u
        with open("canalsur.m3u", "w") as f:
            f.write("#EXTM3U\n")
            f.write(f"#EXTINF:-1,Canal Sur Andalucía\n")
            f.write(m3u8_url + "\n")
        print("✅ Enlace M3U8 guardado en canalsur.m3u")
    else:
        print("❌ No se encontró un enlace M3U8.")

finally:
    # Cerrar el navegador
    driver.quit()
