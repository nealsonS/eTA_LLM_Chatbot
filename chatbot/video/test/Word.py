# modified from https://towardsdatascience.com/speech-recognition-with-timestamps-934ede4234b2 

class Word:
    ''' A class representing a word from the JSON format for vosk speech recognition API '''

    def __init__(self, dict):
        '''
        Parameters:
          dict (dict) dictionary from JSON, containing:
            word (str): recognized word
            start (float): start time of the pronouncing the word, in seconds
            end (float): end time of the pronouncing the word, in seconds
        '''
        self.word = dict["word"]
        self.end = dict["end"]
        self.start = dict["start"]


    def to_string(self):
        ''' Returns a string describing this instance '''
        return "{:20} from {:.2f} sec to {:.2f} sec".format(
            self.word, self.start, self.end)
