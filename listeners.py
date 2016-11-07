from diary import Diary
import tweepy

tracking_words = ['the', 'is', 'a', 'for', 'be', 'to', 'and' 'in', 'that', 'have', 'I',
                  ' ', 'it', 'not', 'on', 'with', 'he', 'as', 'you', 'she', 'do', 'at', 'but', 'why', 'this',
                  'by', 'from', 'they', 'did', 'we', 'say', 'him', 'or', 'an', 'will', 'my', 'one', 'all',
                  'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who']

log = Diary("streaming.log")

class EnglishListener(tweepy.streaming.StreamListener):
    def __init__(self, robot):
        super(EnglishListener, self).__init__()
        self.count = 0
        self.robot = robot

    def on_data(self, data):
        self.robot.handle_data(data)
        return True

    def on_error(self, error):
        if error == 88 or error == 420:
            self.on_limit("Rate limit exceeded")
        else:
            log.error('Sleeping for 30 min due to --')
            log.error(error)
            tweepy.streaming.sleep(1800)

    def on_exception(self, status):
        log.warn('Sleeping for 3 min due to --')
        log.warn(status.args)
        tweepy.streaming.sleep(180)

    def on_limit(self, track):
        log.warn('Sleeping for 30 minutes due to --')
        log.warn(track)
        tweepy.streaming.sleep(1800)

    def on_close(self, resp):
        log.error("Twitter closed connection -- ")
        log.error(resp)
        return False

    def manual_stop(self):
        self.robot.stream.disconnect()


class MentionListener(EnglishListener):
    def __init__(self, robot, handle="@TeachMeBot"):
        super(MentionListener, self).__init__(robot)
        self.count = 0
        self.robot = robot
        self.handle = handle

    def on_data(self, data):
        self.robot.handle_mention(data)