from typing import Callable, Optional

import src.widgets.texioty.texity as texity

import src.widgets.texioty.texoty as texoty
from src.widgets.texioty.helpers.tex_helper import TexiotyHelper
from src.settings import themery as t
from src.services import utils as u
from src.widgets.texioty.question_prompts.foto_worx import FotoWorxHop
from src.widgets.texioty.question_prompts.profilizer import Profilizer

LAB_OPTIONS = ['Depictinator{}',
               'Card%Puzzler()',
               'TC-Blender 690',
               'Card-0wn1oad3r',
               'RanDexter-2110']

FUNCFOTO_OPTIONS = ['Flatop_XT 2200',
                    'S/p/licer R0T8',
                    'Deep-friar 420',
                    'Pixtruderer V3']

PROFILIZER_OPTIONS = ['texioty',
                      'laser-tag',
                      'fotofuncs',
                      'tcg_lab']

class PromptRegistry(TexiotyHelper):
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY):
        super().__init__(txo, txi)
        self.txo = txo
        self.txi = txi
        self.helper_tag = "PRUN"
        self.in_questionnaire_mode = False
        self.current_prompt = "N/A"
        self.foto_worx = FotoWorxHop(txo, txi)
        self.profilemake = Profilizer(txo, txi)
        self.helper_commands = {
            "foto_worx": [self.worxhop_prompt, "Work in the foto hop.",
                          {}, "PRUN", u.rgb_to_hex(t.KHAKI), u.rgb_to_hex(t.BLACK)],
            "profile_make": [self.profiler_prompt, "Make some type of profile.",
                             {}, "PRUN", u.rgb_to_hex(t.KHAKI), u.rgb_to_hex(t.BLACK)]}


    def worxhop_prompt(self):
        self.foto_worx.decide_decision("What station to work in", FUNCFOTO_OPTIONS, 'worxhop_fotoes')
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.foto_worx.worxhop

    def profiler_prompt(self):
        self.profilemake.decide_decision("What kind of profile to make", PROFILIZER_OPTIONS, "profile_type")
        if self.txo.master.deciding_function is None or isinstance(self.txo.master.deciding_function, Callable):
            self.txo.master.deciding_function = self.profilemake.profilize

    def display_help_message(self, helper_tag: Optional[str] = None):
        super().display_help_message(helper_tag)
        self.txo.priont_string("The prompt runner is for prompting the user with questions.")
        self.txo.priont_string("This helper will go through a series of questions, retraining information.")
        self.txo.priont_string("At the end of the prompt, things happen based on the results.")