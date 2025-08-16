from django import template

register = template.Library()

@register.filter
def slice_pages(page_range, current_page):
    current_page = int(current_page)
    start_index = max(0, current_page - 6)
    end_index = min(start_index + 11, len(page_range))
    return page_range[start_index:end_index]

@register.filter
def to_int(i):
    return int(i)