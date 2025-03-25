from openai import OpenAI
import requests
import json
import os
from Word_Document import Word_Document

class AI:
    def __init__(self, ai_model, api_key):
        self.ai_model = ai_model
        self.api_key = api_key
        self.book_type = ""
        self.theme = ""
        self.book_length = 0
        self.chapter_ammount = 0
        self.chapter_slice_ammount = 0
	self.word_document = Word_Document("Text.docx")

    def request(self, message):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )

        completion = self.client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model=self.ai_model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        if not completion.choices or not completion.choices[0].message.content:
            print("Fehler: Keine gültige Antwort erhalten.")
            return None
        return completion.choices[0].message.content
    
    def create_outline(self, book_type, theme, book_length, chapter_ammount):
        self.book_type = book_type
        self.theme = theme
        self.book_length = book_length
        self.chapter_ammount = chapter_ammount

        chapter_slice_ammount = round((book_length / chapter_ammount) / 3.0, 0)
        
        self.chapter_slice_ammount = chapter_slice_ammount
        
        outline = self.request(f"Erstelle eine Gliederung zu einem {book_type} mit dem Thema {theme}, mit {book_length} Seiten und {chapter_ammount} Kapiteln. Unterteile jedes Kapitel in {chapter_slice_ammount} Unterpunkten. Bitte markiere den Anfang und das Ende der Gliederungen mit 5 Sternzeichen, also: *****")
        return outline

    def control_outline(self, ai, outline):
        critic = ai.request(f"Kritisiere folgende Gliederung zu einem {self.book_type} mit dem Thema {self.theme} mit {self.book_length} Seiten und {self.chapter_ammount} Kapiteln: {outline} Markiere bitte den Anfang jedes positivem Kritikpunktes mit drei Plus Zeichen und einem Stern, also: '+++*', das Ende jedes positivem Kritikpunktes mit drei Plussen und einem Hashtag, also: +++# und den Anfang jedes negativen Kritikpunktes mit drei Minussen Zeichen und einem Stern, also: '---*', das Ende jedes positivem Kritikpunktes mit drei Minussen und einem Hashtag, also: ---#. Achte dabei bitte darauf, dass die Menge an Kapiteln und Unterkapiteln sich nicht veränder soll.")
        improved_outline = self.request(f"Verbessere bitte deine erstellte Gliederung {outline} mit folgender Kritik: {critic}")
        return improved_outline

    def create_chapterpart(self, chapter, chapterpart, outline):
        chapterpart = self.request(f"Schreibe bitte zur folgenden Gliederung: {outline} vom Kapitel {chapter} den Abschnitt{chapterpart} vollständig aus. Formatiere bitte den Text so, dass er aus einem txt Dokument in ein docx Dokument umgewandelt werden kann, ohne Formatierungsfehler zu erhalten. Die Schriftart soll Arial sein und überschriften sollen Größer als der Text sein. Bitte achte auf eine gescheite Formatierung")
        return chapterpart
    
    def control_chapterpart(self, ai, outline, chapter, chapterpart, chapterpart_text):
        critic = ai.request(f"Kritisiere folgenden Kapitelausschnitt vom Kapitel {chapter}.{chapterpart} zu einem {self.book_type} mit dem Thema {self.theme} mit {self.book_length} Seiten mit {self.chapter_ammount} Kapiteln und folgender Gliederung {outline}: {chapterpart_text}")
        improved_chapterpart = self.request(f"Verbessere bitte dein erstelltes Kapitel {chapter}.{chapterpart}: {chapterpart_text} mit deiner Gliederung: {outline} mit folgender Kritik: {critic}  Formatiere bitte den Text so, dass er aus einem txt Dokument in ein docx Dokument umgewandelt werden kann, ohne Formatierungsfehler zu erhalten. Die Schriftart soll Arial sein und überschriften sollen Größer als der Text sein. Bitte achte auf eine gescheite Formatierung")
        return improved_chapterpart

    def create_book(self, ai_list, file):
        self.file = open(file, "a")
        
        outline = self.create_outline("Roman", "Actionthriller", 150, 10)
        print(f"outline before: {outline}")
        for ai in ai_list:
            outline = self.control_outline(ai, outline)
        print(f"outline after: {outline}")

        for i_chapter in range(1, self.chapter_ammount + 1):
            for i_chapterpart in range(1, int(self.chapter_slice_ammount) + 1):
                chapter_part = self.create_chapterpart(i_chapter, i_chapterpart, outline)
                print(f"chapterpart before: {chapter_part}")
                for ai in ai_list:
                    chapter_part = self.control_chapterpart(ai, outline, i_chapter, i_chapterpart, chapter_part)
                self.file.write(f"{chapter_part} \n")
                print(f"chapterpart after: {chapter_part}")
            self.file.write("\n")

    def get_title(self):
        title = self.request(f"Welchen Titel würdest du folgendem Buch geben?: {self.book}")
        return title
    
    def get_request_ammount(self):
        response = requests.get(
            url="https://openrouter.ai/api/v1/auth/key",
            headers={
                "Authorization": f"Bearer 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"
            }
        )
        
        return json.dumps(response.json(), indent=2)["data"]["rate_limit"]["requests"]