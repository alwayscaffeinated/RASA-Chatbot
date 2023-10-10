from typing import Any, Text, Dict, List
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet
from json import dumps
from time import time
from math import trunc
from os import mkdir

customer_id = str(trunc(time()))
path = 'E:/Chatbot/output/'+customer_id+'/'
mkdir(path)
             
class ValidateBasicInfoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_basic_info_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("contact_prefer") == 'email':
            updated_slots.remove("confirm_phone")

        return updated_slots
    
class ValidatePhoneForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_phone_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("confirm_phone") != 'other':
            updated_slots.remove("other_phone")

        return updated_slots
    
class ValidateAddressForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_address_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("confirm_address") == 'yes':
            updated_slots.remove("full_address")

        return updated_slots
    
class ActionSubmitForm(Action):   
    def name(self) -> Text:
        return "action_submit_form"

    def run(self, dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
        
        data = {'options': tracker.slots.get('options'),
                'language' : tracker.slots.get('language'),
                'phone' : tracker.slots.get('phone'),
                'phone_type' : tracker.slots.get('phone_type'),
                'contact_prefer' : tracker.slots.get('contact_prefer'),
                'confirm_phone' : tracker.slots.get('confirm_phone'),
                'other_phone' : tracker.slots.get('other_phone'),
                'street_address' : tracker.slots.get('street_address'),
                'city' : tracker.slots.get('city'),
                'zipcode' : tracker.slots.get('zipcode'),
                'confirm_address' : tracker.slots.get('confirm_address'),
                'full_address' : tracker.slots.get('full_address'),
                'home_members' : tracker.slots.get('home_members'),
                'race' : tracker.slots.get('race'),
                'hispanic' : tracker.slots.get('hispanic'),
                'gender' : tracker.slots.get('gender')
                }
        
        json_object = dumps(data,indent=4)
        
        with open(path+'/personal_info_slot_values.json','w') as outfile:
            outfile.write(json_object)
        
        return []
    
class ValidateIncomeSourceForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_income_source_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("income_source") != 'other':
            updated_slots.remove("other_income")

        return updated_slots
    
class ValidateIncomeBelongForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_income_belong_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("income_belong") != 'other':
            updated_slots.remove("other_income_belong")

        return updated_slots
    
class ActionSubmitIncomeForm(Action):
    def name(self) -> Text:
        return "action_submit_income_form"
    
    def run(self,dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
    
        data = {'income_source': tracker.slots.get('income_source'),
                'other_income' : tracker.slots.get('other_income'),
                'income_belong' : tracker.slots.get('income_belong'),
                'other_income_belong' : tracker.slots.get('other_income_belong'),
                'income_amount' : tracker.slots.get('income_amount'),
                'salary_type' : tracker.slots.get('salary_type')
                }
        
        json_object = dumps(data,indent=4)
        
        with open(path+'/income_slot_values_'+tracker.slots.get('income_source')+'.json','w') as outfile:
            outfile.write(json_object)
            
        return_slots = []
        for slot in data.keys():
            return_slots.append(SlotSet(slot,None))
        
        return return_slots
    
class ValidateFixedSpendingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_fixed_spending_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("fixed_spending") == 'none':
            updated_slots.remove("fixed_spending_frequency")
            updated_slots.remove("fixed_spending_amount")

        return updated_slots
    
class ActionSubmitFixedSpendingForm(Action):
    def name(self) -> Text:
        return "action_submit_fixed_form"
    
    def run(self,dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
    
        data = {'fixed_spending': tracker.slots.get('fixed_spending'),
                'fixed_spending_frequency' : tracker.slots.get('fixed_spending_frequency'),
                'fixed_spending_amount' : tracker.slots.get('fixed_spending_amount')
                }
        
        json_object = dumps(data,indent=4)
        
        if tracker.slots.get("fixed_spending") != 'none': 
            with open(path+'/fixed_spending_slot_values_'+tracker.slots.get('fixed_spending')+'.json','w') as outfile:
                outfile.write(json_object)
            
        return_slots = []
        for slot in data.keys():
            return_slots.append(SlotSet(slot,None))
        
        return return_slots
    
class ValidateVariableSpendingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_variable_spending_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("variable_spending") == 'none':
            updated_slots.remove("variable_spending_frequency")
            updated_slots.remove("variable_spending_amount")

        return updated_slots
    
class ActionSubmitVariableSpendingForm(Action):
    def name(self) -> Text:
        return "action_submit_variable_form"
    
    def run(self,dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
    
        data = {'variable_spending': tracker.slots.get('variable_spending'),
                'variable_spending_frequency' : tracker.slots.get('variable_spending_frequency'),
                'variable_spending_amount' : tracker.slots.get('variable_spending_amount')
                }
        
        json_object = dumps(data,indent=4)
        
        if tracker.slots.get("discretionary_expenses") != 'none': 
            with open(path+'/variable_spending_slot_values_'+tracker.slots.get('variable_spending')+'.json','w') as outfile:
                outfile.write(json_object)
            
        return_slots = []
        for slot in data.keys():
            return_slots.append(SlotSet(slot,None))
        
        return return_slots
    
class ValidateDiscretionaryExpenseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_discretionary_expense_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("discretionary_expenses") == 'none':
            updated_slots.remove("discretionary_expenses_frequency")
            updated_slots.remove("discretionary_expenses_amount")

        return updated_slots

class ActionSubmitDiscretionarySpendingForm(Action):
    def name(self) -> Text:
        return "action_submit_discretionary_form"
    
    def run(self,dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
    
        data = {'discretionary_expenses': tracker.slots.get('discretionary_expenses'),
                'discretionary_expenses_frequency' : tracker.slots.get('discretionary_expenses_frequency'),
                'discretionary_expenses_amount' : tracker.slots.get('discretionary_expenses_amount')
                }
        
        json_object = dumps(data,indent=4)
        
        if tracker.slots.get("discretionary_expenses") != 'none': 
            with open(path+'/discretionary_expenses_slot_values_'+tracker.slots.get('discretionary_expenses')+'.json','w') as outfile:
                outfile.write(json_object)
            
        return_slots = []
        for slot in data.keys():
            return_slots.append(SlotSet(slot,None))
        
        return return_slots

class ValidateDebtExpenseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_debt_expenses_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("debt_expenses") == 'none':
            updated_slots.remove("debt_expenses_frequency")
            updated_slots.remove("debt_expenses_amount")

        return updated_slots

class ActionSubmitDebtSpendingForm(Action):
    def name(self) -> Text:
        return "action_submit_debt_form"
    
    def run(self,dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
    
        data = {'debt_expenses': tracker.slots.get('debt_expenses'),
                'debt_expenses_frequency' : tracker.slots.get('debt_expenses_frequency'),
                'debt_expenses_amount' : tracker.slots.get('debt_expenses_amount')
                }
        
        json_object = dumps(data,indent=4)
        
        if tracker.slots.get("debt_expenses") != 'none': 
            with open(path+'/debt_expenses_slot_values_'+tracker.slots.get('debt_expenses')+'.json','w') as outfile:
                outfile.write(json_object)
            
        return_slots = []
        for slot in data.keys():
            return_slots.append(SlotSet(slot,None))
        
        return return_slots
    
class ValidateTaxExpenseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_tax_expenses_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("tax_expenses") == 'none':
            updated_slots.remove("tax_expenses_frequency")
            updated_slots.remove("tax_expenses_amount")

        return updated_slots
    
class ActionSubmitTaxSpendingForm(Action):
    def name(self) -> Text:
        return "action_submit_tax_form"
    
    def run(self,dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
    
        data = {'tax_expenses': tracker.slots.get('tax_expenses'),
                'tax_expenses_frequency' : tracker.slots.get('tax_expenses_frequency'),
                'tax_expenses_amount' : tracker.slots.get('tax_expenses_amount')
                }
        
        json_object = dumps(data,indent=4)
        
        if tracker.slots.get("tax_expenses") != 'none': 
            with open(path+'/tax_expenses_slot_values_'+tracker.slots.get('tax_expenses')+'.json','w') as outfile:
                outfile.write(json_object)
            
        return_slots = []
        for slot in data.keys():
            return_slots.append(SlotSet(slot,None))
        
        return return_slots
    
class ValidateInvestmentExpenseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_investment_expenses_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("investment_expenses") == 'none':
            updated_slots.remove("investment_expenses_frequency")
            updated_slots.remove("investment_expenses_amount")

        return updated_slots
    
class ActionSubmitInvestmentSpendingForm(Action):
    def name(self) -> Text:
        return "action_submit_investment_form"
    
    def run(self,dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
    
        data = {'investment_expenses': tracker.slots.get('investment_expenses'),
                'investment_expenses_frequency' : tracker.slots.get('investment_expenses_frequency'),
                'investment_expenses_amount' : tracker.slots.get('investment_expenses_amount')
                }
        
        json_object = dumps(data,indent=4)
        
        if tracker.slots.get("investment_expenses") != 'none': 
            with open(path+'/investment_expenses_slot_values_'+tracker.slots.get('investment_expenses')+'.json','w') as outfile:
                outfile.write(json_object)
            
        return_slots = []
        for slot in data.keys():
            return_slots.append(SlotSet(slot,None))
        
        return return_slots
    
class ValidateEmergencyExpenseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_emergency_expenses_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("emergency_expenses") == 'no':
            updated_slots.remove("emergency_frequency")
            updated_slots.remove("emergency_amount")

        return updated_slots
    
class ActionSubmitEmergencySpendingForm(Action):
    def name(self) -> Text:
        return "action_submit_emergency_form"
    
    def run(self,dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
    
        data = {'emergency_expenses': tracker.slots.get('emergency_expenses'),
                'emergency_frequency' : tracker.slots.get('emergency_frequency'),
                'emergency_amount' : tracker.slots.get('emergency_amount')
                }
        
        json_object = dumps(data,indent=4)
        
        if tracker.slots.get("emergency_expenses") != 'no': 
            with open(path+'/emergency_expenses_slot_values_'+tracker.slots.get('emergency_expenses')+'.json','w') as outfile:
                outfile.write(json_object)
            
        return_slots = []
        for slot in data.keys():
            return_slots.append(SlotSet(slot,None))
        
        return return_slots
    
class ValidateOtherExpenseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_other_expenses_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("other_expenses") == 'no':
            updated_slots.remove("other_expense_name")
            updated_slots.remove("other_expense_frequency")
            updated_slots.remove("other_expense_amount")
            
        return updated_slots
    
class ActionSubmitOtherSpendingForm(Action):
    def name(self) -> Text:
        return "action_submit_other_form"
    
    def run(self,dispatcher: CollectingDispatcher, 
               tracker: Tracker, 
               domain: Dict[Text,Any])->List[Dict[Text,Any]]:
    
        data = {'other_expense_name': tracker.slots.get('other_expense_name'),
                'other_expense_frequency' : tracker.slots.get('other_expense_frequency'),
                'other_expense_amount' : tracker.slots.get('other_expense_amount')
                }
        
        json_object = dumps(data,indent=4)
        
        if tracker.slots.get("other_expenses") != 'no': 
            with open(path+'/other_expenses_slot_values_'+tracker.slots.get('other_expense_name')+'.json','w') as outfile:
                outfile.write(json_object)
            
        return_slots = []
        for slot in data.keys():
            return_slots.append(SlotSet(slot,None))
        
        return return_slots