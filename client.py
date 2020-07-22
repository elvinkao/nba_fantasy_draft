from PyInquirer import prompt
import nba_fantasy_draft

LEAGUE_SIZES = {"6": 6, "8": 8, "10": 10, "12": 12, "14": 14}
DRAFT_ACTIONS = {"Add player to team":0, "Remove player from team":1, "Find next best player":2, "Print Team":3, "Reset players":4, "Quit":5}
CONFIRMATION = {"No":0, "Yes":1}

class Client():

  def __init__(self):
    self.__dialog()

  def __dialog():
    start_questions = [
      {
        "type": "input",
        "name": "reference_file",
        "message": "Please enter in player reference file for modelling"
      },
      {
        "type": "list",
        "name": "league_size",
        "message": "League Size",
        "choices": LEAGUE_SIZES.keys()
      } 
    ]
    draft_questions = [
      {
        "type": "list",
        "name": "action_type",
        "message": "Next step in the draft",
        "choices": DRAFT_ACTIONS.keys()
      }
    ]
    first_name_question = [
      {
        "type": "input",
        "name": "first_name",
        "message": "What is the first name of the player?",
      }
    ]

    answers = prompt(start_questions)
    file = answers["reference_file"]
    league_size = LEAGUE_SIZES[answers["league_size"]]

    team_number_question = [
      {
        "type": "input",
        "name": "team_number",
        "message": f"What team number? (1 - {league_size})"
      }
    ]
    confirmation_question = [
      {
        "type": "list",
        "name": "confirmation",
        "message": "Are you sure?",
        "choices": CONFIRMATION.keys()
      }
    ]

    my_nba_fantasy_draft = nba_fantasy_draft.NbaFantasyDraft(file)
    print('initialize league')

    answer_num = 0
    while answer_num != 5:
      draft_action_selected = prompt(draft_questions)
      answer_num = DRAFT_ACTIONS[draft_action_selected["action_type"]]

      #add player
      if answer_num == 0:

        full_name_list = []
        while not full_name_list:
          answer_first_name = prompt(first_name_question)
          first_name = answer_first_name["first_name"]
          full_name_list = my_nba_fantasy_draft.get_player_list(first_name).to_dict()

        full_name_dict = {y:x for x,y in full_name_list.items()}
        full_name_question = [
          {
            "type": "list",
            "name": "full_name",
            "message": "Choose player",
            "choices": full_name_dict.keys()
          }
        ]
        answer_full_name = prompt(full_name_question)

        answer_team_number = prompt(team_number_question)
        team_number = answer_team_number["team_number"]
        
        my_nba_fantasy_draft.add_player(answer_full_name["full_name"], answer_team_number["team_number"])


      # remove player from team
      if answer_num == 1:
        full_name_list = []
        while not full_name_list:
          answer_first_name = prompt(first_name_question)
          first_name = answer_first_name["first_name"]
          full_name_list = my_nba_fantasy_draft.get_player_list(first_name).to_dict()

        full_name_dict = {y:x for x,y in full_name_list.items()}
        full_name_question = [
          {
            "type": "list",
            "name": "full_name",
            "message": "Choose player",
            "choices": full_name_dict.keys()
          }
        ]
        answer_full_name = prompt(full_name_question)
        


      # find next best player
      if answer_num == 2:
        my_nba_fantasy_draft.run_simulations(league_size)

      # print team
      if answer_num == 3:
        answer_team_number = prompt(team_number_question)
        team_number = int(answer_team_number["team_number"])
        print(my_nba_fantasy_draft.get_team(team_number, file))
      
      # reset players
      if answer_num == 4:
        answer_confirmation = prompt(confirmation_question)
        if CONFIRMATION[answer_confirmation["confirmation"]] == 1:
          my_nba_fantasy_draft.reset_players(file)

    my_nba_fantasy_draft.save_csv(file)


  if __name__ == "__main__":
    __dialog()