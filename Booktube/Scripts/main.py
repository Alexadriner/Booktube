from openai import OpenAI
from AI import AI
from Word_Document import Word_Document



#KIs erstellen
deepseek = AI("deepseek/deepseek-r1-zero:free", "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")
gemma_3_1b = AI("google/gemma-3-1b-it:free", "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")
reka_flash_3 = AI("rekaai/reka-flash-3:free", "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")
qwen_qwq_32b = AI("qwen/qwq-32b:free", "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")

word_document = Word_Document("Test.docx")





