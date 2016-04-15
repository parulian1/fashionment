"""
Extra HTML Widget classes
"""

import datetime
import re

from django.forms.widgets import Widget,Input,Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.datastructures import MultiValueDict, MergeDict

from django.utils.encoding import force_unicode

__all__ = ('SelectDateWidget','ImageInput','ImageWidget','TextOnlyWidget','SelectFk','SelectMultipleFk')

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class SelectDateWidget(Widget):
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None,lower=0,higher=0):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        if years:
            self.years = years
        else:
          if  lower:
            lower_range=lower
          else:
            lower_range=0
          if higher:
            higher_range=higher
          else:
            higher_range=0

          this_year = datetime.date.today().year
          self.years = range(this_year+lower_range, this_year+higher_range+1)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        day_choices = [(i, i) for i in range(1, 32)]
#        local_attrs['id'] = self.day_field % id_
        local_attrs = self.build_attrs(id=self.day_field % id_)
        select_html = Select(choices=day_choices).render(self.day_field % name, day_val, local_attrs)
        output.append(select_html)

        month_choices = MONTHS.items()
        month_choices.sort()
#        local_attrs = self.build_attrs(id=self.month_field % id_)
        local_attrs['id'] = self.month_field % id_
        select_html = Select(choices=month_choices).render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        local_attrs['id'] = self.year_field % id_
        select_html = Select(choices=year_choices).render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y, m, d = data.get(self.year_field % name), data.get(self.month_field % name), data.get(self.day_field % name)
        if y and m and d:
            return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)

from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.widgets import RadioFieldRenderer,RadioInput,RadioSelect
from django.conf import settings
import os

class ImageInput(RadioInput):
    def __unicode__(self):
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        url='%s%s/%s' % (settings.MEDIA_URL,self.name,conditional_escape(force_unicode(self.choice_label)))
        png_url=url+'.png'
        gif_url=url+'.gif'
        jpg_url=url+'.jpg'
        image_url=''
        if os.path.isfile('.'+png_url):
          image_url=png_url
        elif os.path.isfile('.'+gif_url):
          image_url=gif_url
        elif os.path.isfile('.'+jpg_url):
          image_url=jpg_url
        final_url = mark_safe(u'<img src="%s" alt="" /><span>%s</span>') % (image_url,self.choice_label) 
        return mark_safe(u'<label%s>%s %s</label>' % (label_for, self.tag(), final_url))

class ImageFieldRenderer(RadioFieldRenderer):    
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield ImageInput(self.name, self.value, self.attrs.copy(), choice, i)
    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
                % force_unicode(w) for w in self]))

class ImageWidget(RadioSelect):
  renderer=ImageFieldRenderer
  def __init__(self,toast, *args, **kwargs):
    self.toast='bread'
    super(ImageWidget, self).__init__(*args, **kwargs)

  def render(self, name, value, attrs=None, choices=()):
    return self.get_renderer(name, value, attrs, choices).render()

class TextOnlyWidget(Input):
    def render(self, name, value, attrs=None):
      return mark_safe(u'<b>%s</b>' %  value)

from itertools import chain
class SelectFk(Select):
    def render_options(self, choices, selected_choices):
        def render_option(option_value, option_label,option_name):
            option_value = force_unicode(option_value)
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            option_name = option_name and u" name = %s" % escape(option_name) or ''
            return u'<option%s value="%s"%s>%s</option>' % (
                option_name,
                escape(option_value), 
                selected_html,
                conditional_escape(force_unicode(option_label)))
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label, option_name in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(render_option(*option))
                output.append(u'</optgroup>')
            else:
                output.append(render_option(option_value, option_label, option_name))
        return u'\n'.join(output)

class SelectMultipleFk(SelectFk):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select multiple="multiple"%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe(u'\n'.join(output))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def _has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        for value1, value2 in zip(initial, data):
            if force_unicode(value1) != force_unicode(value2):
                return True
        return False

class NamelessInput(Input):
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class NamelessTextInput(NamelessInput):
  input_type='text'

class NamelessTextInput(NamelessInput):
  input_type='text'

class NamelessRadioInput(NamelessInput):
  input_type='radio'
