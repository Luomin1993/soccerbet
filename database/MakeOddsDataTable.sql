\c oddsdata;
CREATE TABLE oddsdata_ex(
        match_id text PRIMARY KEY,
        ps1      numeric,
        ps2      numeric,
        ps3      numeric,
        pf1      numeric,
        pf2      numeric,
        pf3      numeric,
        goal1    integer,
        goal2    integer,
        team1    text,
        team2    text,
        league   text,
        company  text, 
        match_time timestamp
);
