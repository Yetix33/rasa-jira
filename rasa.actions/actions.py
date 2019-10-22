from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
import atexit

datastore = {}
username = 'pratyush.b'
password = 'Ep123?1998'
jiraEndpoint = 'http://192.168.0.128:8080/'
projectId = 10000

def save():
    with open("database.json", 'w') as f:
        json.dump(datastore, f)
atexit.register(save)

with open("database.json", 'r') as f:
        datastore = json.load(f)

class ActionHelloWorld(Action):

    def name(self):
        return 'my_action'

    def run(self, dispatcher,
            tracker,
            domain):

        dispatcher.utter_message("Hello World!")

        return []

class TaskForm(FormAction):
    def name(self):
        print('it works')
        return "task_form"

    @staticmethod
    def required_slots(tracker):
        return["header", "body", "person", "size", "time", "state"]
        
    def slot_mappings(self):
        return {
            "header": [self.from_entity(entity="header"), self.from_text()],
            "body": [self.from_entity(entity="body"), self.from_text()],
            "person": [self.from_entity(entity="person"), self.from_text()],
            "size": [self.from_entity(entity="size"), self.from_text()],
            "time": [self.from_entity(entity="time"), self.from_text()],
            "state": [self.from_entity(entity="state"), self.from_text()],

        }

    def submit(self,dispatcher,tracker, domain):
        print(tracker.slots['state'])
        datastore[tracker.slots['state']].append({
            "body": tracker.slots['body'],
            "header": tracker.slots['header'],
            "person": tracker.slots['person'],
            "size": tracker.slots['size'],
            "time": tracker.slots['time']
        })
        
        last_hope = {
            "fields": {
                "project": {
                    "id": projectId
                }, 
                "summary": tracker.slots['header'],
                "issuetype": {
                    "id": 10003
                }
            }
        }
        r = requests.post(jiraEndpoint + 'rest/api/2/issue', auth=(username, password), json=last_hope)
    
        dispatcher.utter_template('utter_submit', tracker)
        return[]

################################################################################
class ActionResetSlot(Action):
    def name(self):
        return 'resetSlot_action'
    def run(self, dispatcher, tracker, domain):
        return [SlotSet("header", None), SlotSet("body", None), SlotSet("person", None), SlotSet("size", None), SlotSet("time", None), SlotSet("state", None)]
 
class MoveForm(FormAction):
    def name(self):
        return "move_form"
    @staticmethod
    def required_slots(tracker):
        return["header", "state"]
    def slot_mappings(self):
        return {
            "header": [self.from_entity(entity="header"), self.from_text()],
            "state": [self.from_entity(entity="state"), self.from_text()],
        }
    def submit(self,dispatcher,tracker, domain):
        r = requests.get(jiraEndpoint + 'rest/api/2/search?jql=summary~"' + tracker.slots['header'] + '"', auth=(username, password))
        print(r.json())
        issueId = r.json()['issues'][0]['id']
        print(issueId)
        print(jiraEndpoint + 'rest/api/2/issue/' + issueId + '/transitions')
        transitions = requests.get(jiraEndpoint + 'rest/api/2/issue/' + issueId + '/transitions', auth=(username, password)).json()
        transitionId = 0

        for transition in transitions['transitions'][0:]:
            print(transition)
            print(tracker.slots['state'])
            if (transition['name']).lower() == (tracker.slots['state']).lower():
                transitionId = transition['id']
                break
            print(transitionId)

        transitionBLob = {
            "update": {
            },
            "transition": 
            {
                "id": transitionId
            }
        }

        r = requests.post(jiraEndpoint + 'rest/api/2/issue/' + issueId + '/transitions', auth=(username, password), json=transitionBLob)

        print(r)
        check = True
        for x in range(len(datastore['todo'][0:])):
            if datastore['todo'][x]['header'] == tracker.slots['header']:
                datastore[tracker.slots['state']].append(datastore['todo'].pop(x))
                check = False
        if check:
             for x in range(len(datastore['doing'][0:])):
                if datastore['doing'][x]['header'] == tracker.slots['header']:
                    datastore[tracker.slots['state']].append(datastore['doing'].pop(x))
                    check = False
        if check:
             for x in range(len(datastore['done'][0:])):
                if datastore['done'][x]['header'] == tracker.slots['header']:
                    datastore[tracker.slots['state']].append(datastore['done'].pop(x))
                    check = False
        
        
        dispatcher.utter_template('utter_moved', tracker)
        return[]


def task (projectId, summary, issuetype): 
    return {
        "fields": {
            "project": {
                "id": projectId
            }, 
            "summary": summary,
            "issuetype": {
                "id": issuetype
            }
        }
    }