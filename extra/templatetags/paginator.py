# -*- coding: utf-8 -*-
from django import template

register = template.Library()

def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.
    """
    page_obj=context["page_obj"]
    gets_string = context.get('gets_string')
    page=page_obj.number
    pages=page_obj.paginator.num_pages
    page_numbers = [n for n in \
                    range(page - adjacent_pages, page + adjacent_pages + 1) \
                    if n > 0 and n <= pages]
    return {
        "hits": page_obj.paginator.count,
        "results_per_page": page_obj.paginator.per_page,
        "page": page,
        "pages": pages,
        "page_numbers": page_numbers,
        "next": page_obj.next_page_number(),
        "previous": page_obj.previous_page_number(),
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "show_first": 1 not in page_numbers,
        "show_last": pages not in page_numbers,
        "gets_string":gets_string,
    }

register.inclusion_tag("paginator.html", takes_context=True)(paginator)
