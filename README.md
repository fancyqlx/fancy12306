# fancy12306

## Introduction

This is a simple tool for booking tickets in 12306. We provide some functions to simulate manual input. From my experience of 
using 12306.cn, I think the most annoying thing is enter username, password and select tickets information. Uh-huh, I forget that 
extremely disgusting verification image, but please forgive me that there is no better way to skip this. Thus what we provide 
is loading all the informaiton you need except for verification, and simplify the operations as much as possible. This tool 
has not been finished yet, and we will further imporve it. Although this tool is just a toy that it is a practice for me, I still 
try my best to provide an useful tool.

## Getting Started

### config.ini

There is a **config.ini** file that recording some information for you:

- username: username for loginning the 12306.cn

- password: password for loginning

- passengers: all the passengers of your account, you need not input it by yourself

- wanted_passengers: the passengers for whom you want to book tickets

- from_station: the starting station of your ticket, you can just use *pinying* or input Chinese

- to_station: the ending station

- date: the date of the ticket, the format is *2017-01-01*

The *config.ini* stores all the information we need in the process of booking tickets, so you can modify it by yourself 
in *config.ini* or enter it in command-line when you start the program.

### usage

You just need to put all the codes in no matter which fold, then find **tickets.py**. 
If you run **`python tickets.py`**, it means the program will load *config.ini* by itself and you needn't input anything later. 
If you run **`python tickets.py -c`**, the program will not load *config.ini*, you need input some information later 
and the command-line will guide you to complete it.

**Note that you need to verify the verification by yourself in the brower. We recommand you to use *Chrome*, 
you can change it to *Firefox* in the code if you like.**