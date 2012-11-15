#coding=utf-8
from bootstrap.forms import BootstrapModelForm, Fieldset
from project.models import Project, Action


class ProjectForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"设置", "name", "url", ),
        )
        model = Project
        exclude = ('dateline', 'lastview', 'creator', 'participants', 'key', 'token')


class ActionForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"行为设置", "name", "url", "xpath", "event", "is_flag"),
        )
        model = Action
        exclude = ('project')
