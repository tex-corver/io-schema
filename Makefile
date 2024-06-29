project_path = $(shell pwd)
config_path = $(project_path)/.configs

test: 
	CONFIG_PATH=$(config_path) pytest $(o)
