from api.quizlet import QuizletApi

# Quizlet Caches
quizlet = QuizletApi()
quizlet.cache_vocabulary(['https://quizlet.com/de/646881951/verben-%E5%8B%95%E8%A9%9E-flash-cards/', 'https://quizlet.com/de/651481559/adverben-%E5%89%AF%E8%A9%9E-flash-cards/', 'https://quizlet.com/de/650870756/adjektive-flash-cards/', 'https://quizlet.com/de/649395529/nomen-%E5%90%8D%E8%A9%9E-flash-cards/'], 'manu')