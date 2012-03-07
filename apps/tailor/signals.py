from django.dispatch import Signal


build_item_complete = Signal(providing_args=['thread'])
