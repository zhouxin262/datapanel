#coding=utf-8
from bootstrap.forms import BootstrapModelForm, Fieldset

from models import Project

class ProjectForm(BootstrapModelForm):
	class Meta:
		layout = (
            Fieldset(u"设置", "name", "url", ),
        )
		model = Project
		exclude = ('dateline','lastview','creator','participants','key','token')