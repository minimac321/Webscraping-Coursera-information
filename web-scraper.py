from gui import create_gui


class WebScraper:

    def __init__(self):
        pass

    def fetch_info(self):
        print(f"Working 1")


def main():
    # window
    web_scraper = WebScraper()

    tkWindow = create_gui(web_scraper)
    tkWindow.mainloop()


if __name__ == "__main__":
    main()
