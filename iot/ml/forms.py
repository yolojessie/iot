from django import forms
from ml.models import Survive
from main.constants import MALE, FEMALE, defaultError


SEX_CHOICE = [(1, MALE), (0, FEMALE)]
EMBARKED_CHOICE = [(0, 'C'), (1, 'Q'), (2, 'S')]
PCLASS_CHOICE = [(0, '1st'), (1, '2nd'), (2, '3rd')]
CARBIN_CHOICE = [(0, 'noCabin'), (1, 'C'), (2, 'E'), (3, 'G'), (4, 'D'), (5, 'A'), (6, 'B'), (7, 'F'), (8, 'T')]
TITLE_CHOICE = [(0, 'Mr'), (1, 'Mrs'), (2, 'Miss'), (3, 'Master')]
class SurviveForm(forms.ModelForm):
    Age = forms.FloatField(min_value=1, error_messages=defaultError)               #年齡
    Embarked = forms.ChoiceField(choices=EMBARKED_CHOICE, error_messages=defaultError)        #從哪個港口上船 (C = Cherbourg, Q = Queenstown, S = Southampton) 
    Fare = forms.FloatField(min_value=0.0, error_messages=defaultError)              #費用
    Pclass = forms.ChoiceField(choices=PCLASS_CHOICE, error_messages=defaultError)          #社經地位的代表(上中下)
    Sex = forms.ChoiceField(choices=SEX_CHOICE, error_messages=defaultError)             #性別1男0女
    Family_Size = forms.FloatField(min_value=0, error_messages=defaultError)     #一起去的親戚家庭人數   
    Title2 = forms.ChoiceField(choices=TITLE_CHOICE, error_messages=defaultError)          # 名字前面的特殊開頭
    Cabin = forms.ChoiceField(choices=CARBIN_CHOICE, error_messages=defaultError)            #住的艙位
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') 
        super(SurviveForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        servive = super(SurviveForm, self).save(commit=False)
        servive.user = self.user
        if commit:
            servive.save()
        return servive
    
    
    class Meta:
        model = Survive
        exclude = ['Ticket_info', 'survive', 'user']