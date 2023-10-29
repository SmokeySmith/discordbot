class Pokemon:
    def __init__(self, name, image, url, isShiny) -> None:
        self.name = name
        self.image = image
        self.url = url
        self.isShiny = isShiny
        self.displayName = self.name if not self.isShiny else f":gem: Shiny {self.name} :gem:"

    def __str__(self) -> str:
        return f"{self.isShiny} {self.image}"