from playwright.sync_api import Page


def get_all_txt(url, page: Page):
    try:
        page.goto(url, wait_until="domcontentloaded")  

        #Remove scripts e estilos (invisíveis)
        page.evaluate("""
            () => {
                const elements = document.querySelectorAll("script, style, noscript");
                elements.forEach(el => el.remove());
            }
        """)
        texto = page.inner_text("body")
        
        if len(texto) >= 5000:
            texto = texto[0:4990]
        return texto.strip()
    except Exception as e:
        print(f"[Playwright Erro ao acessar URL]: {url}\nMotivo: {e}")
        return "Nada"