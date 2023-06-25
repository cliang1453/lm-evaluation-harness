"""
Korean legal AI datasets, LBox OPEN
Multi-task on Legal corpus 
https://arxiv.org/pdf/2206.05224.pdf
"""
import numpy as np
from lm_eval.base import Task, MultipleChoiceTask, rf
from lm_eval.metrics import bleu, chrf, ter
from lm_eval.metrics import macro_f1_score, mean, matthews_corrcoef, f1_score, yesno
from lm_eval.utils import general_detokenize

_CITATION ="""
@article{hwang2022multi,
  title={A multi-task benchmark for korean legal language understanding and judgement prediction},
  author={Hwang, Wonseok and Lee, Dongjun and Cho, Kyoungyeon and Lee, Hanuhl and Seo, Minjoon},
  journal={arXiv preprint arXiv:2206.05224},
  year={2022}
}
"""

class LegalBinary(Task):
    """ Predict civil(민사) or criminal(형사) case"""
    VERSION = 0
    DATASET_PATH = "lbox/lbox_open"
    DATASET_NAME = "casename_classification"
    
    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return True

    def training_docs(self):
        if self._training_docs is None:
            self._training_docs = list(map(self._process_doc, self.dataset["train"]))
        return self._training_docs

    def validation_docs(self):
        return map(self._process_doc, self.dataset["valid"])

    def test_docs(self):
        return map(self._process_doc, self.dataset["test"])

    def doc_to_text(self, doc):
        return "문장: {} ".format(doc["facts"])

    def doc_to_target(self, doc):
        return " {}".format({"civil": "민사", "criminal": "형사"}[doc["casetype"]])

    def construct_requests(self, doc, ctx):
        ll_m, _ = rf.loglikelihood(ctx, " 민사")
        ll_h, _ = rf.loglikelihood(ctx, " 형사")
        return ll_m, ll_h
    
    def process_results(self, doc, results):
        ll_m, ll_h = results
        pred = ll_h > ll_m
        gold = {"civil": 0, "criminal": 1}[doc["casetype"]]
        return {
            "acc": pred == gold,
            "macro_f1": (gold, pred)
        }

    def higher_is_better(self):
        return {
            "acc": True,
            "macro_f1": True
        }

    def aggregation(self):
        return {
            "acc": mean,
            "macro_f1": macro_f1_score
        }

class LJPCivil(MultipleChoiceTask):
    VERSION = 0
    DATASET_PATH = "lbox/lbox_open"
    DATASET_NAME = "ljp_civil"
    
    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return True

    def training_docs(self):
        if self._training_docs is None:
            self._training_docs = list(map(self._process_doc, self.dataset["train"]))
        return self._training_docs

    def validation_docs(self):
        return map(self._process_doc, self.dataset["validation"])
    
    def test_docs(self):
        return map(self._process_doc, self.dataset["test"])

    def doc_to_text(self, doc):
        return doc["query"]

    def doc_to_target(self, doc):
        return " {}".format(doc['gold'])

    def proces_label(self, doc):
        return {'구상금':0, '대여금':1, '부당이득금':2, '손해배상(기)':3}[doc['gold']]

    def _process_doc(self, doc):
        out_doc = {
            "query": "{}".format(doc['facts']),
            "choices": ['구상금', '대여금', '부당이득금', '손해배상(기)'],
            "gold": doc['casename']
        }
        return out_doc

    def process_results(self, doc, results):
        pred = np.argmax(results)
        gold = self.proces_label(doc)
        return {
            "acc": pred == gold,
            "macro_f1": (gold, pred)
        }

    def higher_is_better(self):
        return {
            "acc": True,
            "macro_f1": True
        }

    def aggregation(self):
        return {
            "acc": mean,
            "macro_f1": macro_f1_score
        }
        

class LJPCivil(MultipleChoiceTask):
    VERSION = 0
    DATASET_PATH = "lbox/lbox_open"
    DATASET_NAME = "ljp_civil"
    
    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return True

    def training_docs(self):
        if self._training_docs is None:
            self._training_docs = list(map(self._process_doc, self.dataset["train"]))
        return self._training_docs

    def validation_docs(self):
        return map(self._process_doc, self.dataset["validation"])
    
    def test_docs(self):
        return map(self._process_doc, self.dataset["test"])

    def doc_to_text(self, doc):
        return doc["query"]

    def doc_to_target(self, doc):
        return " {}".format(doc['gold'])

    def proces_label(self, doc):
        return {'구상금':0, '대여금':1, '부당이득금':2, '손해배상(기)':3}[doc['gold']]

    def _process_doc(self, doc):
        out_doc = {
            "query": "{}".format(doc['facts']),
            "choices": ['구상금', '대여금', '부당이득금', '손해배상(기)'],
            "gold": doc['casename']
        }
        return out_doc

    def process_results(self, doc, results):
        pred = np.argmax(results)
        gold = self.proces_label(doc)
        return {
            "acc": pred == gold,
            "macro_f1": (gold, pred)
        }

    def higher_is_better(self):
        return {
            "acc": True,
            "macro_f1": True
        }

    def aggregation(self):
        return {
            "acc": mean,
            "macro_f1": macro_f1_score
        }
        

class LJPCriminal(MultipleChoiceTask):
    VERSION = 0
    DATASET_PATH = "lbox/lbox_open"
    DATASET_NAME = "ljp_criminal"
    
    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return True

    def training_docs(self):
        if self._training_docs is None:
            self._training_docs = list(map(self._process_doc, self.dataset["train"]))
        return self._training_docs

    def validation_docs(self):
        return map(self._process_doc, self.dataset["validation"])
    
    def test_docs(self):
        return map(self._process_doc, self.dataset["test"])

    def doc_to_text(self, doc):
        return doc["query"]

    def doc_to_target(self, doc):
        return " {}".format(doc['gold'])

    def proces_label(self, doc):
        return {'강제추행':0, '공무집행방해':1, '교통사고처리특례법위반(치상)':2, '도로교통법위반(음주운전)':3,\
                            '사기':4, '상해':5, '폭행':6}[doc['gold']]

    def _process_doc(self, doc):
        out_doc = {
            "query": "{}".format(doc['facts']),
            "choices": ['강제추행', '공무집행방해', '교통사고처리특례법위반(치상)', \
                                    '도로교통법위반(음주운전)', '사기', '상해', '폭행'],
            "gold": doc['casename']
        }
        return out_doc

    def process_results(self, doc, results):
        pred = np.argmax(results)
        gold = self.proces_label(doc)
        return {
            "acc": pred == gold,
            "macro_f1": (gold, pred)
        }

    def higher_is_better(self):
        return {
            "acc": True,
            "macro_f1": True
        }

    def aggregation(self):
        return {
            "acc": mean,
            "macro_f1": macro_f1_score
        }
        
