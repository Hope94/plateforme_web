import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pfe_plateforme_web.settings')

import django
django.setup()

import hashlib
from main.models import Apk,Feature,Extract,Dataset
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


def insert_apk(path_to_apk,malignity=-1,dataset=Dataset.objects.get_or_create(name="user"))->Apk:
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
    feature=Feature.objects.get_or_create(name,type)
    feature.save()
    return feature

def insert_extract(apk,feature,nb_feature)->Extract:
    extract=Extract.objects.get_or_create(apk=apk,feature=feature,nb_feature=nb_feature)
    extract.save()
    return extract

def get_apk_record(apk_id: int) -> Apk:
    apk=Apk.objects.get(pk=apk_id)
    return apk

def get_apks()->list:
    return [apk for apk in Apk.objects.all()]

def get_apk_features(apk_id: int) -> list:
    apk=Apk.objects.get(pk=apk_id)[0]
    extract = Extract.objects.get(apk=apk)
    return [(feature,nb_feature) for (feature,nb_feature) in (extract.feature,extract.nb_feature)]

def get_apk_malignity(apk_name: str) -> int:
    apk=Apk.objects.get(name=apk_name)[0]
    return apk.malignity


def get_datasets_apks(datasets: list) -> list:
    return [apk for apk in Apk.objects.get(datasets=datasets)]

def is_apk_in_db(apk_name: str, apk_dataset: str) -> bool:
    datasets=Apk.objects.get(name=apk_name).datasets
    for dataset in datasets:
        if dataset.name==apk_dataset:
            return True

    return False


if __name__=='__main__':
    app_name="sample.apk"
    path_to_apk=os.path.join(APK_DIR,app_name)
    print(path_to_apk)
    #apk=add_apk(path_to_apk=path_to_apk,malignity="1")
    for apk in get_apks():
        print(apk.id)



