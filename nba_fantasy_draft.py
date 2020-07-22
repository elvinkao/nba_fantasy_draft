import pandas as pd
import concurrent.futures
import time
import sys

class NbaFantasyDraft(object):

  def __init__(self, filename):
    self.__player_df = pd.read_csv(filename)
    self.__filename = filename
    self.__player_df = self.__player_df.loc[:, ~self.__player_df.columns.str.contains('^Unnamed')]

    # add number of positions played
    self.__player_df['num_elig_positions'] = self.__player_df['is_g'] + self.__player_df['is_pg'] \
        + self.__player_df['is_sg'] + self.__player_df['is_f'] \
        + self.__player_df['is_sf'] + self.__player_df['is_pf'] \
        + self.__player_df['is_c'] + self.__player_df['is_util']

  def select_pg(self, player_df):
    # return player with least positions played and plays PG
    df = player_df[player_df['is_pg'] == 1]
    min_positions = df.num_elig_positions.min()
    df = df[df['num_elig_positions'] == min_positions]
    if len(df) > 0:
        return df.sample()
    else:
        return df

  def select_sg(self, player_df):
    # return player with least positions played and plays SG
    df = player_df[player_df['is_sg'] == 1]
    min_positions = df.num_elig_positions.min()
    df = df[df['num_elig_positions'] == min_positions]
    if len(df) > 0:
        return df.sample()
    else:
        return df

  def select_sf(self, player_df):
    # return player with least positions played and plays SF
    df = player_df[player_df['is_sf'] == 1]
    min_positions = df.num_elig_positions.min()
    df = df[df['num_elig_positions'] == min_positions]
    if len(df) > 0:
        return df.sample()
    else:
        return df

  def select_pf(self, player_df):
    # return player with least positions played and plays PF
    df = player_df[player_df['is_pf'] == 1]
    min_positions = df.num_elig_positions.min()
    df = df[df['num_elig_positions'] == min_positions]
    if len(df) > 0:
        return df.sample()
    else:
        return df

  def select_g(self, player_df):
    # return player with least positions played and plays G
    df = player_df[player_df['is_g'] == 1]
    min_positions = df.num_elig_positions.min()
    df = df[df['num_elig_positions'] == min_positions]
    if len(df) > 0:
        return df.sample()
    else:
        return df

  def select_f(self, player_df):
    # return player with least positions played and plays F
    df = player_df[player_df['is_f'] == 1]
    min_positions = df.num_elig_positions.min()
    df = df[df['num_elig_positions'] == min_positions]
    if len(df) > 0:
        return df.sample()
    else:
        return df

  def select_c(self, player_df):
    # return player with least positions played and plays C
    df = player_df[player_df['is_c'] == 1]
    min_positions = df.num_elig_positions.min()
    df = df[df['num_elig_positions'] == min_positions]
    if len(df) > 0:
        return df.sample()
    else:
        return df

  def select_util(self, player_df):
    # return player with least positions played and plays UTIL
    df = player_df[player_df['is_util'] == 1]
    min_positions = df.num_elig_positions.min()
    df = df[df['num_elig_positions'] == min_positions]
    if len(df) > 0:
        return df.sample()
    else:
        return df

  def get_player_list(self, first_name):
    return self.__player_df[self.__player_df['Player'].str.lower().str.startswith(first_name.lower())]['Player']

  def add_player(self, player_name, team_number):

    find_df = self.__player_df[self.__player_df['Player'].str.lower()==player_name.lower()]
    if(len(find_df == 1)):
      self.__player_df.loc[self.__player_df['Player'].str.lower() == player_name.lower(), ['rand_team']] = team_number
    else:
      print('***ERROR', player_name, 'not found')
    self.__player_df = self.__player_df

  def remove_player(self, player_name):
    find_df = self.__player_df[self.__player_df['Player'].str.lower()==player_name.lower()]
    if(len(find_df == 1)):
      self.__player_df.loc[self.__player_df['Player'].str.lower() == player_name.lower(), ['rand_team']] = 0
    else:
      print('***ERROR', player_name, 'not found')


  def reset_players(self,filename):
    self.__player_df = pd.read_csv(filename)
    self.__player_df['rand_team'] = 0
    self.__player_df.to_csv(filename)

  def get_team(self,team_number,filename):
    # print player names from team number
    self.save_csv(filename)
    self.__player_df = pd.read_csv(filename)
    return self.__player_df[self.__player_df['rand_team']==team_number]['Player']

  def save_csv(self,filename):
    self.__player_df.to_csv(filename)

  def create_teams_in_progress(self, num_teams):
    # For each team, which positions left to fill, find a random player and assign to team
    # End of player selection process, only keep drafted players
    # ----------------------
    # Get team performance compared to other teams
    # Number of categories won compared to other teams
    # Number of head to head matchups won compared to other teams
    # return summary dataframe (player, rand_team, performance metrics)
    
    draft_players = self.__player_df.copy()

    # Change order of choosing players
    # Fill more specific spots first for validation if team has filled the spot, then more general
    
    for i in range(1,num_teams + 1):
        
        # get players on team being evaluated
        curr_team_players = draft_players[draft_players['rand_team'] == i]
        
        # find a PG
        pg_returned = self.select_pg(curr_team_players)
        if(len(pg_returned) == 0):
            rand_player = draft_players[(draft_players['is_pg']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove PG from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(pg_returned)]

        # find a SG
        sg_returned = self.select_sg(curr_team_players)
        if(len(pg_returned) == 0):
            rand_player = draft_players[(draft_players['is_sg']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove SG from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(sg_returned)]

        # find a SF
        sf_returned = self.select_sf(curr_team_players)
        if(len(sg_returned) == 0):
            rand_player = draft_players[(draft_players['is_sf']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove SF from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(sf_returned)]

        # find a PF
        pf_returned = self.select_pf(curr_team_players)
        if(len(pf_returned) == 0):
            rand_player = draft_players[(draft_players['is_pf']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove PF from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(pf_returned)]

        # find a C
        c_returned = self.select_c(curr_team_players)
        if(len(c_returned) == 0):
            rand_player = draft_players[(draft_players['is_c']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove C from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(c_returned)]

        # find a C
        c_returned = self.select_c(curr_team_players)
        if(len(c_returned) == 0):
            rand_player = draft_players[(draft_players['is_c']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove C from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(c_returned)]
        
        # find a G
        g_returned = self.select_g(curr_team_players)
        if(len(g_returned) == 0):
            rand_player = draft_players[(draft_players['is_g']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove G from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(g_returned)]
        
        # find a F
        f_returned = self.select_f(curr_team_players)
        if(len(f_returned) == 0):
            rand_player = draft_players[(draft_players['is_f']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove F from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(f_returned)]

        # find a Util
        util_returned = self.select_util(curr_team_players)
        if(len(util_returned) == 0):
            rand_player = draft_players[(draft_players['is_util']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove Util from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(util_returned)]

        # find a Util
        util_returned = self.select_util(curr_team_players)
        if(len(util_returned) == 0):
            rand_player = draft_players[(draft_players['is_util']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove Util from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(util_returned)]

        # find a Util
        util_returned = self.select_util(curr_team_players)
        if(len(util_returned) == 0):
            rand_player = draft_players[(draft_players['is_util']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove Util from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(util_returned)]

        # find a Util
        util_returned = self.select_util(curr_team_players)
        if(len(util_returned) == 0):
            rand_player = draft_players[(draft_players['is_util']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove Util from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(util_returned)]

        # find a Util
        util_returned = self.select_util(curr_team_players)
        if(len(util_returned) == 0):
            rand_player = draft_players[(draft_players['is_util']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove Util from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(util_returned)]

        # find a Util
        util_returned = self.select_util(curr_team_players)
        if(len(util_returned) == 0):
            rand_player = draft_players[(draft_players['is_util']==1) & (draft_players['rand_team']==0)].sample()
            rand_player = rand_player.Player.to_string(index=False).strip()
            draft_players.loc[draft_players['Player'] == rand_player, ['rand_team']] = i
        else:
            # remove Util from curr_team_players
            curr_team_players = curr_team_players[~curr_team_players.isin(util_returned)]

    # select only players drafted
    draft_players = draft_players[draft_players['rand_team']>0]
    
    # get draft team results
    draft_teams = draft_players.groupby(['rand_team'])[['FGM','FGA','FTM','FTA','3PTM','PTS','REB','AST','ST','BLK','TO']].apply(sum).reset_index()

    draft_teams['FGP'] = draft_teams['FGM'] / draft_teams['FGA']
    draft_teams['FTP'] = draft_teams['FTM'] / draft_teams['FTA']
    
    # get scores
    cat_win = []
    cat_loss = []
    matchup_win = []
    matchup_loss = []
    for curr_team in draft_teams['rand_team']:
        hh_cat_win = 0
        hh_cat_loss = 0
        hh_match_win = 0
        hh_match_loss = 0

        for matchup_team in draft_teams['rand_team']:
            hhwins = 0
            hhlosses = 0
            # loop only for other teams
            if curr_team != matchup_team:
                # FGP
                if (float(draft_teams[draft_teams['rand_team']==curr_team]['FGP']) > float(draft_teams[draft_teams['rand_team']==matchup_team]['FGP'])):
                    hhwins += 1
                else:
                    hhlosses += 1
                # FTP
                if (float(draft_teams[draft_teams['rand_team']==curr_team]['FTP']) > float(draft_teams[draft_teams['rand_team']==matchup_team]['FTP'])):
                    hhwins += 1
                else:
                    hhlosses += 1
                # PTS
                if (float(draft_teams[draft_teams['rand_team']==curr_team]['PTS']) > float(draft_teams[draft_teams['rand_team']==matchup_team]['PTS'])):
                    hhwins += 1
                else:
                    hhlosses += 1
                # REBS
                if (float(draft_teams[draft_teams['rand_team']==curr_team]['REB']) > float(draft_teams[draft_teams['rand_team']==matchup_team]['REB'])):
                    hhwins += 1
                else:
                    hhlosses += 1
                # AST
                if (float(draft_teams[draft_teams['rand_team']==curr_team]['AST']) > float(draft_teams[draft_teams['rand_team']==matchup_team]['AST'])):
                    hhwins += 1
                else:
                    hhlosses += 1
                # ST
                if (float(draft_teams[draft_teams['rand_team']==curr_team]['ST']) > float(draft_teams[draft_teams['rand_team']==matchup_team]['ST'])):
                    hhwins += 1
                else:
                    hhlosses += 1
                # BLK
                if (float(draft_teams[draft_teams['rand_team']==curr_team]['BLK']) > float(draft_teams[draft_teams['rand_team']==matchup_team]['BLK'])):
                    hhwins += 1
                else:
                    hhlosses += 1
                # BLK
                if (float(draft_teams[draft_teams['rand_team']==curr_team]['TO']) < float(draft_teams[draft_teams['rand_team']==matchup_team]['TO'])):
                    hhwins += 1
                else:
                    hhlosses += 1

                # Add heads up result
                if hhwins > hhlosses:
                    hh_match_win += 1
                else:
                    hh_match_loss += 1

            # Add heads up category totals
            hh_cat_win = hh_cat_win + hh_match_win
            hh_cat_loss = hh_cat_loss + hh_match_loss  

        # when current team match over append scores
        cat_win.append(hh_cat_win)
        cat_loss.append(hh_cat_loss)
        matchup_win.append(hh_match_win)
        matchup_loss.append(hh_match_loss)

    draft_teams['cat_win'] = cat_win
    draft_teams['cat_loss'] = cat_loss
    draft_teams['matchup_win'] = matchup_win
    draft_teams['matchup_loss'] = matchup_loss
    
    rand_summary = draft_players[['Player','rand_team']].merge(draft_teams[['rand_team','cat_win','cat_loss','matchup_win','matchup_loss']], on='rand_team')

    return rand_summary

  def run_simulations(self, num_teams):
    iteration_size = 50
    starttime = time.perf_counter()

    self.save_csv(self.__filename)
    self.__player_df = pd.read_csv(self.__filename)

    # first create_team
    draft_players = self.create_teams_in_progress(num_teams)
    num_simulations = 1

    elapsed_time = round(time.perf_counter()-starttime,2)
    while elapsed_time < 25:

      with concurrent.futures.ProcessPoolExecutor() as executor:

        # list comprehension
        results = [executor.submit(self.create_teams_in_progress, num_teams) for _ in range(iteration_size)]

        for f in concurrent.futures.as_completed(results):
          draft_players = draft_players.append(f.result(), ignore_index=True)    

        num_simulations = num_simulations + iteration_size
        elapsed_time = round(time.perf_counter()-starttime,2)

    # team 1 will be our team, so we want to see the player that benefits our team the most
    sim_summary = draft_players[draft_players['rand_team']==1].groupby(['Player'])[['cat_win','cat_loss','matchup_win','matchup_loss']].apply(sum).reset_index()
    sim_summary['cat_perc'] = sim_summary['cat_win'] / (sim_summary['cat_win'] + sim_summary['cat_loss'])
    sim_summary['matchup_perc'] = sim_summary['matchup_win'] / (sim_summary['matchup_win'] + sim_summary['matchup_loss'])
    print(sim_summary.sort_values(by=['cat_perc'], ascending=False).head(20))

    endtime = time.perf_counter()
    print(f'Finished in {round(endtime-starttime,2)} seconds(s) with {num_simulations} simulations')