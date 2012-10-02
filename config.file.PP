#
# Config File conventions.  '#' is a comment character. anything after ignored.
#                           '[ ]' contains section designators.

[jira] # Configuration information for jira.
url=https://jira.oceanobservatories.org/tasks/
#url=https://jira-dev.oceanobservatories.org/tasks
username=unwin      # optional, for unchallenged operation
#password=PASSWORD      # optional, for unchallenged operation
csv_file_name=R3 PnP Task List - R3I1-PP.csv # optional, for unchallenged operation

reporter=graybeal      # defaults to username, unless specified here

separator=,
quote_char="
filter_folumn=Iteration
filter_value=R3I1

[Projects] # (key, value)
Planning & Prosecution=CIDEVPP

[priorities]
blocker=Blocker
B=Blocker
5=Blocker
High=Critical
H=Critical
4=Critical
Medium=Major
M=Major
3=Major
Low=Minor
L=Minor
2=Minor
1=Trivial

[jira_priority]
Blocker=1
Critical=2
Major=3
Minor=4
Trivial=5
Must Complete=6
Should Complete=7
Good to Complete=8
Nice to Complete=9


[field_mappings]    # This designates the column mappings from the google spreadsheet CSV to what we do with them????
OOI_CATEGORY_NUMBER=0 #?? This column should stay set until reset by another value. Blank = use last defined value.
Type=1
RT-ID=2
IT-ID=3
Iteration=4
Task=5
Description=6
Outcome=7
Risk (RTs)=8
R1I3-PP=9
R1E1-PP=10
R1E2-PP=11
Jira Task Num=12
Priority=13
Work Days=14
Assignee=15
Support Developer=16
Design URL=17
Comments=18
Status=19
Possible Risks=20
#Confidence=20

[Used_mappings]    # This designates the column numbers to what the migrator will use them for, possibly making above redundant.
Description=6
TaskTitle=5
Priority=13
TimeEstimate=14
Assignee=15
AffectsVersion=9,10,11 # if X in column, then add column name to affects version.
Components=0 # value should stay set until overwritten by a non blank value.  Also need to do a link lookup on it.

[output_mappings] # Column to overwrite with values resulting from addition to Jira.  Dumps input back as output, with the addition of these column mappings which overwrite the origional contents.
12=JiraKey

