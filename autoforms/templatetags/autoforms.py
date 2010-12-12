#encoding=utf-8
from django import template
from django.template import resolve_variable,TemplateSyntaxError
import re

register = template.Library()
kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")

def form_value(value):
  if not value:
	return ''
  if type(value) == list:
	return ','.join(value)
  return value

register.filter('formvalue',form_value)


class DataListNode(template.Node):
    def __init__(self,form,args,kwargs):
        self.form = form
        self.args = args
        self.kwargs = kwargs
        self.fields = None
        self.template = 'autoforms/datalist.html'
        if self.args:
            if len(args) >= 3:
                self.fields = args[2]
            if len(args) >=4:
                self.template = args[3]
        elif self.kwargs:
            self.fields = self.kwargs.get('fields',None)
            self.template = self.kwargs.get('template',None)
        if self.fields:
            self.fields = self.fields.split(',')

    def render(self,context);
        formlist = self.form.search(*self.args,**self.kwargs)
        context = {'datalist':formlist,'fields':self.fields}
        tp = template.Template(self.template)
        return tp.render(context)



def formdata(parser,token):
    bits = token.split_contents()
        if len(bits) < 2:
            raise TemplateSyntaxError("'%s' takes at least one argument (form to a view)" % bits[0])
    form = bits[1]
    args = []
    kwargs = {}
    bits = bits[2:]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name,value = match.groups()
            if name:
                kwarg[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return DataListNode(form,args,kwargs)

register.tag(formdata)
