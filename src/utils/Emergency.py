#  ******************************************************
#  * Copyright (C) 2023 Julian Wieser
#  * julian.wieser@i-wieser.com
#  *
#  * This project can not be copied and/or distributed without the express
#  * permission of Julian Wieser
#  *******************************************************
class Emergency(object):
    origin = ''
    id = ''
    level = ''
    name = ''
    operationName = ''
    location = ''
    info = ''
    caller = ''
    program = ''
    status = ''
    receiveTad = ''
    watchOutTad = ''
    finishedTad = ''
    navigation_Figure = None

    def __init__(self, xmlOrder):
        for field in xmlOrder:
            if field.tag == "origin":
                self.origin = field.text
            elif field.tag == "operation-id":
                self.id = field.text
            elif field.tag == "level":
                self.level = field.text
            elif field.tag == "name":
                self.name = field.text
            elif field.tag == "operation-name":
                self.operationName = field.text
            elif field.tag == "location":
                self.location = field.text
            elif field.tag == "info":
                self.info = field.text
            elif field.tag == "caller":
                self.caller = field.text
            elif field.tag == "program":
                self.program = field.text
            elif field.tag == "status":
                self.status = field.text
            elif field.tag == "receive-tad":
                selfReceiveTad = field.text
            elif field.tag == "watch-out-tad":
                self.watchOutTad = field.text
            elif field.tag == "finished-tad":
                self.finishedTad = field.text

    @staticmethod
    def field(label, value):
        if value is None:
            return ""
        return label + ':' + ' ' * (40 - len(label)) + value + '\r\n'

    @staticmethod
    def fieldHtml(label, value):
        if value is None:
            return ""
        return '<tr><td>%s</td><td>%s</td></tr>' % (label, value)

    def toString(self):
        result = self.field('Einsatz', self.id)
        result += self.field('Einsatzort', self.location)
        result += self.field('Alarmstichwort', self.operationName)
        result += self.field('Alarmtext', self.info)
        result += self.field('Hausname', self.name)
        result += self.field('Alarmstufe', self.level)
        result += self.field('Anrufertelefonnummer', self.caller)
        result += self.field('Sirenenprogramm', self.program)
        result += self.field('Alarmstatus:', self.status)
        result += self.field('Alarmiert um:', self.receiveTad)
        result += self.field('Ausgerückt um:', self.watchOutTad)
        result += self.field('Eingerückt um:', self.finishedTad)
        return result

    def toHtml(self):
        result = '<h2>Einsatz: %s</h2>' % (self.id)
        result += '<table style="border:1px solid black;">'
        result += self.fieldHtml('Einsatzort', self.location)
        result += self.fieldHtml('Alarmstichwort', self.operationName)
        result += self.fieldHtml('Alarmtext', self.info)
        result += self.fieldHtml('Hausname', self.name)
        result += self.fieldHtml('Alarmstufe', self.level)
        result += self.fieldHtml('Anrufertelefonnummer', self.caller)
        result += self.fieldHtml('Sirenenprogramm', self.program)
        result += self.fieldHtml('Alarmstatus:', self.status)
        result += self.fieldHtml('Alarmiert um:', self.receiveTad)
        result += self.fieldHtml('Ausgerückt um:', self.watchOutTad)
        result += self.fieldHtml('Eingerückt um:', self.finishedTad)
        result += '</table>'
        return result
