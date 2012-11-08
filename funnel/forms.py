#coding=utf-8
from bootstrap.forms import BootstrapModelForm, Fieldset
from funnel.models import Funnel, FunnelAction


class FunnelForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"", "name"),
        )
        model = Funnel
        exclude = ('project')


class FunnelActionForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"", "action",),
        )
        model = FunnelAction
        exclude = ('funnel','order')
