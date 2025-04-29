class ScreenRegion:
    def __init__(self, left: int, top: int, width: int, height: int):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def __repr__(self):
        return f"ScreenRegion(left={self.left}, top={self.top}, width={self.width}, height={self.height})"
