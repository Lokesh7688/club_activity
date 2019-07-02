#!/home/ubuntu/miniconda3/envs/eec2/bin
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/ubuntu/club_activity/club_activity/")

from app import app as application
application.secret_key = 'app se kya matlab'
