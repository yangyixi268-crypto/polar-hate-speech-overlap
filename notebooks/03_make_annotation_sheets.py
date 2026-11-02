import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

SEED = 42
DATA = '../data-public'
OUT = '../data'

GUIDELINES = """Annotation Guidelines

WARNING: You will encounter polarized and hateful content during this task. Please take breaks as needed and prioritize your mental well-being.

POLARIZATION refers to increasingly extreme, divided beliefs or behaviors between opposing groups.
Attitude polarization includes:
  - Negative attitudes toward out-groups
  - Blind support for in-groups
  - Stereotyping, vilification, dehumanization, or intolerance

Polarization is NOT the same as hate speech!
HATE SPEECH refers to any form of expression used to intimidate, humiliate, incite violence against, or promote hatred toward a particular group or class of people.
A polarized statement does not necessarily contain hate speech.

Reacting negatively to an individual's personal opinion is NOT polarization. If the reaction targets the group, ideology, identity, or community to which that person belongs, it IS polarization.
Always consider the overall context and meaning, not just individual words.

EXAMPLES
1. "You do not need to be a student to defend student rights, a woman to defend women's rights, gay to defend gay rights, or an animal to defend animal rights."
   Polarization: NO | Hate speech: NO. A response to polarized content; the author shows no polarized attitude.
2. "How narrow-minded you are. Everyone in this world has the right to live."
   Polarization: NO | Hate speech: NO. Reacting to an individual's personal opinion.
3. "Because of the narrow mindedness of you and people like you, there are people in this country who are unable to enjoy their right to live."
   Polarization: YES | Hate speech: NO. Directed at the group or viewpoint the person belongs to.
4. "Because of your administration, this place has been left to those people."
   Polarization: YES | Hate speech: NO. Other elements contribute to polarization.
5. "I don't know if this is even an answer or if you just hate for no reason. This is the first time I've seen a homophobic atheist. [...] Because of people like you, 60% of trans people attempt suicide. Why are you so full of hate?"
   Polarization: YES | Hate speech: NO. Polarized concepts with an "us versus them" framing.
6. "Those who do not vote are dishonorable pigs."
   Polarization: YES | Hate speech: YES. Non-voters framed as an opposing group and insulted.

TASKS (fill one row per text in the 'Annotation' sheet)
Task 1a - polarization: Yes = the message clearly reflects attitude polarization; No = no polarization indicators.
Task 1b - pol_confidence: How sure are you about your polarization decision?
  1 = Not at all confident, 2 = Slightly, 3 = Moderately, 4 = Very, 5 = Extremely confident
Task 2a - offensiveness (hate speech):
  1 = Not offensive, 2 = Slightly, 3 = Moderately, 4 = Very, 5 = Extremely offensive
Task 2b - off_confidence: How sure are you about your offensiveness rating?
  1 = Not at all confident, 2 = Slightly, 3 = Moderately, 4 = Very, 5 = Extremely confident
comment (optional): write a short note if you are unsure or the text is ambiguous.

Please annotate independently and do not discuss the texts with other annotators."""

def build(df, path):
    wb = Workbook()
    g = wb.active
    g.title = 'Guidelines'
    for i, line in enumerate(GUIDELINES.split('\n'), start=1):
        c = g.cell(row=i, column=1, value=line)
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if line.isupper() or line == 'Annotation Guidelines':
            c.font = Font(bold=True)
    g.column_dimensions['A'].width = 120

    ws = wb.create_sheet('Annotation')
    headers = ['id', 'text', 'polarization', 'pol_confidence', 'offensiveness', 'off_confidence', 'comment']
    ws.append(headers)
    for _, r in df.iterrows():
        ws.append([r['id'], r['text'], None, None, None, None, None])
    n = len(df) + 1

    head_fill = PatternFill('solid', fgColor='DDEBF7')
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = head_fill
    for row in ws.iter_rows(min_row=2, max_row=n):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical='top')
    for col, w in zip('ABCDEFG', [14, 80, 14, 15, 14, 15, 40]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = 'C2'

    for col, options in [('C', '"Yes,No"'), ('D', '"1,2,3,4,5"'), ('E', '"1,2,3,4,5"'), ('F', '"1,2,3,4,5"')]:
        dv = DataValidation(type='list', formula1=options, allow_blank=True,
                            showErrorMessage=True, errorTitle='Invalid value',
                            error='Please choose a value from the list.')
        ws.add_data_validation(dv)
        dv.add(f'{col}2:{col}{n}')

    wb.active = 1
    wb.save(path)

# main set: the 300 sampled instances (text only, no POLAR labels)
sample = pd.read_csv(f'{OUT}/sample_300.csv')
for a in ['A1', 'A2', 'A3']:
    build(sample, f'{OUT}/annotation_{a}.xlsx')

# pilot set: 20 test instances that are NOT in the main sample
test = pd.read_csv(f'{DATA}/test/eng.csv')
rest = test[~test['id'].isin(sample['id'])]
pilot = pd.concat([
    rest[rest['polarization'] == 1].sample(10, random_state=SEED),
    rest[rest['polarization'] == 0].sample(10, random_state=SEED),
]).sample(frac=1, random_state=SEED)
pilot[['id']].to_csv(f'{OUT}/pilot_ids.csv', index=False)
build(pilot, f'{OUT}/pilot_annotation.xlsx')

print('Created: annotation_A1/A2/A3.xlsx (300 rows each), pilot_annotation.xlsx (20 rows)')
