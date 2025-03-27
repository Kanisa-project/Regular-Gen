import datetime
import json
import os
import random
import tkinter as tk
from dataclasses import dataclass
from os.path import exists
from typing import Dict, Any
import subprocess

import gaimPlay
import helper_widget
# import ppppp
import settings as s
import texoty
import texity
import logging
import sys

import msg_client


@dataclass
class CommandRegistry:
    """
    A registry for custom commands for use within Texioty.
    """
    commands: Dict[str, texity.Command]

    def add_command(self, name: str, handler: Any, msg: str, p_args: Any, helper_type: Any,
                    t_color: str, b_color: str) -> None:
        """
        Add a new command that Texity will recognize and Texoty can display.
        :param name: Name of the command, also the command itself.
        :param handler: Defined function for execution.
        :param msg: A message of helping for the help display.
        :param p_args: Possible arguments for Texity.
        :param helper_type: Exact arguments for Texity to use.
        :param t_color: Text color for help display.
        :param b_color: Background color for help display.
        :return:
        """
        self.commands[name] = texity.Command(name=name,
                                             handler=handler,
                                             help_message=msg,
                                             possible_args=p_args,
                                             helper_type=helper_type,
                                             text_color=t_color,
                                             bg_color=b_color)

    def execute_command(self, name: str, args: tuple) -> None:
        """
        Executes the command being used in Texity.
        :param name: Name of the command being executed.
        :param args: Arguments to be used in the command execution.
        :return:
        """
        command = self.commands.get(name)
        print(f"{name} executing fine")
        if command:
            print(command.handler)
            command.handler(args)
        else:
            print(f"Command '{name}' not found.")


class TEXIOTY(tk.LabelFrame):
    def __init__(self, width, height, master=None):
        """
        Textual input from Texity, such as commands and other necessary inputs. Textual output from Texoty, such as help display
        and confirmation prompting.

        :param width: Width of the Texioty Widget frame.
        :param height: Height of the Texioty Widget frame.
        :param master: Parent widget
        """
        super(TEXIOTY, self).__init__(master)
        self.current_mode = "Texioty"
        self.in_play_gaim_mode = False
        self.configure(text="Texioty:  ")

        # INITIATE DIARY VARIABLES
        self.diary_line_length = 75
        self.diarySentenceList = []
        self.in_diary_mode = False

        self.question_prompt_dict = {}
        self.question_keys = []
        self.current_question_index = 0
        self.registry = CommandRegistry({})
        self.helper_dict = {"TXTY": [self]}
        self.available_profiles = s.available_profiles
        self.active_profile = self.available_profiles["guest"]
        self.gaim_player: gaimPlay.gaimPlayer = None

        self.texoty = texoty.TEXOTY(int(width) + 16, int(height), master=self)
        self.texoty.grid(column=0, row=0)
        self.texity = texity.TEXITY(width=int(width // 6), master=self)
        self.texity.grid(column=0, row=1)
        self.texo_w = self.texoty.texoty_w
        self.in_questionnaire_mode = False
        self.response_dict = {}

        self.texity.focus_set()
        self.texity.bind('<KP_Enter>', lambda e: self.process_command())
        self.texity.bind('<Return>', lambda e: self.process_command())

        # Set up basic commands for Texioty to know automatically.
        self.texioty_commands = {
            "help": [self.display_help_message, "Displays a message of hope and help.",
                     {"TXTY": "Texioty, the main attraction.",
                      "CLDR": "Calendar for dates and stuff.",
                      "IDUT": "IDUTC and the beginning.",
                      "KNVO": "Kinvow with visual display.",
                      "ARTY": "Artyles from the aRtay.",
                      "GAIM": "Gaim playing for the player.",
                      "MUJC": "Mujic playing for a user."}, "TXTY", s.rgb_to_hex(s.INDIAN_RED), s.rgb_to_hex(s.BLACK)],
            "exit": [self.close_program, "Exits the program.",
                     {}, "TXTY", s.rgb_to_hex(s.INDIAN_RED), s.rgb_to_hex(s.BLACK)],
            "commands": [self.display_available_commands, "Displays all available commands.",
                         {}, "TXTY", s.rgb_to_hex(s.INDIAN_RED), s.rgb_to_hex(s.BLACK)],
            "login": [self.log_profile_in, "This logs the user into a profile: ",
                      {'guest': "Basic account with a few permissions."}, "TXTY", s.rgb_to_hex(s.LIGHT_GREEN),
                      s.rgb_to_hex(s.BLACK)],
            "logout": [self.log_profile_out, "This logs the user out of a profile.",
                       {}, "TXTY", s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            "dear_sys,": [self.start_diary_mode, "Creates a new .diary/ entry.",
                          {}, "TXTY", s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            "/until_next_time": [self.stop_diary_mode, "Ends and saves the .diary/ entry.",
                                 {}, "TXTY", s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            "echo": [self.echooo, "Echo some errors.",
                     {}, "TXTY", s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            "quit": [self.quit_gaim, "Quit any gaim you might be playing.",
                     {}, "TXTY", s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            "tex8": [self.texoty.create_from_masterpiece, "Create a textual vision.",
                     {}, "TXTY", s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],
            "welcome": [self.welcome_message, "Show welcome message.",
                        {}, "TXTY", s.rgb_to_hex(s.LIGHT_GREEN), s.rgb_to_hex(s.BLACK)],

        }

        # Add the basic commands for Texioty.
        self.add_command_dict(self.texioty_commands)
        # self.registry.commands["help"].handler([])
        self.welcome_message([])

    def add_command_dict(self, command_dict: dict):
        """
        Add another dictionary of commands to the registry for Texioty to use.
        :param command_dict: Dictionary of commands to add to registry.
        :return:
        """
        for command in command_dict:
            self.registry.add_command(name=command,
                                      handler=command_dict[command][0],
                                      msg=command_dict[command][1],
                                      p_args=command_dict[command][2],
                                      helper_type=command_dict[command][3],
                                      t_color=command_dict[command][4],
                                      b_color=command_dict[command][5])
            self.texoty.tag_config(f'{command}',
                                   background=f'{command_dict[command][5]}', foreground=f'{command_dict[command][4]}')

    def close_program(self, args):
        """
        Literally just close the whole application.
        :param args:
        :return:
        """
        self.master.destroy()

    def add_helper_widget(self, helper_type: str, helper: helper_widget.helpingWidget):
        """
        Add a helper widget and all of its commands to texioty while supplying access to texoty.
        :param helper:
        :param helper_type: Type of helper (e.g. Database/API/Other)
        :return:
        """
        helper.txo = self.texoty
        if len(helper.texioty_commands) > 0:
            self.add_command_dict(helper.texioty_commands)
        self.helper_dict[helper_type] = [helper]
        # print(f'{helper_type} added.')

    def priont_helper_widgets(self, args):
        """
        Displays any helper widgets that have been added to texioty.
        :param args:
        :return:
        """
        print(self.helper_dict)
        for key, value in self.helper_dict.items():
            self.texoty.priont_list(list(value[0].texioty_commands.keys()), parent_key=key)

    def display_help_message(self, args):
        """
        Print the available commands for use with a header added to the top.
        :param args:
        :return:
        """

        self.texoty.clear_add_header("Helping")
        if "TXTY" in args:
            self.display_help_txty()
        elif "CLDR" in args:
            self.display_help_cldr()
        elif "IDUT" in args:
            self.display_help_idut()
        elif "KNVO" in args:
            self.display_help_knvo()
        elif "ARTY" in args:
            self.display_help_arty()
        elif "GAIM" in args:
            self.display_help_gaim()
        elif "MUJC" in args:
            self.display_help_mujc()
        else:
            self.texoty.priont_string("⦓⦙ Seems like you might need some help, good luck!")
            self.texoty.priont_string("⦓⦙ These are the current helpers and their commands available to Texioty: \n")
            self.priont_helper_widgets(args)
            self.texoty.priont_string("\n⦓⦙ You can use the 4 letter ID to get more info about that helper.")
            # self.texoty.priont_string("⦓⦙ ")
            self.texoty.priont_string("")
            self.texoty.priont_string("⦓⦙ Try typing 'help TXTY' or 'help IDUT' or 'help KNVO'. \n")

    def display_available_commands(self, args):
        """Prints out all the commands that are available."""
        self.texoty.clear_add_header("Commands")
        # command_index = 0
        print(self.registry.commands)
        for helper in list(self.helper_dict.keys()):
            for command in self.registry.commands:
                if self.registry.commands[command].helper_type == helper:
                    self.texoty.priont_command(self.registry.commands[command])
                    # command_index += 1
            self.texoty.priont_break_line(right_text=helper)

    def process_command(self, event=None):
        """
        Process the command before executing it. Decide which helpers to use or if just a regular command.
        :return:
        """
        if self.in_questionnaire_mode:
            # self.texoty.priont_string(f"⦓⦙ Processing as questionnaire")
            parsed_input = self.texity.parse_question_response()
            self.store_response(parsed_input.split("›")[-1])
        elif self.in_play_gaim_mode and self.texity.parse_gaim_play() != "quit":
            # self.texoty.priont_string(f"⦓⦙ Processing as Gaim")
            parsed_input = self.texity.parse_gaim_play()
            self.execute_gaim_play(parsed_input)
        elif self.in_diary_mode and self.texity.parse_diary_line() != "/until_next_time":
            # self.texoty.priont_string(f"⦓⦙ Processing as diary")
            parsed_input = self.texity.parse_diary_line()
            self.add_diary_line(parsed_input)
        else:
            # self.texoty.priont_string(f"⦓⦙ Processing as Texioty")
            parsed_input = self.texity.parse_input_command()
            command = parsed_input[0]
            arguments = parsed_input[1:]
            self.execute_command(command, arguments)
        self.set_texity()

    def set_texity(self):
        if self.in_play_gaim_mode and self.gaim_player.loaded_gaim == "Hangman":
            self.texity.command_string_var.set("guess ")
        elif self.in_play_gaim_mode and self.gaim_player.loaded_gaim == "Blackjack":
            self.texity.command_string_var.set("blaja ")
        elif self.in_questionnaire_mode:
            pass
        else:
            self.texity.command_string_var.set("")
        # self.texoty.set_header(self.gaim_player.loaded_gaim)

    def execute_command(self, command, arguments):
        """
        Execute the processed command, then add it to the list of processed commands.
        :param command: The command to be using.
        :param arguments: Arguments for the command to use.
        :return:
        """
        # self.clear_texoty()
        if command in self.registry.commands:
            # print(command, "is in registry")
            try:
                self.registry.execute_command(command, arguments)
            except PermissionError as e:
                self.texoty.priont_string("Sorry dude, you ain't got that kinda permission.")
                self.texoty.priont_string(str(e))
            except KeyError as e:
                self.texoty.priont_string(f"Missing the {e} key or something.")
            except IndexError as e:
                self.texoty.priont_string("Missing at least one index.")
                self.texoty.priont_string(str(e))

            if "start" in command:
                self.in_play_gaim_mode = self.gaim_player.inGaim
            self.texity.used_command_list.append(self.texity.command_string_var.get())
        else:
            self.texoty.priont_string(f"⦓⦙ Uhh, I don't recognize '{command}'")
        # ONLY PRINT A RANDOM LOADING PHRASE IF NOT IN THESE MODES OR THIS COMMAND.
        if self.in_play_gaim_mode or self.in_questionnaire_mode or command == "tex8":
            pass
        else:
            self.texoty.priont_string("⦓⦙ " + s.random_loading_phrase())

    def start_question_prompt(self, question_dict: dict, clear_txo=True):
        """
        Checks if Textioty is already in a questionnaire prompt. If not, sets up the first question and starts the
        prompt to receive answers. Anything typed and sent in Texity will be saved as answers for the prompt questions.
        @param clear_txo:
        @param question_dict: Dictionary of questions, consider making a dataclass.
        :return:
        """
        if clear_txo:
            self.texoty.clear_add_header("Questionnaire")
        if not self.in_questionnaire_mode:
            self.question_prompt_dict = question_dict
            self.question_keys = list(question_dict.keys())
            self.in_questionnaire_mode = True
            self.current_question_index = 0
            self.display_question()
        else:
            self.texoty.priont_string("Already in a questionnaire prompt.")
            self.display_question()

    # def ask_question(self, question: str, default_ans="NoDefault") -> str:
    #     self.texity.command_string_var.set(question + f"   [{default_ans}]")
    #     return ""

    def display_question(self):
        """Displays a question from the loaded questionnaire prompt dictionary."""
        if self.current_question_index < len(self.question_keys):
            question_key = self.question_keys[self.current_question_index]
            question = self.question_prompt_dict[question_key][0]
            self.texity.command_string_var.set(question + f" [{self.question_prompt_dict[question_key][2]}]  ›")
            self.texity.icursor(tk.END)
        else:
            self.end_question_prompt(self.question_prompt_dict)

    def end_question_prompt(self, question_dict: dict) -> dict:
        self.texoty.priont_string("Prompt ended, here are the results: ")
        self.texoty.priont_dict(question_dict)
        self.in_questionnaire_mode = False
        self.response_dict = question_dict
        self.response_dict['font_digit'][3](int(self.response_dict['font_digit'][1]))
        return question_dict

    def log_profile_in(self, args):
        """Check args[0] for a username and args[1] for a password. Logs in a profile if a match."""
        try:
            if args[0] in self.available_profiles:
                try:
                    if args[1] == self.available_profiles[args[0]].password:
                        self.texoty.priont_string(f"⦓⦙ Welcome, {args[0]}!")
                        self.active_profile = self.available_profiles[args[0]]
                        self.texoty.set_header_theme(self.active_profile.color_theme[0],
                                                     self.active_profile.color_theme[1],
                                                     16,
                                                     self.active_profile.color_theme[2])
                    else:
                        self.texoty.priont_string(f"⦓⦙ Wrong password, buster.")
                except IndexError:
                    self.texoty.priont_string(f"⦓⦙ Don't forget to type a password.")
            else:
                self.texoty.priont_string(f"⦓⦙ I don't recognize '{args[0]}' as profile username.")
        except IndexError:
            self.texoty.priont_string("⦓⦙ What username to login to?")

    def log_profile_out(self, args):
        if self.active_profile:
            self.texoty.priont_string(f"Logging {self.active_profile.username} out. Goodbye!")
            self.active_profile = self.available_profiles["guest"]
            self.texoty.set_header_theme(self.active_profile.color_theme[0],
                                         self.active_profile.color_theme[1],
                                         16,
                                         self.active_profile.color_theme[2])
        else:
            self.texoty.priont_string("You have to log in before you can log out.")

    def start_diary_mode(self, args) -> datetime:
        """Start a diary entry."""
        start_now = datetime.datetime.now()
        self.in_diary_mode = True
        self.texoty.priont_string(f"-Entering diary mode-   {start_now}")
        opening_line = timestamp_line_entry(start_now, 'dear_sys,', lead_line='ts',
                                            follow_line=' ' * (self.diary_line_length - len('dear_sys,')))
        self.diarySentenceList = [opening_line]
        return start_now

    def add_diary_line(self, new_line):
        self.texoty.priont_string(f'  [+{"".join(random.sample(new_line, len(new_line)))}')
        self.diarySentenceList.append(timestamp_line_entry(datetime.datetime.now(), new_line, lead_line='  ',
                                                           follow_line='_' * (self.diary_line_length - len(
                                                               new_line) - 2)))

    def stop_diary_mode(self, args) -> datetime:
        """Stop a diary entry."""
        end_now = datetime.datetime.now()
        self.in_diary_mode = False
        self.texoty.priont_string(f"-Exiting diary mode-   {end_now}")
        ending_line = timestamp_line_entry(end_now, '/until_next_time', lead_line='ts',
                                           follow_line=' ' * (self.diary_line_length - len('/until_next_time')))
        self.diarySentenceList.append(ending_line)
        create_date_entry(end_now, self.diarySentenceList)
        return end_now

    def store_response(self, answer):
        """ Store the response in the questionnaire dictionary and advance to the next question."""
        question_key = self.question_keys[self.current_question_index]
        if answer == "":
            answer = self.question_prompt_dict[question_key][2]
            self.texoty.priont_string("|>  " + str(answer) + " (Default)")
        else:
            self.texoty.priont_string("|>  " + str(answer))
        self.question_prompt_dict[question_key][1] = answer

        self.current_question_index += 1
        self.display_question()
        # if question_key == "confirmation":
        #     if answer.startswith('y'):
        #         pass
        #     else:
        #         self.texoty.priont_string("Canceling, please restart the prompt.")

    def get_responses(self):
        self.texoty.priont_dict(self.question_prompt_dict)

    # def handle_errors(self, error_message: str, severity="INFO"):
    #     text_color = s.BLACK
    #     if severity == "ERROR":
    #         text_color = s.ORANGE_RED
    #     self.texoty.priont_string(f"⦓⦙ {severity}: {error_message}")

    def execute_gaim_play(self, parsed_input):
        gaim_command = parsed_input.split()[0]
        gaim_args = parsed_input.split()[1]
        # print(gaim_command, gaim_args)
        if gaim_command == "guess":
            self.texoty.priont_string(f"execute gaimplay: {parsed_input}")
            self.registry.execute_command(gaim_command, gaim_args)
        if "hit" in gaim_args or "stay" in gaim_args:
            self.texoty.priont_string(f"execute gaimplay: {parsed_input}")
            self.registry.execute_command(gaim_command, gaim_args)

    def quit_gaim(self, args):
        self.texoty.priont_string("Quitting, you quitter.")
        self.in_play_gaim_mode = False

    # def prepare_new_recipe(self, args):
    #     prep_new_recipe_dict = {}
    #     if "new_recipe_name" in list(self.question_prompt_dict.keys()):
    #         self.elaborate_new_recipe(self.question_prompt_dict)
    #     else:
    #         prep_new_recipe_dict = {"new_recipe_name": ["What is the name of the recipe?", "", "NewReci"],
    #                                 "num_ingreds": ["How many individual ingredients? ", "", "3"],
    #                                 "num_directs": ['How many different directions?', '', '3']}
    #     self.start_question_prompt(prep_new_recipe_dict)
    #
    # def elaborate_new_recipe(self, prepped_question_dict: dict):
    #     new_recipe_question_dict = {}
    #     for i in range(int(prepped_question_dict['num_ingreds'][1])):
    #         new_recipe_question_dict[f'ingred_{i}'] = [f'ingredient {i}: ', "", "Nodefault"]
    #     for i in range(int(prepped_question_dict['num_directs'][1])):
    #         new_recipe_question_dict[f'direct_{i}'] = [f'direction {i}: ', "", "Nodefault"]
    #     self.texoty.priont_string("List each amount and ingredient separately:   (7 potatoes)")
    #     self.start_question_prompt(new_recipe_question_dict)

    def welcome_message(self, welcoming_msgs: list):
        self.texoty.clear_add_header("Welcome!")
        today_date = datetime.datetime.date(datetime.datetime.now())
        today_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][
            datetime.datetime.weekday(today_date)]
        self.texoty.priont_string(
            f"⦓⦙ Welcome to kanisaGen! The date is {today_date} on a {today_day}.")
        for msg in welcoming_msgs:
            self.texoty.priont_string("⦓⦙ " + msg)
        self.texoty.priont_string("\n")

        cmnds = [random.choice(["help", "commands"]),
                 random.choice(["kre8dict", "dear_sys,"]),
                 random.choice(["exit"])]
        self.texoty.priont_list(cmnds, parent_key="Here are a few commands you could try:")
        sequence = ["glyph add 2", "glyth add 4", "kin8"]
        self.texoty.priont_string("")
        self.texoty.priont_list(sequence, parent_key="Or try this sequence of commands:", numbered=True)
        self.texoty.priont_string("⦓⦙ Type 'glyph add 2' and press enter, then 'glyth add 4' and press enter.")
        self.texoty.priont_string("⦓⦙ Finally type 'kin8' and press enter, the result should show on the right.")

    def display_help_txty(self):
        # self.texoty.priont_list(list(self.helper_dict['TXTY'][0].texioty_commands.keys()), parent_key="TXTY")
        self.texoty.priont_string("""help╕ ◄╡ This is the command name, what you will type in Texity.
    ╞► Displays a message of hope and help. ◄╡ Description of command.
    ├TXTY » Texioty, the ma...  ◄╡  These are the different
    ├CLDR » Calendar for da...  ◄╡  arguments you can use after the
    ├IDUT » IDUTC and the b...  ◄╡  command name for different effects.
    ├KNVO » Kinvow with vis...  ◄╡  
    ├ARTY » Artyles from th...  ◄╡  The argument is separated from its
    ├GAIM » Gaim playing fo...  ◄╡  description by a '»', only type what
    └MUJC » Mujic playing f...  ◄╡  is before the '»' excluding the '»'
        """)
        self.texoty.priont_string("⦓⦙ TXTY is a powerhouse of commanding and conquering. With the\n"
                                  "   ability to process and execute commands, you can make all sorts\n"
                                  "   of art and mostly just art. Art is a really big category though. \n\n")

        self.texoty.priont_string("⦓⦙ All successfully entered commands will be stored into a history. \n"
                                  "   Pressing the up and down arrow keys will cycle through previous commands. \n\n")

    def display_help_cldr(self):
        self.texoty.priont_string(
            '''
            CLDR is able to keep track of any events while also able to set timers and triggers,
            for different needs.
            '''
        )

    def display_help_idut(self):
        self.texoty.priont_string("⦓⦙ This is the starting point of a kre8dict. The kre8dict\n"
                                  "   is the starting point of the masterpiece, coincidence? \n"
                                  "   I THINK NOT!")

    def display_help_knvo(self):
        self.texoty.priont_string("⦓⦙ KNVO is the simplest of displays. Displaying images fit to \n"
                                  "   it's canvas, it shows that kanisa might be thinking.\n"
                                  "   I THINK NOT!")

    def display_help_arty(self):
        self.texoty.priont_string("""kin8╕ ◄╡ This is the command name, what you will type in Texity.
    ╞► Create a masterpiece on Kinvow. ◄╡ Description of command.
    ├glyth » Gather glyth opti...  ◄╡  
    ├glyph » Gather glyph opti...  ◄╡  These are the different
    ├wordie » Gather wordie op...  ◄╡  arguments you can use after the
    ├spirite » Gather spirite ...  ◄╡  command name for different effects.
    ├recipe » Gather recipe op...  ◄╡  
    ├foto » Gather foto option...  ◄╡  The argument is separated from its
    ├mujic » Gather mujic opti...  ◄╡  description by a '»', only type what
    ├gaim » Gather gaim option...  ◄╡  is before the '»' excluding the '»'
    └meem » Gather meem option...  ◄╡
    """)
        self.texoty.priont_string("⦓⦙ ARTY contains the means for creating a Masterpiece file. \n"
                                  "   It has plenty of options for many different outcomes, try a sample.\n"
                                  "   Click the 'Random' or 'All' button, then type 'kin8 glyth'.")

    def display_help_gaim(self):
        self.texoty.priont_string("⦓⦙ GAIM keeps track of different gaim playing necessities.\n"
                                  "   This is where you can see points and different important information.\n"
                                  "   ")

    def display_help_mujc(self):
        self.texoty.priont_string("⦓⦙ MUJC is able to pull info from the masterpiece file to make sounds. \n"
                                  "   Not much is developed on it yet.\n"
                                  "   ")

    def echooo(self, args):
        client = msg_client.MsgClient(txty=self, host='35.149.156.127', port=42069)
        # pass


def create_date_entry(entry_time: datetime, entry_list: list):
    """
    Create a date entry for today.
    :param entry_time: Exact time the entry was created.
    :param entry_list: List of entry lines.
    :return:
    """
    entry_date_name = f'{entry_time.year}_{entry_time.month}_{entry_time.day}'
    # entry_list.pop(len(entry_list) - 3)
    if exists(f'.diary/{entry_date_name}.txt'):
        with open(f'.diary/{entry_date_name}.txt', 'a') as f:
            for ent in entry_list:
                f.write(ent + "\n")
            f.write("\n")
    else:
        with open(f'.diary/{entry_date_name}.txt', 'w') as f:
            for ent in entry_list:
                f.write(ent + "\n")
            f.write("\n")


def timestamp_line_entry(entry_time: datetime, entry_line: str, lead_line=" ", follow_line=" ") -> str:
    """
    Take an entry line and add a time stamp with a lead and follow string.

    :param entry_time: Hour:Minute:Seconds
    :param entry_line: Text to be timestamped
    :param lead_line: Text to the left of the entry_line
    :param follow_line: Text to the right of the entry_line
    :return:
    """
    time_stamp = f'{entry_time.hour:02d}:{entry_time.minute:02d}:{entry_time.second:02d}'
    ret_str = lead_line + entry_line + follow_line
    if lead_line == "ts":
        ret_str = '  ' + entry_line + follow_line + time_stamp
        if entry_line == "dear_sys," or entry_line == "/until_next_time":
            ret_str = entry_line + follow_line + time_stamp + f':{entry_time.microsecond:2d}'

    return ret_str
