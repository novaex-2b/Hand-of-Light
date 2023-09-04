import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class EnvConfig(
    BaseSettings,
    env_file=(".env.server", ".env"),
    env_file_encoding = "utf-8",
    env_nested_delimiter = "__",
    extra="ignore",
):
    """Our default configuration for models that should load from .env files."""

class _Roles(EnvConfig, env_prefix='roles_'):

    # self-assignable roles (via welcome page)
    kichains: int = 1080310681502494780
    buoys: int = 1080310834716229682
    skyelights: int = 1080311236798980129
    eienjoyers: int = 1092646564834582528
    announcements: int = 1081190528021954570
    house_updates: int = 1081190620875460668
    house_activities: int = 1081190801830330398

    # special roles
    server_booster: int = 1084154921210892419

    # color roles
    kichain_pink: int = 1086133654448767056
    buoys_grey: int = 1086133806051889172
    skyelights_yellow: int = 1086133907373686784

    # Kiki membership roles
    kiki_members: int = 1085889432042876998
    kiki_t1: int = 1085889432042876999
    kiki_t2: int = 1085889432042877000
    kiki_t3: int = 1085889432042877001
    kiki_t4: int = 1085889432042877002
    kiki_t5: int = 1085889432042877003
    kiki_t6: int = 1085889432042877004

    # Kilia membership roles
    kilia_members: int = 1085737759215456426
    kilia_t1: int = 1085737759215456427
    kilia_t2: int = 1085737759215456428
    kilia_t3: int = 1085737759215456429
    kilia_t4: int = 1085737759215456430
    kilia_t5: int = 1085737759215456431
    kilia_t6: int = 1085737759215456432

    # Skye membership roles
    skye_members: int = 1086135847511924786
    skye_t1: int = 1086135847511924787
    skye_t2: int = 1086135847511924788
    skye_t3: int = 1086135847511924789
    skye_t4: int = 1086135847511924790 
    skye_t5: int = 1086135847511924791
    skye_t6: int = 1086135847511924792

    # Staff and Mods
    staff: int = 1079631141641916416
    head_mods: int = 1080319027144040488
    mod_team: int = 1081158211345842198
    discord_mods: int = 1081157932114268230 
    youtube_mods: int = 1081158137790349376
    reddit_mods: int = 1094612113063944334

    # Talents
    talents: int = 1082796401542574200
    Kiki: int = 1065888380992368681
    Kilia: int = 1065726810094043257
    Skye: int = 1068396088370937926

Roles = _Roles()

class _Guild(EnvConfig, env_prefix='guild_'):
    id: int = 1079591113951826040
    invite: str = "https://discord.gg/eienproject"

    moderations_roles: tuple[int,...] = (Roles.staff, Roles.mod_team, Roles.head_mods, Roles.discord_mods, Roles.youtube_mods, Roles.reddit_mods)
    talents: tuple[int, ...] = (Roles.Kiki, Roles.Kilia, Roles.Skye)
    replies_allowed: tuple[int, ...] = (Roles.staff, Roles.head_mods, Roles.Kiki, Roles.Kilia, Roles.Skye)

Guild = _Guild()
