import os
import random
from src.widgets.texioty.question_prompts.base_prompt import BasePrompt


class Profilizer(BasePrompt):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)

    def profilize(self, profile_type: str):
        match profile_type:
            case 'texioty':
                self.prompt_texioty_profile()
            case 'laser-tag':
                self.start_question_prompt({"lastag_name": [f"What to name the laser tagger?", "",
                                                            os.getcwd().split('/')[2]],
                                            "faction_side": ["Which side to pledge allegiance?", "",
                                                             random.choice(['lepht', 'rhite'])],
                                            "faction_color": ["Which color is the current dedication?", "",
                                                              random.choice(['red', 'green', 'blue',
                                                                             'cyan', 'magenta', 'yellow',
                                                                             'white', 'grey', 'black'])]})
            case 'fotofuncs':
                pass
            case 'tcg_lab':
                pass


    def prompt_texioty_profile(self):
        self.txo.master.change_current_mode("Questionnaire", self.helper_commands)
        self.txo.master.current_prompt = self
        self.start_question_prompt(
                {"profile_name": [f"What to name the profile?", "", os.getcwd().split('/')[2]],
                 "password": [f"What to use for password?", "", str(random.randint(1000, 9999))],
                 "color_theme": ["Which color theme to use?", "", random.choice(['bluebrrryy dark', 'bluebrrryy light',
                                                                                 'nulbrrryyy dark', 'nulbrrryyy light'])],
                 "confirming_function": ["Does this look good?", "", random.choice(['yes', 'no']), self.txo.master.create_profile]},
                clear_txo=True)
