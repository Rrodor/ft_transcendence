from django import template

register = template.Library()

@register.filter(name='friendship_user')
def friendship_user(friendship, user):
    friend = friendship.user1 if friendship.user1 != user else friendship.user2
    return friend