import pandas as pd


def calculate_hs_percentage(parser):
    kills_df = parser.kills

    # filtering kill df for only hs property
    kills_df = kills_df[["attacker_name", "headshot", "round"]]

    # count total kills by a player per round
    total_kills = kills_df.groupby(["attacker_name", "round"]).size().reset_index(name="total_kills")

    # count total headshots by a player per round
    total_headshots_round = kills_df[kills_df["headshot"] == True].groupby(
        ["attacker_name", "round"]).size().reset_index(
        name="total_headshots_round")

    # merge two df
    merged_df = pd.merge(total_kills, total_headshots_round, on=["attacker_name", "round"], how="left")
    merged_df["total_headshots_round"] = merged_df["total_headshots_round"].fillna(0).astype(int)

    # calculate percentage of headshots per round
    merged_df["hs_percentage_round"] = (merged_df["total_headshots_round"] / merged_df["total_kills"]) * 100
    merged_df["hs_percentage_round"] = merged_df["hs_percentage_round"].fillna(0).astype(int)

    # calculate total kills and total headshots across all rounds for each attacker_name
    total_kills_all = kills_df.groupby("attacker_name").size().reset_index(name="total_kills_all")
    total_headshots_all = kills_df[kills_df["headshot"]].groupby("attacker_name").size().reset_index(
        name="total_headshots_all")

    # merge total_kills_all and total_headshots_all df
    merged_total_df = pd.merge(total_kills_all, total_headshots_all, on="attacker_name", how="left")
    merged_total_df["total_headshots_all"] = merged_total_df["total_headshots_all"].fillna(0).astype(int)

    # calculate percentage of hs in all rounds
    merged_total_df["hs_percentage_total"] = (merged_total_df["total_headshots_all"] / merged_total_df[
        "total_kills_all"]) * 100
    merged_total_df["hs_percentage_total"] = merged_total_df["hs_percentage_total"].fillna(0).astype(int)

    # merge round and total df
    final_df = pd.merge(merged_df, merged_total_df, on="attacker_name", how="left")

    # sort df
    hs_df = final_df.sort_values(by=["attacker_name", "round"]).reset_index(drop=True)

    # returning
    return hs_df
