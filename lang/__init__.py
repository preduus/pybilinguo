import glob
import json
import os.path

path = os.path.dirname(os.path.abspath(__file__))


class Lang:
    translactions = {}

    def __init__(self, lang: str):
        self.get_lang_contract(lang)

    def get_lang_contract(self, lang: str):
        contract_file = glob.glob(f"{path}/contracts/{lang.lower()}.json")
        """ check if lang contract is not found """
        if not len(contract_file):
            raise Exception("Language not detected!")

        file = open(contract_file[0], 'r')
        get_contract_object = json.loads(file.read())

        self.translactions = get_contract_object

    def get(self, value: str):
        if value not in self.translactions:
            return value
        return self.translactions.get(value)