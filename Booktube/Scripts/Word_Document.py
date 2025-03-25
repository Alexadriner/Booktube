from docx import Document

class Word_Document:
    def __init__(self, name):
        document = Document()
        document.save(name)

    def remove_insignificancies(self, text):
        for character in text:
            if character == "{" or "}" or "`":
                text.remove(character)

        text_array = text.split()
        for word in text_array:
            if word == "boxed":
                text_array.remove(word)

        SEPARATOR = " "
        improved_text = SEPARATOR.join(text_array)
        return improved_text

    def append_paragraph(self, paragraph):
        improved_paragraph = self.remove_insignificancies(paragraph)