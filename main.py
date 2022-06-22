from distutils.log import INFO
from os import system
from classes.Absolubot import AbsoluBot
from classes.LogConfig import LogConfig

import sys
import getopt

def init(argv):

    log = LogConfig()
    log.logger.info("Initializing...")
   
    arg_timeout = ""
    arg_sleep = ""
    arg_output = ""
    arg_help = "{0} -t <timeout> -s <sleep> -o <output>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "ht:s:o:", ["help", "timeout=", 
        "sleep=", "output="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-t", "--timeout"):
            arg_timeout = arg
        elif opt in ("-s", "--sleep"):
            arg_sleep = arg
        elif opt in ("-o", "--output"):
            arg_output = arg

    log.logger.info("Parameters: timeout="+arg_timeout+" sleep="+arg_sleep+ " output="+arg_output)

    bot = AbsoluBot(arg_timeout,arg_sleep,arg_output,log)
    bot.downloadDrinksLinks()
    bot.start()
    sys.exit(0)

if __name__ == "__main__":
    init(sys.argv)
