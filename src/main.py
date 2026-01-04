from textnode import TextNode, TextType

def main():
    text1 = TextNode("Hello, World!", TextType.TEXT)
    text2 = TextNode("This is bold text.", TextType.BOLD)
    text3 = TextNode("This is some anchor text.", TextType.LINK, url="https://www.boot.dev")
    print(text1)
    print(text2)
    print(text3)

if __name__ == "__main__":
    main()