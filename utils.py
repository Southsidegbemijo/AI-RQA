
def process_interview(text):
    lines = text.split('\n')

    interviewer = None
    interviewee = None

    for line in lines:
        if 'Interviewer:' in line:
            # If there's already a pair waiting to included, we can include it
            if interviewer is not None:
                yield {'Interviewer': interviewer, 'Interviewee': interviewee}
                interviewer = None
                interviewee = None
            interviewer = line.replace('Interviewer:', '').strip()
        elif 'Interviewee:' in line:
            interviewee = line.replace('Interviewee:', '').strip()

    if interviewer is not None:
        yield {'Interviewer': interviewer, 'Interviewee': interviewee if interviewee else "[No Reply]" }
