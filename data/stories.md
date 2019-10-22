## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## silly
* silly
  - my_action

## form path
* add
  - task_form
  - form{"name": "task_form"}
  - form{"name": null}
  - utter_formDone
  - resetSlot_action

## move state
* move
  - move_form

## Chat with me

* move
    - move_form

## Chat with me

* move
    - move_form

## Chat with me

* move
    - move_form

## Chat with me

* move
    - move_form

## Chat with me

* move
    - move_form
