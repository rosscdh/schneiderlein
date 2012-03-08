from django.dispatch import Signal


build_item_commence = Signal(providing_args=['thread'])
build_item_complete = Signal(providing_args=['thread'])
