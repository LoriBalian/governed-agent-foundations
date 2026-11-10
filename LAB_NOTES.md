# Lab notes: Agents I (governing actions)

Name: Lori Balian
GitHub username: LoriBalian

Write one to three sentences per lab, with numbers or names from YOUR run. Commit and push this file to your fork by 9:25, then open a pull request titled "Lab notes: Firstname Lastname".

## Lab 0: the loop
What are the five things the loop does on every step, and which two of them are governance rather than intelligence?
The five steps are observe, plan, check, act, and log. Check and log are the governance steps because they make sure the agent follows the rules and keeps track of what it does.

## Lab 1: the model as a tool
P003 and P006: their probabilities and bands from your run. Which feature drove P006's risk most? Who authored the model card the agent relies on?
P003 had a 12.8% risk (LOW), and P006 had a 90.9% risk (HIGH). P006's biggest risk factor was prior admissions. The Week 6 federation coordinator created the model card, and the agent just uses it.

## Lab 2: capability is not permission
Three refusals: the tool or patient, and the policy line that caused each. After your edit (max_patients_per_task, max_tool_calls_per_task), what finished that did not before, and who should be allowed to make that edit?
The policy blocked exporting patient records because it wasn't allowed, accessing P011 because they belonged to Kestrel, and checking more than one patient because of the limit. After I changed the limits to 3 patients and 12 tool calls, the agent finished all 3 patients in 11 calls. Only the approved governance team should be able to change these limits, and the changes should be tracked in the policy version and GitHub.

## Lab 3: the approval gate
What did the log record when you approved and when you rejected? Name one action in your final project that belongs in approval_required, and one that does not, with a reason.
When I approved the follow-up, the agent booked it. When I rejected it, the agent stopped after 2 tool calls, and both decisions were recorded. I would require approval for scheduling follow-ups because it affects patient care, but not for checking readmission risk because it's just providing information.

## Lab 4: evidence
From your audit summary: tasks, allowed calls, refusals, approvals. Who should read this log, how often, and what would make them pull the agent?
My audit log had 61 events from 10 tasks, with 32 allowed calls, 3 refusals, 5 approvals, and 1 rejection. I think the Clinical AI Committee should check the log every month and stop the agent if it breaks the rules or its accuracy falls below 78%. Follow-ups could eventually be scheduled automatically if testing shows it's safe and the approval results support it.

## Lab 5: a language model in the planner's seat (if you ran it)
Did the model take the same route as the scripted planner? With --inject on P009: did it try export_records, and what stopped it?
I tried using the OpenAI model, but I didn't have API credits. I used the scripted planner instead, and it gave P009 a 68.6% risk (HIGH) and booked a follow-up after I approved it. I couldn't test the injected note with the AI model, but the policy would block export_records because it isn't allowed.

## Declaration
I ran every command above in my own Codespace and the numbers are from my own run.  Initials: LB
