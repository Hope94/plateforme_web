import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pfe_plateforme_web.settings')

import django
django.setup()

import hashlib
from django.forms.models import model_to_dict
from main.models import Apk,Feature,Extract,Dataset,PermissionAPI,SuspiciousAPI
from main.androguard.androguard.util import get_certificate_name_string
from pfe_plateforme_web.settings import APK_DIR




class AndroguardAnalysis(object):

    def __init__(self, app_path):
        self.app_path = app_path
        from androguard.core.bytecodes.apk import APK
        self.a = APK(app_path)
        self.d = None
        self.dx = None

    def get_detailed_analysis(self):
        from androguard.misc import AnalyzeDex
        self.d, self.dx = AnalyzeDex(self.a.get_dex(), raw=True)

    def get_developer_name(self):
        developer = ""
        signatures = self.a.get_signature_names ()
        for signature in signatures:
            cert = self.a.get_certificate (signature)
            issuer = get_certificate_name_string (cert.issuer)
            attr_list = issuer.split (',')
            for attr in attr_list:
                if attr.startswith (" organizationName") or attr.startswith ("organizationName"):
                    developer = attr.split ('=')[1]
        return developer

def get_hashes(app_path, block_size=2 ** 8):
    md5 = hashlib.md5 ()
    sha1 = hashlib.sha1 ()
    sha256 = hashlib.sha256 ()
    f = open (app_path, 'rb')
    while True:
        data = f.read (block_size)
        if not data:
            break

        md5.update (data)
        sha1.update (data)
        sha256.update (data)
    return [md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()]


def insert_apk(path_to_apk,malignity=-1)->Apk:
    androguard=AndroguardAnalysis(app_path=path_to_apk)
    hashes=get_hashes(path_to_apk)
    name =androguard.a.get_app_name()
    package = androguard.a.get_package()
    developer = androguard.get_developer_name()
    displayed_version = androguard.a.get_androidversion_name()
    size = os.path.getsize(path_to_apk)
    md5 = hashes[0]
    sha1 = hashes[1]
    sha256 = hashes[2]
    apk=Apk.objects.get_or_create(name=name
                                  ,malignity=malignity
                                  ,package=package
                                  ,developer=developer
                                  ,displayed_version=displayed_version
                                  ,size=size,md5=md5,sha1=sha1,sha256=sha256)[0]
    apk.save()
    return apk

def insert_feature(name,type)->Feature:
    feature=Feature.objects.get_or_create(name=name,type=type)[0]
    feature.save()
    return feature

def insert_extract(apk,feature,nb_feature)->Extract:
    extract=Extract.objects.get_or_create(apk=apk,feature=feature,nb_feature=nb_feature)[0]
    extract.save()
    return extract

def get_apk_record(apk_id: int) -> Apk:
    apk=Apk.objects.get(pk=apk_id)
    return apk

def get_apks()->list:
    return [apk for apk in Apk.objects.all()]

def get_apk_features(apk_id: int) -> list:
    apk=Apk.objects.get(pk=apk_id)
    list_extract = Extract.objects.filter(apk=apk).all()
    return [(e.feature,e.nb_feature) for e in list_extract]

def get_apk_malignity(apk_name: str) -> int:
    apk=Apk.objects.get(name=apk_name)
    return apk.malignity


def get_datasets_apks(datasets: list) -> set:
    apks=set()
    for dataset in datasets:
        apks.update(dataset.apk_set.all())
    return apks

def is_apk_in_db(sha256) -> bool:
    num_results = Apk.objects.filter (sha256=sha256).count ()
    return num_results!=0


def get_api_permission_mapping():
    return PermissionAPI.objects.all()


def get_suspicious_api():
    return SuspiciousAPI.objects.all()

def add_apk_to_dataset(apk:Apk,dataset_name:str):
    dataset = Dataset.objects.get_or_create (name=dataset_name)[0]
    dataset.save()
    apk.datasets.add(dataset)
    apk.save()



if __name__=='__main__':
    app_name="sample.apk"
    path_to_apk=os.path.join(APK_DIR,app_name)
    print(insert_apk(path_to_apk=path_to_apk,malignity="0").pk)



