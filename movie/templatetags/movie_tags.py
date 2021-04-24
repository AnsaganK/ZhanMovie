from django import template
import json
import random
register = template.Library()

@register.filter(name="shortContent")
def shortContent(text):
    return text[:150]

@register.filter(name='isRole')
def isRole(user, role):
    if user.is_authenticated and user.profile.role:
        if user.profile.role.name_ru == role:
            return True
    return False

@register.filter(name="validDate")
def validDate(number):
    if number:
        number = int(number)
        if number<10:
            return '0'+str(number)
        return str(number)
    return None

@register.filter(name="refactorList")
def refactorList(query):
    data = ''
    for i in query:
        data += str(i.name) + ', '
    data = data[:-2]
    return data
@register.filter(name='returnDicEl')
def returnDicEl(data, id):
    return data[id]



@register.filter(name="getFirstElement")
def getFirstElement(element):
    return int(element[0])