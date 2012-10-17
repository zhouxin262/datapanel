#coding=utf-8
from bootstrap import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
from models import Project, Action, TrackCondition, TrackConditionTester

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
            Fieldset(u"行为设置","name", "url","xpath","event" ),
            )
        model = Action
        exclude = ('project')

class ConditionForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"条件设定", "name" ),
            )
        model = TrackCondition
        exclude = ('project')

class ConditionTesterForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"条件设定", "operator", "col_name", "test_operator", "test_value"),
            )
        model = TrackConditionTester
        exclude = ('condition')