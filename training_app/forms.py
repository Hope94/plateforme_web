from django import forms

MALWARE_DATASETS= [
    ('virusshare', 'Virusshare'),
    ('drebin', 'Drebin'),
    ]

BEGNIN_DATASETS= [
    ('dzplay', 'DZPlay'),
    ('darwin', 'Darwin'),
    ]

class DatasetsForm(forms.Form):
    list_begin_datasets=forms.CharField(label='Dataset des apps begnines', widget=forms.Select(choices=BEGNIN_DATASETS))
    list_malware_datasets=forms.CharField(label='Dataset des malwares',widget=forms.Select(choices=MALWARE_DATASETS))
