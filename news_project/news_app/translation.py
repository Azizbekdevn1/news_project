from modeltranslation.translator import register,TranslationOptions,translator

from .models import News,Category
#1-usul
@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields =('title','body')

#2-usul

#translator.register(News,NewsTranslationOptions)
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields =('name',)







