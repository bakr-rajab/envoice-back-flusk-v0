import sys
import os
sys.path.append("/home/mahmoudhfahmy/Mahmoud.hfahmy_data/freelance_projects/the_accountant/src/license/")
from ..flow import LicenseFlow


class LiceseCore:

    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_license(cls, data):
        return LicenseFlow.license_handeler("create", data)

    @classmethod
    def edite_license(cls, data):
        return LicenseFlow.license_handeler("update",data, data["type_code"])

    @classmethod
    def get_license(cls, data):
        return LicenseFlow.license_handeler("select", data)

    @classmethod
    def get_all_license(cls, data):
        return LicenseFlow.license_handeler("select_all", data)

    @classmethod
    def delete_license(cls, data):
        return LicenseFlow.license_handeler("delete", data["key"], data["value"])

    @classmethod
    def check_license(cls, data):
        return LicenseFlow.license_handeler("check", data)
