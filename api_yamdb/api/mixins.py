from rest_framework import mixins, viewsets


class MixinSetCreateListDestroy(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass
