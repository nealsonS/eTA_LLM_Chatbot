# modified from https://towardsdatascience.com/speech-recognition-with-timestamps-934ede4234b2 

class Word:
    ''' A class representing a word from the JSON format for vosk speech recognition API '''

    def __init__(self, dict):
        '''
        Parameters:
          dict (dict) dictionary from JSON, containing:
            word (str): recognized word
            text (str): recognized word
            start (float): start time of the pronouncing the word, in seconds
            end (float): end time of the pronouncing the word, in seconds
            duration (float): total time of pronouncing the word, in seconds (end - start)
        '''
        self.word = dict["word"]
        self.text = dict["word"]
        self.end = dict["end"]
        self.start = dict["start"]
        self.duration = dict["end"] - dict["start"]


    def to_string(self):
        ''' Returns a string describing this instance '''
        return {'text': self.text, 'start': self.start, 'duration': self.duration}
        #return "{:20} starting from {:.2f} sec taking {:.2f} secs".format(
        #    self.text, self.start, self.duration)
