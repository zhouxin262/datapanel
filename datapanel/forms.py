#coding=utf-8
from bootstrap import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
from models import Project, Action

class ProjectForm(BootstrapModelForm):
	class Meta:
		layout = (
            Fieldset(u"设置", "name", "url", ),
        )
		model = Project
		exclude = ('dateline','lastview','creator','participants','key','token')


class ActionForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"动作","name", "url","xpath","event" ),
            )
        model = Action
        exclude = ('project')
