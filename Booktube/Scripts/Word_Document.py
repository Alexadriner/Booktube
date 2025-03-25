from docx import Document

class Word_Document:
    def __init__(self, name):
        self.document = Document()
        self.document.save(name)

    def remove_insignificancies(self, text):
        for character in text:
            if character == "{" or "}" or "`" or "*":
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
					self.documment.add_paragraph(improved_paragraph)