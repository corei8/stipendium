try:
    import tomllib
except ModuleNotFoundError:
    import timli as tomllib

with open("config/recipients.toml", mode="rb") as fp:
    config = tomllib.load(fp)


