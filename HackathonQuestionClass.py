from re import I
from tkinter.messagebox import QUESTION
from HackClass import companiesList, dictionaries

#QUESTION
Companies = companiesList()
sectorDict, countryDict = dictionaries()

class Question:
    """Class that describes a general Question with a prompt, answer, predifined E, S, and G weights, and industry weight"""
    def __init__(self, prompt, e_weight, s_weight, g_weight, industry_weight = 0, industry = ""):
        self.prompt = prompt
        self.e_weight = e_weight
        self.s_weight = s_weight
        self.g_weight = g_weight
        self.industry_weight = industry_weight
        self.industry = industry

class IndustryQuestion:
    """Question Determining which industry to pay attention to."""
    def __init__(self, prompt):
        self.prompt = prompt

behavior_question_prompts = [
    "Q1. What balance of profit to ESG impact do you expect in your investments. (1 high profits, 5 high impact)\n\n",
    "Q2. How much do you care about how the company is treating it's workers?(1-5 Scale)\n\n",
    "Q3. How important is the company's carbon footprint to you?(1-5 Scale)\n\n"
]

behavior_questions = [
    Question(behavior_question_prompts[0], 0.15, 0.15, 0.7),
    Question(behavior_question_prompts[1], 0.2, 0.6, 0.2),
    Question(behavior_question_prompts[2], 0.7, 0.15, 0.15)
]

def run_behavorial_questions(behavior_questions):
    answers = []
    for question in behavior_questions:
        answer = input(question.prompt)
        assert answer != '' and 1 <= int(answer) <= 5, "Please pick a number from 1 to 5"   #will it break if i is decimal
        answers.append(int(answer))
    return answers

industry_question_prompts = """What industries would like to invest in? (Select 3) -- Please answer with the indexes separated by commas (e.g. 1,2,3)\n"""
for i in range(1, len(sectorDict.keys())):
    industry_question_prompts += f"({list(sectorDict.values())[i]}) {list(sectorDict.keys())[i]}\n"

industry_question = IndustryQuestion(industry_question_prompts)

def run_industry_question(industry_question):
    industry_dict = {}
    for i in range(len(sectorDict.keys())):
        industry_dict[list(sectorDict.values())[i]] = list(sectorDict.keys())[i]
    answer = input(industry_question.prompt).split(",")
    for i in range(len(answer)):
        answer[i] = int(answer[i])
    preferred_industries = []
    for i in range(1, len(industry_dict.keys()) + 1):
        for j in answer:
            if i == j:
                preferred_industries.append(industry_dict[i])
    return preferred_industries

E_weights = []
S_weights = []
G_weights = []

def Run_Survey():
    """Go through the quiz? and get a list of the ratings"""
    favored_industries = run_industry_question(industry_question)
    answers = run_behavorial_questions(behavior_questions)
    questions = behavior_questions

    for i in range(3):
        E_weights.append(round(answers[0] * questions[i].e_weight, 2))
        S_weights.append(round(answers[1] * questions[i].s_weight, 2))
        G_weights.append(round(answers[2] * questions[i].g_weight, 2))

    return favored_industries

def adjust_E():
    E_value = sum(E_weights)
    e_adjustment = round(E_value / len(E_weights), 2)
    return e_adjustment

def adjust_S():
    S_value = sum(S_weights)
    s_adjustment = round(S_value / len(S_weights), 2)
    return s_adjustment

def adjust_G():
    G_value = sum(G_weights)
    g_adjustment = round(G_value / len(G_weights), 2)
    return g_adjustment

def personalized_E(calculated_e):
    return adjust_E() * calculated_e

def personalized_S(calculated_s):
    return adjust_S() * calculated_s

def personalized_G(calculated_g):
    return adjust_G() * calculated_g

def normalize_weights(a, b, c):
    s = sum([a, b, c])
    return a/s, b/s, c/s

def personalized_ESG(calculated_e, calculated_s, calculated_g):
    return personalized_E(calculated_e) + personalized_S(calculated_s) + personalized_G(calculated_g)


def test(outputNum=3):
    industries = Run_Survey()
    comps = []
    for i in Companies:
        if i.sector in industries:
            comps.append(i)
    distribution = list(normalize_weights(adjust_E(), adjust_S(), adjust_G()))
    allComps = {}
    differences = []
    for i in comps:
        compDist = list(i.normalized())
        difference = (distribution[0]-compDist[0]) + (distribution[1]-compDist[1]) + (distribution[2]-compDist[2])
        if difference in list(allComps.keys()):
            allComps[difference] = allComps[difference] + [i]
        else:
            allComps[difference] = [i]
            differences += [difference]
    differences.sort()
    SortedCompanies = []
    for i in differences:
        SortedCompanies.append(allComps[i])
    print([i.Ticker for i in PickOut(SortedCompanies, outputNum)])
    
def PickOut(SortedCompanies, outputNum):
    moshpit = []
    for _ in range(outputNum):
        moshpit += SortedCompanies[_]
    dict = {}
    kvals = []
    for i in moshpit:
        k = i.earningsGrowth
        kvals += [k]
        if k in list(dict.keys()):
            dict[k] = dict[k] + [i]
        else:
            dict[k] = [i]
    kvals.sort()
    kvals.reverse()
    output = []
    on = outputNum
    while 0 < outputNum:
        a = dict[kvals[on-outputNum]]
        if len(a) > outputNum:
            output += a[:outputNum]
            outputNum = 0
        else:
            output += a
            outputNum -= len(a)
    if not output:
        return moshpit[:on]
    return output
test() 


