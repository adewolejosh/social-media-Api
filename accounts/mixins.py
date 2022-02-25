from django.http import Http404


class ObjectDetailMixin:
    model = None

    def get_object(self, id):
        try:
            obj = self.model.objects.get(id=id)
            self.check_object_permissions(self.request, obj)
        except self.model.DoesNotExist:
            raise Http404('could not find the requested resource')
        return obj
