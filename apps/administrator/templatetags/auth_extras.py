from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='exclude_group')
def exclude_group(user, group_name):
    return user.groups.exclude(name=group_name).exists()
